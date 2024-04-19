__version__ = "0.1"
__author__ = "Diego Basgal", "Henrique Pfeifer"
__credits__ = ["Lucas Lavratti", ...]
__description__ = "Este módulo corresponde a implementação da operação da Tomada da Água."

import pytz
import logging
import traceback
import numpy as np

import src.comporta as cp
import src.dicionarios.dict as d
import src.funcoes.leitura as lei
import src.funcoes.escrita as esc
import src.conectores.servidores as srv
import src.conectores.banco_dados as bd
import src.funcoes.condicionadores as c

from time import sleep
from datetime import datetime, timedelta

from src.dicionarios.const import *
from src.dicionarios.reg_elipse import *


logger = logging.getLogger("logger")


class TomadaAgua:
    def __init__(self, cfg: "dict"=None, serv: "srv.Servidores"=None, bd: "bd.BancoDados"=None) -> "None":

        # ATRIBUIÇÃO DE VARIÁVEIS

        self.bd = bd

        self.clp = serv.clp

        self.cfg = cfg
        self.aguardando_reservatorio: "int" = 0

        self.cp: "dict[str, cp.Comporta]" = {}
        self.cp["CP1"] = cp.Comporta(1, serv, self)
        self.cp["CP2"] = cp.Comporta(2, serv, self)

        self.cp["CP1"].comporta_adjacente = self.cp["CP2"]
        self.cp["CP2"].comporta_adjacente = self.cp["CP1"]

        self.nivel_montante = lei.LeituraModbusFloat(
            self.clp['TDA'],
            REG_CLP["TDA"]["NV_MONTANTE"],
            wordorder=False,
            descricao="[TDA] Leitura Nível Montante"
        )
        self.perda_grade_1 = lei.LeituraModbusFloat(
            self.clp["TDA"],
            REG_CLP["TDA"]["NV_JUSANTE_GRADE_CP1"],
            descricao="[TDA] Leitura Perda Grade CP1"
        )
        self.perda_grade_2 = lei.LeituraModbusFloat(
            self.clp["TDA"],
            REG_CLP["TDA"]["NV_JUSANTE_GRADE_CP2"],
            descricao="[TDA] Leitura Perda Grade CP2"
        )

        self.status_valvula_borboleta = lei.LeituraModbusBit(
            self.clp["TDA"],
            REG_CLP["TDA"]["VB_FECHANDO"],
            descricao="[TDA] Status Válvula Borboleta",
        )
        self.status_unidade_hidraulica = lei.LeituraModbusBit(
            self.clp["TDA"],
            REG_CLP["TDA"]["UH_DISPONIVEL"],
            descricao="[TDA] Status Unidade Hidáulica",
        )
        self.status_limpa_grades = lei.LeituraModbusBit(
            self.clp["TDA"],
            REG_CLP["TDA"]["LG_OPE_MANUAL"],
            descricao="[TDA] Limpa Grades Manual",
        )

        self._modo_lg: "int" = 1

        self.ema_anterior: "int" = -1

        self.erro_nivel: "float" = 0
        self.erro_nivel_anterior: "float" = 0
        self.nivel_montante_anterior: "float" = 0

        self.condicionadores: "list[c.CondicionadorBase]" = []
        self.condicionadores_essenciais: "list[c.CondicionadorBase]" = []

        # FINALIZAÇÃO __INIT__

        self.iniciar_ultimo_estado_lg()


    def resetar_emergencia(self) -> "bool":
        """
        Função para acionar comandos de reset de TRIPS/Alarmes
        """

        try:
            res = esc.EscritaModBusBit.escrever_bit(self.clp["TDA"], REG_CLP["TDA"]["VB_CMD_RST_FLH"], valor=1)
            return res

        except Exception:
            logger.error("[TDA] Houve um erro ao realizar o Reset de Emergência.")
            logger.debug(f"[TDA] Traceback: {traceback.format_exc()}")
            return False


    def calcular_ema_montante(self, ema_anterior, periodo=40, smoothing=5, casas_decimais=5) -> "float":
        """
        Função com filtro EMA de leitura de nível montante, para evitar variações muito
        agressivas de controle de potência.
        """

        constante = smoothing / (1 + periodo)
        ema = self.nivel_montante.valor * constante + ema_anterior * (1 - constante)
        ema = np.round(ema, casas_decimais)

        return ema


    def atualizar_montante(self) -> "None":
        """
        Função para atualizar valores anteriores de nível montante e erro de cálculo para
        cálculos futuros de ajuste de potência.
        """


        if self.ema_anterior == -1 and self.nivel_montante.valor != None:
            self.ema_anterior = 0
            self.nivel_montante_anterior = self.nivel_montante.valor
        else:
            ema = self.calcular_ema_montante(self.nivel_montante_anterior)
            self.nivel_montante_anterior = ema

        self.erro_nivel_anterior = self.erro_nivel
        self.erro_nivel = self.nivel_montante_anterior - self.cfg["nv_alvo"]


    def iniciar_ultimo_estado_lg(self) -> "None":
        """
        Função para extrair do banco de dados o último estado registrado do Limpa Grades
        """

        self._modo_lg = self.bd.get_ultimo_estado_lg()[0]


    def forcar_estado_disponivel_lg(self) -> "None":
        """
        Função para forçar o estado disponível no Limpa Grades.
        """

        self._modo_lg = LG_DISPONIVEL
        self.bd.update_estado_lg(LG_DISPONIVEL)


    def forcar_estado_indisponivel_lg(self) -> "None":
        """
        Função para forçar o estado indisponível no Limpa Grades.
        """

        self._modo_lg = LG_INDISPONIVEL
        self.bd.update_estado_lg(LG_INDISPONIVEL)


    def operar_limpa_grades(self) -> "None":
        """
        Função para operar o Limpa Grades.

        Verifica se o Limpa Grades está em modo Manual ou Indisponível e caso esteja,
        avisa o operador e segue com a operação normal.
        Se o Limpa Grades estiver Disponível, extrai o dado com período de acionamento
        do Banco, para comparar com o horário atual. Se a comparação dos horários estiver
        dentro da faixa, inicia a operação.
        """

        perda = self.bd.get_disparo_perda_lg()
        perda_1 = perda[0]
        perda_2 = perda[1]

        horario = self.bd.get_horario_operar_lg()
        agora = datetime.now(pytz.timezone("Brazil/East")).replace(tzinfo=None)

        if perda_1 >= self.perda_grade_1.valor or perda_2 >= self.perda_grade_2.valor:
            logger.debug("")
            logger.debug(f"[TDA] Atenção! Foi identificado um valor de perda nas grades para disparo de Limpeza!")

        elif agora <= horario[0] <= agora + timedelta(minutes=5):
            logger.debug("")
            logger.debug(f"[TDA] Atenção! Enviando comando de Limpeza de Grades por período pré definido!")

            prox_horario = agora + timedelta(days=horario[1], hours=horario[2])
            self.bd.update_horario_operar_lg([prox_horario.strftime('%Y-%m-%d %H:%M:%S')])

        elif agora + timedelta(minutes=6) > horario[0]:
            logger.debug("")
            logger.debug(f"[TDA] Atenção! Foi identificado que o horário para a limpeza de grades passou do período estipulado.")
            logger.debug(f"[TDA] Reagendando limpeza para o próximo horário...")

            prox_horario = agora + timedelta(days=horario[1], hours=horario[2])
            self.bd.update_horario_operar_lg([prox_horario.strftime('%Y-%m-%d %H:%M:%S')])
            return

        else:
            return

        if self.verificar_condicoes_lg() and self._modo_lg == LG_DISPONIVEL:
            logger.debug(f"[LG]           Enviando comando:          \"OPERAR LIMPA GRADES\"")
            esc.EscritaModBusBit.escrever_bit(self.clp["TDA"], REG_CLP["TDA"]["LG_CMD_RST_FLH"], valor=1)
            esc.EscritaModBusBit.escrever_bit(self.clp["TDA"], REG_CLP["TDA"]["LG_CMD_LIMPEZA"], valor=1)
            return


    def verificar_condicoes_lg(self) -> "bool":
        """
        Função para verificar as pré-condições de operação do Limpa Grades.
        """

        flags = 0

        try:
            if self.l_lg_manual.valor:
                logger.debug("[LG]  Não é possível operar o Limpa Grades em modo \"MANUAL\"")
                flags += 1

            elif self._modo_lg == LG_INDISPONIVEL:
                logger.debug("[LG]  Não é possível operar o Limpa Grades no estado \"INDISPONÍVEL\"")
                flags += 1

            elif not self.l_lg_parado.valor:
                logger.debug("[LG]  O Limpa Grades já está em operação.")
                flags += 1

            elif not self.l_lg_permissao.valor:
                logger.debug("[LG]  Sem Permissão para operar o Limpa Grades.")
                flags += 1


            logger.warning(f"[LG]  Foram identificadas \"{flags}\" condições de bloqueio para operação do Limpa Grades. Favor normalizar.") \
                if flags > 0 else logger.debug("[LG]  Condições de operação validadas.")

            return False if flags > 0 else True

        except Exception:
            logger.exception(f"[LG]  Houve um erro ao verificar as pré-condições do Limpa Grades.")
            logger.debug(f"[LG]  Traceback: {traceback.format_exc()}")
            return False


    def verificar_condicionadores(self) -> "list[c.CondicionadorBase]":
        """
        Função para verificação de TRIPS/Alarmes.

        Verifica os condicionadores ativos e retorna lista com os mesmos para a função de verificação
        da Classe da Usina determinar as ações necessárias.
        """

        autor = 0

        leituras = self.clp["TDA"].read_holding_registers(0, 55)

        if True in (condic.status(leituras) for condic in self.condicionadores_essenciais):
            condics_ativos = [condic for condics in [self.condicionadores_essenciais, self.condicionadores] for condic in condics if condic.ativo]

            logger.debug("")
            if self.condicionadores_ativos == []:
                logger.debug(f"[TDA] Foram detectados Condicionadores ativos na Tomada da Água!")
            else:
                logger.debug(f"[TDA] Ainda há Condicionadores ativos na Tomada da Água!")

            for condic in condics_ativos:
                if condic.teste:
                    logger.debug(f"[TDA] Descrição: \"{condic.descricao}\", Gravidade: \"{CONDIC_STR_DCT[condic.gravidade] if condic.gravidade in CONDIC_STR_DCT else 'Desconhecida'}\", Obs.: \"TESTE\"")
                    continue

                elif condic in self.condicionadores_ativos:
                    logger.debug(f"[TDA] Descrição: \"{condic.descricao}\", Gravidade: \"{CONDIC_STR_DCT[condic.gravidade] if condic.gravidade in CONDIC_STR_DCT else 'Desconhecida'}\"")
                    continue

                else:
                    logger.warning(f"[TDA] Descrição: \"{condic.descricao}\", Gravidade: \"{CONDIC_STR_DCT[condic.gravidade] if condic.gravidade in CONDIC_STR_DCT else 'Desconhecida'}\"")
                    self.condicionadores_ativos.append(condic)
                    self.bd.update_alarmes([
                        datetime.now(pytz.timezone("Brazil/East")).replace(tzinfo=None),
                        condic.gravidade,
                        condic.descricao,
                        "X" if autor == 0 else ""
                    ])
                    sleep(1)
                    autor += 1

            logger.debug("")
            return condics_ativos

        else:
            self.condicionadores_ativos = []
            return []


    def verificar_leituras(self) -> "None":
        """
        Função para verificação de leituras por acionamento temporizado.

        Verifica leituras específcas para acionamento da manuteção. As leituras são disparadas
        em períodos separados por um tempo pré-definido.
        """

        leituras = self.clp["TDA"].read_holding_registers(0, 55)

        if not self.l_filtro_limpo_uh.ler(leituras):
            logger.warning("[TDA] O filtro da UH da TDA está sujo. Favor realizar limpeza/troca.")

        if self.l_nv_jusante_cp1.ler(leituras):
            logger.warning("[TDA] Houve uma falha no sensor de nível jusante da comporta 1. Favor verificar.")

        if self.l_nv_jusante_cp2.ler(leituras):
            logger.warning("[TDA] Houve uma falha no sensor de nível jusante da comporta 2. Favor verificar.")

        if not self.l_ca_tensao.ler(leituras):
            logger.warning("[TDA] Foi dentificado que o CA da tomada da água está sem tensão. Favor verificar.")

        if self.l_lg_manual.ler(leituras):
            logger.warning("[TDA] Foi identificado que o Limpa Grades entrou em operação manual. Favor verificar.")

        if self.l_nv_jusante_grade_cp1.ler(leituras):
            logger.warning("[TDA] Houve uma falha no sensor de nível jusante grade da comporta 1. Favor verificar.")

        if self.l_nv_jusante_grade_cp2.ler(leituras):
            logger.warning("[TDA] Houve uma falha no sensor de nível jusante grade da comporta 2. Favor verificar.")

        if self.l_falha_atuada_lg.ler(leituras) and not d.voip["LG_FALHA_ATUADA"][0]:
            logger.warning("[TDA] Foi identificado que o limpa grades está em falha. Favor verificar.")
            d.voip["LG_FALHA_ATUADA"][0] = True
        elif not self.l_falha_atuada_lg.ler(leituras) and d.voip["LG_FALHA_ATUADA"][0]:
            d.voip["LG_FALHA_ATUADA"][0] = False

        if self.l_falha_ler_nv_montante.ler(leituras) and not d.voip["FALHA_NIVEL_MONTANTE"][0]:
            logger.warning("[TDA] Houve uma falha na leitura de nível montante. Favor verificar.")
            d.voip["FALHA_NIVEL_MONTANTE"][0] = True
        elif not self.l_falha_ler_nv_montante.ler(leituras) and d.voip["FALHA_NIVEL_MONTANTE"][0]:
            d.voip["FALHA_NIVEL_MONTANTE"][0] = False


    def carregar_leituras(self) -> "None":
        """
        Função para carregamento de leituras necessárias para a operação.
        """

        # CONDICIONADORES ESSENCIAIS
        self.l_sem_emergencia = lei.LeituraModbusBit(self.clp["TDA"], REG_CLP["TDA"]["BOTAO_EMERGENCIA_ACIONADO"], descricao="[TDA] Emergência")
        self.condicionadores_essenciais.append(c.CondicionadorBase(self.l_sem_emergencia, CONDIC_NORMALIZAR))


        # CONDICIONADORES
        self.l_ca_tensao = lei.LeituraModbusBit(self.clp["TDA"], REG_CLP["TDA"]["SUBTENSAO_CA"], invertido=True, descricao="[TDA] Tensão CA Status ")
        self.condicionadores.append(c.CondicionadorBase(self.l_ca_tensao, CONDIC_NORMALIZAR))

        self.l_falha_ligar_bomba_uh = lei.LeituraModbusBit(self.clp["TDA"], REG_CLP["TDA"]["UNIDADE_HIDRAULICA_FALHA_LIGAR_BOMBA"], descricao="[TDA] UHTDA Falha Ligar Bomba")
        self.condicionadores.append(c.CondicionadorBase(self.l_falha_ligar_bomba_uh, CONDIC_NORMALIZAR))


        self.l_filtro_limpo_uh = lei.LeituraModbusBit(self.clp["TDA"], REG_CLP["TDA"]["UNIDADE_HIDRAULICA_FILTRO_SUJO"], invertido=True, descricao="[TDA] UHTDA Filtro Sujo")
        self.l_falha_ler_nv_montante = lei.LeituraModbusBit(self.clp["TDA"], REG_CLP["TDA"]["FALHA_LEITURA_NIVEL_MONTANTE"], descricao="[TDA] Nível Montante Falha")
        self.l_nv_jusante_cp1 = lei.LeituraModbusBit(self.clp["TDA"], REG_CLP["TDA"]["FALHA_LEITURA_NIVEL_JUSANTE_COMPORTA_1"], descricao="[TDA] Falha Leitura Nível Justante Comporta 1")
        self.l_nv_jusante_cp2 = lei.LeituraModbusBit(self.clp["TDA"], REG_CLP["TDA"]["FALHA_LEITURA_NIVEL_JUSANTE_COMPORTA_2"], descricao="[TDA] Falha Leitura Nível Justante Comporta 2")
        self.l_nv_jusante_grade_cp1 = lei.LeituraModbusBit(self.clp["TDA"], REG_CLP["TDA"]["FALHA_LEITURA_NIVEL_JUSANTE_GRADE_COMPORTA_1"], descricao="[TDA] Nível Leitura Justante Grade Comporta 1 Falha")
        self.l_nv_jusante_grade_cp2 = lei.LeituraModbusBit(self.clp["TDA"], REG_CLP["TDA"]["FALHA_LEITURA_NIVEL_JUSANTE_GRADE_COMPORTA_2"], descricao="[TDA] Nível Leitura Justante Grade Comporta 2 Falha")

        self.l_lg_permissao = lei.LeituraModbusBit(self.clp["TDA"], REG_CLP["TDA"]["LIMPA_GRADES_PERMISSIVOS_OK"], descricao="[TDA] Limpa Grades Permissivos")
        self.l_lg_parado = lei.LeituraModbusBit(self.clp["TDA"], REG_CLP["TDA"]["LIMPA_GRADES_PERMISSIVO_03_ESTADO_DO_LIMPA_GRADES_EM_POSICAO_INICIAL"], descricao="[TDA] Limpa Grades Parado")
        self.l_falha_atuada_lg = lei.LeituraModbusBit(self.clp["TDA"], REG_CLP["TDA"]["LIMPA_GRADES_PERMISSIVO_00_SEM_FALHA_ATUADA"], descricao="[TDA] Limpa Grades Falha")
        self.l_lg_manual = lei.LeituraModbusBit(self.clp["TDA"], REG_CLP["TDA"]["LIMPA_GRADES_OPERACAO_MANUAL"], descricao="[TDA] Limpa Grades Operação Manual")
        # LEITURA PERIÓDICA