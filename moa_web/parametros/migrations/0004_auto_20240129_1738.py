# Generated by Django 2.2.12 on 2024-01-29 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parametros', '0003_alter_parametrosusina_valor_ie_inicial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parametrosusina',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
