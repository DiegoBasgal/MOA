# Generated by Django 4.2.3 on 2024-02-28 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parametros', '0020_parametrosusina_alerta_temperatura_oleo_uhrv_ug1_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='parametrosusina',
            name='hora_desativar_moa',
            field=models.IntegerField(default=18),
        ),
        migrations.AlterField(
            model_name='parametrosusina',
            name='horario_disparo_lg',
            field=models.DateTimeField(default='2024-02-28 19:36:58'),
        ),
    ]
