# avisos/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('enviar-correo/', views.enviar_correo_vista, name='enviar_correo'),
]