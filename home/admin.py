from django.contrib import admin
from .models import Pedido
from .models import CadastrarProduto
from .models import CriarCliente
from .models import CadastroEmpresa
from .admin_site import CustomAdminSite

# Create custom admin site
admin_site = CustomAdminSite(name='admin')

# Register models with the custom admin site
admin_site.register(Pedido)
admin_site.register(CadastrarProduto)
admin_site.register(CriarCliente)
admin_site.register(CadastroEmpresa)
