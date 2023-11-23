# Generated by Django 4.2.5 on 2023-11-24 11:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('parametros', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Agendamento',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('data', models.DateTimeField()),
                ('observacao', models.TextField()),
                ('executado', models.IntegerField(default=0)),
                ('campo_auxiliar', models.TextField()),
                ('criado_por', models.CharField(max_length=255)),
                ('modificado_por', models.CharField(max_length=255)),
                ('ts_criado', models.DateTimeField()),
                ('ts_modificado', models.DateTimeField()),
                ('comando', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='parametros.comando')),
            ],
        ),
    ]
