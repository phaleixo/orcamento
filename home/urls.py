from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from .views import criar_pedido
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('all/', views.all, name="all"),
    path('login/', views.login, name="login"),
    path('accounts/', include('django.contrib.auth.urls')),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('excluir_pedido/<int:pedido_id>/', views.excluir_pedido, name='excluir_pedido'),
    path('excluir_produto/<int:cadastrarproduto_id>/', views.excluir_produto, name='excluir_produto'),
    path('produtos/editar/<int:produto_id>/', views.editar_produto, name='editar_produto'),
    path('imprimir_pedido/<int:pedido_id>/', views.imprimir_pedido, name='imprimir_pedido'),
    path('criar_pedido/', criar_pedido, name='criar_pedido'),
    path('impressao/', views.imprimir_pedido, name="impressao"),
    path('cadastrar_produtos/', views.cadastrar_produtos, name="cadastrar_produtos"),
    path('cadastrar_clientes/', views.cadastrar_clientes, name="cadastrar_clientes"),
    path('cadastrar_empresa/', views.cadastrar_empresa, name="cadastrar_empresa"),
    path('cadastrar_vendedores/', views.cadastrar_vendedores, name="cadastrar_vendedores"),
    path('all_vendedores/', views.all_vendedores, name="all_vendedores"),
    path('vendedores/editar/<int:vendedor_id>/', views.editar_vendedor, name='editar_vendedor'),
    path('all_produtos/', views.all_produtos, name="all_produtos"),
    path('all_clientes/', views.all_clientes, name="all_clientes"),
    path('clientes/editar/<int:cliente_id>/', views.editar_cliente, name='editar_cliente'),
    path('configuracoes/', views.configuracoes, name="configuracoes"),
    path('gerenciamento/', views.gerenciamento, name="gerenciamento"),
    path('buscar_cliente/', views.buscar_cliente, name='buscar_cliente'),
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
