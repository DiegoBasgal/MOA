import logging

import src.funcoes.leitura as l
import src.conectores.servidores as s

from time import sleep
from logging.config import fileConfig

from src.dicionarios.reg import *


fileConfig("/opt/operacao-autonoma/testes/log_testes.ini")
log = logging.getLogger("teste")

permissivo: "dict[str, l.LeituraModbusBit]" = {}

permissivo[f'1'] = l.LeituraModbusBit(s.Servidores.clp["AD"], REG_AD["Alarme28_01"], descricao="[AD]  Relé Falta de Fase CA Atuado")
permissivo[f'2'] = l.LeituraModbusBit(s.Servidores.clp["AD"], REG_AD["Alarme28_08"], descricao="[AD]  UHCD - Nível de Óleo Crítico")
permissivo[f'3'] = l.LeituraModbusBit(s.Servidores.clp["AD"], REG_AD["Alarme28_11"], descricao="[AD]  UHCD - Sobretemperatura do Óleo - Trip")
permissivo[f'4'] = l.LeituraModbusBit(s.Servidores.clp["AD"], REG_AD["Alarme30_00"], descricao="[AD]  Sensor de Fumaça Atuado")
permissivo[f'5'] = l.LeituraModbusBit(s.Servidores.clp["AD"], REG_AD["Alarme30_10"], descricao="[AD]  Erro de Leitura na entrada analógica da posição da comporta 01")
permissivo[f'6'] = l.LeituraModbusBit(s.Servidores.clp["AD"], REG_AD["Alarme30_11"], descricao="[AD]  Erro de Leitura na entrada analógica da posição da comporta 02")
permissivo[f'7'] = l.LeituraModbusBit(s.Servidores.clp["AD"], REG_AD["Alarme31_00"], descricao="[AD]  Alimentação 380Vca Principal - Disj. Q380.0 Desligado")
permissivo[f'8'] = l.LeituraModbusBit(s.Servidores.clp["AD"], REG_AD["Alarme31_01"], descricao="[AD]  Alimentação 380Vca Principal - Disj. Q380.0 Inconsistência")
permissivo[f'9'] = l.LeituraModbusBit(s.Servidores.clp["AD"], REG_AD["Alarme31_02"], descricao="[AD]  Alimentação 380Vca Principal - Disj. Q380.0 Trip")
permissivo[f'10'] = l.LeituraModbusBit(s.Servidores.clp["AD"], REG_AD["Alarme31_05"], descricao="[AD]  Alimentação Circuitos de Comando - Disj. Q24.3 Desligado")

for p in range(len(permissivo)):
    log.debug(f"Permissivo {p+1}:")
    log.debug(f"{permissivo[f'{p+1}'].descricao}: {permissivo[f'{p+1}'].valor}")
    log.debug("")
    log.debug("")