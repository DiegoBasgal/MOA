# Generated by Django 4.2.5 on 2023-11-21 10:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('parametros', '0006_rename_alerta_temperatura_mancal_la_1_ug2_parametrosusina_alerta_temperatura_fase_u_ug1_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='parametrosusina',
            old_name='alerta_temperatura_oleo_uhct_ug1',
            new_name='alerta_temperatura_oleo_uhrv_ug1',
        ),
        migrations.RenameField(
            model_name='parametrosusina',
            old_name='alerta_temperatura_oleo_uhct_ug2',
            new_name='alerta_temperatura_oleo_uhrv_ug2',
        ),
        migrations.RenameField(
            model_name='parametrosusina',
            old_name='alerta_temperatura_oleo_uhct_ug3',
            new_name='alerta_temperatura_oleo_uhrv_ug3',
        ),
        migrations.RenameField(
            model_name='parametrosusina',
            old_name='alerta_temperatura_oleo_uhct_ug4',
            new_name='alerta_temperatura_oleo_uhrv_ug4',
        ),
        migrations.RenameField(
            model_name='parametrosusina',
            old_name='limite_temperatura_oleo_uhct_ug1',
            new_name='limite_temperatura_oleo_uhrv_ug1',
        ),
        migrations.RenameField(
            model_name='parametrosusina',
            old_name='limite_temperatura_oleo_uhct_ug2',
            new_name='limite_temperatura_oleo_uhrv_ug2',
        ),
        migrations.RenameField(
            model_name='parametrosusina',
            old_name='limite_temperatura_oleo_uhct_ug3',
            new_name='limite_temperatura_oleo_uhrv_ug3',
        ),
        migrations.RenameField(
            model_name='parametrosusina',
            old_name='limite_temperatura_oleo_uhct_ug4',
            new_name='limite_temperatura_oleo_uhrv_ug4',
        ),
    ]
