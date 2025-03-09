from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import User


class Pedido(models.Model):
    vendedor = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    data = models.DateField()
    nome_cliente = models.CharField(max_length=100)
    contato = models.CharField(max_length=11)
    cpf_cnpj = models.CharField(max_length=14)
    descricao_pedido = models.TextField()
    descricao_impresso = models.TextField()
    valor_total = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Campos legados - mantemos para compatibilidade com código existente
    produto = models.CharField(max_length=100, null=True, blank=True)
    quantidade = models.IntegerField(null=True, blank=True)
    valor_unitario = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    def __str__(self):
        return f"Pedido de {self.nome_cliente} em {self.data}"

    class Meta:
        ordering = ['-id']  # Ordenar por id em ordem decrescente


class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, related_name='itens', on_delete=models.CASCADE)
    produto = models.ForeignKey('CadastrarProduto', on_delete=models.CASCADE)
    quantidade = models.IntegerField()
    valor_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    
    @property
    def subtotal(self):
        return self.quantidade * self.valor_unitario
    
    def __str__(self):
        return f"{self.quantidade} x {self.produto.produto}"


class CadastrarProduto(models.Model):
    cod_produto = models.CharField(max_length=100)
    produto = models.CharField(max_length=100)
    valorproduto = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  
    descricao_produto = models.TextField(max_length=100)  
    def __str__(self):
        return self.produto
    

class CriarCliente(models.Model):
    nome_cliente = models.CharField(
        max_length=100, 
        validators=[MinLengthValidator(2)]  # Mínimo de 2 caracteres
    )
    cpf_cnpj = models.CharField(
        max_length=14, unique=True,
        validators=[MinLengthValidator(11)]  # Mínimo de 11 caracteres (para CPF)
    )
    contato = models.CharField(
        max_length=11,
        validators=[MinLengthValidator(10)]  # Mínimo de 10 caracteres (para número de telefone)
    )
    detal_cliente = models.TextField(
        max_length=100,
        blank=False,         
        null=False,         
        validators=[MinLengthValidator(1)]
    )

    # Campos de endereço
    cep = models.CharField(
        max_length=9,
        validators=[MinLengthValidator(8)]  # CEP com 8 caracteres
    )
    logradouro = models.CharField(max_length=255, default="Logradouro Desconhecido")
    numero = models.CharField(max_length=20, default="SN")
    bairro = models.CharField(max_length=100, default="Bairro Desconhecido")
    cidade = models.CharField(max_length=100, default="Cidade Desconhecida")
    estado = models.CharField(max_length=2, default="NI")
    
    def __str__(self):
        return f'{self.nome_cliente} - {self.cpf_cnpj} - {self.contato}'

class CadastroEmpresa(models.Model):
    nome_empresa = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(2)]
        
    )
    cpf_cnpj = models.CharField(
        max_length=14,
        validators=[MinLengthValidator(11)]
        
    )
    contato = models.CharField(
        max_length=11,
        validators=[MinLengthValidator(10)]
        
    )
    logo = models.ImageField(
        upload_to='logomarca/',  
        null=True,
        blank=True
    )

    # Campos de endereço
    cep = models.CharField(
        max_length=9,
        validators=[MinLengthValidator(8)]  # CEP com 8 caracteres
    )
    logradouro = models.CharField(max_length=255, default="Logradouro Desconhecido")
    numero = models.CharField(max_length=20, default="SN")
    bairro = models.CharField(max_length=100, default="Bairro Desconhecido")
    cidade = models.CharField(max_length=100, default="Cidade Desconhecida")
    estado = models.CharField(max_length=2, default="NI")
      

    def __str__(self):
        return f'{self.nome_empresa} - {self.cpf_cnpj} - {self.contato} - {self.cep} - {self.logradouro} - {self.numero} - {self.bairro} - {self.cidade} - {self.estado}'

