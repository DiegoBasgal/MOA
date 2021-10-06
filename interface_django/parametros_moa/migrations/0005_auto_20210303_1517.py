# Generated by Django 3.1.5 on 2021-03-03 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parametros_moa', '0004_auto_20210303_1459'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='parametrosusina',
            name='nv_comporta_anterior_1',
        ),
        migrations.RemoveField(
            model_name='parametrosusina',
            name='nv_comporta_anterior_2',
        ),
        migrations.RemoveField(
            model_name='parametrosusina',
            name='nv_comporta_anterior_3',
        ),
        migrations.RemoveField(
            model_name='parametrosusina',
            name='nv_comporta_anterior_4',
        ),
        migrations.RemoveField(
            model_name='parametrosusina',
            name='nv_comporta_anterior_5',
        ),
        migrations.RemoveField(
            model_name='parametrosusina',
            name='nv_comporta_proximo_1',
        ),
        migrations.RemoveField(
            model_name='parametrosusina',
            name='nv_comporta_proximo_2',
        ),
        migrations.RemoveField(
            model_name='parametrosusina',
            name='nv_comporta_proximo_3',
        ),
        migrations.RemoveField(
            model_name='parametrosusina',
            name='nv_comporta_proximo_4',
        ),
        migrations.RemoveField(
            model_name='parametrosusina',
            name='nv_comporta_proximo_5',
        ),
        migrations.RemoveField(
            model_name='parametrosusina',
            name='posicao_comporta',
        ),
        migrations.AddField(
            model_name='parametrosusina',
            name='nv_comporta_pos_0_ant',
            field=models.DecimalField(decimal_places=15, default=0, max_digits=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='parametrosusina',
            name='nv_comporta_pos_0_prox',
            field=models.DecimalField(decimal_places=15, default=0, max_digits=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='parametrosusina',
            name='nv_comporta_pos_1_ant',
            field=models.DecimalField(decimal_places=15, default=0, max_digits=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='parametrosusina',
            name='nv_comporta_pos_1_prox',
            field=models.DecimalField(decimal_places=15, default=0, max_digits=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='parametrosusina',
            name='nv_comporta_pos_2_ant',
            field=models.DecimalField(decimal_places=15, default=0, max_digits=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='parametrosusina',
            name='nv_comporta_pos_2_prox',
            field=models.DecimalField(decimal_places=15, default=0, max_digits=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='parametrosusina',
            name='nv_comporta_pos_3_ant',
            field=models.DecimalField(decimal_places=15, default=0, max_digits=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='parametrosusina',
            name='nv_comporta_pos_3_prox',
            field=models.DecimalField(decimal_places=15, default=0, max_digits=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='parametrosusina',
            name='nv_comporta_pos_4_ant',
            field=models.DecimalField(decimal_places=15, default=0, max_digits=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='parametrosusina',
            name='nv_comporta_pos_4_prox',
            field=models.DecimalField(decimal_places=15, default=0, max_digits=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='parametrosusina',
            name='nv_comporta_pos_5_ant',
            field=models.DecimalField(decimal_places=15, default=0, max_digits=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='parametrosusina',
            name='nv_comporta_pos_5_prox',
            field=models.DecimalField(decimal_places=15, default=0, max_digits=30),
            preserve_default=False,
        ),
    ]
