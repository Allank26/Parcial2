from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import Producto, ListaCompra, ProductoEnLista, HistorialCompra, ProductoEnHistorial
from .tasks import enviar_correo_inicio_sesion, enviar_correo_lista_compra, enviar_correo_cancelacion

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            enviar_correo_inicio_sesion.delay(user.email)
            return redirect('productos')
    return render(request, 'login.html')

@login_required
def productos_view(request):
    productos = Producto.objects.all()
    lista, created = ListaCompra.objects.get_or_create(usuario=request.user)
    productos_en_lista = ProductoEnLista.objects.filter(lista=lista)
    
    # Obtiene los IDs de los productos que ya están en la lista
    productos_ids_en_lista = productos_en_lista.values_list('producto_id', flat=True)

    if request.method == 'POST':
        producto_id = request.POST.get('producto_id')
        cantidad = int(request.POST.get(f'cantidad_{producto_id}', 1))
        if producto_id:  # Asegúrate de que el producto_id no sea None
            try:
                producto = Producto.objects.get(id=producto_id)
                # Verifica si el producto ya está en la lista
                producto_en_lista, created = ProductoEnLista.objects.get_or_create(lista=lista, producto=producto)
                if not created:
                    producto_en_lista.cantidad += cantidad
                else:
                    producto_en_lista.cantidad = cantidad
                producto_en_lista.save()
            except Producto.DoesNotExist:
                # Manejo del caso en que el producto no existe
                pass
        return redirect('productos')

    return render(request, 'productos.html', {'productos': productos, 'productos_ids_en_lista': productos_ids_en_lista})

@login_required
def ver_lista_view(request):
    # Intentamos obtener o crear la lista de compra para el usuario
    lista, created = ListaCompra.objects.get_or_create(usuario=request.user)
    
    # Obtenemos los productos que están en la lista del usuario
    productos_en_lista = ProductoEnLista.objects.filter(lista=lista)
    
    if request.method == 'POST':
        if 'quitar' in request.POST:
            # Obtener el ID del producto a quitar
            producto_id = request.POST.get('producto_id')
            # Buscar el producto en la lista y eliminarlo
            producto_en_lista = productos_en_lista.filter(producto_id=producto_id).first()
            if producto_en_lista:
                producto_en_lista.delete()  # Quitar el producto de la lista

        elif 'comprar' in request.POST:
            # Crear un historial de compra cuando se realiza la compra
            historial = HistorialCompra.objects.create(usuario=request.user)
            for item in productos_en_lista:
                ProductoEnHistorial.objects.create(historial=historial, producto=item.producto, cantidad=item.cantidad)
            enviar_correo_lista_compra.delay(request.user.email, historial.id)
            
            # Eliminar la lista de compras del usuario tras la compra
            lista.delete()
            return redirect('perfil')
        
        elif 'cancelar' in request.POST:
            # Enviar correo y cancelar la lista de compras
            enviar_correo_cancelacion.delay(request.user.email, lista.id)
            lista.delete()
            return redirect('productos')
    
    return render(request, 'ver_lista.html', {'productos_en_lista': productos_en_lista})

@login_required
def perfil_view(request):
    historial = HistorialCompra.objects.filter(usuario=request.user)
    return render(request, 'perfil.html', {'historial': historial})

def logout_view(request):
    logout(request)
    return redirect('login')

