from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from .views import criar_pedido


urlpatterns = [
    path('all/', views.all, name="all"),
    path('login/', views.login, name="login"),
    path('accounts/', include('django.contrib.auth.urls')),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('excluir_pedido/<int:pedido_id>/', views.excluir_pedido, name='excluir_pedido'),
    path('imprimir_pedido/<int:pedido_id>/', views.imprimir_pedido, name='imprimir_pedido'),
    path('criar_pedido/', criar_pedido, name='criar_pedido'),
    path('impressao/', views.imprimir_pedido, name="impressao"),
    path('cadastrar_produtos/', views.cadastrar_produtos, name="cadastrar_produtos"),
    path('cadastrar_clientes/', views.cadastrar_clientes, name="cadastrar_clientes"),
    path('cadastrar_empresa/', views.cadastrar_empresa, name="cadastrar_empresa"),
    path('cadastrar_vendedores/', views.cadastrar_vendedores, name="cadastrar_vendedores"),
    path('all_produtos/', views.all_produtos, name="all_produtos"),
    path('all_clientes/', views.all_clientes, name="all_clientes"),
    path('gerenciamento/', views.gerenciamento, name="gerenciamento"),
    path('buscar_cliente/', views.buscar_cliente, name='buscar_cliente'),
    
]
