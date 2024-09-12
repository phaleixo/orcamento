from django.contrib import admin
from .models import Pedido
from .models import CadastrarProduto
from .models import CriarCliente
from .models import CadastroEmpresa


admin.site.register(Pedido)
admin.site.register(CadastrarProduto)
admin.site.register(CriarCliente)
admin.site.register(CadastroEmpresa)
