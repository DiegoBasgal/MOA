import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt

VAZAO_SANITARIA = 0
VAZAO_NOMINAL_TURBINA = 17.87
NUM_MAQUINAS = 2
VOLUME_RESERVATORIO = 1.9 * 10 ** 6

TEMPO_PARTIDA = 20 + 106 + 193
TEMPO_TOMADA_DE_CARGA = 1.5 * 60

amostras_por_minuto = 1


# Considera-se que o reservatório iniciará em nível mínimo, dessa forma é necessário adicionar vazão para
# que o sistema estabilize no nível de referência. Deixar uma vazão estável por um tempo para que as máquinas possam estabilizar também.
#
# 1  -> Estabilização com 2 UGs
# 2  -> Degrau + 10% da vazão nominal da usina
# 3  -> Degrau - 20% da vazão nominal da usina
# 4  -> Degrau para 70% da potência de 1 UG
# 5  -> Rampa até vertimento
# 6  -> Vertimento excessivo
# 7  -> Rampa de redução de vazão até 60% da vazão mínima da máquina, para replecionamento do reservatório
# 8  -> Rampa até vazão nominal de uma máquina
# 9  -> Oscilação de vazão na região de transição
# 10 -> Rampa até 75% da vazão nominal da usina
# 11 -> Oscilação na região de operação de 2 ugs (50% e 100% da vazão nominal da usina)
# 12 -> rampas curtas com inclinações diferentes entre 80% e 100% da vazão de uma ug, para teste de sobressinal da região crítica
# 13 -> Degrau para vazão mínima de uma ug


def encher_e_estabilizar_reservatorio(volume_reservatorio, vazao_ugs, steps):

    print("")
    print("Encher e estabilizar:")

    variacao = 0.8 * vazao_ugs / steps
    print(f"Variação -> {variacao}:")

    array = np.concatenate(((volume_reservatorio * 0.8,), np.arange(0, 0.8 * vazao_ugs, variacao)))
    print(f"Array -> {array}")

    return array

def vazao_continua(steps, vazao):

    print("")
    print("Vazão contínua:")

    array = np.ones(round(steps)) * vazao
    print(f"Array -> {array}")

    return array

def rampa_vazao(inicio, fim, steps):

    print("")
    print("Rampa vazão:")

    variacao = (fim - inicio) / steps
    print(f"Variação -> {variacao}")

    array = np.arange(inicio, fim, variacao)
    print(f"Array -> {array}")

    return array

def oscilar_vazao(amplitude, constante, steps):

    print("")
    print("Oscilar vazao:")

    wt = np.arange(0, 1, 1/steps) * 2 * math.pi
    print(f"WT -> {wt}")

    array = np.sin(wt)
    print(f"Array -> {array}")

    array = constante + array
    print(f"Array -> {array}")

    array[array<0] = 0
    print(f"Array -> {array}")

    return array


# 1 -> Estabilização com 2 UGs

steps = round((2 * (TEMPO_PARTIDA + TEMPO_TOMADA_DE_CARGA) / 60) * amostras_por_minuto)

passo1 = encher_e_estabilizar_reservatorio(VOLUME_RESERVATORIO, 2 * VAZAO_NOMINAL_TURBINA, steps)

vazao = passo1

# 2 -> Degrau + 10% da vazão nominal da usina

steps = round(((TEMPO_TOMADA_DE_CARGA * 2) / 60) / amostras_por_minuto)
steps = max(10, steps)

passo2 = vazao_continua(steps, passo1[-1] + 0.1 * VAZAO_NOMINAL_TURBINA * 2)

vazao = np.concatenate((vazao, passo2))


# 3 -> Degrau - 10% da vazão nominal da usina
passo3 = vazao_continua(steps, passo2[-1] - 0.2 * VAZAO_NOMINAL_TURBINA * 2)
vazao = np.concatenate((vazao, passo3))

# 4 -> Degrau para 70% da potência de 1 UG
passo4 = vazao_continua(steps, 0.7 * VAZAO_NOMINAL_TURBINA)
vazao = np.concatenate((vazao, passo4))

# 5 -> Rampa até vertimento
steps = round(20 / amostras_por_minuto)
passo5 = rampa_vazao(passo4[-1], 2 * 2 * VAZAO_NOMINAL_TURBINA, steps)
vazao = np.concatenate((vazao, passo5))

# 6  -> Vertimento excessivo
steps = round((2 * (TEMPO_PARTIDA + TEMPO_TOMADA_DE_CARGA) / 60) / amostras_por_minuto)
passo6 = vazao_continua(steps, 2 * 2 * VAZAO_NOMINAL_TURBINA)
vazao = np.concatenate((vazao, passo6))

