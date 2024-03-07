import logging

import src.funcoes.leitura as l
import src.conectores.servidores as s

from time import sleep
from logging.config import fileConfig

from src.dicionarios.reg import *


fileConfig("/opt/operacao-autonoma/testes/log_testes.ini")
log = logging.getLogger("teste")


l_condic: "dict[str,l.LeituraModbusBit]" = {}

l_condic['1'] = l.LeituraModbusBit(s.Servidores.clp["AD"], REG_AD["Alarme28_00"], descricao="[AD]  Botão de Emergência Pressionado")
l_condic['2'] = l.LeituraModbusBit(s.Servidores.clp["AD"], REG_AD["Alarme28_12"], descricao="[AD]  UHCD - Botão de Emergência Pressionado")
l_condic['3'] = l.LeituraModbusBit(s.Servidores.clp["AD"], REG_AD["UHCD_OPERACIONAL"], descricao="[AD]  UHCD - Operacional")
l_condic['4'] = l.LeituraModbusBit(s.Servidores.clp["AD"], REG_AD["PCAD_FALTA_FASE"], descricao="[AD]  PCAD - Falta Fase")
l_condic['5'] = l.LeituraModbusBit(s.Servidores.clp["AD"], REG_AD["Alarme28_01"], descricao="[AD]  Relé Falta de Fase CA Atuado")
l_condic['6'] = l.LeituraModbusBit(s.Servidores.clp["AD"], REG_AD["Alarme28_04"], descricao="[AD]  UHCD - Pressão de Óleo Baixa")
l_condic['7'] = l.LeituraModbusBit(s.Servidores.clp["AD"], REG_AD["Alarme28_05"], descricao="[AD]  UHCD - Pressão de Óleo Alta na Linha da Comporta 01")
l_condic['8'] = l.LeituraModbusBit(s.Servidores.clp["AD"], REG_AD["Alarme28_06"], descricao="[AD]  UHCD - Pressão de Óleo Alta na Linha da Comporta 02")
l_condic['9'] = l.LeituraModbusBit(s.Servidores.clp["AD"], REG_AD["Alarme28_07"], descricao="[AD]  UHCD - Filtro de Retorno Sujo")
l_condic['10'] = l.LeituraModbusBit(s.Servidores.clp["AD"], REG_AD["Alarme28_08"], descricao="[AD]  UHCD - Nível de Óleo Crítico")
l_condic['11'] = l.LeituraModbusBit(s.Servidores.clp["AD"], REG_AD["Alarme28_09"], descricao="[AD]  UHCD - Nível de Óleo Alto")
l_condic['12'] = l.LeituraModbusBit(s.Servidores.clp["AD"], REG_AD["Alarme28_10"], descricao="[AD]  UHCD - Sobretemperatura do Óleo - Alarme")
l_condic['13'] = l.LeituraModbusBit(s.Servidores.clp["AD"], REG_AD["Alarme28_11"], descricao="[AD]  UHCD - Sobretemperatura do Óleo - Trip")
l_condic['14'] = l.LeituraModbusBit(s.Servidores.clp["AD"], REG_AD["Alarme29_00"], descricao="[AD]  UHCD - Bomba de Óleo 01 - Falha no Acionamento")
l_condic['15'] = l.LeituraModbusBit(s.Servidores.clp["AD"], REG_AD["Alarme29_01"], descricao="[AD]  UHCD - Bomba de Óleo 01 - Disjuntor QM1 Aberto")
l_condic['16'] = l.LeituraModbusBit(s.Servidores.clp["AD"], REG_AD["Alarme29_02"], descricao="[AD]  UHCD - Bomba de Óleo 02 - Falha no Acionamento")
l_condic['17'] = l.LeituraModbusBit(s.Servidores.clp["AD"], REG_AD["Alarme29_03"], descricao="[AD]  UHCD - Bomba de Óleo 02 - Disjuntor QM2 Aberto")
l_condic['18'] = l.LeituraModbusBit(s.Servidores.clp["AD"], REG_AD["Alarme29_05"], descricao="[AD]  Comporta 01 - Falha na Abertura")
l_condic['19'] = l.LeituraModbusBit(s.Servidores.clp["AD"], REG_AD["Alarme29_06"], descricao="[AD]  Comporta 01 - Falha no Fechamento")
l_condic['20'] = l.LeituraModbusBit(s.Servidores.clp["AD"], REG_AD["Alarme29_07"], descricao="[AD]  Comporta 01 - Falha Tempo Abertura Step Excedido")
l_condic['21'] = l.LeituraModbusBit(s.Servidores.clp["AD"], REG_AD["Alarme29_09"], descricao="[AD]  Comporta 02 - Falha na Abertura")
l_condic['22'] = l.LeituraModbusBit(s.Servidores.clp["AD"], REG_AD["Alarme29_10"], descricao="[AD]  Comporta 02 - Falha no Fechamento")
l_condic['23'] = l.LeituraModbusBit(s.Servidores.clp["AD"], REG_AD["Alarme29_11"], descricao="[AD]  Comporta 02 - Falha Tempo Abertura Step Excedido")
l_condic['24'] = l.LeituraModbusBit(s.Servidores.clp["AD"], REG_AD["Alarme29_13"], descricao="[AD]  Falha no Carregador de Baterias")
l_condic['25'] = l.LeituraModbusBit(s.Servidores.clp["AD"], REG_AD["Alarme30_00"], descricao="[AD]  Sensor de Fumaça Atuado")
l_condic['26'] = l.LeituraModbusBit(s.Servidores.clp["AD"], REG_AD["Alarme30_01"], descricao="[AD]  Sensor de Fumaça Desconectado")
l_condic['27'] = l.LeituraModbusBit(s.Servidores.clp["AD"], REG_AD["Alarme30_04"], descricao="[AD]  Sensor de Presença Atuado")
l_condic['28'] = l.LeituraModbusBit(s.Servidores.clp["AD"], REG_AD["Alarme30_05"], descricao="[AD]  Sensor de Presença Inibido")
l_condic['29'] = l.LeituraModbusBit(s.Servidores.clp["AD"], REG_AD["Alarme30_08"], descricao="[AD]  Erro de Leitura na entrada analógica da temperatura do Óleo da UHCD")
l_condic['30'] = l.LeituraModbusBit(s.Servidores.clp["AD"], REG_AD["Alarme30_09"], descricao="[AD]  Erro de Leitura na entrada analógica do nível de óleo da UHCD")
l_condic['31'] = l.LeituraModbusBit(s.Servidores.clp["AD"], REG_AD["Alarme30_10"], descricao="[AD]  Erro de Leitura na entrada analógica da posição da comporta 01")
l_condic['32'] = l.LeituraModbusBit(s.Servidores.clp["AD"], REG_AD["Alarme30_11"], descricao="[AD]  Erro de Leitura na entrada analógica da posição da comporta 02")
l_condic['33'] = l.LeituraModbusBit(s.Servidores.clp["AD"], REG_AD["Alarme31_00"], descricao="[AD]  Alimentação 380Vca Principal - Disj. Q380.0 Desligado")
l_condic['34'] = l.LeituraModbusBit(s.Servidores.clp["AD"], REG_AD["Alarme31_01"], descricao="[AD]  Alimentação 380Vca Principal - Disj. Q380.0 Inconsistência")
l_condic['35'] = l.LeituraModbusBit(s.Servidores.clp["AD"], REG_AD["Alarme31_02"], descricao="[AD]  Alimentação 380Vca Principal - Disj. Q380.0 Trip")
l_condic['36'] = l.LeituraModbusBit(s.Servidores.clp["AD"], REG_AD["Alarme31_03"], descricao="[AD]  Alimentação Carregador de Baterias - Disj. Q220.0 Desligado")
l_condic['37'] = l.LeituraModbusBit(s.Servidores.clp["AD"], REG_AD["Alarme31_04"], descricao="[AD]  Alimentação Banco de Baterias - Disj. Q24.0 Desligado")
l_condic['38'] = l.LeituraModbusBit(s.Servidores.clp["AD"], REG_AD["Alarme31_05"], descricao="[AD]  Alimentação Circuitos de Comando - Disj. Q24.3 Desligado")
l_condic['39'] = l.LeituraModbusBit(s.Servidores.clp["AD"], REG_AD["Alarme31_06"], descricao="[AD]  Alimentação Inversor 24/220Vca - Disj. Q24.4 Desligado")
l_condic['40'] = l.LeituraModbusBit(s.Servidores.clp["AD"], REG_AD["UHCD_TEMPE_OLEO_H"], descricao="[AD]  UHCD - Temperatura Óleo Alta")
l_condic['41'] = l.LeituraModbusBit(s.Servidores.clp["AD"], REG_AD["UHCD_TEMPE_OLEO_HH"], descricao="[AD]  UHCD - Temperatura Óleo Muito Alta")
l_condic['42'] = l.LeituraModbus(s.Servidores.clp["AD"], REG_AD["UHCD_TEMPERATURA_OLEO"], descricao="[AD]  UHCD - Temperatura Óleo")
l_condic['43'] = l.LeituraModbus(s.Servidores.clp["AD"], REG_AD["UHCD_NIVEL_OLEO"], descricao="[AD]  UHCD - Nível Óleo")

for c in range(len(l_condic)):
    log.debug(f"Condicionador {c+1}:")
    log.debug(f"{l_condic[f'{c+1}'].descricao}: {l_condic[f'{c+1}'].valor}")
    log.debug("")