# avisos/tasks.py
from celery import shared_task
from django.core.mail import send_mail

@shared_task
def enviar_correo():
    try:
        send_mail(
            'Aviso importante',
            'Se ha realizado una compra exitosa.',
            'allan@parcial.com',
            ['jeremy@parcial.com'],
            fail_silently=False,
        )
        return 'Correo enviado correctamente.'
    except Exception as e:
        return f'Error al enviar el correo: {str(e)}'
