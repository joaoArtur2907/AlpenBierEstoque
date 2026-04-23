from .models import NotificacaoSistema

def alertas_sistema(request):

    if not request.user.is_authenticated:
        return {'alertas_globais': None, 'total_alertas': 0}

    alertas = NotificacaoSistema.objects.filter(lida=False).order_by('-data_criacao')
    return {
        'alertas_globais': alertas,
        'total_alertas': alertas.count(),
    }