from django.contrib import admin

from django.contrib import admin
from .models import NotificacaoSistema


@admin.register(NotificacaoSistema)
class NotificacaoSistemaAdmin(admin.ModelAdmin):
    list_display = ('tipo', 'mensagem', 'lida', 'data_criacao')

    list_filter = ('tipo', 'lida')

    search_fields = ('mensagem',)