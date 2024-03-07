import logging

import src.funcoes.leitura as l
import src.conectores.servidores as s

from time import sleep
from logging.config import fileConfig

from src.dicionarios.reg import *


fileConfig("/opt/operacao-autonoma/testes/log_testes.ini")
log = logging.getLogger("teste")


l_condic: "dict[str,l.LeituraModbusBit]" = {}
l_mensageiro: "dict[str,l.LeituraModbusBit]" = {}


l_condic['1'] = l.LeituraModbusBit(s.Servidores.clp["SA"], REG_SE["DJ52L_MOLA_CARREGADA"], descricao="[SE]  DJ52L - Mola Carregada")
l_condic['2'] = l.LeituraModbusBit(s.Servidores.clp["SA"], REG_SE["DJ52L_COND_FECHAMENTO"], descricao="[SE]  DJ52L - Condição de Fechamento")
l_condic['3'] = l.LeituraModbusBit(s.Servidores.clp["SA"], REG_SE["Alarme01_00"], descricao="[SE]  PACP - Botão de Emergência Pressionado (Abertura 52L)")
l_condic['4'] = l.LeituraModbusBit(s.Servidores.clp["SA"], REG_SE["Alarme01_01"], descricao="[SE]  Emergência Supervisório Pressionada (Abertura 52L)")
l_condic['5'] = l.LeituraModbusBit(s.Servidores.clp["SA"], REG_SE["Alarme01_12"], descricao="[SE]  Relé de Proteção SEL787 - TRIP")
l_condic['6'] = l.LeituraModbusBit(s.Servidores.clp["SA"], REG_SE["Alarme02_00"], descricao="[SE]  Relé de Proteção SEL311C - TRIP")
l_condic['7'] = l.LeituraModbusBit(s.Servidores.clp["SA"], REG_SE["DJ52L_GAS_SF6_2"], invertido=True, descricao="[SE]  Disjuntor 52L Gás SF6 2")
l_condic['8'] = l.LeituraModbusBit(s.Servidores.clp["SA"], REG_SE["DJ52L_FALHA_ABERTURA"], descricao="[SE]  Disjuntor 52L Falha Abertura")
l_condic['9'] = l.LeituraModbusBit(s.Servidores.clp["SA"], REG_SE["SECC_89L_ABERTA"], descricao="[SE]  Seccionadora 89L Aberta")
l_condic['10'] = l.LeituraModbusBit(s.Servidores.clp["SA"], REG_SE["Alarme01_13"], descricao="[SE]  Relé de Proteção SEL787 - Falha 50/62BF")
l_condic['11'] = l.LeituraModbusBit(s.Servidores.clp["SA"], REG_SE["Alarme01_14"], descricao="[SE]  Relé de Proteção SEL787 - Falha de Hardware")
l_condic['12'] = l.LeituraModbusBit(s.Servidores.clp["SA"], REG_SE["Alarme02_01"], descricao="[SE]  Relé de Proteção SEL311C - Falha 50/62BF")
l_condic['13'] = l.LeituraModbusBit(s.Servidores.clp["SA"], REG_SE["Alarme02_02"], descricao="[SE]  Relé de Proteção SEL311C - Falha de Hardware")
l_condic['14'] = l.LeituraModbusBit(s.Servidores.clp["SA"], REG_SE["Alarme02_04"], descricao="[SE]  Relé de Proteção 59N - Alarme")
l_condic['15'] = l.LeituraModbusBit(s.Servidores.clp["SA"], REG_SE["Alarme02_05"], descricao="[SE]  Relé de Proteção 59N - Trip")
l_condic['16'] = l.LeituraModbusBit(s.Servidores.clp["SA"], REG_SE["Alarme02_07"], descricao="[SE]  Relé de Bloqueio 86BF (Falha Disjuntor) - Atuado")
l_condic['17'] = l.LeituraModbusBit(s.Servidores.clp["SA"], REG_SE["Alarme02_08"], descricao="[SE]  Relé de Bloqueio 86TE (Proteções do Trafo Elevador) - Atuado")
l_condic['18'] = l.LeituraModbusBit(s.Servidores.clp["SA"], REG_SE["Alarme02_11"], descricao="[SE]  Seccionadora 89L - Lâmina de Terra Fechada")
l_condic['19'] = l.LeituraModbusBit(s.Servidores.clp["SA"], REG_SE["Alarme02_12"], descricao="[SE]  Seccionadora 89L - Lâmina de Terra Bloqueada")
l_condic['20'] = l.LeituraModbusBit(s.Servidores.clp["SA"], REG_SE["Alarme02_13"], descricao="[SE]  Seccionadora 89L - Atenção! Chave em Modo Local")
l_condic['21'] = l.LeituraModbusBit(s.Servidores.clp["SA"], REG_SE["Alarme03_00"], descricao="[SE]  Disjuntor 52L - Falha na Abertura")
l_condic['22'] = l.LeituraModbusBit(s.Servidores.clp["SA"], REG_SE["Alarme03_01"], descricao="[SE]  Disjuntor 52L - Falha no Fechamento")
l_condic['23'] = l.LeituraModbusBit(s.Servidores.clp["SA"], REG_SE["Alarme03_02"], descricao="[SE]  Disjuntor 52L - Inconsistência Status Aberto/Fechado")
l_condic['24'] = l.LeituraModbusBit(s.Servidores.clp["SA"], REG_SE["Alarme03_03"], descricao="[SE]  Disjuntor 52L - Falta Tensão Vcc")
l_condic['25'] = l.LeituraModbusBit(s.Servidores.clp["SA"], REG_SE["Alarme03_04"], descricao="[SE]  Disjuntor 52L - Mola Descarregada")
l_condic['26'] = l.LeituraModbusBit(s.Servidores.clp["SA"], REG_SE["Alarme03_05"], descricao="[SE]  Disjuntor 52L - Alarme Pressão Baixa Gás SF6")
l_condic['27'] = l.LeituraModbusBit(s.Servidores.clp["SA"], REG_SE["Alarme03_06"], descricao="[SE]  Disjuntor 52L - Trip Pressão Baixa Gás SF6 ( Impedimento do Fechamento 52L)")
l_condic['28'] = l.LeituraModbusBit(s.Servidores.clp["SA"], REG_SE["Alarme03_07"], descricao="[SE]  Disjuntor 52L - Atenção! Chave em Modo Local")
l_condic['29'] = l.LeituraModbusBit(s.Servidores.clp["SA"], REG_SE["Alarme03_08"], descricao="[SE]  Disjuntor 52L - Falha no Circuito do Motor de Carregamento da Mola")
l_condic['30'] = l.LeituraModbusBit(s.Servidores.clp["SA"], REG_SE["Alarme05_02"], descricao="[SE]  Trafo Elevador - Alarme Relé Buchholz")
l_condic['31'] = l.LeituraModbusBit(s.Servidores.clp["SA"], REG_SE["Alarme05_03"], descricao="[SE]  Trafo Elevador - Trip Relé Buchholz Bloqueio (Bloqueio 86TE)")
l_condic['32'] = l.LeituraModbusBit(s.Servidores.clp["SA"], REG_SE["Alarme05_04"], descricao="[SE]  Trafo Elevador - Trip Nível de Óleo Baixo (Bloqueio 86TE)")
l_condic['33'] = l.LeituraModbusBit(s.Servidores.clp["SA"], REG_SE["Alarme05_05"], descricao="[SE]  Trafo Elevador - Alarme Nível de Óleo Alto")
l_condic['34'] = l.LeituraModbusBit(s.Servidores.clp["SA"], REG_SE["Alarme05_06"], descricao="[SE]  Trafo Elevador - Alarme Sobretemperatura do Óleo")
l_condic['35'] = l.LeituraModbusBit(s.Servidores.clp["SA"], REG_SE["Alarme05_07"], descricao="[SE]  Trafo Elevador - Trip Sobretemperatura do Óleo (Bloqueio 86TE)")
l_condic['36'] = l.LeituraModbusBit(s.Servidores.clp["SA"], REG_SE["Alarme05_08"], descricao="[SE]  Trafo Elevador - Alarme Sobretemperatura do Enrolamento")
l_condic['37'] = l.LeituraModbusBit(s.Servidores.clp["SA"], REG_SE["Alarme05_09"], descricao="[SE]  Trafo Elevador - Trip Sobretemperatura do Enrolamento (Bloqueio 86TE)")
l_condic['38'] = l.LeituraModbusBit(s.Servidores.clp["SA"], REG_SE["Alarme05_10"], descricao="[SE]  Trafo Elevador - Alarme Válvula de Alívio de Pressão")
l_condic['39'] = l.LeituraModbusBit(s.Servidores.clp["SA"], REG_SE["Alarme05_11"], descricao="[SE]  Trafo Elevador - Trip Válvula de Alívio de Pressão (Bloqueio 86TE)")
l_condic['40'] = l.LeituraModbusBit(s.Servidores.clp["SA"], REG_SE["Alarme05_12"], descricao="[SE]  Trafo Elevador - Falha Relé Monitor de Temperatura")
l_condic['41'] = l.LeituraModbusBit(s.Servidores.clp["SA"], REG_SE["Alarme05_13"], descricao="[SE]  Trafo Elevador - Trip Pressão Súbita (Bloqueio 86TE)")
l_condic['42'] = l.LeituraModbusBit(s.Servidores.clp["SA"], REG_SE["Alarme05_14"], descricao="[SE]  Trafo Elevador - Falha Ventilação Forçada")
l_condic['43'] = l.LeituraModbusBit(s.Servidores.clp["SA"], REG_SE["Alarme09_07"], descricao="[SE]  PACP-SE - Sensor de Fumaça Atuado")
l_condic['44'] = l.LeituraModbusBit(s.Servidores.clp["SA"], REG_SE["Alarme09_08"], descricao="[SE]  PACP-SE - Sensor de Fumaça Desconectado")
l_condic['45'] = l.LeituraModbusBit(s.Servidores.clp["SA"], REG_SE["Alarme12_03"], descricao="[SE]  PDSA-CC - Alimentação Painel do Trafo Elevador - Disj. Q125.7 Desligado")
l_condic['46'] = l.LeituraModbusBit(s.Servidores.clp["SA"], REG_SE["Alarme14_07"], descricao="[SE]  PDSA-CA - Alimentação do Painel PACP-SE - Disj. Q220.6 Desligado")
l_condic['47'] = l.LeituraModbusBit(s.Servidores.clp["SA"], REG_SE["Alarme16_04"], descricao="[SE]  Disjuntor 52L - Alimentação Motor de Carregamento da Mola - Disj. F1 Desligado")
l_condic['48'] = l.LeituraModbusBit(s.Servidores.clp["SA"], REG_SE["Alarme16_05"], descricao="[SE]  Disjuntor 52L - Alimentação Circuito de Aquecimento - Disj. F2 Desligado")
l_condic['49'] = l.LeituraModbusBit(s.Servidores.clp["SA"], REG_SE["Alarme16_06"], descricao="[SE]  Seccionadora 89L - Alimentação Circuito de Comando - Disj. F1 Desligado")
l_condic['50'] = l.LeituraModbusBit(s.Servidores.clp["SA"], REG_SE["Alarme16_07"], descricao="[SE]  Seccionadora 89L - Alimentação Motor de Acionamento - Disj. F3 Desligado")
l_condic['51'] = l.LeituraModbusBit(s.Servidores.clp["SA"], REG_SE["Alarme16_08"], descricao="[SE]  Seccionadora 89L - Alimentação Motor de Acionamento  - Disj. F3 Inconsistência")
l_condic['52'] = l.LeituraModbusBit(s.Servidores.clp["SA"], REG_SE["Alarme16_09"], descricao="[SE]  Seccionadora 89L - Alimentação Motor de Acionamento  - Disj. F3 Trip")
l_condic['53'] = l.LeituraModbusBit(s.Servidores.clp["SA"], REG_SE["Alarme18_04"], descricao="[SE]  PACP-SE - Falha de Comunicação com o Relé de Proteção SEL311C")
l_condic['54'] = l.LeituraModbusBit(s.Servidores.clp["SA"], REG_SE["Alarme18_05"], descricao="[SE]  PACP-SE - Falha de Comunicação com o Relé de Proteção SEL787")
l_condic['55'] = l.LeituraModbusBit(s.Servidores.clp["SA"], REG_SE["Alarme18_13"], descricao="[SE]  Relé de Proteção SEL311C - Sobrecorrente Temporizada de Fase (51P) (Abertura 52L)")
l_condic['56'] = l.LeituraModbusBit(s.Servidores.clp["SA"], REG_SE["Alarme18_14"], descricao="[SE]  Relé de Proteção SEL311C - Sobrecorrente Residual Temporizada (51G) (Abertura 52L)")
l_condic['57'] = l.LeituraModbusBit(s.Servidores.clp["SA"], REG_SE["Alarme18_15"], descricao="[SE]  Relé de Proteção SEL311C - Proteção de Distância de Fase Zona 01 (21P_Z1) (Abertura 52L)")
l_condic['58'] = l.LeituraModbusBit(s.Servidores.clp["SA"], REG_SE["Alarme19_00"], descricao="[SE]  Relé de Proteção SEL311C - Proteção de Distância de Fase Zona 02 (21P_Z2) (Abertura 52L)")
l_condic['59'] = l.LeituraModbusBit(s.Servidores.clp["SA"], REG_SE["Alarme19_01"], descricao="[SE]  Relé de Proteção SEL311C - Proteção de Distância de Fase Zona 03 Reversa (21P_Z3R) (Abertura 52L)")
l_condic['60'] = l.LeituraModbusBit(s.Servidores.clp["SA"], REG_SE["Alarme19_02"], descricao="[SE]  Relé de Proteção SEL311C - Proteção de Distância de Neutro Zona 01 (21N_Z1) (Abertura 52L)")
l_condic['61'] = l.LeituraModbusBit(s.Servidores.clp["SA"], REG_SE["Alarme19_03"], descricao="[SE]  Relé de Proteção SEL311C - Proteção de Distância de Neutro Zona 02 (21N_Z2) (Abertura 52L)")
l_condic['62'] = l.LeituraModbusBit(s.Servidores.clp["SA"], REG_SE["Alarme19_04"], descricao="[SE]  Relé de Proteção SEL311C - Proteção de Distância de Neutro Zona 03 Reversa (21N_Z3R) (Abertura 52L)")
l_condic['63'] = l.LeituraModbusBit(s.Servidores.clp["SA"], REG_SE["Alarme19_05"], descricao="[SE]  Relé de Proteção SEL311C - Proteção SubTensão (27P) (Abertura 52L)")
l_condic['64'] = l.LeituraModbusBit(s.Servidores.clp["SA"], REG_SE["Alarme19_15"], descricao="[SE]  Relé de Proteção SEL787 - Proteção Diferencial (87T) (Abertura 52L)")
l_condic['65'] = l.LeituraModbusBit(s.Servidores.clp["SA"], REG_SE["Alarme20_00"], descricao="[SE]  Relé de Proteção SEL787 - Sobrecorrente Instantânea Lado de Baixa (50P_BT) (Abertura 52L) ")
l_condic['66'] = l.LeituraModbusBit(s.Servidores.clp["SA"], REG_SE["Alarme20_01"], descricao="[SE]  Relé de Proteção SEL787 - Sobrecorrente Temporizada de Neutro (51N) (Abertura 52L)")
l_condic['67'] = l.LeituraModbusBit(s.Servidores.clp["SA"], REG_SE["Alarme20_02"], descricao="[SE]  Relé de Proteção SEL787 - Sobrecorrente Temporizada Lado de Baixa (51P_BT) (Abertura 52L)")
l_condic['68'] = l.LeituraModbusBit(s.Servidores.clp["SA"], REG_SE["Alarme20_03"], descricao="[SE]  Relé de Proteção SEL787 - Sobrecorrente Temporizada Lado de Alta (51P_AT) (Abertura 52L)")
l_condic['69'] = l.LeituraModbusBit(s.Servidores.clp["SA"], REG_SE["Alarme20_04"], descricao="[SE]  Relé de Proteção SEL787 - Grade de Proteção das Portas CSG-U1 ou CPS-U1 Aberta (Abertura 52L)")
l_condic['70'] = l.LeituraModbusBit(s.Servidores.clp["SA"], REG_SE["Alarme20_05"], descricao="[SE]  Relé de Proteção SEL787 - Grade de Proteção das Portas CSG-U2 ou CPS-U2 Aberta (Abertura 52L)")
l_condic['71'] = l.LeituraModbusBit(s.Servidores.clp["SA"], REG_SE["Alarme20_15"], descricao="[SE]  Relé de Proteção SEL787 - Grade de Proteção das Portas CSG-U3 ou CPS-U3 Aberta (Abertura 52L)")
l_condic['72'] = l.LeituraModbusBit(s.Servidores.clp["SA"], REG_SE["Alarme21_00"], descricao="[SE]  Relé de Proteção SEL787 - Grade de Proteção das Portas CSG-U4 ou CPS-U4 Aberta (Abertura 52L)")
l_condic['73'] = l.LeituraModbusBit(s.Servidores.clp["SA"], REG_SE["Alarme21_01"], descricao="[SE]  Relé de Proteção SEL787 - Grade de Proteção das Portas CSA-01 ou CSA-02 Aberta (Abertura 52L)")
l_condic['74'] = l.LeituraModbus(s.Servidores.clp["SA"], REG_SE["DJ_02"], descricao="[SE]  PACP-SE - Alimentação Circuitos de Comando - Disj. Q125.0")
l_condic['75'] = l.LeituraModbus(s.Servidores.clp["SA"], REG_SE["DJ_04"], descricao="[SE]  PACP-SE - Alimentação Relés de Proteção SEL311C e SEL787 - Disj. Q125.2")
l_condic['76'] = l.LeituraModbus(s.Servidores.clp["SA"], REG_SE["DJ_07"], descricao="[SE]  PACP-SE - Alimentação Circuito de Comando Disjuntor 52L - Disj. Q125.6")
l_condic['77'] = l.LeituraModbus(s.Servidores.clp["SA"], REG_SE["DJ_08"], descricao="[SE]  PACP-SE - Alimentação Motor Carregamento da Mola do Disjuntor 52L - Disj. Q125.7")
l_condic['78'] = l.LeituraModbus(s.Servidores.clp["SA"], REG_SE["DJ_24"], descricao="[SE]  PDSA-CC - Alimentação do Painel PDSA-CA - Disj. Q125.3")
l_condic['79'] = l.LeituraModbus(s.Servidores.clp["SA"], REG_SE["DJ_28"], descricao="[SE]  PDSA-CC - Alimentação Painel do Trafo Elevador - Disj. Q125.7")
l_condic['80'] = l.LeituraModbus(s.Servidores.clp["SA"], REG_SE["DJ_65"], descricao="[SE]  PDSA-CA - Alimentação 125Vcc Principal - Disj. Q125.0")

