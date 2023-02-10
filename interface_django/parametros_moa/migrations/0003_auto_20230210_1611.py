# Generated by Django 2.2.12 on 2023-02-10 19:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parametros_moa', '0002_parametrosusina_nv_pos_grade'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parametrosusina',
            name='kd',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=15),
        ),
        migrations.AlterField(
            model_name='parametrosusina',
            name='ki',
            field=models.DecimalField(decimal_places=2, default=0.1, max_digits=15),
        ),
        migrations.AlterField(
            model_name='parametrosusina',
            name='kie',
            field=models.DecimalField(decimal_places=2, default=0.1, max_digits=15),
        ),
        migrations.AlterField(
            model_name='parametrosusina',
            name='kp',
            field=models.DecimalField(decimal_places=2, default=2, max_digits=15),
        ),
        migrations.AlterField(
            model_name='parametrosusina',
            name='pot_disp',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='parametrosusina',
            name='pot_minima',
            field=models.DecimalField(decimal_places=2, default=200, max_digits=10),
        ),
        migrations.AlterField(
            model_name='parametrosusina',
            name='pot_nominal',
            field=models.DecimalField(decimal_places=2, default=1000, max_digits=10),
        ),
        migrations.AlterField(
            model_name='parametrosusina',
            name='pot_nominal_ug',
            field=models.DecimalField(decimal_places=2, default=500, max_digits=10),
        ),
        migrations.AlterField(
            model_name='parametrosusina',
            name='ug1_disp',
            field=models.DecimalField(decimal_places=1, default=1, max_digits=10),
        ),
        migrations.AlterField(
            model_name='parametrosusina',
            name='ug1_pot',
            field=models.DecimalField(decimal_places=1, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='parametrosusina',
            name='ug1_setpot',
            field=models.DecimalField(decimal_places=1, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='parametrosusina',
            name='ug2_disp',
            field=models.DecimalField(decimal_places=1, default=1, max_digits=10),
        ),
        migrations.AlterField(
            model_name='parametrosusina',
            name='ug2_pot',
            field=models.DecimalField(decimal_places=1, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='parametrosusina',
            name='ug2_setpot',
            field=models.DecimalField(decimal_places=1, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='parametrosusina',
            name='valor_ie_inicial',
            field=models.DecimalField(decimal_places=2, default=0.5, max_digits=10),
        ),
    ]
