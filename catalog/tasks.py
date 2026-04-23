from celery import shared_task
from datetime import timedelta, date
from .models import ProdutoVenda, Locacao, NotificacaoSistema

@shared_task
def checar_alertas_diarios():
    # Limpa alertas antigos
    NotificacaoSistema.objects.filter(lida=False).delete()

    hoje = date.today()
    daqui_sete_dias = hoje + timedelta(days=7)

    # Busca produtos prestes a vencer (7 dias min)
    produtos_vencendo = ProdutoVenda.objects.filter(
        validade__lte=daqui_sete_dias,
        quantidade__gte=0
    )

    for produto in produtos_vencendo:
        mensagem = f"<strong>ALERTA:</strong> O lote de {produto.tipo} no depósito '{produto.local.nome}' vence em {produto.validade.strftime('%d/%m/%Y')}!"
        NotificacaoSistema.objects.get_or_create(
            tipo="VENCIMENTO",
            mensagem=mensagem,
            lida=False
        )
    # busca equipamentos não devolvidos após prazo
    alugueis_atrasados = Locacao.objects.filter(
        dataFim__lt= hoje,
        devolvido=False
    )

    for aluguel in alugueis_atrasados:
        mensagem = f"<strong>ATRASO:</strong> Locação para {aluguel.cliente_local} deveria ter sido devolvida em {aluguel.dataFim.strftime('%d/%m/%Y')}."
        NotificacaoSistema.objects.get_or_create(
            tipo="ATRASO",
            mensagem=mensagem,
            lida=False
        )

    return f"Checagem concluída: {produtos_vencendo.count()} produtos vencendo, {alugueis_atrasados.count()} alugueis atrasados."