from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Define o módulo de settings do Django para o Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'automotivas.settings')

app = Celery('automotivas')

# Lê as configurações do Django e aplica a namespace "CELERY" para todas as configurações relacionadas
app.config_from_object('django.conf:settings', namespace='CELERY')

# Descobre automaticamente tasks em cada app registrado no Django
app.autodiscover_tasks()

# Exemplo de uma task simples (opcional)
@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

