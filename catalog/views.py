from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db import transaction
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.views import generic
from .models import Locacao, EquipamentoAlugavel, Cliente, Venda, ItemVenda
from django.shortcuts import get_object_or_404
from datetime import date
from .forms import VendaForm, ItemVendaFormSet

from catalog.models import Locacao, Local, ProdutoVenda, TipoItem, EquipamentoAlugavel


# Create your views here.

class LocalListView(ListView):
    model = Local
    template_name = 'core/local_list.html'
    context_object_name = 'locais'

class CreateLocalView(CreateView):
    model = Local
    fields = '__all__'
    template_name = 'core/local_form.html'
    success_url = reverse_lazy('local_list')

class UpdateLocalView(UpdateView):
    model = Local
    fields = ['nome', 'endereco']
    success_url = reverse_lazy('local_list')
    template_name = 'core/local_form.html'

class DeleteLocalView(DeleteView):
    model = Local
    success_url = reverse_lazy('local_list')
    template_name = 'core/local_confirm_delete.html'

class LocalDetailView(generic.DetailView):
    model = Local
    template_name = 'core/local_detail.html'
    context_object_name = 'local'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['itens_venda'] = self.object.produtovenda_set.all().select_related('tipo')
        context['equipamentos'] = self.object.equipamentoalugavel_set.all().select_related('tipo')
        return context

class ProdutoVendaListView(ListView):
    model = ProdutoVenda
    template_name = 'core/registro_venda_list.html'
    context_object_name = 'registro_venda'

class ProdutoVendaCreateView(CreateView):
    model = ProdutoVenda
    fields = '__all__'
    template_name = 'core/produtovenda_form.html'

    # pega o id do viveiro e adiciona diretamente no formulario
    def get_initial(self):
        initial = super().get_initial()
        local_id = self.kwargs.get('local_id')
        if local_id:
            initial['local'] = local_id
        return initial

    # faz o campo viveiro ser readonly
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        local_id = self.kwargs.get('local_id')
        if local_id:
            form.fields['local'].initial = local_id
            form.fields['local'].widget.attrs['readonly'] = True
        return form

    def get_success_url(self):
        return reverse('local_detail', kwargs={'pk': self.object.local.id})

class ProdutoVendaUpdateView(UpdateView):
    model = ProdutoVenda
    fields = '__all__'
    template_name = 'core/produtovenda_form.html'

    def get_success_url(self):
        return reverse('local_detail', kwargs={'pk': self.object.local.id})

class ProdutoVendaDeleteView(DeleteView):
    model = ProdutoVenda
    fields = '__all__'
    template_name = 'core/produtovenda_confirm_delete.html'

    def get_success_url(self):
        return reverse('local_detail', kwargs={'pk': self.object.local.id})


class TipoItemListView(ListView):
    model = TipoItem
    template_name = 'core/tipoitem_list.html'
    context_object_name = 'itens'

class TipoItemCreateView(CreateView):
    model = TipoItem
    fields = '__all__'
    template_name = 'core/tipoitem_form.html'
    success_url = reverse_lazy('tipoitem_list')

class TipoItemUpdateView(UpdateView):
    model = TipoItem
    fields = '__all__'
    template_name = 'core/tipoitem_form.html'
    success_url = reverse_lazy('tipoitem_list')

class TipoItemDeleteView(DeleteView):
    model = TipoItem
    fields = '__all__'
    template_name = 'core/tipoitem_confirm_delete.html'
    success_url = reverse_lazy('tipoitem_list')


class EquipamentoAlugavelCreateView(CreateView):
    model = EquipamentoAlugavel
    fields = '__all__'
    template_name = 'core/equipamentoalugavel_form.html'

    # pega o id do viveiro e adiciona diretamente no formulario
    def get_initial(self):
        initial = super().get_initial()
        local_id = self.kwargs.get('local_id')
        if local_id:
            initial['local'] = local_id
        return initial

    # faz o campo viveiro ser readonly
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        local_id = self.kwargs.get('local_id')
        if local_id:
            form.fields['local_origem'].initial = local_id
            form.fields['local_origem'].widget.attrs['readonly'] = True
        return form

    def get_success_url(self):
        return reverse('local_detail', kwargs={'pk': self.object.local_origem.id})

class EquipamentoAlugavelUpdateView(UpdateView):
    model = EquipamentoAlugavel
    fields = '__all__'
    template_name = 'core/equipamentoalugavel_form.html'

    def get_success_url(self):
        return reverse('local_detail', kwargs={'pk': self.object.local_origem.id})

class EquipamentoAlugavelDeleteView(DeleteView):
    model = EquipamentoAlugavel
    fields = '__all__'
    template_name = 'core/equipamentoalugavel_confirm_delete.html'

    def get_success_url(self):
        return reverse('local_detail', kwargs={'pk': self.object.local_origem.id})


class LocacaoCreateView(CreateView):
    model = Locacao
    fields = ['cliente_local', 'dataInicio', 'dataFim']
    template_name = 'core/locacao_form.html'

    def form_valid(self, form):
        # Captura o equipamento pelo ID passado na URL
        equipamento = get_object_or_404(EquipamentoAlugavel, pk=self.kwargs.get('pk'))

        # Associa o equipamento à locação
        form.instance.equipamento = equipamento

        # LÓGICA DE STATUS: Muda o status para Alugado
        equipamento.status = 'ALUG'
        equipamento.save()

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Passa o equipamento para o template para mostrar o nome/série
        context['equipamento'] = get_object_or_404(EquipamentoAlugavel, pk=self.kwargs.get('pk'))
        return context

    def get_success_url(self):
        # Retorna para o local de origem do equipamento
        return reverse('local_detail', kwargs={'pk': self.object.equipamento.local_origem.id})


