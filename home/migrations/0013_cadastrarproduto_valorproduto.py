# Generated by Django 4.2.4 on 2024-09-13 22:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0012_pedido_vendedor'),
    ]

    operations = [
        migrations.AddField(
            model_name='cadastrarproduto',
            name='valorproduto',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
