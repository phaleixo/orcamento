# Generated by Django 4.2.4 on 2024-04-13 09:28

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedido',
            name='campo_data',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Data'),
            preserve_default=False,
        ),
    ]
