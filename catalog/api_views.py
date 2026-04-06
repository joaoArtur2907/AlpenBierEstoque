from django.template.defaulttags import querystring
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import ProdutoVenda, Local
from .serializers import ProdutoVendaSerializer, LocalSerializer

class LocalViewSet(viewsets.ReadOnlyModelViewSet):
    """Retorna Locais"""
    queryset = Local.objects.all()
    serializer_class = LocalSerializer
    permission_classes = [IsAuthenticated]

class ProdutoVendaViewSet(viewsets.ReadOnlyModelViewSet):
    """Retorna estoque, lotes de produtos iguais são separados por validade e local"""
    serializer_class = ProdutoVendaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # otimização de banco
        queryset = ProdutoVenda.objects.select_related('tipo', 'local').all()

        # captura os parâmetros da url
        local_id = self.request.query_params.get('local', None)
        tipo_id = self.request.query_params.get('tipo', None)

        # aplica filtros
        if local_id:
            queryset = queryset.filter(local=local_id)
        if tipo_id:
            queryset = queryset.filter(tipo=tipo_id)

        # ordena pela validade mais curta
        return queryset.order_by('validade')