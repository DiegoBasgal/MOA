__version__ = "0.1"
__author__ = "Diego Basgal", "Henrique Pfeifer"
__credits__ = ["Lucas Lavratti", ...]
__description__ = "Este módulo corresponde a implementação da operação da Tomada da Água."

import pytz
import logging
import traceback

import src.comporta as cp
import src.conectores.servidores as srv
import src.conectores.banco_dados as bd
import src.funcoes.condicionadores as c

from datetime import datetime, timedelta

from src.dicionarios.const import *
from src.funcoes.leitura import *
from src.funcoes.escrita import EscritaModBusBit as EMB


logger = logging.getLogger("logger")


class TomadaAgua:

    # ATRIBUIÇÃO DE VARIÁVEIS
    cfg = None
    bd: "bd.BancoDados" = None
    clp = srv.Servidores.clp

    cps: "dict[str, cp.Comporta]" = {}
    cps["CP1"] = cp.Comporta(1)
    cps["CP2"] = cp.Comporta(2)

    cps["CP1"].comporta_adjacente = cps["CP2"]
    cps["CP2"].comporta_adjacente = cps["CP1"]

    aguardando_reservatorio: "int" = 0

    nivel_montante = LeituraModbus( # LeituraModbusFloat(
        clp['TDA'],
        REG_CLP["TDA"]["NV_MONTANTE"],
        escala=0.01,
        fundo_escala=400,
        descricao="[TDA] Leitura Nível Montante"
    )
    perda_grade_1 = LeituraModbus( # LeituraModbusFloat(
        clp["TDA"],
        REG_CLP["TDA"]["NV_JUSANTE_GRADE_CP1"],
        descricao="[TDA] Leitura Perda Grade CP1"
    )
    perda_grade_2 = LeituraModbus( # LeituraModbusFloat(
        clp["TDA"],
        REG_CLP["TDA"]["NV_JUSANTE_GRADE_CP2"],
        descricao="[TDA] Leitura Perda Grade CP2"
    )

    status_valvula_borboleta = LeituraModbusBit(
        clp["TDA"],
        REG_CLP["TDA"]["VB_FECHANDO"],
        descricao="[TDA] Status Válvula Borboleta",
    )
    status_unidade_hidraulica = LeituraModbusBit(
        clp["TDA"],
        REG_CLP["TDA"]["UH_DISPONIVEL"],
        descricao="[TDA] Status Unidade Hidáulica",
    )
    status_limpa_grades = LeituraModbusBit(
        clp["TDA"],
        REG_CLP["TDA"]["LG_OPE_MANUAL"],
        descricao="[TDA] Limpa Grades Manual",
    )

    modo_lg: "int" = 1

    erro_nivel: "float" = 0
    erro_nivel_anterior: "float" = 0
    nivel_montante_anterior: "float" = 0

    condicionadores: "list[c.CondicionadorBase]" = []
    condicionadores_essenciais: "list[c.CondicionadorBase]" = []
    condicionadores_ativos: "list[c.CondicionadorBase]" = []

    # FINALIZAÇÃO __INIT__
    # cls.iniciar_ultimo_estado_lg()


    @classmethod
    def resetar_emergencia(cls) -> "bool":
        """
        Função para acionar comandos de reset de TRIPS/Alarmes
        """

        try:
            # res = EMB.escrever_bit(cls.clp["TDA"], REG_CLP["TDA"]["VB_CMD_RST_FLH"], valor=1)
            # return res
            return True

        except Exception:
            logger.error("[TDA] Houve um erro ao realizar o Reset de Emergência.")
            logger.debug(traceback.format_exc())
            return False


    @classmethod
    def atualizar_montante(cls) -> "None":
        """
        Função para atualizar valores anteriores de nível montante e erro de cálculo para
        cálculos futuros de ajuste de potência.
        """

        cls.nivel_montante_anterior = cls.nivel_montante.valor
        cls.erro_nivel_anterior = cls.erro_nivel
        cls.erro_nivel = cls.nivel_montante_anterior - cls.cfg["nv_alvo"]


    @classmethod
    def iniciar_ultimo_estado_lg(cls) -> "None":
        """
        Função para extrair do banco de dados o último estado registrado do Limpa Grades
        """

        cls._modo_lg = cls.bd.get_ultimo_estado_lg()[0]


    @classmethod
    def forcar_estado_disponivel_lg(cls) -> "None":
        """
        Função para forçar o estado disponível no Limpa Grades.
        """

        cls._modo_lg = LG_DISPONIVEL
        cls.bd.update_estado_lg(LG_DISPONIVEL)


    @classmethod
    def forcar_estado_indisponivel_lg(cls) -> "None":
        """
        Função para forçar o estado indisponível no Limpa Grades.
        """

        cls._modo_lg = LG_INDISPONIVEL
        cls.bd.update_estado_lg(LG_INDISPONIVEL)


    @classmethod
    def operar_limpa_grades(cls) -> "None":
        """
        Função para operar o Limpa Grades.

        Verifica se o Limpa Grades está em modo Manual ou Indisponível e caso esteja,
        avisa o operador e segue com a operação normal.
        Se o Limpa Grades estiver Disponível, extrai o dado com período de acionamento
        do Banco, para comparar com o horário atual. Se a comparação dos horários estiver
        dentro da faixa, inicia a operação.
        """

        perda = cls.bd.get_disparo_perda_lg()
        perda_1 = perda[0]
        perda_2 = perda[1]

        horario = cls.bd.get_horario_operar_lg()
        agora = datetime.now(pytz.timezone("Brazil/East")).replace(tzinfo=None)

        if perda_1 >= cls.perda_grade_1.valor or perda_2 >= cls.perda_grade_2.valor:
            logger.debug("")
            logger.debug(f"[TDA] Atenção! Foi identificado um valor de perda nas grades para disparo de Limpeza!")

        elif agora <= horario[0] <= agora + timedelta(minutes=5):
            logger.debug("")
            logger.debug(f"[TDA] Atenção! Enviando comando de Limpeza de Grades por período pré definido!")

            prox_horario = agora + timedelta(days=horario[1], hours=horario[2])
            cls.bd.update_horario_operar_lg([prox_horario.strftime('%Y-%m-%d %H:%M:%S')])

        elif agora + timedelta(minutes=6) > horario[0]:
            logger.debug("")
            logger.debug(f"[TDA] Atenção! Foi identificado que o horário para a limpeza de grades passou do período estipulado.")
            logger.debug(f"[TDA] Reagendando limpeza para o próximo horário...")

            prox_horario = agora + timedelta(days=horario[1], hours=horario[2])
            cls.bd.update_horario_operar_lg([prox_horario.strftime('%Y-%m-%d %H:%M:%S')])
            return

        else:
            return

        if cls.verificar_condicoes_lg() and cls._modo_lg == LG_DISPONIVEL:
            logger.debug(f"[LG]           Enviando comando:          \"OPERAR LIMPA GRADES\"")
            # ESC.escrever_bit(cls.clp["TDA"], REG_CLP["TDA"]["LG_CMD_RST_FLH"], valor=1)
            # ESC.escrever_bit(cls.clp["TDA"], REG_CLP["TDA"]["LG_CMD_LIMPEZA"], valor=1)
            return


    @classmethod
    def verificar_condicoes_lg(cls) -> "bool":
        """
        Função para verificar as pré-condições de operação do Limpa Grades.
        """

        flags = 0

        try:
            if cls.l_lg_manual.valor:
                logger.debug("[LG]  Não é possível operar o Limpa Grades em modo \"MANUAL\"")
                flags += 1

            elif cls._modo_lg == LG_INDISPONIVEL:
                logger.debug("[LG]  Não é possível operar o Limpa Grades no estado \"INDISPONÍVEL\"")
                flags += 1

            elif not cls.l_lg_parado.valor:
                logger.debug("[LG]  O Limpa Grades já está em operação.")
                flags += 1

            elif not cls.l_lg_permissao.valor:
                logger.debug("[LG]  Sem Permissão para operar o Limpa Grades.")
                flags += 1


            logger.warning(f"[LG]  Foram identificadas \"{flags}\" condições de bloqueio para operação do Limpa Grades. Favor normalizar.") \
                if flags > 0 else logger.debug("[LG]  Condições de operação validadas.")

            return False if flags > 0 else True

        except Exception:
            logger.exception(f"[LG]  Houve um erro ao verificar as pré-condições do Limpa Grades.")
            logger.debug(f"[LG]  Traceback: {traceback.format_exc()}")
            return False


    @classmethod
    def verificar_condicionadores(cls) -> "list[c.CondicionadorBase]":
        """
        Função para verificação de TRIPS/Alarmes.

        Verifica os condicionadores ativos e retorna lista com os mesmos para a função de verificação
        da Classe da Usina determinar as ações necessárias.
        """

        autor = 0

        leituras = cls.clp["TDA"].read_holding_registers(0, 55)

        if True in (condic.status(leituras) for condic in cls.condicionadores_essenciais):
            condics_ativos = [condic for condics in [cls.condicionadores_essenciais, cls.condicionadores] for condic in condics if condic.ativo]

            logger.debug("")
            if cls.condicionadores_ativos == []:
                logger.debug(f"[TDA] Foram detectados Condicionadores ativos na Tomada da Água!")
            else:
                logger.debug(f"[TDA] Ainda há Condicionadores ativos na Tomada da Água!")

            for condic in condics_ativos:
                if condic.teste:
                    logger.debug(f"[TDA] Descrição: \"{condic.descricao}\", Gravidade: \"{CONDIC_STR_DCT[condic.gravidade] if condic.gravidade in CONDIC_STR_DCT else 'Desconhecida'}\", Obs.: \"TESTE\"")
                    continue

                elif condic in cls.condicionadores_ativos:
                    logger.debug(f"[TDA] Descrição: \"{condic.descricao}\", Gravidade: \"{CONDIC_STR_DCT[condic.gravidade] if condic.gravidade in CONDIC_STR_DCT else 'Desconhecida'}\"")
                    continue

                else:
                    logger.warning(f"[TDA] Descrição: \"{condic.descricao}\", Gravidade: \"{CONDIC_STR_DCT[condic.gravidade] if condic.gravidade in CONDIC_STR_DCT else 'Desconhecida'}\"")
                    cls.condicionadores_ativos.append(condic)
                    cls.bd.update_alarmes([
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
            cls.condicionadores_ativos = []
            return []


    @classmethod
    def verificar_leituras(cls) -> "None":
        """
        Função para verificação de leituras por acionamento temporizado.

        Verifica leituras específcas para acionamento da manuteção. As leituras são disparadas
        em períodos separados por um tempo pré-definido.
        """
        return


    @classmethod
    def carregar_leituras(cls) -> "None":
        """
        Função para carregamento de leituras necessárias para a operação.
        """
        return