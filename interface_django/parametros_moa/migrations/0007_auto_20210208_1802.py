# Generated by Django 3.1.5 on 2021-02-08 21:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parametros_moa', '0006_contato'),
    ]

    operations = [
        migrations.AddField(
            model_name='parametrosusina',
            name='ug1_tempo',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='parametrosusina',
            name='ug2_tempo',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
