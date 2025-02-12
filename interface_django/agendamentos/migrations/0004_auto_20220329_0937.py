# Generated by Django 3.2.6 on 2022-03-29 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agendamentos', '0003_agendamento_executado'),
    ]

    operations = [
        migrations.AddField(
            model_name='agendamento',
            name='campo_auxiliar',
            field=models.TextField(default=' '),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='agendamento',
            name='criado_por',
            field=models.CharField(default='Teste', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='agendamento',
            name='modificado_por',
            field=models.CharField(default='Teste', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='agendamento',
            name='ts_criado',
            field=models.DateTimeField(default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='agendamento',
            name='ts_modificado',
            field=models.DateTimeField(default=None),
            preserve_default=False,
        ),
    ]
