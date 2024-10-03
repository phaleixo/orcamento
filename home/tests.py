from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Group
from django.contrib.messages import get_messages
from .models import CadastrarProduto, CadastroEmpresa, CriarCliente
from django.core.files.uploadedfile import SimpleUploadedFile

# Teste Cadastro de Produtos 
class CadastrarProdutoViewTest(TestCase):
    def setUp(self):
        # Cria um usuário para autenticação
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')

    def test_cadastrar_produtos_get(self):
        # Testa o método GET
        response = self.client.get(reverse('cadastrar_produtos'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cadastrar_produtos.html')

    def test_cadastrar_produtos_post_sucesso(self):
        # Dados válidos para o produto
        produto_data = {
            'cod_produto': '001',
            'produto': 'Produto Teste',
            'valorproduto': '100.50',
            'descricao_produto': 'Descrição do produto de teste'
        }

        response = self.client.post(reverse('cadastrar_produtos'), data=produto_data)
        self.assertEqual(response.status_code, 200)

        # Verifica se o produto foi criado
        self.assertTrue(CadastrarProduto.objects.filter(produto='Produto Teste').exists())

        # Verifica se a mensagem de sucesso foi criada
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Produto cadastrado com sucesso!')

    def test_cadastrar_produtos_post_erro(self):
        # Dados inválidos para o produto (falta 'produto')
        produto_data = {
            'cod_produto': '001',
            'valorproduto': '100.50',
            'descricao_produto': 'Descrição do produto de teste'
        }

        response = self.client.post(reverse('cadastrar_produtos'), data=produto_data)
        self.assertEqual(response.status_code, 200)

        # Verifica se o produto NÃO foi criado
        self.assertFalse(CadastrarProduto.objects.filter(cod_produto='001').exists())

        # Verifica se a mensagem de erro foi criada
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Erro ao cadastrar produto. Verifique os dados e tente novamente.')


# Teste Cadastro de Clientes 
class CadastrarClienteViewTest(TestCase):
    def setUp(self):
        # Cria um usuário para autenticação
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')

    def test_cadastrar_clientes_get(self):
        # Testa o método GET
        response = self.client.get(reverse('cadastrar_clientes'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cadastrar_clientes.html')

    

    def test_cadastrar_clientes_post_erro(self):
        # Dados inválidos para o cliente (falta 'nome_cliente')
        cliente_data = {
            'cpf_cnpj': '12345678901',
            'contato': '11999999999',
            'detal_cliente': 'Detalhes do cliente'
        }

        response = self.client.post(reverse('cadastrar_clientes'), data=cliente_data)
        self.assertEqual(response.status_code, 200)

   
#Teste Cadastrar Vendedores
class CadastrarVendedoresViewTest(TestCase):
    def setUp(self):
        # Cria um usuário para autenticação
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')

        # Cria o grupo "Vendedores"
        self.grupo_vendedores = Group.objects.create(name='vendedores')

    def test_cadastrar_vendedores_get(self):
        # Testa o método GET
        response = self.client.get(reverse('cadastrar_vendedores'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cadastrar_vendedores.html')

    def test_cadastrar_vendedores_post_sucesso(self):
        # Dados válidos para o novo vendedor
        vendedor_data = {
            'username': 'novovendedor',
            'password1': 'teste12345',
            'password2': 'teste12345',
            'nome_completo': 'Vendedor Teste',
            'cod_vendedor': '12345'
        }

        response = self.client.post(reverse('cadastrar_vendedores'), data=vendedor_data)
        self.assertEqual(response.status_code, 200)

        # Verifica se o vendedor foi criado
        user = User.objects.get(username='novovendedor')
        self.assertEqual(user.first_name, 'Vendedor Teste')
        self.assertEqual(user.last_name, '12345')

        # Verifica se o vendedor foi adicionado ao grupo "Vendedores"
        self.assertTrue(user.groups.filter(name='vendedores').exists())

        # Verifica se a mensagem de sucesso foi criada
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Vendedor cadastrado com sucesso e adicionado ao grupo Vendedores!')

    def test_cadastrar_vendedores_post_erro(self):
        # Dados inválidos para o novo vendedor (senhas não coincidem)
        vendedor_data = {
            'username': 'novovendedor',
            'password1': 'teste12345',
            'password2': 'teste54321',
            'nome_completo': 'Vendedor Teste',
            'cod_vendedor': '12345'
        }

        response = self.client.post(reverse('cadastrar_vendedores'), data=vendedor_data)
        self.assertEqual(response.status_code, 200)

        # Verifica se o vendedor NÃO foi criado
        self.assertFalse(User.objects.filter(username='novovendedor').exists())

        # Verifica se a mensagem de erro foi criada
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Erro ao cadastrar vendedor. Verifique os dados.')              