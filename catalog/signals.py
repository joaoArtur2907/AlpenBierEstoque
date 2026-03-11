
from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from .models import ProdutoVenda, HistoricoMovimentacaoEstoque
# observadores
# antes de salvar
@receiver(pre_save, sender=ProdutoVenda)
def preparar_auditoria(sender, instance, **kwargs):
    if instance.pk: # item já existe no banco
        try:
            produto_original = sender.objects.get(pk=instance.pk)
            # Guarda o valor antigo temporariamente
            instance._estoque_anterior = produto_original.quantidade
        except sender.DoesNotExist:
            instance._estoque_anterior = 0
    else: # item novo
        instance._estoque_anterior = 0

# depois de salvar
@receiver(post_save, sender=ProdutoVenda)
def auditar_salvamento(sender, instance, created, **kwargs):
    estoque_anterior = getattr(instance, '_estoque_anterior', 0)
    estoque_novo = instance.quantidade

    if estoque_anterior != estoque_novo:
        diferenca = estoque_novo - estoque_anterior
        tipo = "ENTRADA" if diferenca > 0 else "SAIDA"

        HistoricoMovimentacaoEstoque.objects.create(
            produto=instance,
            produto_nome_snapshot=instance.tipo.nomeTipo,
            tipo_movimento=tipo,
            quantidade_alterada=diferenca,
            estoque_anterior=estoque_anterior,
            estoque_atual=estoque_novo,
            origem="Criação Inicial" if created else "Atualização de Estoque"
        )

# item deletado
@receiver(post_delete, sender=ProdutoVenda)
def auditar_exclusao(sender, instance, **kwargs):
    HistoricoMovimentacaoEstoque.objects.create(
        produto=None,
        produto_nome_snapshot=instance.tipo.nomeTipo,
        tipo_movimento="SAIDA",
        quantidade_alterada=-instance.quantidade,
        estoque_anterior=instance.quantidade,
        estoque_atual=0,
        origem="Produto Excluído do Sistema"
    )