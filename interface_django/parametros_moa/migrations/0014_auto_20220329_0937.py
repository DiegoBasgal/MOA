# Generated by Django 3.2.6 on 2022-03-29 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("parametros_moa", "0013_auto_20211213_1440"),
    ]

    operations = [
        migrations.AddField(
            model_name="comando",
            name="executavel_em_autmoatico",
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name="comando",
            name="executavel_em_manual",
            field=models.BooleanField(default=False),
        ),
    ]
