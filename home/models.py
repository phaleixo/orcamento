from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import User
import os
from django.core.files.storage import default_storage
from django.conf import settings


class Pedido(models.Model):
    vendedor = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    data = models.DateField()
    nome_cliente = models.CharField(max_length=100)
    contato = models.CharField(max_length=11)
    cpf_cnpj = models.CharField(max_length=14)
    produto = models.CharField(max_length=100)
    quantidade = models.IntegerField()
    valor_unitario = models.DecimalField(max_digits=10, decimal_places=2)     
    descricao_pedido = models.TextField()
    descricao_impresso = models.TextField()
    valor_total = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"Pedido de {self.nome_cliente} em {self.data}"

    class Meta:
        ordering = ['-id']  # Ordenar por data_pedido em ordem decrescente    


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
    blank=True,         # Campo pode ser deixado em branco no formulário
    null=True,          # Campo pode armazenar valor NULL no banco de dados
    validators=[MinLengthValidator(0)]  # Mínimo de 0 caracteres, o que significa opcional
    )
    def __str__(self):
        return f'{self.nome_cliente} - {self.cpf_cnpj} - {self.contato} - {self.detal_cliente}' 

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
    end_empresa = models.TextField(
        max_length=100,
        blank=True,
        null=True,
        validators=[MinLengthValidator(0)]
    )
    logo = models.ImageField(
        upload_to='logomarca/',  
        null=True,
        blank=True
    )  

    def __str__(self):
        return f'{self.nome_empresa} - {self.cpf_cnpj} - {self.contato} - {self.end_empresa}'

