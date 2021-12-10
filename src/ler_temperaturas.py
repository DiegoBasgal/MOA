from cmath import sqrt
import os
import json
import field_connector

# carrega as configurações
config_file = os.path.join(os.path.dirname(__file__), 'config.json')
with open(config_file, 'r') as file:
    cfg = json.load(file)
    
fc = field_connector.FieldConnector(cfg)

print("temperatura_enrolamento_fase_r_ug1: {}".format(fc.get_temperatura_enrolamento_fase_r_ug1()))
print("temperatura_enrolamento_fase_s_ug1: {}".format(fc.get_temperatura_enrolamento_fase_s_ug1()))
print("temperatura_enrolamento_fase_t_ug1: {}".format(fc.get_temperatura_enrolamento_fase_t_ug1()))
print("temperatura_mancal_la_casquilho_ug1: {}".format(fc.get_temperatura_mancal_la_casquilho_ug1()))
print("temperatura_mancal_la_contra_escora_1_ug1: {}".format(fc.get_temperatura_mancal_la_contra_escora_1_ug1()))
print("temperatura_mancal_la_contra_escora_2_ug1: {}".format(fc.get_temperatura_mancal_la_contra_escora_2_ug1()))
print("temperatura_mancal_la_escora_1_ug1: {}".format(fc.get_temperatura_mancal_la_escora_1_ug1()))
print("temperatura_mancal_la_escora_2_ug1 {}".format(fc.get_temperatura_mancal_la_escora_2_ug1()))
print("temperatura_mancal_lna_casquilho_ug1: {}".format(fc.get_temperatura_mancal_lna_casquilho_ug1()))
print("")
print("temperatura_enrolamento_fase_r_ug2: {}".format(fc.get_temperatura_enrolamento_fase_r_ug2()))
print("temperatura_enrolamento_fase_s_ug2: {}".format(fc.get_temperatura_enrolamento_fase_s_ug2()))
print("temperatura_enrolamento_fase_t_ug2: {}".format(fc.get_temperatura_enrolamento_fase_t_ug2()))
print("temperatura_mancal_la_casquilho_ug2: {}".format(fc.get_temperatura_mancal_la_casquilho_ug2()))
print("temperatura_mancal_la_contra_escora_1_ug2: {}".format(fc.get_temperatura_mancal_la_contra_escora_1_ug2()))
print("temperatura_mancal_la_contra_escora_2_ug2: {}".format(fc.get_temperatura_mancal_la_contra_escora_2_ug2()))
print("temperatura_mancal_la_escora_1_ug2: {}".format(fc.get_temperatura_mancal_la_escora_1_ug2()))
print("temperatura_mancal_la_escora_2_ug2 {}".format(fc.get_temperatura_mancal_la_escora_2_ug2()))
print("temperatura_mancal_lna_casquilho_ug2: {}".format(fc.get_temperatura_mancal_lna_casquilho_ug2()))
