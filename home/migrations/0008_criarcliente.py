# Generated by Django 4.2.4 on 2024-08-10 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_cadastrarproduto'),
    ]

    operations = [
        migrations.CreateModel(
            name='CriarCliente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome_cliente', models.CharField(max_length=100)),
                ('cpf_cnpj', models.CharField(max_length=14)),
                ('contato', models.CharField(max_length=11)),
                ('detal_cliente', models.TextField(max_length=100)),
            ],
        ),
    ]
