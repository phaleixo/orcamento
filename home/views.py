from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required,  user_passes_test
from django.contrib.auth import logout
from django.views.decorators.http import require_POST
from .models import CadastroEmpresa, Pedido, CadastrarProduto,CriarCliente, ItemPedido
from .forms import EditarVendedorForm, PedidoForm
from datetime import date
from datetime import datetime
from decimal import Decimal, InvalidOperation
from .forms import CadastrarProdutoForm
from .forms import CriarClienteForm
from .forms import CadastroEmpresaForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from django.contrib.auth.models import User
from .forms import EditarProdutoForm
from django.contrib.auth.models import Group
from django.db import models
from django.db.models import Sum, Count, F, DecimalField
from django.db.models.expressions import ExpressionWrapper


# Função para buscar cliente e exibir em all_clientes.html
def buscar_cliente(request):
    cpf_cnpj = request.GET.get('cpf_cnpj', None)
    if cpf_cnpj:
        try:
            cliente = CriarCliente.objects.get(cpf_cnpj=cpf_cnpj)
            data = {
                'nome_cliente': cliente.nome_cliente,
                'contato': cliente.contato,
            }
            return JsonResponse(data)
        except CriarCliente.DoesNotExist:
            return JsonResponse({'error': 'Cliente não encontrado'}, status=404)
    return JsonResponse({'error': 'CPF/CNPJ não informado'}, status=400)

# Função para verificar se o usuário pertence ao grupo 'gestores'
def is_in_group_gestores(user):
    return user.groups.filter(name='gestores').exists()

#Tela inicial de Vendedores onde é possivel cadastrar clientes e fazer orçamentos
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

    # Para cada pedido, verificar se tem itens associados e garantir que o texto esteja em maiúsculas
    for pedido in pedidos:
        pedido.nome_cliente = pedido.nome_cliente.upper() if pedido.nome_cliente else ''
        pedido.cpf_cnpj = pedido.cpf_cnpj.upper() if pedido.cpf_cnpj else ''
        # Prefetch dos itens relacionados
        pedido.itens_lista = pedido.itens.all()

    context = {
        'data_atual': data_atual,
        'pedidos': pedidos,
    }

    return render(request, 'all.html', context)

# Função para Logout
@require_POST
def custom_logout(request):
    logout(request)
    return render ('login.html')  # Redireciona para a página de login (login.html)

# Função para verificar se o usuário pertence ao grupo 'gestores'      
def is_in_group_gestores(user):
    return user.groups.filter(name='gestores').exists()

