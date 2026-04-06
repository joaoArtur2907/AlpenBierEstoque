from rest_framework import serializers
from .models import TipoItem, Local, ProdutoVenda

class TipoItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoItem
        fields = ['id', 'nomeTipo']

class LocalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Local
        fields = ['id', 'nome']

class ProdutoVendaSerializer(serializers.ModelSerializer):
    # mandando objeto detalhado para leitura
    # mantendo campos originais para possivel POST

    tipo_detalhe = TipoItemSerializer(source='tipo', read_only=True)
    local_detalhe = LocalSerializer(source='local', read_only=True)

    class Meta:
        model = ProdutoVenda
        fields = [
            'id',
            'tipo', 'tipo_detalhe',
            'local', 'local_detalhe',
            'validade', 'quantidade'
        ]

