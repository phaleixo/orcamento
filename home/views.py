from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required,  user_passes_test
from django.contrib.auth import logout
from django.views.decorators.http import require_POST
from .models import Pedido, CadastrarProduto
from .forms import PedidoForm
from datetime import date
from datetime import datetime
from decimal import Decimal, InvalidOperation
from .forms import CadastrarProdutoForm
from .forms import CriarClienteForm
from .forms import CadastroEmpresaForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.utils import timezone


# Função para verificar se o usuário pertence ao grupo 'gestores'
def is_in_group_gestores(user):
    return user.groups.filter(name='gestores').exists()

@login_required
def all(request):
    # Se o usuário for do grupo 'gestores', redirecionar para a página de gerenciamento
    if is_in_group_gestores(request.user):
        return redirect('gerenciamento')

    # Caso não seja do grupo 'gestores', exibir pedidos apenas do usuário logado
    pedidos = Pedido.objects.filter(vendedor=request.user)
    now = timezone.now()
    ano = str(now.year).zfill(4)
    mes = str(now.month).zfill(2)
    dia = str(now.day).zfill(2)
    data_atual = ano + mes + dia

    for pedido in pedidos:
        pedido.nome_cliente = pedido.nome_cliente.upper() if pedido.nome_cliente else ''
        pedido.cpf_cnpj = pedido.cpf_cnpj.upper() if pedido.cpf_cnpj else ''
        

    context = {
        'data_atual': data_atual,
        'pedidos': pedidos,
    }

    return render(request, 'all.html', context)

@require_POST
def custom_logout(request):
    logout(request)
    return render ('login.html')  # Redireciona para a página de login (login.html)

# Função para verificar se o usuário pertence ao grupo 'gestores'      
def is_in_group_gestores(user):
    return user.groups.filter(name='gestores').exists()

@login_required
@user_passes_test(is_in_group_gestores)
def gerenciamento(request):
    pedidos = Pedido.objects.all()
    now = datetime.now()
    ano = str(now.year).zfill(4) 
    mes = str(now.month).zfill(2) 
    dia = str(now.day).zfill(2)
    data_atual = ano + mes + dia
    for pedido in pedidos:
        pedido.nome_cliente = pedido.nome_cliente.upper() if pedido.nome_cliente else ''
        pedido.cpf_cnpj = pedido.cpf_cnpj.upper() if pedido.cpf_cnpj else ''
    
    context = {
        'data_atual': data_atual,
        'pedidos': pedidos
    }
    return render(request, 'gerenciamento.html', context)

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            # Autenticar o usuário
            user = form.get_user()
            auth_login(request, user)
            # Redirecionar para a página 'all.html' após o login
            return redirect('all')  # 'all' é o nome da URL para 'all.html'
    else:
        form = AuthenticationForm()
    
    return render(request, 'login.html', {'form': form})


# Função para converter valor monetário brasileiro em Decimal
def parse_decimal_br(value):
    return Decimal(value.replace('.', '').replace(',', '.'))

@login_required
def criar_pedido(request):
    data_atual = datetime.now().date()  # Obter a data atual (sem hora)

    if request.method == 'POST':
        form = PedidoForm(request.POST)
        if form.is_valid():
            # Processar a data do formulário e atribuir ao campo data_pedido
            data_str = request.POST.get('data', None)  # Obter a data do formulário
            if data_str:
                try:
                    data = date.fromisoformat(data_str)
                    form.instance.data_pedido = data  # Atribuir data ao campo data_pedido
                except ValueError:
                    # Lidar com erro de formatação de data, se necessário
                    pass

            # Processar o valor_unitario do formulário e atribuir ao campo valor_unitario
            valor_str = form.cleaned_data['valor_unitario']
            if valor_str:
                try:
                    valor = parse_decimal_br(valor_str)  # Função para converter valor monetário brasileiro em Decimal
                    form.instance.valor_unitario = valor  # Atribuir valor_unitario ao campo valor_unitario
                except ValueError:
                    # Lidar com erro de conversão de valor
                    pass
            # Atribuir o usuário logado ao pedido
            form.instance.vendedor = request.user  
            form.save()
            return redirect('all')  # Redirecionar para página de sucesso após salvar
        
    else:
        produtos = CadastrarProduto.objects.all()
        form = PedidoForm()

    # Criar o contexto com o formulário e a data atual
    context = {
        'form': form,
        'data_atual': data_atual,
        'produtos' : produtos,
    }

    return render(request, 'criar_pedido.html', context)


def parse_decimal_br(value):
    """Função para converter valor monetário brasileiro em Decimal."""
    try:
        # Converter value para string se ainda não for uma string
        if not isinstance(value, str):
            value = str(value)
        
        # Remover caracteres não numéricos (exceto ponto e vírgula) e substituir vírgula por ponto
        numeric_chars = [c for c in value if c.isdigit() or c == ',' or c == '.']
        cleaned_value = ''.join(numeric_chars)
        decimal_value = Decimal(cleaned_value.replace(',', '.'))
        return decimal_value
    except InvalidOperation:
        raise ValueError("Valor monetário inválido")
    
@login_required
def excluir_pedido(request, pedido_id):
    # Obter o pedido pelo ID
    pedido = get_object_or_404(Pedido, pk=pedido_id)
    if request.method == 'POST':# Verificar se o formulário foi submetido via POST
        pedido.delete() # Processar a exclusão do pedido
        return redirect('all')# Redirecionar para a página de inicio
    
    return render(request, 'confirmar_exclusao.html', {'pedido': pedido})# Se não for um POST, renderizar um template de confirmação de exclusão

@login_required
def imprimir_pedido(request, pedido_id):
    pedido = Pedido.objects.get(pk=pedido_id)
    context = {
        'pedido': pedido
    }
    return render(request, 'impressao.html', context)# Redirecionar para a página de impressão
   
@login_required
def cadastrar_produtos(request):
    if request.method == 'POST':
        form = CadastrarProdutoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Produto cadastrado com sucesso!')
            
        else:
            messages.error(request, 'Erro ao cadastrar produto. Verifique os dados e tente novamente.')
            print(form.errors)    
    else:
        form = CadastrarProdutoForm()
    
    return render(request, 'cadastrar_produtos.html', {'form': form})

@login_required
def cadastrar_clientes(request):
    if request.method == 'POST':
        form = CriarClienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente cadastrado com sucesso!')
            
        else:
            print(form.errors)
            messages.error(request, 'Erro ao cadastrar cliente. Verifique os dados e tente novamente.')    
    else:
        form = CriarClienteForm()
    
    return render(request, 'cadastrar_clientes.html', {'form': form})

@login_required
def cadastrar_empresa(request):
    if request.method == 'POST':
        form = CadastroEmpresaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Empresa cadastrada com sucesso!')
            
        else:
            print(form.errors)
            messages.error(request, 'Erro ao cadastrar Empresa. Verifique os dados e tente novamente.')    
    else:
        form = CadastroEmpresaForm()
    
    return render(request, 'cadastrar_empresa.html', {'form': form})
    
@login_required
def cadastrar_vendedores(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        nome_completo = request.POST.get('nome_completo')
        cod_vendedor = request.POST.get('cod_vendedor')
        
        if form.is_valid():
            user = form.save()
            user.first_name = nome_completo
            user.last_name = cod_vendedor
            user.save()

            messages.success(request, 'Vendedor cadastrado com sucesso!')
            
        else:
            print(form.errors)
            messages.error(request, 'Erro ao cadastrar vendedor. Verifique os dados.')
    else:
        form = UserCreationForm()
    
    return render(request, 'cadastrar_vendedores.html', {'form': form})