# Tela incial de Gestores onde é Gerenciamento de Produtos, Vendedores e Clientes
@login_required
@user_passes_test(is_in_group_gestores)
def gerenciamento(request):
    # Período para filtrar os dados
    periodo = request.GET.get('periodo', 'semana')
    
    now = timezone.now().date()
    if periodo == 'semana':
        data_inicio = now - timezone.timedelta(days=7)
    elif periodo == 'mes':
        data_inicio = now.replace(day=1)
    elif periodo == 'ano':
        data_inicio = now.replace(month=1, day=1)
    else:
        data_inicio = now - timezone.timedelta(days=7)  # Default: última semana
    
    # Obter todos os pedidos para exibição na tabela principal
    pedidos = Pedido.objects.all()
    
    # Estatísticas para o dashboard
    total_clientes = CriarCliente.objects.count()
    novos_clientes = CriarCliente.objects.filter(id__gte=0).count()  # Placeholder, ajuste conforme necessário
    
    total_pedidos = Pedido.objects.filter(data__gte=data_inicio).count()
    
    # Calcular valor total dos pedidos
    valor_total_query = Pedido.objects.filter(data__gte=data_inicio).aggregate(
        total=Sum('valor_total')
    )
    valor_total_pedidos = valor_total_query['total'] if valor_total_query['total'] else 0
    
    total_produtos = CadastrarProduto.objects.count()
    
    # Estatísticas por vendedor
    vendedores_pedidos = Pedido.objects.filter(data__gte=data_inicio).values(
        'vendedor__username'
    ).annotate(
        name=F('vendedor__username'),
        count=Count('id'),
        total=Sum('valor_total')
    ).order_by('-count')
    
    # Abordagem alternativa para top produtos que evita o erro de multiplicação
    # Primeiro obtenha os produtos mais vendidos por quantidade
    top_produtos_ids = ItemPedido.objects.filter(
        pedido__data__gte=data_inicio
    ).values('produto').annotate(
        quantidade=Sum('quantidade')
    ).order_by('-quantidade')[:5]
    
    # Depois calcule os valores totais separadamente
    top_produtos = []
    for item in top_produtos_ids:
        produto_id = item['produto']
        qtd = item['quantidade']
        
        try:
            produto_obj = CadastrarProduto.objects.get(id=produto_id)
            
            # Calcular o valor total para este produto
            itens_produto = ItemPedido.objects.filter(
                produto_id=produto_id,
                pedido__data__gte=data_inicio
            )
            
            # Calcular manualmente a soma do subtotal
            total_valor = sum(item.quantidade * item.valor_unitario for item in itens_produto)
            
            top_produtos.append({
                'nome': produto_obj.produto,
                'quantidade': qtd,
                'total': total_valor
            })
        except CadastrarProduto.DoesNotExist:
            # Caso o produto não exista mais, ignorar
            continue
    
    # Formatando dados para o template
    for pedido in pedidos:
        pedido.nome_cliente = pedido.nome_cliente.upper() if pedido.nome_cliente else ''
        pedido.cpf_cnpj = pedido.cpf_cnpj.upper() if pedido.cpf_cnpj else ''
        pedido.itens_lista = pedido.itens.all()
    
    context = {
        'data_atual': f"{now.year}{now.month:02d}{now.day:02d}",
        'pedidos': pedidos,
        # Dashboard data
        'total_clientes': total_clientes,
        'novos_clientes': novos_clientes,
        'total_pedidos': total_pedidos,
        'valor_total_pedidos': valor_total_pedidos,
        'total_produtos': total_produtos,
        'vendedores_pedidos': vendedores_pedidos,
        'top_produtos': top_produtos,
        'periodo': periodo
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

# Criar novo Orcamento
@login_required
def criar_pedido(request):
    data_atual = datetime.now().date()  # Obter a data atual (sem hora)
    cpfs_cnpjs = Pedido.objects.values_list('cpf_cnpj', flat=True)
    produtos = CadastrarProduto.objects.all()

    if request.method == 'POST':
        # Obter dados básicos do pedido
        nome_cliente = request.POST.get('nome_cliente')
        contato = request.POST.get('contato')
        cpf_cnpj = request.POST.get('cpf_cnpj')
        descricao_pedido = request.POST.get('descricao_pedido')
        descricao_impresso = request.POST.get('descricao_impresso')
        valor_total = request.POST.get('valor_total')
        
        # Processar a data do pedido
        data_str = request.POST.get('data', None)
        if data_str:
            try:
                data = date.fromisoformat(data_str)
            except ValueError:
                data = datetime.now().date()
        else:
            data = datetime.now().date()
        
        # Obter produtos, quantidades e valores unitários
        produtos_ids = request.POST.getlist('produtos[]')
        quantidades = request.POST.getlist('quantidades[]')
        valores_unitarios = request.POST.getlist('valores_unitarios[]')
        
        # Para compatibilidade com código existente, também pegamos os valores antigos
        produto_principal = request.POST.get('produto', None)
        quantidade_principal = request.POST.get('quantidade', None)
        valor_unitario_principal = request.POST.get('valor_unitario', None)
        
        # Verificar se temos pelo menos um produto válido
        if not produtos_ids:
            messages.error(request, 'É necessário adicionar pelo menos um produto ao pedido.')
            return render(request, 'criar_pedido.html', {
                'cpfs_cnpjs': cpfs_cnpjs,
                'data_atual': data_atual,
                'produtos': produtos
            })
        
        # Converter valor_total para decimal
        try:
            valor_total_decimal = Decimal(valor_total)
        except (InvalidOperation, TypeError):
            valor_total_decimal = Decimal('0.00')
        
        # Criar o pedido
        pedido = Pedido.objects.create(
            vendedor=request.user,
            data=data,
            nome_cliente=nome_cliente,
            contato=contato,
            cpf_cnpj=cpf_cnpj,
            descricao_pedido=descricao_pedido,
            descricao_impresso=descricao_impresso,
            valor_total=valor_total_decimal,
            # Campos legados
            produto=produto_principal,
            quantidade=quantidade_principal,
            valor_unitario=valor_unitario_principal
        )
        
        # Salvar os itens do pedido
        for i in range(len(produtos_ids)):
            if i < len(quantidades) and i < len(valores_unitarios) and produtos_ids[i]:
                try:
                    produto = CadastrarProduto.objects.get(id=produtos_ids[i])
                    quantidade = int(quantidades[i])
                    valor_unitario = Decimal(valores_unitarios[i])
                    
                    ItemPedido.objects.create(
                        pedido=pedido,
                        produto=produto,
                        quantidade=quantidade,
                        valor_unitario=valor_unitario
                    )
                except (CadastrarProduto.DoesNotExist, ValueError, InvalidOperation):
                    # Registrar erro e continuar com os próximos itens
                    continue
        
        return redirect('all')
        
    else:
        produtos = CadastrarProduto.objects.all()

    # Criar o contexto com o formulário e a data atual
    context = {
        'cpfs_cnpjs' : cpfs_cnpjs,
        'data_atual': data_atual,
        'produtos' : produtos
    }

    return render(request, 'criar_pedido.html', context)

# Função para converter valor monetário brasileiro em Decimal.
def parse_decimal_br(value):
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

# Excluir Orcamento    
@login_required
def excluir_pedido(request, pedido_id):
    # Obter o pedido pelo ID
    pedido = get_object_or_404(Pedido, pk=pedido_id)
    if request.method == 'POST':# Verificar se o formulário foi submetido via POST
        pedido.delete() # Processar a exclusão do pedido
        return redirect('all')# Redirecionar para a página de inicio
    
    return render(request, 'confirmar_exclusao.html', {'pedido': pedido})# Se não for um POST, renderizar um template de confirmação de exclusão

# Imprimir Orcamento
@login_required
def imprimir_pedido(request, pedido_id):    
    pedido = Pedido.objects.get(pk=pedido_id)
    configuracoes = CadastroEmpresa.objects.first()
    
    # Obter itens do pedido (se houver)
    itens_pedido = pedido.itens.all()
    
    context = {
        'pedido': pedido,
        'configuracoes': configuracoes,
        'itens_pedido': itens_pedido
    }
    return render(request, 'impressao.html', context)# Redirecionar para a página de impressão

# Cadastrar Novos Produtos   
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

# Cadastrar Novos Clientes
@login_required
def cadastrar_clientes(request):
    if request.method == 'POST':
        form = CriarClienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente cadastrado com sucesso!')
        else:
            messages.error(request, 'Erro ao cadastrar cliente. Verifique os dados e tente novamente.')
    else:
        form = CriarClienteForm()
    
    return render(request, 'cadastrar_clientes.html', {'form': form})

# Cadastrar Empresa emissora dos orcamentos
@login_required
def cadastrar_empresa(request):
    if request.method == 'POST':
        form = CadastroEmpresaForm(request.POST, request.FILES)  # Inclua request.FILES
        if form.is_valid():
            form.save()
            messages.success(request, 'Empresa cadastrada com sucesso!')
        else:
            print(form.errors)
            messages.error(request, 'Erro ao cadastrar Empresa. Verifique os dados e tente novamente.')    
    else:
        form = CadastroEmpresaForm()

    return render(request, 'cadastrar_empresa.html', {'form': form})

# Cadastrar Novos Vendedores  
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

            # Adiciona o usuário ao grupo "Vendedores"
            grupo_vendedores = Group.objects.get(name='vendedores')
            user.groups.add(grupo_vendedores)
            user.save()

            messages.success(request, 'Vendedor cadastrado com sucesso e adicionado ao grupo Vendedores!')
            
        else:
            messages.error(request, 'Erro ao cadastrar vendedor. Verifique os dados.')
    else:
        form = UserCreationForm()
    
    return render(request, 'cadastrar_vendedores.html', {'form': form})

# Editar dados do vendedor 
@login_required
def editar_vendedor(request, vendedor_id):
    vendedor = get_object_or_404(User, id=vendedor_id)
    
    if request.method == 'POST':
        form = EditarVendedorForm(request.POST, instance=vendedor)
        if form.is_valid():
            form.save()
            return redirect('all_vendedores')  # Redireciona para a lista de vendedores
    else:
        form = EditarVendedorForm(instance=vendedor)
    
    context = {
        'form': form,
        'vendedor': vendedor,
    }
    
    return render(request, 'editar_vendedor.html', context)

# Exibir todos os clientes
@login_required
def all_clientes(request):
    cliente = CriarCliente.objects.all()
    context = {
        'cliente': cliente,
    }
    return render (request, 'all_clientes.html', context)

# Editar dados do cliente 
@login_required
def editar_cliente(request, cliente_id):
    cliente = get_object_or_404(CriarCliente, id=cliente_id)
    
    if request.method == 'POST':
        form = CriarClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('all_clientes')  # Redireciona para a lista de clientes
    else:
        form = CriarClienteForm(instance=cliente)
    
    context = {
        'form': form,
        'cliente': cliente,
    }
    
    return render(request, 'editar_cliente.html', context)

# Exibir todos os Produtos
@login_required
def all_produtos(request):
    produto = CadastrarProduto.objects.all()
    context = {
        'produto': produto,
    }
    return render (request, 'all_produtos.html', context)

# Excluir Produto    
@login_required
def excluir_produto(request, cadastrarproduto_id):
    # Obter o pedido pelo ID
    produto = get_object_or_404(CadastrarProduto, pk=cadastrarproduto_id)
    if request.method == 'POST':# Verificar se o formulário foi submetido via POST
        produto.delete() # Processar a exclusão do pedido
        return redirect('all_produtos')# Redirecionar para a página de inicio
    
    return render(request, 'confirmar_exclusao_produto.html', {'produto': produto})

# Editar Produtos
@login_required
def editar_produto(request, produto_id):
    produto = get_object_or_404(CadastrarProduto, id=produto_id)
    
    if request.method == 'POST':
        form = EditarProdutoForm(request.POST, instance=produto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Produto atualizado com sucesso!')
            return redirect('all_produtos')  # Redireciona de volta para a lista de produtos
        else:
            messages.error(request, 'Erro ao atualizar o produto. Verifique os dados.')
    else:
        form = EditarProdutoForm(instance=produto)
    
    return render(request, 'editar_produto.html', {'form': form, 'produto': produto})

# Exibir todos os Vendedores
@login_required
def all_vendedores(request):
    vendedor = User.objects.filter(groups__name='vendedores')
    context = {
        'vendedor': vendedor,
    }
    return render (request, 'all_vendedores.html', context)

# Exibir Dados da Empresa
@login_required
def all_empresa(request):
    if not is_in_group_gestores(request.user):
        messages.error(request, 'Você não tem permissão para acessar esta página.')
        referer = request.META.get('HTTP_REFERER')
        if referer:
            return redirect(referer)
        
    else:
        empresa = CadastroEmpresa.objects.first()
        context = {
            'empresa': empresa,
        }
        return render(request, 'all_empresa.html', context)

# Configurações da empresa
@login_required
def configuracoes(request):
    # Verifica se existe pelo menos uma empresa cadastrada
    if not CadastroEmpresa.objects.exists():
        messages.info(request, 'Nenhuma empresa cadastrada. Redirecionando para cadastro.')
        return redirect('cadastrar_empresa')  # Ajuste para o nome correto da sua URL de cadastro

    # Se houver empresas, carrega a primeira (ou você pode ajustar essa lógica conforme necessário)
    empresa = CadastroEmpresa.objects.first()  # Obtém a primeira empresa cadastrada

    if request.method == 'POST':
        form = CadastroEmpresaForm(request.POST, request.FILES, instance=empresa)  # Carregar instância para edição
        if form.is_valid():
            form.save()
            messages.success(request, 'Configurações da empresa atualizadas com sucesso!')
            return redirect('configuracoes')  # Redireciona após salvar
        else:
            messages.error(request, 'Erro ao atualizar as configurações da empresa.')
    else:
        form = CadastroEmpresaForm(instance=empresa)  # Preencher o formulário com os dados da empresa

    context = {
        'form': form,
    }
    return render(request, 'configuracoes.html', context)
