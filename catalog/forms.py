from django import forms
from .models import Venda, ItemVenda

class VendaForm(forms.ModelForm):
    class Meta:
        model = Venda
        fields = ['cliente']

ItemVendaFormSet = forms.inlineformset_factory(
    Venda, ItemVenda,
    fields=['tipo_item', 'quantidade', 'preco_unitario'],
    extra=1, # Começa com apenas 1 linha
    can_delete=True
)