class EquipamentoDevolverView(generic.View):
    def get(self, request, *args, **kwargs):
        # Busca o equipamento
        equipamento = get_object_or_404(EquipamentoAlugavel, pk=self.kwargs.get('pk'))

        # Muda o status de volta para Disponível
        equipamento.status = 'DISP'
        equipamento.save()

        # Busca a locação ativa deste equipamento e marca como devolvida
        locacao = Locacao.objects.filter(equipamento=equipamento, devolvido=False).last()
        if locacao:
            locacao.devolvido = True
            locacao.save()

        # Redireciona de volta para o detalhe do local
        return redirect('local_detail', pk=equipamento.local_origem.id)

# cliente

class ClienteListView(ListView):
    model = Cliente
    template_name = 'core/cliente_list.html'
    context_object_name = 'clientes'

class ClienteCreateView(CreateView):
    model = Cliente
    fields = '__all__'
    template_name = 'core/cliente_form.html'
    success_url = reverse_lazy('cliente_list')

class ClienteUpdateView(UpdateView):
    model = Cliente
    fields = '__all__'
    template_name = 'core/cliente_form.html'
    success_url = reverse_lazy('cliente_list')

class ClienteDeleteView(DeleteView):
    model = Cliente
    fields = '__all__'
    template_name = 'core/cliente_confirm_delete.html'
    success_url = reverse_lazy('cliente_list')


class VendaCreateView(CreateView):
    model = Venda
    form_class = VendaForm
    template_name = 'core/venda_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        local_id = self.kwargs.get('local_id')

        # Filtro para o dropdown: apenas produtos com estoque > 0 neste local
        tipos_disponiveis = TipoItem.objects.filter(
            produtovenda__local_id=local_id,
            produtovenda__quantidade__gt=0
        ).distinct()

        # Prioriza o formset que já contém erros, se existir
        if 'itens' in kwargs:
            itens_formset = kwargs['itens']
        else:
            if self.request.POST:
                itens_formset = ItemVendaFormSet(self.request.POST)
            else:
                itens_formset = ItemVendaFormSet()

        # Aplica o filtro de estoque em cada linha da tabela
        for f in itens_formset.forms:
            f.fields['tipo_item'].queryset = tipos_disponiveis

        context['itens'] = itens_formset
        context['local_id'] = local_id
        return context

    def form_valid(self, form):
        # Instancia o formset para validação
        itens_formset = ItemVendaFormSet(self.request.POST)
        local = get_object_or_404(Local, pk=self.kwargs.get('local_id'))

        if itens_formset.is_valid():
            # Validação de Estoque antes de salvar
            for item_form in itens_formset:
                if item_form.cleaned_data and not item_form.cleaned_data.get('DELETE'):
                    tipo = item_form.cleaned_data.get('tipo_item')
                    qtd_pedida = item_form.cleaned_data.get('quantidade')

                    preco = item_form.cleaned_data.get('preco_unitario')

                    # Validação de valor negativo ou zero
                    if qtd_pedida <= 0:
                        item_form.add_error('quantidade', "A quantidade deve ser maior que zero.")
                        return self.render_to_response(self.get_context_data(form=form, itens=itens_formset))

                    if preco < 0:
                        item_form.add_error('preco_unitario', "O preço não pode ser negativo.")
                        return self.render_to_response(self.get_context_data(form=form, itens=itens_formset))

                    total_estoque = sum(p.quantidade for p in ProdutoVenda.objects.filter(local=local, tipo=tipo))

                    if total_estoque < qtd_pedida:
                        # Adiciona o erro e retorna o formset específico
                        item_form.add_error('quantidade', f"Estoque insuficiente! (Disponível: {total_estoque})")
                        return self.render_to_response(self.get_context_data(form=form, itens=itens_formset))



            with transaction.atomic():
                form.instance.local_origem = local
                form.instance.data_venda = date.today()

                if form.instance.cliente:
                    form.instance.cliente_nome_snapshot = form.instance.cliente.nome

                self.object = form.save()

                itens = itens_formset.save(commit=False)
                total_venda = 0

                for item in itens:
                    item.venda = self.object

                    if item.tipo_item:
                        item.produto_nome_snapshot = item.tipo_item.nomeTipo

                    estoque = list(ProdutoVenda.objects.filter(local=local, tipo=item.tipo_item).order_by('validade'))

                    restante = item.quantidade
                    for lote in estoque:
                        if restante <= 0: break
                        if lote.quantidade <= restante:
                            restante -= lote.quantidade
                            lote.delete()
                        else:
                            lote.quantidade -= restante
                            lote.save()
                            restante = 0

                    total_venda += (item.quantidade * item.preco_unitario)
                    item.save()

                self.object.valor_total = total_venda
                self.object.save()
                return redirect(self.get_success_url())

        return self.render_to_response(self.get_context_data(form=form, itens=itens_formset))

    def get_success_url(self):
        return reverse('local_detail', kwargs={'pk': self.kwargs.get('local_id')})
class VendaListView(ListView):
    model = Venda
    template_name = 'core/venda_list.html'
    context_object_name = 'vendas'

    def get_queryset(self):
        queryset = Venda.objects.all().order_by('-data_venda')
        local_id = self.request.GET.get('local') # Pega o ?local=ID da URL
        if local_id:
            queryset = queryset.filter(local_origem_id=local_id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['locais'] = Local.objects.all() # Para o botão de filtro
        return context