# avisos/views.py
from django.shortcuts import render
from .tasks import enviar_correo  # Importa la tarea de Celery

# Función para la página principal
def index(request):
    return render(request, 'index.html')  # Asegúrate de que tienes un archivo 'index.html'

# Función que manejará el envío de correos
def enviar_aviso(request):
    if request.method == 'POST':
        enviar_correo.delay()  # Llama a la tarea de Celery para enviar el correo
        return render(request, 'exito.html')  # Redirige a la página de éxito
    return render(request, 'index.html')
