# Generated by Django 4.2 on 2023-06-14 19:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ModoManual',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('comando_dj52l', models.IntegerField(default=1)),
                ('modo_ug1', models.IntegerField(default=1)),
                ('modo_ug2', models.IntegerField(default=1)),
            ],
        ),
    ]
