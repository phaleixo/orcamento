from django.contrib.admin import AdminSite
from django.db.models import Count, Sum
from django.db.models.functions import Coalesce
from .models import Pedido, CadastrarProduto, CriarCliente, User
from django.contrib.auth.models import Group

class CustomAdminSite(AdminSite):
    def index(self, request, extra_context=None):
        # Get total counts
        total_clientes = CriarCliente.objects.count()
        total_pedidos = Pedido.objects.count()
        total_produtos = CadastrarProduto.objects.count()
        
        # Calculate total revenue
        valor_total_pedidos = Pedido.objects.aggregate(
            total=Coalesce(Sum('valor_total'), 0)
        )['total']
        
        # Get top vendedores (users in the 'vendedores' group)
        vendedores_group = Group.objects.get(name='vendedores')
        vendedores_pedidos = User.objects.filter(groups=vendedores_group).annotate(
            count=Count('pedido'),
            total=Coalesce(Sum('pedido__valor_total'), 0)
        ).values('username', 'count', 'total').order_by('-total')[:5]
        
        # Get top produtos
        top_produtos = CadastrarProduto.objects.annotate(
            quantidade=Count('pedido'),
            total=Coalesce(Sum('pedido__valor_total'), 0)
        ).values('produto', 'quantidade', 'total').order_by('-total')[:5]
        
        # Add the data to the context
        extra_context = extra_context or {}
        extra_context.update({
            'total_clientes': total_clientes,
            'total_pedidos': total_pedidos,
            'total_produtos': total_produtos,
            'valor_total_pedidos': valor_total_pedidos,
            'vendedores_pedidos': vendedores_pedidos,
            'top_produtos': top_produtos,
        })
        
        return super().index(request, extra_context=extra_context) 