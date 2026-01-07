from django import forms
from .models import Venda, ItemVenda

class VendaForm(forms.ModelForm):
    class Meta:
        model = Venda
        fields = ['cliente']

# O Formset permite adicionar vários ItemVenda a uma Venda
ItemVendaFormSet = forms.inlineformset_factory(
    Venda, ItemVenda,
    fields=['tipo_item', 'quantidade', 'preco_unitario'],
    extra=3, # Quantos espaços vazios aparecem inicialmente
    can_delete=True
)