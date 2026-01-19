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
from django import core
# from django.contrib import admin
from django.urls import path
from catalog import views
from django.urls import path, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('admin/', admin.site.urls),

    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(template_name='registration/logged_out.html'), name='logout'),
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

    path('equipamento/<int:pk>/alugar/', views.LocacaoCreateView.as_view(), name='locacao_create'),
    path('equipamento/<int:pk>/devolver/', views.EquipamentoDevolverView.as_view(), name='equipamento_devolver'),

    # cliente

    path('cliente/', views.ClienteListView.as_view(), name='cliente_list'),
    path('cliente/novo/', views.ClienteCreateView.as_view(), name='cliente_create'),
    path('cliente/editar/<int:pk>/', views.ClienteUpdateView.as_view(), name='cliente_update'),
    path('cliente/deletar/<int:pk>/', views.ClienteDeleteView.as_view(), name='cliente_delete'),

    # venda
    path('local/<int:local_id>/venda/nova/', views.VendaCreateView.as_view(), name='venda_create'),
    path('vendas/', views.VendaListView.as_view(), name='venda_list'),

    # users
    path('usuarios/', views.UserListView.as_view(), name='user-list'),
    path('usuarios/create', views.UserCreateView.as_view(), name='usuarios-create'),
    path('usuarios/<int:pk>/update', views.UserUpdateView.as_view(), name='usuarios-update'),
    path('usuarios/<int:pk>/delete', views.UserDeleteView.as_view(), name='usuarios-delete'),



]
