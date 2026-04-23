import os
from celery import Celery

# configs padrão do django pro celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'EstoqueAlpenBier.settings')

# cria instancia do celery
app = Celery('EstoqueAlpenBier')

# le as configs do settings
app.config_from_object('django.conf.settings', namespace='CELERY')

# procura por arquivos chamados "tasks"
app.autodiscover_tasks()