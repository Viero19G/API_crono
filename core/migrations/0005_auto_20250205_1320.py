# Generated by Django 3.2.25 on 2025-02-05 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_remove_atividade_operacoes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='atividade',
            name='data_hora_fim',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='atividade',
            name='data_hora_inicio',
            field=models.TextField(),
        ),
    ]
