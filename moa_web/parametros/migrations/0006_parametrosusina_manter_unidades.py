# Generated by Django 4.2.3 on 2023-11-27 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parametros', '0005_alter_controleestados_ultimo_estado_ug1_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='parametrosusina',
            name='manter_unidades',
            field=models.BooleanField(default=False),
        ),
    ]
