from datetime import datetime

from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models import UniqueConstraint
from django.urls import reverse
from django.db.models.functions import Lower

# Create your models here.

class TipoItem(models.Model):
    nomeTipo = models.CharField(max_length=120)

    def __str__(self):
        return self.nomeTipo

class Local(models.Model):
    nome = models.CharField(max_length=120)
    endereco = models.CharField(max_length=120)

    def __str__(self):
        return self.nome

class ProdutoVenda(models.Model):
    tipo = models.ForeignKey(TipoItem, on_delete=models.CASCADE)
    local = models.ForeignKey(Local, on_delete=models.CASCADE)
    validade = models.DateField()
    quantidade = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.tipo.nomeTipo} em {self.local.nome}"

class EquipamentoAlugavel(models.Model):

    STATUS_CHOICES = [('DISP', 'Disponivel'),('ALUG', 'Alugado'), ('MANU', 'Manutenção')]

    tipo = models.ForeignKey(TipoItem, on_delete=models.CASCADE)
    local_origem = models.ForeignKey(Local, on_delete=models.CASCADE)
    numeracao = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DISP')
    preco = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.tipo.nomeTipo} em {self.local_origem.nome}"


class Locacao(models.Model):
    equipamento = models.ForeignKey(EquipamentoAlugavel, on_delete=models.CASCADE)
    cliente_local = models.CharField(max_length=120)
    dataInicio = models.DateField()
    dataFim = models.DateField()
    devolvido = models.BooleanField(default=False)


class Cliente(models.Model):
    nome = models.CharField(max_length=120)
    endereco = models.CharField(max_length=120, blank=True, null=True)
    cpf_cnpj = models.CharField(max_length=120, unique=True, verbose_name="CPF/CNPJ", blank=True, null=True)
    telefone = models.CharField(max_length=120, blank=True, null=True)

    def __str__(self):
        return self.nome

# adicionar historico de vendas/transações

# class Venda(models.Model):
#     itensComprados = models.ManyToManyField(TipoItem)
#     Comprador = models.ForeignKey(Cliente, on_delete=models.CASCADE)
#     DataVenda = models.DateField()

class Venda(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    local_origem = models.ForeignKey(Local, on_delete=models.CASCADE)
    data_venda = models.DateField(blank=True, null=True)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Venda {self.id} - {self.cliente.nome}"

class ItemVenda(models.Model):
    venda = models.ForeignKey(Venda, on_delete=models.CASCADE, related_name='itens')
    tipo_item = models.ForeignKey(TipoItem, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(default=0)
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

