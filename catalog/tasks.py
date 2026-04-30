from celery import shared_task
from datetime import timedelta, date
from .models import ProdutoVenda, Locacao, NotificacaoSistema

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.auth.models import User
from django.conf import settings

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

    # emails

    total_pendencias = produtos_vencendo.count() + alugueis_atrasados.count()

    if total_pendencias > 0:
        # busca apenas emails dos administradores
        emails_admin = list(User.objects.filter(is_superuser=True).exclude(email='').values_list('email', flat=True))

        if emails_admin:
            assunto = f"Alpen Bier: {total_pendencias} Pendencias no Estoque"

            # renderiza html
            html_mensagem = render_to_string(
                'emails/relatorio_diario.html',{
                    'produtos': produtos_vencendo,
                    'alugueis': alugueis_atrasados,
                }
            )

            # cria versão em texto puro caso html seja bloqueado
            texto_puro = strip_tags(html_mensagem)

            send_mail(
                subject=assunto,
                message=texto_puro,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=emails_admin,
                html_message=html_mensagem,
                fail_silently=False,
            )

    return f"Checagem concluída: {produtos_vencendo.count()} produtos vencendo, {alugueis_atrasados.count()} alugueis atrasados."

