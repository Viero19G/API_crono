# Generated by Django 3.2.25 on 2025-01-28 11:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_tempos'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='atividade',
            name='operacoes',
        ),
    ]
