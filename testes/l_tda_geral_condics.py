import logging

import src.funcoes.leitura as l
import src.conectores.servidores as s

from time import sleep
from logging.config import fileConfig

from src.dicionarios.reg import *


fileConfig("/opt/operacao-autonoma/testes/log_testes.ini")
log = logging.getLogger("teste")


l_condic: "dict[str,l.LeituraModbusBit]" = {}

l_condic['1'] = l.LeituraModbusBit(s.Servidores.clp["TDA"], REG_TDA["Alarme01_04"], descricao="[TDA] Falha no CLP (Trip 86H UGs)")
l_condic['2'] = l.LeituraModbusBit(s.Servidores.clp["TDA"], REG_TDA["Alarme01_05"], descricao="[TDA] Falha Alimentação do CLP (Trip 86H UGs)")
l_condic['3'] = l.LeituraModbusBit(s.Servidores.clp["TDA"], REG_TDA["Alarme01_06"], descricao="[TDA] Falha Alimentação do CLP Temporizada")
l_condic['4'] = l.LeituraModbusBit(s.Servidores.clp["TDA"], REG_TDA["Alarme22_00"], descricao="[TDA] Relé Falta de Fase CA Atuado")
l_condic['5'] = l.LeituraModbusBit(s.Servidores.clp["TDA"], REG_TDA["Alarme22_03"], descricao="[TDA] UHTA01 - Pressão de Óleo Baixa")
l_condic['6'] = l.LeituraModbusBit(s.Servidores.clp["TDA"], REG_TDA["Alarme22_04"], descricao="[TDA] UHTA01 - Pressão de Óleo Alta na Linha da Comporta 01")
l_condic['7'] = l.LeituraModbusBit(s.Servidores.clp["TDA"], REG_TDA["Alarme22_05"], descricao="[TDA] UHTA01 - Pressão de Óleo Alta na Linha da Comporta 02")
l_condic['8'] = l.LeituraModbusBit(s.Servidores.clp["TDA"], REG_TDA["Alarme22_06"], descricao="[TDA] UHTA01 - Filtro de Retorno Sujo")
l_condic['9'] = l.LeituraModbusBit(s.Servidores.clp["TDA"], REG_TDA["Alarme22_07"], descricao="[TDA] UHTA01 - Nível de Óleo Crítico")
l_condic['10'] = l.LeituraModbusBit(s.Servidores.clp["TDA"], REG_TDA["Alarme22_08"], descricao="[TDA] UHTA01 - Nível de Óleo Alto")
l_condic['11'] = l.LeituraModbusBit(s.Servidores.clp["TDA"], REG_TDA["Alarme22_09"], descricao="[TDA] UHTA01 - Sobretemperatura do Óleo - Alarme")
l_condic['12'] = l.LeituraModbusBit(s.Servidores.clp["TDA"], REG_TDA["Alarme22_14"], descricao="[TDA] UHTA01 - Bomba de Óleo 01 - Falha no Acionamento")
l_condic['13'] = l.LeituraModbusBit(s.Servidores.clp["TDA"], REG_TDA["Alarme22_15"], descricao="[TDA] UHTA01 - Bomba de Óleo 01 - Disjuntor QM1 Aberto")
l_condic['14'] = l.LeituraModbusBit(s.Servidores.clp["TDA"], REG_TDA["Alarme23_01"], descricao="[TDA] UHTA01 - Bomba de Óleo 02 - Falha no Acionamento")
l_condic['15'] = l.LeituraModbusBit(s.Servidores.clp["TDA"], REG_TDA["Alarme23_02"], descricao="[TDA] UHTA01 - Bomba de Óleo 02 - Disjuntor QM2 Aberto")
l_condic['16'] = l.LeituraModbusBit(s.Servidores.clp["TDA"], REG_TDA["Alarme23_04"], descricao="[TDA] Comporta 01 - Falha na Abertura")
l_condic['17'] = l.LeituraModbusBit(s.Servidores.clp["TDA"], REG_TDA["Alarme23_05"], descricao="[TDA] Comporta 01 - Falha no Fechamento")
l_condic['18'] = l.LeituraModbusBit(s.Servidores.clp["TDA"], REG_TDA["Alarme23_06"], descricao="[TDA] Comporta 01 - Falha no Cracking")
l_condic['19'] = l.LeituraModbusBit(s.Servidores.clp["TDA"], REG_TDA["Alarme23_07"], descricao="[TDA] Comporta 01 - Falha na Reposição")
l_condic['20'] = l.LeituraModbusBit(s.Servidores.clp["TDA"], REG_TDA["Alarme23_08"], descricao="[TDA] Comporta 01 - Falha nos Sensores de Posição")
l_condic['21'] = l.LeituraModbusBit(s.Servidores.clp["TDA"], REG_TDA["Alarme23_11"], descricao="[TDA] Comporta 02 - Falha na Abertura")
l_condic['22'] = l.LeituraModbusBit(s.Servidores.clp["TDA"], REG_TDA["Alarme23_12"], descricao="[TDA] Comporta 02 - Falha no Fechamento")
l_condic['23'] = l.LeituraModbusBit(s.Servidores.clp["TDA"], REG_TDA["Alarme23_13"], descricao="[TDA] Comporta 02 - Falha no Cracking")
l_condic['24'] = l.LeituraModbusBit(s.Servidores.clp["TDA"], REG_TDA["Alarme23_14"], descricao="[TDA] Comporta 02 - Falha na Reposição")
l_condic['25'] = l.LeituraModbusBit(s.Servidores.clp["TDA"], REG_TDA["Alarme23_15"], descricao="[TDA] Comporta 02 - Falha nos Sensores de Posição")
l_condic['26'] = l.LeituraModbusBit(s.Servidores.clp["TDA"], REG_TDA["Alarme24_02"], descricao="[TDA] UHTA02 - Pressão de Óleo Baixa")
l_condic['27'] = l.LeituraModbusBit(s.Servidores.clp["TDA"], REG_TDA["Alarme24_03"], descricao="[TDA] UHTA02 - Pressão de Óleo Alta na Linha da Comporta 03")
l_condic['28'] = l.LeituraModbusBit(s.Servidores.clp["TDA"], REG_TDA["Alarme24_04"], descricao="[TDA] UHTA02 - Pressão de Óleo Alta na Linha da Comporta 04")
l_condic['29'] = l.LeituraModbusBit(s.Servidores.clp["TDA"], REG_TDA["Alarme24_05"], descricao="[TDA] UHTA02 - Filtro de Retorno Sujo")
l_condic['30'] = l.LeituraModbusBit(s.Servidores.clp["TDA"], REG_TDA["Alarme24_06"], descricao="[TDA] UHTA02 - Nível de Óleo Crítico")
l_condic['31'] = l.LeituraModbusBit(s.Servidores.clp["TDA"], REG_TDA["Alarme24_07"], descricao="[TDA] UHTA02 - Nível de Óleo Alto")
l_condic['32'] = l.LeituraModbusBit(s.Servidores.clp["TDA"], REG_TDA["Alarme24_08"], descricao="[TDA] UHTA02 - Sobretemperatura do Óleo - Alarme")
l_condic['33'] = l.LeituraModbusBit(s.Servidores.clp["TDA"], REG_TDA["Alarme24_10"], descricao="[TDA] UHTA02 - Botão de Emergência Acionado")
l_condic['34'] = l.LeituraModbusBit(s.Servidores.clp["TDA"], REG_TDA["Alarme24_13"], descricao="[TDA] UHTA02 - Bomba de Óleo 01 - Falha no Acionamento")
l_condic['35'] = l.LeituraModbusBit(s.Servidores.clp["TDA"], REG_TDA["Alarme24_14"], descricao="[TDA] UHTA02 - Bomba de Óleo 01 - Disjuntor QM3 Aberto")
l_condic['36'] = l.LeituraModbusBit(s.Servidores.clp["TDA"], REG_TDA["Alarme25_00"], descricao="[TDA] UHTA02 - Bomba de Óleo 02 - Falha no Acionamento")
l_condic['37'] = l.LeituraModbusBit(s.Servidores.clp["TDA"], REG_TDA["Alarme25_01"], descricao="[TDA] UHTA02 - Bomba de Óleo 02 - Disjuntor QM4 Aberto")
l_condic['38'] = l.LeituraModbusBit(s.Servidores.clp["TDA"], REG_TDA["Alarme25_03"], descricao="[TDA] Comporta 03 - Falha na Abertura")
l_condic['39'] = l.LeituraModbusBit(s.Servidores.clp["TDA"], REG_TDA["Alarme25_04"], descricao="[TDA] Comporta 03 - Falha no Fechamento")
l_condic['40'] = l.LeituraModbusBit(s.Servidores.clp["TDA"], REG_TDA["Alarme25_05"], descricao="[TDA] Comporta 03 - Falha no Cracking")
l_condic['41'] = l.LeituraModbusBit(s.Servidores.clp["TDA"], REG_TDA["Alarme25_06"], descricao="[TDA] Comporta 03 - Falha na Reposição")
l_condic['42'] = l.LeituraModbusBit(s.Servidores.clp["TDA"], REG_TDA["Alarme25_07"], descricao="[TDA] Comporta 03 - Falha nos Sensores de Posição")
l_condic['43'] = l.LeituraModbusBit(s.Servidores.clp["TDA"], REG_TDA["Alarme25_10"], descricao="[TDA] Comporta 04 - Falha na Abertura")
l_condic['44'] = l.LeituraModbusBit(s.Servidores.clp["TDA"], REG_TDA["Alarme25_11"], descricao="[TDA] Comporta 04 - Falha no Fechamento")
l_condic['45'] = l.LeituraModbusBit(s.Servidores.clp["TDA"], REG_TDA["Alarme25_12"], descricao="[TDA] Comporta 04 - Falha no Cracking")
l_condic['46'] = l.LeituraModbusBit(s.Servidores.clp["TDA"], REG_TDA["Alarme25_13"], descricao="[TDA] Comporta 04 - Falha na Reposição")
l_condic['47'] = l.LeituraModbusBit(s.Servidores.clp["TDA"], REG_TDA["Alarme25_14"], descricao="[TDA] Comporta 04 - Falha nos Sensores de Posição")
l_condic['48'] = l.LeituraModbusBit(s.Servidores.clp["TDA"], REG_TDA["Alarme26_01"], descricao="[TDA] Sensor de Fumaça Atuado")
l_condic['49'] = l.LeituraModbusBit(s.Servidores.clp["TDA"], REG_TDA["Alarme26_02"], descricao="[TDA] Sensor de Fumaça Desconectado")
l_condic['50'] = l.LeituraModbusBit(s.Servidores.clp["TDA"], REG_TDA["Alarme26_04"], descricao="[TDA] Sensor de Presença Atuado")
l_condic['51'] = l.LeituraModbusBit(s.Servidores.clp["TDA"], REG_TDA["Alarme26_05"], descricao="[TDA] Sensor de Presença Inibido")
l_condic['52'] = l.LeituraModbusBit(s.Servidores.clp["TDA"], REG_TDA["Alarme26_07"], descricao="[TDA] Erro de Leitura na entrada analógica da temperatura do Óleo da UHTA01")
l_condic['53'] = l.LeituraModbusBit(s.Servidores.clp["TDA"], REG_TDA["Alarme26_08"], descricao="[TDA] Erro de Leitura na entrada analógica do nível de óleo da UHTA01")
l_condic['54'] = l.LeituraModbusBit(s.Servidores.clp["TDA"], REG_TDA["Alarme26_09"], descricao="[TDA] Erro de Leitura na entrada analógica da temperatura do Óleo da UHTA02")
l_condic['55'] = l.LeituraModbusBit(s.Servidores.clp["TDA"], REG_TDA["Alarme26_10"], descricao="[TDA] Erro de Leitura na entrada analógica do nível de óleo da UHTA02")
l_condic['56'] = l.LeituraModbusBit(s.Servidores.clp["TDA"], REG_TDA["Alarme26_11"], descricao="[TDA] Erro de Leitura na entrada analógica da posição da comporta 01")
l_condic['57'] = l.LeituraModbusBit(s.Servidores.clp["TDA"], REG_TDA["Alarme26_12"], descricao="[TDA] Erro de Leitura na entrada analógica da posição da comporta 02")
l_condic['58'] = l.LeituraModbusBit(s.Servidores.clp["TDA"], REG_TDA["Alarme26_13"], descricao="[TDA] Erro de Leitura na entrada analógica da posição da comporta 03")
l_condic['59'] = l.LeituraModbusBit(s.Servidores.clp["TDA"], REG_TDA["Alarme26_14"], descricao="[TDA] Erro de Leitura na entrada analógica da posição da comporta 04")
l_condic['60'] = l.LeituraModbusBit(s.Servidores.clp["TDA"], REG_TDA["Alarme27_00"], descricao="[TDA] Grade 01 Suja")
l_condic['61'] = l.LeituraModbusBit(s.Servidores.clp["TDA"], REG_TDA["Alarme27_01"], descricao="[TDA] Grade 02 Suja")
l_condic['62'] = l.LeituraModbusBit(s.Servidores.clp["TDA"], REG_TDA["Alarme27_02"], descricao="[TDA] Grade 03 Suja")
l_condic['63'] = l.LeituraModbusBit(s.Servidores.clp["TDA"], REG_TDA["Alarme27_03"], descricao="[TDA] Grade 04 Suja")

for c in range(len(l_condic)):
    log.debug(f"Condicionador {c+1}:")
    log.debug(f"{l_condic[f'{c+1}'].descricao}: {l_condic[f'{c+1}'].valor}")
    log.debug("")