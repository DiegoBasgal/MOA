# Acerto de escala para os dados provenientes da clp
from math import sqrt

nv_montante_zero = 620      # 620m
nv_montante_escala = 1000   # REG[0] retorna em mm

# Constantes COV
USINA_CAP_RESERVATORIO = 43000.0
USINA_DEPLECAO = 0.5
USINA_GF_MWm = 2.6
USINA_GER_ESTIMADA_MWm = [2.08, 2.25, 1.78, 1.66, 2.42, 3.06, 2.77, 2.73, 2.97, 3.52, 3.2, 2.69]
USINA_GRAVIDADE = 9.8
USINA_NV_MAX = 643.5
USINA_NV_MIN = 643.0
USINA_NV_MONTANTE_INICIAL = 0
USINA_PERMANENCIA = 0.8540
USINA_PESO_ESP_h20 = 988
USINA_POTENCIA_NOMINAL = 5
USINA_QUEDA_BRUTA = 35.30
USINA_QUEDA_LIQUIDA = 34.31
USINA_VAZAO_NOMINAL_MAQ = 8.7
USINA_VAZAO_SANITARIA_COTA = 641
USINA_VAZAO_MAXIMA_TURBINAVEL = 17.4


def q_turbinada(UG1, UG2):

    """
    Retorna o valor da turbinada conforme conforme cálculo preestabelecido
    Cálculo retirado da planilha de excel
    """

    resultado = 0
    if UG1 > 1.0:
        resultado += (4.50629 * (UG1 ** 10) - 76.41655 * (UG1 ** 9) + 573.2949 * (UG1 ** 8) - 2503.93565 * (
                    UG1 ** 7) + 7045.30229 * (UG1 ** 6) - 13332.41115 * (UG1 ** 5) + 17168.57033 * (
                                  UG1 ** 4) - 14840.58664 * (UG1 ** 3) + 8233.58463 * (
                                  UG1 ** 2) - 2643.3025 * UG1 + 375.46773)
    if UG2 > 1.0:
        resultado += (4.50629 * (UG2 ** 10) - 76.41655 * (UG2 ** 9) + 573.2949 * (UG2 ** 8) - 2503.93565 * (
                    UG2 ** 7) + 7045.30229 * (UG2 ** 6) - 13332.41115 * (UG2 ** 5) + 17168.57033 * (
                                  UG2 ** 4) - 14840.58664 * (UG2 ** 3) + 8233.58463 * (
                                  UG2 ** 2) - 2643.3025 * UG2 + 375.46773)
    return resultado


def q_vertimento(nv):

    """
    Retorna o valor do vertimento conforme cálculo preestabelecido
    Cálculo retirado da planilha de excel
    """

    resultado = 0
    if nv > USINA_NV_MAX:
        resultado = 2.11 * (0.096006 * ((nv - 643.5) / 2.78) ** 3 - 0.270618 * ((nv - 643.5) / 2.78) ** 2 + 0.386699 * (
                    (nv - 643.5) / 2.78) + 0.783742) * 46.5 * (nv - 643.5) ** 1.5
    return resultado


def q_comporta(fechado, pos1, pos2, pos3, pos4, aberto, montante):

    resultado = 0
    h = 0

    if fechado != 0:
        h = 0
    if pos1 != 0:
        h = 0.050
    if pos2 != 0:
        h = 0.100
    if pos3 != 0:
        h = 0.150
    if pos4 != 0:
        h = 1.500
    if aberto != 0:
        h = 3.000

    if montante >= 636.5:
        resultado = 3 * h * sqrt(19.62*(montante-636.5))
    else:
        resultado = 0

    return resultado


def q_sanitaria(nv):

        temp = (nv-USINA_VAZAO_SANITARIA_COTA) if nv > USINA_VAZAO_SANITARIA_COTA else 0
        return 0.07474 * sqrt(19.62*temp)      # vazao


def q_afluente(tempo, UG1, UG2, nv_mont, nv_mont_ant, pos_comporta):

    """
    Retorna o valor do afluente conforme cálculo preestabelecido
    Cálculo retirado da planilha de excel
    """

    if not isinstance(nv_mont_ant, float):
        return -1

    resultado = 0
    aux = 0

    resultado += q_turbinada(UG1, UG2)
    resultado += q_vertimento(nv_mont)
    resultado += q_sanitaria(nv_mont)
    comp_fechada = pos_comporta & 0b1
    comp_pos1 = pos_comporta & 0b10
    comp_pos2 = pos_comporta & 0b100
    comp_pos3 = pos_comporta & 0b1000
    comp_pos4 = pos_comporta & 0b10000
    comp_aberta = pos_comporta & 0b100000
    resultado += q_comporta(comp_fechada, comp_pos1, comp_pos2, comp_pos3, comp_pos4, comp_aberta, nv_mont)

    if nv_mont > USINA_NV_MAX:
        aux += USINA_NV_MAX
    else:
        aux += nv_mont

    if nv_mont_ant > USINA_NV_MAX:
        aux -= USINA_NV_MAX
    else:
        aux -= nv_mont_ant

    resultado += (aux * ((USINA_CAP_RESERVATORIO / (USINA_NV_MAX - USINA_NV_MIN)) / tempo))

    return resultado

