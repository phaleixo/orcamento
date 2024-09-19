from django import forms
from .models import Pedido
from .models import CadastrarProduto
from .models import CriarCliente
from .models import CadastroEmpresa
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User



class PedidoForm(forms.ModelForm):
    produto = forms.ModelChoiceField(
        queryset=CadastrarProduto.objects.all(),
        label='Produto',
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    valor_unitario = forms.DecimalField(
        label='Valor Unit. R$',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'R$ 0,00'}),
        required=False
    )
    class Meta:
        model = Pedido
        fields = '__all__'  # Use todos os campos do modelo Pedido
        # Caso queira selecionar campos específicos:
        #fields = ['data', 'nome_cliente', 'contato', 'cpf_cnpj','descricao_pedido', 'descricao_impresso', 'valor_total']
        
class CadastrarProdutoForm(forms.ModelForm):    
    class Meta:
        model = CadastrarProduto
        fields = ['cod_produto', 'produto', 'descricao_produto','valorproduto']

class CriarClienteForm(forms.ModelForm):
    class Meta:
        model = CriarCliente
        fields = ['nome_cliente', 'cpf_cnpj', 'contato', 'detal_cliente']

class CadastroEmpresaForm(forms.ModelForm):
    class Meta:
        model = CadastroEmpresa
        fields = ['nome_empresa','logo', 'cpf_cnpj', 'contato', 'end_empresa',]

class CustomUserCreationForm(UserCreationForm):
    full_name = forms.CharField(max_length=100, required=True, help_text='Nome completo')

    class Meta:
        model = User
        fields = ('username', 'full_name', 'password1', 'password2')

# Forms para edicao de produtos
class EditarProdutoForm(forms.ModelForm):
    class Meta:
        model = CadastrarProduto
        fields = ['cod_produto', 'produto', 'valorproduto', 'descricao_produto']

# Forms para edicao de vendedores
class EditarVendedorForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['last_name', 'first_name', 'username']
        labels = {
            'last_name': 'Código do Vendedor',  # Personalizando o rótulo
            'first_name': 'Nome do Vendedor',
            'username': 'Nome de Usuário',
        }       