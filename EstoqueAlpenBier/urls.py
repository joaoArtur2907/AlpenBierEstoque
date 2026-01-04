"""
URL configuration for EstoqueAlpenBier project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.urls import path
from catalog import views
from django.urls import path, include

urlpatterns = [
    #    path('admin/', admin.site.urls),
    # locais
    path('locais/', views.LocalListView.as_view(), name='local_list'),
    path('locais/novo/', views.CreateLocalView.as_view(), name='local_create'),
    path('locais/editar/<int:pk>/', views.UpdateLocalView.as_view(), name='local_update'),
    path('locais/deletar/<int:pk>/', views.DeleteLocalView.as_view(), name='local_delete'),
    path('locais/<int:pk>/', views.LocalDetailView.as_view(), name='local_detail'),
    # produto
    path('produtovenda/<int:local_id>/novo/', views.ProdutoVendaCreateView.as_view(), name='produtovenda_create'),
    path('produtovenda/editar/<int:pk>/', views.ProdutoVendaUpdateView.as_view(), name='produtovenda_update'),
    path('produtovenda/deletar/<int:pk>/', views.ProdutoVendaDeleteView.as_view(), name='produtovenda_delete'),

    # tipo item
    path('tipoitem/', views.TipoItemListView.as_view(), name='tipoitem_list'),
    path('tipoitem/novo/', views.TipoItemCreateView.as_view(), name='tipoitem_create'),
    path('tipoitem/editar/<int:pk>/', views.TipoItemUpdateView.as_view(), name='tipoitem_update'),
    path('tipoitem/deletar/<int:pk>/', views.TipoItemDeleteView.as_view(), name='tipoitem_delete'),

    # item alugavel

    path('equipamentoalugavel/<int:local_id>/novo/', views.EquipamentoAlugavelCreateView.as_view(), name='equipamentoalugavel_create'),
    path('equipamentoalugavel/editar/<int:pk>/', views.EquipamentoAlugavelUpdateView.as_view(), name='equipamentoalugavel_update'),
    path('equipamentoalugavel/deletar/<int:pk>/', views.EquipamentoAlugavelDeleteView.as_view(), name='equipamentoalugavel_delete'),


]
