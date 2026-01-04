from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.views import generic


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