# Generated by Django 4.2.4 on 2024-09-29 10:45

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0020_alter_criarcliente_detal_cliente_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='criarcliente',
            name='detal_cliente',
            field=models.TextField(max_length=100, validators=[django.core.validators.MinLengthValidator(1)]),
        ),
    ]
