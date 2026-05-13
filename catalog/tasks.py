import os.path

import pandas as pd
from celery import shared_task
from datetime import timedelta, date
from .models import ProdutoVenda, Locacao, NotificacaoSistema, Local, TipoItem

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

@shared_task
def processar_planilha_estoque(caminho_arquivo):
    try:
        # le arquivo csv ou excel
        if caminho_arquivo.endswith('.csv'):
            df = pd.read_csv(caminho_arquivo)
        else:
            df = pd.read_excel(caminho_arquivo)

        sucessos = 0
        erros = []

        # percorre cada linha
        for index, row in df.iterrows():
            nome_produto = "Desconhecido" # Sempre bom ter o fallback
            try:
                # extrai dados das linhas
                nome_produto = str(row['produto']).strip()
                nome_deposito = str(row['deposito']).strip()
                quantidade = int(row['quantidade'])

                validade = pd.to_datetime(row['data_validade'], format='%d/%m/%Y').date()

                # busca referencias no bd
                tipo = TipoItem.objects.get(nomeTipo=nome_produto)
                local = Local.objects.get(nome=nome_deposito)

                # registra no estoque
                ProdutoVenda.objects.create(
                    tipo=tipo,
                    local=local,
                    quantidade=quantidade,
                    validade=validade,
                )
                sucessos += 1

            except Exception as e:
                # se produto não existir/data errada anota erro e pula
                erros.append(f"Erro na linha {index + 2} ({nome_produto}): {str(e)}")

        # apaga arquivo temporario para não lotar pasta
        if os.path.exists(caminho_arquivo):
            os.remove(caminho_arquivo)

        print(f"\n--- RESULTADO: {sucessos} adicionados, {len(erros)} erros ---\nErros detalhados: {erros}\n")

        # cria notiff
        if len(erros) == 0:
            mensagem_alerta = f"<strong>SUCESSO NA IMPORTAÇÃO:</strong> A planilha foi lida perfeitamente! {sucessos} novos lotes foram adicionados ao estoque."
        else:
            mensagem_alerta = f"<strong>AVISO DE IMPORTAÇÃO:</strong> Processamento finalizado. {sucessos} itens adicionados, mas ocorreram {len(erros)} erros (linhas ignoradas). Verifique se os nomes batem com o cadastro."

        NotificacaoSistema.objects.create(
            tipo="IMPORTACAO",
            mensagem=mensagem_alerta,
            lida=False
        )

        return f"Planilha processada! {sucessos} adicionados. {len(erros)} erros."

    except Exception as e:
        # Se falhar totalmente, cria notificação de erro
        NotificacaoSistema.objects.create(
            tipo="IMPORTACAO",
            mensagem=f"<strong>FALHA CRÍTICA:</strong> Não foi possível ler a planilha enviada. Erro: {str(e)}",
            lida=False
        )
        return f"Falha crítica ao ler o arquivo: {str(e)}"