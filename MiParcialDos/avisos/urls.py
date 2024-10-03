from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('productos/', views.productos_view, name='productos'),
    path('ver-lista/', views.ver_lista_view, name='ver_lista'),
    path('perfil/', views.perfil_view, name='perfil'),
    path('logout/', views.logout_view, name='logout'),
]
