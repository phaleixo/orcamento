# Generated by Django 4.2.4 on 2024-09-14 17:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0013_cadastrarproduto_valorproduto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedido',
            name='cpf_cnpj',
            field=models.CharField(max_length=14, unique=True),
        ),
    ]
