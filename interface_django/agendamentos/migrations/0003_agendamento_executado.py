# Generated by Django 3.1.5 on 2021-02-19 18:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agendamentos', '0002_auto_20210218_1641'),
    ]

    operations = [
        migrations.AddField(
            model_name='agendamento',
            name='executado',
            field=models.IntegerField(default=0),
        ),
    ]
