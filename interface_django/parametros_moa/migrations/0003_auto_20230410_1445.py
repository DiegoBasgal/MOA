# Generated by Django 3.2.12 on 2023-04-10 17:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parametros_moa', '0002_parametrosusina_tda_offline'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='parametrosusina',
            name='modbus_server_ip',
        ),
        migrations.RemoveField(
            model_name='parametrosusina',
            name='modbus_server_porta',
        ),
        migrations.AlterField(
            model_name='parametrosusina',
            name='clp_moa_ip',
            field=models.CharField(default='192.168.0.116', max_length=15),
        ),
    ]