l_mensageiro['1'] = l.LeituraModbusBit(s.Servidores.clp["SA"], REG_SE["DJ52L_MODO_LOCAL"], descricao="[SE]  Disjuntor 52L Modo Local")
l_mensageiro['2'] = l.LeituraModbusBit(s.Servidores.clp["SA"], REG_SE["DJ52L_ALIM125VCC_MOTOR"], invertido=True, descricao="[SE]  Disjuntor 52L Motor Alimentação 125VCC Desligado")
l_mensageiro['3'] = l.LeituraModbusBit(s.Servidores.clp["SA"], REG_SE["DJ52L_FALTA_VCC"], descricao="[SE]  Disjuntor 52L Falta VCC")
l_mensageiro['4'] = l.LeituraModbusBit(s.Servidores.clp["SA"], REG_SE["DJ52L_GAS_SF6_1"], invertido=True, descricao="[SE]  Disjuntor 52L Gás SF6 1")
l_mensageiro['5'] = l.LeituraModbusBit(s.Servidores.clp["SA"], REG_SE["SECC_MODO_LOCAL"], descricao="[SE]  Seccionadora Modo Local")
l_mensageiro['6'] = l.LeituraModbusBit(s.Servidores.clp["SA"], REG_SE["SECC_LAMINA_FECHADA"], descricao="[SE]  Seccionadora Lamina Fechada")
l_mensageiro['7'] = l.LeituraModbusBit(s.Servidores.clp["SA"], REG_SE["SECC_ALIM_VCC_CMD"], descricao="[SE]  Seccionadora Comando Alimentação VCC Acionado")
l_mensageiro['8'] = l.LeituraModbusBit(s.Servidores.clp["SA"], REG_SE["SECC_ALIM_VCC_BLOQ"], descricao="[SE]  Seccionadora Comando Alimentação VCC Bloqueio")
l_mensageiro['9'] = l.LeituraModbus(s.Servidores.clp["SA"], REG_SE["DJ_17"], descricao="[SE]  CSA-U1 - Alimentação Circuitos de Sinalização - Disj. Q125.0")
l_mensageiro['10'] = l.LeituraModbus(s.Servidores.clp["SA"], REG_SE["DJ_18"], descricao="[SE]  CSA-U2 - Alimentação Circuitos de Sinalização - Disj. Q125.0")
l_mensageiro['11'] = l.LeituraModbus(s.Servidores.clp["SA"], REG_SE["DJ_26"], descricao="[SE]  PDSA-CC - Alimentação do Cubículo CSA-U1 - Disj. Q125.5")
l_mensageiro['12'] = l.LeituraModbus(s.Servidores.clp["SA"], REG_SE["DJ_27"], descricao="[SE]  PDSA-CC - Alimentação do Cubículo CSA-U2 - Disj. Q125.6")
l_mensageiro['13'] = l.LeituraModbus(s.Servidores.clp["SA"], REG_SE["DJ_29"], descricao="[SE]  PDSA-CC - Alimentação Monitor de Temperatura do TSA-01 - Disj. Q125.8")
l_mensageiro['14'] = l.LeituraModbus(s.Servidores.clp["SA"], REG_SE["DJ_30"], descricao="[SE]  PDSA-CC - Alimentação Monitor de Temperatura do TSA-02 - Disj. Q125.9")
l_mensageiro['15'] = l.LeituraModbus(s.Servidores.clp["SA"], REG_SE["DJ_31"], descricao="[SE]  PDSA-CC - Alimentação Reserva - Disj. Q125.10")
l_mensageiro['16'] = l.LeituraModbus(s.Servidores.clp["SA"], REG_SE["DJ_34"], descricao="[SE]  PDSA-CC - Alimentação do Quadro Q49-U1 - Disj. 1Q125.2")
l_mensageiro['17'] = l.LeituraModbus(s.Servidores.clp["SA"], REG_SE["DJ_41"], descricao="[SE]  PDSA-CC - Alimentação do Quadro Q49-U2 - Disj. 2Q125.2")
l_mensageiro['18'] = l.LeituraModbus(s.Servidores.clp["SA"], REG_SE["DJ_48"], descricao="[SE]  PDSA-CC - Alimentação do Quadro Q49-U3 - Disj. 3Q125.2")
l_mensageiro['19'] = l.LeituraModbus(s.Servidores.clp["SA"], REG_SE["DJ_55"], descricao="[SE]  PDSA-CC - Alimentação do Quadro Q49-U4 - Disj. 4Q125.2")
l_mensageiro['20'] = l.LeituraModbus(s.Servidores.clp["SA"], REG_SE["DJ_60"], descricao="[SE]  PDSA-CA - Alimentação Bomba Drenagem 01 - Disj. QM1")
l_mensageiro['21'] = l.LeituraModbus(s.Servidores.clp["SA"], REG_SE["DJ_61"], descricao="[SE]  PDSA-CA - Alimentação Bomba Drenagem 02 - Disj. QM2")
l_mensageiro['22'] = l.LeituraModbus(s.Servidores.clp["SA"], REG_SE["DJ_62"], descricao="[SE]  PDSA-CA - Alimentação Bomba Drenagem 03 - Disj. QM3")
l_mensageiro['23'] = l.LeituraModbus(s.Servidores.clp["SA"], REG_SE["DJ_63"], descricao="[SE]  PDSA-CA - Alimentação do Compressor de AR - Disj. QM4")
l_mensageiro['24'] = l.LeituraModbus(s.Servidores.clp["SA"], REG_SE["DJ_67"], descricao="[SE]  PDSA-CA - Alimentação do Painel PCTA - Disj. Q380.1")
l_mensageiro['25'] = l.LeituraModbus(s.Servidores.clp["SA"], REG_SE["DJ_71"], descricao="[SE]  PDSA-CA - Alimentação do Elevador da Casa de Força - Disj. Q380.5")
l_mensageiro['26'] = l.LeituraModbus(s.Servidores.clp["SA"], REG_SE["DJ_72"], descricao="[SE]  PDSA-CA - Alimentação do Painel PCAD - Disj. Q380.6")
l_mensageiro['27'] = l.LeituraModbus(s.Servidores.clp["SA"], REG_SE["DJ_73"], descricao="[SE]  PDSA-CA - Alimentação Sistema de Retrolavagem do Filtro 01 - Disj. Q380.7")
l_mensageiro['28'] = l.LeituraModbus(s.Servidores.clp["SA"], REG_SE["DJ_74"], descricao="[SE]  PDSA-CA - Alimentação Sistema de Retrolavagem do Filtro 02 - Disj. Q380.8")
l_mensageiro['29'] = l.LeituraModbus(s.Servidores.clp["SA"], REG_SE["DJ_75"], descricao="[SE]  PDSA-CA - Alimentação do Carregador de Baterias 01 - Disj. Q380.9")
l_mensageiro['30'] = l.LeituraModbus(s.Servidores.clp["SA"], REG_SE["DJ_76"], descricao="[SE]  PDSA-CA - Alimentação do Carregador de Baterias 02 - Disj. Q380.10")
l_mensageiro['31'] = l.LeituraModbus(s.Servidores.clp["SA"], REG_SE["DJ_89"], descricao="[SE]  PDSA-CA - Alimentação Bomba 01 Injeção Água Selo Mecânico - Disj. QM5")
l_mensageiro['32'] = l.LeituraModbus(s.Servidores.clp["SA"], REG_SE["DJ_90"], descricao="[SE]  PDSA-CA - Alimentação Bomba 02 Injeção Água Selo Mecânico - Disj. QM6")
l_mensageiro['33'] = l.LeituraModbus(s.Servidores.clp["SA"], REG_SE["DJ_91"], descricao="[SE]  PDSA-CA - Alimentação Bomba 01 Água Serviço - Disj. QM7")
l_mensageiro['34'] = l.LeituraModbus(s.Servidores.clp["SA"], REG_SE["DJ_92"], descricao="[SE]  PDSA-CA - Alimentação Bomba 02 Água Serviço - Disj. QM8")
l_mensageiro['35'] = l.LeituraModbus(s.Servidores.clp["SA"], REG_SE["DJ_93"], descricao="[SE]  PDSA-CA - Alimentação UCP Bombas de Drenagem - Disj. Q220.11")
l_mensageiro['36'] = l.LeituraModbus(s.Servidores.clp["SA"], REG_SE["DJ_94"], descricao="[SE]  PDSA-CA - Alimentação Torre de Resfriamento - Disj. Q380.11")
l_mensageiro['37'] = l.LeituraModbus(s.Servidores.clp["SA"], REG_SE["DJ_95"], descricao="[SE]  PDSA-CA - Alimentação Compressor de Ar - Disj. Q380.12")

for c in range(len(l_condic)):
    log.debug(f"Condicionador {c+1}:")
    log.debug(f"{l_condic[f'{c+1}'].descricao}: {l_condic[f'{c+1}'].valor}")
    log.debug("")

log.debug("")

for c in range(len(l_mensageiro)):
    log.debug(f"Mensageiro {c+1}:")
    log.debug(f"{l_mensageiro[f'{c+1}'].descricao}: {l_mensageiro[f'{c+1}'].valor}")
    log.debug("")