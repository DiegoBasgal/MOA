# Generated by Django 4.2.3 on 2023-11-30 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parametros', '0015_remove_parametrosusina_tempo_disparo_lg_m_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='parametrosusina',
            old_name='valor_disparo_lg_perda_ug1',
            new_name='valor_disparo_lg_p1',
        ),
        migrations.RenameField(
            model_name='parametrosusina',
            old_name='valor_disparo_lg_perda_ug2',
            new_name='valor_disparo_lg_p2',
        ),
        migrations.AlterField(
            model_name='parametrosusina',
            name='hora_disparo_lg',
            field=models.DateTimeField(default='2023-11-30 10:42:23'),
        ),
    ]
