# MiParcialDos/celery.py
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Establece el módulo de configuración predeterminado de Django para el programa 'celery'.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MiParcialDos.settings')

app = Celery('MiParcialDos')

# Carga la configuración de Django en Celery.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Descubre tareas automáticamente en todos los módulos 'tasks.py' de las aplicaciones registradas en Django.
app.autodiscover_tasks()
