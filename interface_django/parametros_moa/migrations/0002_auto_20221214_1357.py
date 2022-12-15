# Generated by Django 3.2.12 on 2022-12-14 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parametros_moa', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='parametrosusina',
            old_name='alerta_temperatura_mancal_casq_rad_ug2',
            new_name='alerta_temperatura_enrolamento_trafo',
        ),
        migrations.RenameField(
            model_name='parametrosusina',
            old_name='alerta_temperatura_mancal_casq_rad_ug1',
            new_name='alerta_temperatura_mancal_contra_esc_comb_ug1',
        ),
        migrations.RenameField(
            model_name='parametrosusina',
            old_name='alerta_temperatura_mancal_escora_comb_ug1',
            new_name='alerta_temperatura_mancal_contra_esc_comb_ug2',
        ),
        migrations.RenameField(
            model_name='parametrosusina',
            old_name='alerta_temperatura_mancal_escora_comb_ug2',
            new_name='alerta_temperatura_mancal_guia_interno_1_ug1',
        ),
        migrations.RenameField(
            model_name='parametrosusina',
            old_name='alerta_temperatura_nucleo_gerador_2_ug1',
            new_name='alerta_temperatura_mancal_guia_interno_1_ug2',
        ),
        migrations.RenameField(
            model_name='parametrosusina',
            old_name='alerta_temperatura_nucleo_gerador_2_ug2',
            new_name='alerta_temperatura_mancal_guia_interno_2_ug1',
        ),
        migrations.RenameField(
            model_name='parametrosusina',
            old_name='alerta_temperatura_nucleo_gerador_3_ug1',
            new_name='alerta_temperatura_mancal_guia_interno_2_ug2',
        ),
        migrations.RenameField(
            model_name='parametrosusina',
            old_name='alerta_temperatura_nucleo_gerador_3_ug2',
            new_name='alerta_temperatura_mancal_guia_ug1',
        ),
        migrations.RenameField(
            model_name='parametrosusina',
            old_name='limite_temperatura_mancal_casq_rad_ug1',
            new_name='limite_temperatura_enrolamento_trafo',
        ),
        migrations.RenameField(
            model_name='parametrosusina',
            old_name='limite_temperatura_mancal_casq_rad_ug2',
            new_name='limite_temperatura_mancal_contra_esc_comb_ug1',
        ),
        migrations.RenameField(
            model_name='parametrosusina',
            old_name='limite_temperatura_mancal_escora_comb_ug1',
            new_name='limite_temperatura_mancal_contra_esc_comb_ug2',
        ),
        migrations.RenameField(
            model_name='parametrosusina',
            old_name='limite_temperatura_mancal_escora_comb_ug2',
            new_name='limite_temperatura_mancal_guia_interno_1_ug1',
        ),
        migrations.RenameField(
            model_name='parametrosusina',
            old_name='limite_temperatura_nucleo_gerador_2_ug1',
            new_name='limite_temperatura_mancal_guia_interno_1_ug2',
        ),
        migrations.RenameField(
            model_name='parametrosusina',
            old_name='limite_temperatura_nucleo_gerador_2_ug2',
            new_name='limite_temperatura_mancal_guia_interno_2_ug1',
        ),
        migrations.RenameField(
            model_name='parametrosusina',
            old_name='limite_temperatura_nucleo_gerador_3_ug1',
            new_name='limite_temperatura_mancal_guia_interno_2_ug2',
        ),
        migrations.RenameField(
            model_name='parametrosusina',
            old_name='limite_temperatura_nucleo_gerador_3_ug2',
            new_name='limite_temperatura_mancal_guia_ug1',
        ),
        migrations.AddField(
            model_name='parametrosusina',
            name='alerta_perda_grade_ug1',
            field=models.DecimalField(decimal_places=3, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='parametrosusina',
            name='alerta_perda_grade_ug2',
            field=models.DecimalField(decimal_places=3, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='parametrosusina',
            name='alerta_temperatura_mancal_guia_ug2',
            field=models.DecimalField(decimal_places=2, default=100, max_digits=10),
        ),
        migrations.AddField(
            model_name='parametrosusina',
            name='alerta_temperatura_oleo_trafo',
            field=models.DecimalField(decimal_places=2, default=100, max_digits=10),
        ),
        migrations.AddField(
            model_name='parametrosusina',
            name='alerta_temperatura_patins_mancal_comb_1_ug1',
            field=models.DecimalField(decimal_places=2, default=100, max_digits=10),
        ),
        migrations.AddField(
            model_name='parametrosusina',
            name='alerta_temperatura_patins_mancal_comb_1_ug2',
            field=models.DecimalField(decimal_places=2, default=100, max_digits=10),
        ),
        migrations.AddField(
            model_name='parametrosusina',
            name='alerta_temperatura_patins_mancal_comb_2_ug1',
            field=models.DecimalField(decimal_places=2, default=100, max_digits=10),
        ),
        migrations.AddField(
            model_name='parametrosusina',
            name='alerta_temperatura_patins_mancal_comb_2_ug2',
            field=models.DecimalField(decimal_places=2, default=100, max_digits=10),
        ),
        migrations.AddField(
            model_name='parametrosusina',
            name='limite_temperatura_mancal_guia_ug2',
            field=models.DecimalField(decimal_places=2, default=200, max_digits=10),
        ),
        migrations.AddField(
            model_name='parametrosusina',
            name='limite_temperatura_oleo_trafo',
            field=models.DecimalField(decimal_places=2, default=200, max_digits=10),
        ),
        migrations.AddField(
            model_name='parametrosusina',
            name='limite_temperatura_patins_mancal_comb_1_ug1',
            field=models.DecimalField(decimal_places=2, default=200, max_digits=10),
        ),
        migrations.AddField(
            model_name='parametrosusina',
            name='limite_temperatura_patins_mancal_comb_1_ug2',
            field=models.DecimalField(decimal_places=2, default=200, max_digits=10),
        ),
        migrations.AddField(
            model_name='parametrosusina',
            name='limite_temperatura_patins_mancal_comb_2_ug1',
            field=models.DecimalField(decimal_places=2, default=200, max_digits=10),
        ),
        migrations.AddField(
            model_name='parametrosusina',
            name='limite_temperatura_patins_mancal_comb_2_ug2',
            field=models.DecimalField(decimal_places=2, default=200, max_digits=10),
        ),
        migrations.AddField(
            model_name='parametrosusina',
            name='perda_grade_maxima_ug1',
            field=models.DecimalField(decimal_places=3, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='parametrosusina',
            name='perda_grade_maxima_ug2',
            field=models.DecimalField(decimal_places=3, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='parametrosusina',
            name='perda_grade_ug1',
            field=models.DecimalField(decimal_places=3, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='parametrosusina',
            name='perda_grade_ug2',
            field=models.DecimalField(decimal_places=3, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='parametrosusina',
            name='pos_comporta',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='parametrosusina',
            name='ug1_nv_pos_grade',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='parametrosusina',
            name='ug2_nv_pos_grade',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='parametrosusina',
            name='nv_alvo',
            field=models.DecimalField(decimal_places=3, default=462.0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='parametrosusina',
            name='nv_maximo',
            field=models.DecimalField(decimal_places=3, default=462.37, max_digits=10),
        ),
        migrations.AlterField(
            model_name='parametrosusina',
            name='nv_minimo',
            field=models.DecimalField(decimal_places=3, default=461.37, max_digits=10),
        ),
        migrations.AlterField(
            model_name='parametrosusina',
            name='nv_montante',
            field=models.DecimalField(decimal_places=3, default=462.0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='parametrosusina',
            name='nv_religamento',
            field=models.DecimalField(decimal_places=3, default=461.8, max_digits=10),
        ),
        migrations.AlterField(
            model_name='parametrosusina',
            name='pot_minima',
            field=models.DecimalField(decimal_places=5, default=911.0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='parametrosusina',
            name='pot_nominal',
            field=models.DecimalField(decimal_places=5, default=5900.0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='parametrosusina',
            name='pot_nominal_ug',
            field=models.DecimalField(decimal_places=5, default=3037.5, max_digits=10),
        ),
    ]
