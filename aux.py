VAZAO_SANITARIA = 0
VAZAO_NOMINAL_TURBINA = 17.87
NUM_MAQUINAS = 2
VOLUME_RESERVATORIO = 1.9 * 10 ** 6

TEMPO_PARTIDA = 20 + 106 + 193
TEMPO_TOMADA_DE_CARGA = 1.5 * 60

amostras_por_minuto = 1

steps = round((2 * (TEMPO_PARTIDA + TEMPO_TOMADA_DE_CARGA) / 60) * amostras_por_minuto)

print(steps)