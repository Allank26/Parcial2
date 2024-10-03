from celery import shared_task
from django.core.mail import send_mail
from .models import HistorialCompra, ListaCompra

from celery import shared_task
from django.core.mail import send_mail

@shared_task
def enviar_correo_inicio_sesion(email):
    send_mail(
        'Inicio de sesión',
        f'El usuario con el correo {email} ha iniciado sesión.',
        'elvendedor@parcial.com',
        ['elvendedor@parcial.com'],
        fail_silently=False,
    )

@shared_task
def enviar_correo_lista_compra(email, historial_id):
    historial = HistorialCompra.objects.get(id=historial_id)
    productos = "\n".join([f"{item.producto.nombre} (x{item.cantidad})" for item in historial.productoenhistorial_set.all()])
    send_mail(
        'Lista de compra',
        f'El usuario con el correo {email} ha solicitado los siguientes productos:\n{productos}',
        'elvendedor@parcial.com',
        ['elvendedor@parcial.com', email],
        fail_silently=False,
    )

@shared_task
def enviar_correo_cancelacion(email, lista_id):
    lista = ListaCompra.objects.get(id=lista_id)
    productos = "\n".join([f"{item.producto.nombre} (x{item.cantidad})" for item in lista.productoenlista_set.all()])
    send_mail(
        'Cancelación de compra',
        f'El usuario con el correo {email} ha cancelado la siguiente lista de productos:\n{productos}',
        'elvendedor@parcial.com',
        ['elvendedor@parcial.com', email],
        fail_silently=False,
    )


