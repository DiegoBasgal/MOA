# Generated by Django 2.2.12 on 2024-04-19 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Alarmes',
            fields=[
                ('data', models.DateTimeField(primary_key=True, serialize=False)),
                ('gravidade', models.IntegerField(default=0)),
                ('descricao', models.TextField(default='')),
            ],
        ),
    ]