# 7  -> Rampa de redução de vazão até 60% da vazão mínima da máquina, para replecionamento do reservatório
steps = 20 * amostras_por_minuto
passo7 = rampa_vazao(passo6[-1], 0.6 * VAZAO_NOMINAL_TURBINA, steps)
vazao = np.concatenate((vazao, passo7))

# 8  -> Rampa até vazão nominal de uma máquina
steps = 20 * amostras_por_minuto
passo8 = rampa_vazao(passo7[-1], VAZAO_NOMINAL_TURBINA, steps)
vazao = np.concatenate((vazao, passo8))

# 9  -> Oscilação de vazão na região de transição
steps = 40 * amostras_por_minuto
passo9 = oscilar_vazao(0.5 * VAZAO_NOMINAL_TURBINA, passo8[-1], steps)
vazao = np.concatenate((vazao, passo9))

# 10 -> Rampa até 75% da vazão nominal da usina
steps = 20 * amostras_por_minuto
passo10 = rampa_vazao(passo9[-1], 0.75 * 2 * VAZAO_NOMINAL_TURBINA, steps)
vazao = np.concatenate((vazao, passo10))

''# 11 -> Oscilação na região de operação de 2 ugs (50% e 100% da vazão nominal da usina)
steps = 40 * amostras_por_minuto
passo11 = oscilar_vazao(0.5 * VAZAO_NOMINAL_TURBINA, passo10[-1], steps)
vazao = np.concatenate((vazao, passo11))

# 12 -> rampas curtas com inclinações diferentes entre 80% e 100% da vazão de uma ug, para teste de sobressinal da região crítica
steps = steps = (2 * (TEMPO_PARTIDA + TEMPO_TOMADA_DE_CARGA) / 60) * amostras_por_minuto
passo12 = vazao_continua(steps, VAZAO_NOMINAL_TURBINA * 0.8)
vazao_continua_nominal = vazao_continua(steps, VAZAO_NOMINAL_TURBINA)
vazao = np.concatenate((vazao, passo12))

steps_rampa = 20 * amostras_por_minuto
passo13 = rampa_vazao(passo12[-1], VAZAO_NOMINAL_TURBINA, steps_rampa)
vazao = np.concatenate((vazao, passo13))

vazao = np.concatenate((vazao, vazao_continua_nominal))
vazao = np.concatenate((vazao, passo12))

steps_rampa = 10 * amostras_por_minuto
passo14 = rampa_vazao(passo12[-1], VAZAO_NOMINAL_TURBINA, steps_rampa)
vazao = np.concatenate((vazao, passo14))

vazao = np.concatenate((vazao, vazao_continua_nominal))
vazao = np.concatenate((vazao, passo12))

steps_rampa = 5 * amostras_por_minuto
passo16 = rampa_vazao(passo12[-1], VAZAO_NOMINAL_TURBINA, steps_rampa)
vazao = np.concatenate((vazao, passo16))

vazao = np.concatenate((vazao, vazao_continua_nominal))
vazao = np.concatenate((vazao, passo12))

# 13 -> Degrau para vazão mínima de uma ug
passo16 = vazao_continua(2 * steps, VAZAO_NOMINAL_TURBINA * 0.3)
vazao = np.concatenate((vazao, passo16))

# 14 ->  Degrau para vazão mínima de uma ug
passo17 = vazao_continua(2 * steps, VAZAO_NOMINAL_TURBINA * 0.8)
vazao = np.concatenate((vazao, passo17))

# 13 -> Degrau para vazão mínima de uma ug
passo18 = vazao_continua(2 * steps, VAZAO_NOMINAL_TURBINA * 1.2)
vazao = np.concatenate((vazao, passo18))

# 13 -> Degrau para vazão mínima de uma ug
passo19 = vazao_continua(2 * steps, VAZAO_NOMINAL_TURBINA * 1.9)
vazao = np.concatenate((vazao, passo19))

steps = 60 * amostras_por_minuto
passo16 = rampa_vazao(vazao[-1], VAZAO_SANITARIA, steps)
vazao = np.concatenate((vazao, passo16))

steps = 12 * 60 * amostras_por_minuto
passo16 = vazao_continua(steps, VAZAO_SANITARIA)
vazao = np.concatenate((vazao, passo16))

print(f"Array total -> {vazao}")

for v in vazao:
    print(v)


# x = np.arange(1, len(vazao))

# plt.figure()
# plt.grid()
# plt.plot(x, vazao[1:], color='#a7a7a7')
# #plt.plot(saida_ema.iloc[100:], color='r')
# #plt.legend(['Entrada Nível', 'Saída EMA'])
# plt.ylabel('Vazão [m³/s]')
# #plt.xticks(rotation = 90)
# plt.savefig('/opt/operacao-autonoma/vazao.png', bbox_inches='tight')

# dataframe = pd.DataFrame(vazao, index=np.arange(0,len(vazao)))

# dataframe.to_csv('/opt/operacao-autonoma/vazao_teste_moa_XAV.csv')