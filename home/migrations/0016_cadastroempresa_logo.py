# Generated by Django 4.2.4 on 2024-09-19 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0015_alter_criarcliente_cpf_cnpj_alter_pedido_cpf_cnpj'),
    ]

    operations = [
        migrations.AddField(
            model_name='cadastroempresa',
            name='logo',
            field=models.ImageField(blank=True, null=True, upload_to='statics/image/logomarca/'),
        ),
    ]
