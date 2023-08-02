# Generated by Django 4.2.4 on 2023-08-02 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parametros', '0005_alter_parametrosusina_clp_moa_ip_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='controleestados',
            name='ultimo_estado_ug2',
        ),
        migrations.RemoveField(
            model_name='controleestados',
            name='ultimo_estado_ug3',
        ),
        migrations.RemoveField(
            model_name='parametrosusina',
            name='alerta_caixa_espiral_ug2',
        ),
        migrations.RemoveField(
            model_name='parametrosusina',
            name='alerta_caixa_espiral_ug3',
        ),
        migrations.RemoveField(
            model_name='parametrosusina',
            name='alerta_temperatura_fase_r_ug1',
        ),
        migrations.RemoveField(
            model_name='parametrosusina',
            name='alerta_temperatura_fase_r_ug2',
        ),
        migrations.RemoveField(
            model_name='parametrosusina',
            name='alerta_temperatura_fase_r_ug3',
        ),
        migrations.RemoveField(
            model_name='parametrosusina',
            name='alerta_temperatura_fase_s_ug1',
        ),
        migrations.RemoveField(
            model_name='parametrosusina',
            name='alerta_temperatura_fase_s_ug2',
        ),
        migrations.RemoveField(
            model_name='parametrosusina',
            name='alerta_temperatura_fase_s_ug3',
        ),
        migrations.RemoveField(
            model_name='parametrosusina',
            name='alerta_temperatura_fase_t_ug1',
        ),
        migrations.RemoveField(
            model_name='parametrosusina',
            name='alerta_temperatura_fase_t_ug2',
        ),
        migrations.RemoveField(
            model_name='parametrosusina',
            name='alerta_temperatura_fase_t_ug3',
        ),
        migrations.RemoveField(
            model_name='parametrosusina',
            name='alerta_temperatura_mancal_guia_contra_ug1',
        ),
        migrations.RemoveField(
            model_name='parametrosusina',
            name='alerta_temperatura_mancal_guia_contra_ug2',
        ),
        migrations.RemoveField(
            model_name='parametrosusina',
            name='alerta_temperatura_mancal_guia_contra_ug3',
        ),
        migrations.RemoveField(
            model_name='parametrosusina',
            name='alerta_temperatura_mancal_guia_escora_ug1',
        ),
        migrations.RemoveField(
            model_name='parametrosusina',
            name='alerta_temperatura_mancal_guia_escora_ug2',
        ),
        migrations.RemoveField(
            model_name='parametrosusina',
            name='alerta_temperatura_mancal_guia_escora_ug3',
        ),
        migrations.RemoveField(
            model_name='parametrosusina',
            name='alerta_temperatura_mancal_guia_radial_ug1',
        ),
        migrations.RemoveField(
            model_name='parametrosusina',
            name='alerta_temperatura_mancal_guia_radial_ug2',
        ),
        migrations.RemoveField(
            model_name='parametrosusina',
            name='alerta_temperatura_mancal_guia_radial_ug3',
        ),
        migrations.RemoveField(
            model_name='parametrosusina',
            name='alerta_temperatura_mancal_rad_dia_1_ug1',
        ),
        migrations.RemoveField(
            model_name='parametrosusina',
            name='alerta_temperatura_mancal_rad_dia_1_ug2',
        ),
        migrations.RemoveField(
            model_name='parametrosusina',
            name='alerta_temperatura_mancal_rad_dia_1_ug3',
        ),
        migrations.RemoveField(
            model_name='parametrosusina',
            name='alerta_temperatura_mancal_rad_dia_2_ug1',
        ),
        migrations.RemoveField(
            model_name='parametrosusina',
            name='alerta_temperatura_mancal_rad_dia_2_ug2',
        ),
        migrations.RemoveField(
            model_name='parametrosusina',
            name='alerta_temperatura_mancal_rad_dia_2_ug3',
        ),
        migrations.RemoveField(
            model_name='parametrosusina',
            name='alerta_temperatura_mancal_rad_tra_1_ug1',
        ),
        migrations.RemoveField(
            model_name='parametrosusina',
            name='alerta_temperatura_mancal_rad_tra_1_ug2',
        ),
        migrations.RemoveField(
            model_name='parametrosusina',
            name='alerta_temperatura_mancal_rad_tra_1_ug3',
        ),
        migrations.RemoveField(
            model_name='parametrosusina',
            name='alerta_temperatura_mancal_rad_tra_2_ug1',
        ),
        migrations.RemoveField(
            model_name='parametrosusina',
            name='alerta_temperatura_mancal_rad_tra_2_ug2',
        ),
        migrations.RemoveField(
            model_name='parametrosusina',
            name='alerta_temperatura_mancal_rad_tra_2_ug3',
        ),
        migrations.RemoveField(
            model_name='parametrosusina',
            name='alerta_temperatura_nucleo_estator_ug1',
        ),
        migrations.RemoveField(
            model_name='parametrosusina',
            name='alerta_temperatura_nucleo_estator_ug2',
        ),
        migrations.RemoveField(
            model_name='parametrosusina',
            name='alerta_temperatura_nucleo_estator_ug3',
        ),
        migrations.RemoveField(
            model_name='parametrosusina',
            name='alerta_temperatura_saida_de_ar_ug1',
        ),
        migrations.RemoveField(
            model_name='parametrosusina',
            name='alerta_temperatura_saida_de_ar_ug2',
        ),
        migrations.RemoveField(
            model_name='parametrosusina',
            name='alerta_temperatura_saida_de_ar_ug3',
        ),
        migrations.RemoveField(
            model_name='parametrosusina',
            name='clp_ug2_ip',
        ),
        migrations.RemoveField(
            model_name='parametrosusina',
            name='clp_ug2_porta',
        ),
        migrations.RemoveField(
            model_name='parametrosusina',
            name='clp_ug3_ip',
        ),
        migrations.RemoveField(
            model_name='parametrosusina',
            name='clp_ug3_porta',
        ),
        migrations.RemoveField(
            model_name='parametrosusina',
            name='limite_caixa_espiral_ug2',
        ),
        migrations.RemoveField(
            model_name='parametrosusina',
            name='limite_caixa_espiral_ug3',
        ),
        migrations.RemoveField(
            model_name='parametrosusina',
            name='limite_temperatura_fase_r_ug1',
        ),
        migrations.RemoveField(
            model_name='parametrosusina',
            name='limite_temperatura_fase_r_ug2',
        ),
        migrations.RemoveField(
            model_name='parametrosusina',
            name='limite_temperatura_fase_r_ug3',
        ),
        migrations.RemoveField(
            model_name='parametrosusina',
            name='limite_temperatura_fase_s_ug1',
        ),
        migrations.RemoveField(
            model_name='parametrosusina',
            name='limite_temperatura_fase_s_ug2',
        ),
        migrations.RemoveField(
            model_name='parametrosusina',
            name='limite_temperatura_fase_s_ug3',
        ),
        migrations.RemoveField(
            model_name='parametrosusina',
            name='limite_temperatura_fase_t_ug1',
        ),
        migrations.RemoveField(
            model_name='parametrosusina',
            name='limite_temperatura_fase_t_ug2',
        ),
        migrations.RemoveField(
            model_name='parametrosusina',
            name='limite_temperatura_fase_t_ug3',
        ),
        migrations.RemoveField(
            model_name='parametrosusina',
            name='limite_temperatura_mancal_guia_contra_ug1',
        ),
        migrations.RemoveField(
            model_name='parametrosusina',
            name='limite_temperatura_mancal_guia_contra_ug2',
        ),
        migrations.RemoveField(
            model_name='parametrosusina',
            name='limite_temperatura_mancal_guia_contra_ug3',
        ),
        migrations.RemoveField(
            model_name='parametrosusina',
            name='limite_temperatura_mancal_guia_escora_ug1',
        ),
        migrations.RemoveField(
            model_name='parametrosusina',
            name='limite_temperatura_mancal_guia_escora_ug2',
        ),
        migrations.RemoveField(
            model_name='parametrosusina',
            name='limite_temperatura_mancal_guia_escora_ug3',
        ),
        migrations.RemoveField(
            model_name='parametrosusina',
            name='limite_temperatura_mancal_guia_radial_ug1',
        ),
        migrations.RemoveField(
            model_name='parametrosusina',
            name='limite_temperatura_mancal_guia_radial_ug2',
        ),
        migrations.RemoveField(
            model_name='parametrosusina',
            name='limite_temperatura_mancal_guia_radial_ug3',
        ),
        migrations.RemoveField(
            model_name='parametrosusina',
            name='limite_temperatura_mancal_rad_dia_1_ug1',
        ),
        migrations.RemoveField(
            model_name='parametrosusina',
            name='limite_temperatura_mancal_rad_dia_1_ug2',
        ),
        migrations.RemoveField(
            model_name='parametrosusina',
            name='limite_temperatura_mancal_rad_dia_1_ug3',
        ),
        migrations.RemoveField(
            model_name='parametrosusina',
            name='limite_temperatura_mancal_rad_dia_2_ug1',
        ),
        migrations.RemoveField(
            model_name='parametrosusina',
            name='limite_temperatura_mancal_rad_dia_2_ug2',
        ),
        migrations.RemoveField(
            model_name='parametrosusina',
            name='limite_temperatura_mancal_rad_dia_2_ug3',
        ),
        migrations.RemoveField(
            model_name='parametrosusina',
            name='limite_temperatura_mancal_rad_tra_1_ug1',
        ),
        migrations.RemoveField(
            model_name='parametrosusina',
            name='limite_temperatura_mancal_rad_tra_1_ug2',
        ),
        migrations.RemoveField(
            model_name='parametrosusina',
            name='limite_temperatura_mancal_rad_tra_1_ug3',
        ),
        migrations.RemoveField(
            model_name='parametrosusina',
            name='limite_temperatura_mancal_rad_tra_2_ug1',
        ),
        migrations.RemoveField(
            model_name='parametrosusina',
            name='limite_temperatura_mancal_rad_tra_2_ug2',
        ),
        migrations.RemoveField(
            model_name='parametrosusina',
            name='limite_temperatura_mancal_rad_tra_2_ug3',
        ),
        migrations.RemoveField(
            model_name='parametrosusina',
            name='limite_temperatura_nucleo_estator_ug1',
        ),
        migrations.RemoveField(
            model_name='parametrosusina',
            name='limite_temperatura_nucleo_estator_ug2',
        ),
        migrations.RemoveField(
            model_name='parametrosusina',
            name='limite_temperatura_nucleo_estator_ug3',
        ),
        migrations.RemoveField(
            model_name='parametrosusina',
            name='limite_temperatura_saida_de_ar_ug1',
        ),
        migrations.RemoveField(
            model_name='parametrosusina',
            name='limite_temperatura_saida_de_ar_ug2',
        ),
        migrations.RemoveField(
            model_name='parametrosusina',
            name='limite_temperatura_saida_de_ar_ug3',
        ),
        migrations.RemoveField(
            model_name='parametrosusina',
            name='modo_de_escolha_das_ugs',
        ),
        migrations.RemoveField(
            model_name='parametrosusina',
            name='ug1_prioridade',
        ),
        migrations.RemoveField(
            model_name='parametrosusina',
            name='ug2_pot',
        ),
        migrations.RemoveField(
            model_name='parametrosusina',
            name='ug2_prioridade',
        ),
        migrations.RemoveField(
            model_name='parametrosusina',
            name='ug2_setpot',
        ),
        migrations.RemoveField(
            model_name='parametrosusina',
            name='ug2_ultimo_estado',
        ),
        migrations.RemoveField(
            model_name='parametrosusina',
            name='ug3_pot',
        ),
        migrations.RemoveField(
            model_name='parametrosusina',
            name='ug3_prioridade',
        ),
        migrations.RemoveField(
            model_name='parametrosusina',
            name='ug3_setpot',
        ),
        migrations.RemoveField(
            model_name='parametrosusina',
            name='ug3_ultimo_estado',
        ),
        migrations.AlterField(
            model_name='parametrosusina',
            name='clp_moa_ip',
            field=models.CharField(default='0.0.0.0', max_length=15),
        ),
        migrations.AlterField(
            model_name='parametrosusina',
            name='clp_sa_ip',
            field=models.CharField(default='0.0.0.0', max_length=15),
        ),
        migrations.AlterField(
            model_name='parametrosusina',
            name='clp_sa_porta',
            field=models.IntegerField(default=502),
        ),
        migrations.AlterField(
            model_name='parametrosusina',
            name='clp_tda_ip',
            field=models.CharField(default='0.0.0.0', max_length=15),
        ),
        migrations.AlterField(
            model_name='parametrosusina',
            name='clp_tda_porta',
            field=models.IntegerField(default=502),
        ),
        migrations.AlterField(
            model_name='parametrosusina',
            name='clp_ug1_ip',
            field=models.CharField(default='0.0.0.0', max_length=15),
        ),
        migrations.AlterField(
            model_name='parametrosusina',
            name='clp_ug1_porta',
            field=models.IntegerField(default=502),
        ),
        migrations.AlterField(
            model_name='parametrosusina',
            name='pot_minima',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='parametrosusina',
            name='pot_nominal',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='parametrosusina',
            name='pot_nominal_ug',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=10),
        ),
    ]
