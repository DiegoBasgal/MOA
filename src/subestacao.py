__version__ = "0.1"
__author__ = "Diego Basgal", "Henrique Pfeifer"
__credits__ = ["Lucas Lavratti", ...]
__description__ = "Este módulo corresponde a implementação da operação da Subestação."

import pytz
import logging
import traceback

import src.bay as bay
import src.dicionarios.dict as dct
import src.funcoes.condicionadores as c

from datetime import datetime

from src.funcoes.leitura import *
from src.dicionarios.const import *

from src.conectores.servidores import Servidores
from src.conectores.banco_dados import BancoDados
from src.funcoes.escrita import EscritaModBusBit as EMB


logger = logging.getLogger("logger")


class Subestacao:
    def __init__(self, serv: "Servidores"=None, bd: "BancoDados"=None) -> "None":

        # ATRIBUIÇÃO DE VARIÁVEIS

        self.__bd = bd

        self.clp = serv.clp
        self.rele = serv.rele

        self.tensao_vs = LeituraModbus(
            self.clp["SA"],
            REG_CLP["SE"]["LT_VAB"],
        )
        self.tensao_vab = LeituraModbusFloat(
            self.clp["SA"],
            REG_CLP["SE"]["LT_VAB"],
            escala=1000,
            descricao="[SE]  Leitura Tensão VAB"
        )
        self.tensao_vbc = LeituraModbusFloat(
            self.clp["SA"],
            REG_CLP["SE"]["LT_VBC"],
            escala=1000,
            descricao="[SE]  Leitura Tensão VBC"
        )
        self.tensao_vca = LeituraModbusFloat(
            self.clp["SA"],
            REG_CLP["SE"]["LT_VCA"],
            escala=1000,
            descricao="[SE]  Leitura Tensão VCA"
        )
        self.dj_linha_se = LeituraModbusBit(
            self.rele["SE"],
            REG_RELE["SE"]["DJL_FECHADO"],
            descricao="[SE][RELE] Disjuntor Linha Status"
        )
        self.dj_linha_bay = LeituraModbusBit(
            self.rele["BAY"],
            REG_RELE["BAY"]["DJL_FECHADO"],
            descricao="[BAY][RELE] Disjuntor Bay Status"
        )

        self.dj_bay_aberto: "bool" = False

        self.condicionadores: "list[c.CondicionadorBase]" = []
        self.condicionadores_essenciais: "list[c.CondicionadorBase]" = []
        self.condicionadores_ativos: "list[c.CondicionadorBase]" = []


    def resetar_emergencia(self) -> "bool":
        """
        Função para acionar comandos de reset de TRIPS/Alarmes
        """

        try:
            res = EMB.escrever_bit(self.clp["SA"], REG_CLP["SE"]["BLQ_GERAL_CMD_REARME"], valor=1)
            res = EMB.escrever_bit(self.clp["SA"], REG_CLP["SE"]["86T_CMD_REARME"], valor=1)
            res = EMB.escrever_bit(self.clp["SA"], REG_CLP["SE"]["86BF_CMD_REARME"], valor=1)
            res = EMB.escrever_bit(self.clp["SA"], REG_CLP["SE"]["REGISTROS_CMD_RST"], valor=1)
            return res

        except Exception:
            logger.exception(f"[SE]  Houve um erro ao realizar o Reset de Emergência.")
            logger.debug(f"[SE]  Traceback: {traceback.format_exc()}")
            return False


    def fechar_dj_linha(self) -> "int":
        """
        Função para acionamento do comando de fechamento do Disjuntor de Linha.

        Verifica se o Disjuntor de Linha está fechado e caso não estja, chama a função de verificação
        de condições de fechamento do Disjuntor. Caso retorne que o Disjuntor do BAY está aberto, sinaliza
        para a função de normalização da usina, que há a necessidade de realizar o fchamento do Disjuntor
        do BAY. Caso a verificação retorne que há uma falha com as condições, sinaliza que houve uma falha
        e impede o fechamento do Disjuntor. Caso o Disjuntor já esteja fechado, avisa o operador e retorna
        o sinal de fechamento OK.
        """

        try:
            if not self.dj_linha_se.valor:
                logger.info("[SE]  O Disjuntor da Subestação está aberto!")
                if self.verificar_dj_linha():
                    logger.debug(f"[SE]  Enviando comando:                   \"FECHAR DISJUNTOR\"")
                    logger.debug("")
                    EMB.escrever_bit(self.clp["SA"], REG_CLP["SE"]["DJL_CMD_FECHAR"],  valor=1)
                    return True

                else:
                    logger.warning("[SE]  Não foi possível realizar o fechamento do Disjuntor.")
                    logger.debug("")
                    return False

            else:
                return True

        except Exception:
            logger.exception(f"[SE]  Houve um erro ao realizar o fechamento do Disjuntor de Linha.")
            logger.debug(f"[SE]  Traceback: {traceback.format_exc()}")
            return False


    def verificar_dj_linha(self) -> "bool":
        """
        Função para verificação de condições de fechamento do Disjuntor de Linha.

        Verifica as seguintes condições:
        - Se o Disjuntor do BAY está aberto;
        - Se há algum sinal de trip no Relé do Tranformador Elevador;
        - Se há qualquer leitura de corrente na barra do BAY (Barra Morta = False & Barra Viva = True);
        - Se a Seccionadora do BAY está fechada;
        - Se há algum sinal do alarme no Relé de Buchholz do Transformador Elevador;
        - Se a mola do Disjuntor está carregada;
        - Se o Disjuntor está em modo Remoto.
        Caso qualquer das condições acima retornar diferente do esperado, avisa o operador e impede o
        comando de fechamento do Disjuntor.
        """

        flags = 0
        logger.debug("[SE]  Verificando Condições do Disjuntor SE...")

        try:
            if self.secc_fechada.valor:
                logger.warning("[SE]  A Seccionadora está Aberta!")
                flags += 1

            if not self.l_djL_remoto.valor:
                logger.warning("[SE]  O Disjuntor não está em modo remoto!")
                flags += 1

            if not self.dj_linha_bay.valor:
                logger.warning("[SE]  O Disjuntor do Bay está aberto!")
                self.dj_bay_aberto = True
                flags += 1

            if self.l_barra_viva.valor:
                logger.warning("[SE]  Foi identificada leitura de Tensão na barra do Bay!")
                flags += 1

            if self.l_trip_rele_te.valor:
                logger.warning("[SE]  O sinal de trip do relé do transformador elevador está ativado!")
                flags += 1

            if self.l_alarme_gas_te.valor:
                logger.warning("[SE]  Foi identificado sinal de alarme no Relé de Buchholz do Transformador Elevador!")
                flags += 1

            if not self.l_mola_carregada.valor:
                logger.warning("[SE]  A mola do Disjuntor não está carregada!")
                flags += 1

            logger.warning(f"[SE]  Foram identificadas \"{flags}\" condições de bloqueio ao realizar fechamento do Disjuntor. Favor normalizar.") \
                if flags > 0 else logger.debug("[SE]  Condições de Fechamento Validadas.")

            return False if flags > 0 else True

        except Exception:
            logger.exception(f"[SE]  Houve um erro ao verificar as pré-condições de fechameto do Dijuntor de Linha.")
            logger.debug(f"[SE]  Traceback: {traceback.format_exc()}")
            return False


    def verificar_tensao_trifasica(self) -> "bool":
        """
        Função para verificação de Tensão na linha da Subestação.
        """

        try:
            if (TENSAO_LINHA_BAIXA < self.tensao_vab.valor < TENSAO_LINHA_ALTA) \
                and (TENSAO_LINHA_BAIXA < self.tensao_vbc.valor < TENSAO_LINHA_ALTA) \
                and (TENSAO_LINHA_BAIXA < self.tensao_vca.valor < TENSAO_LINHA_ALTA):
                return True
            else:
                logger.warning("[SE]  Tensão da linha fora do limite.")
                return False

        except Exception:
            logger.exception(f"[SE]  Houve um erro ao realizar a verificação da tensão na linha.")
            logger.debug(f"[SE]  Traceback: {traceback.format_exc()}")
            return False


    def verificar_condicionadores(self) -> "list[c.CondicionadorBase]":
        """
        Função para verificação de TRIPS/Alarmes.

        Verifica os condicionadores ativos e retorna lista com os mesmos para a função de verificação
        da Classe da Usina determinar as ações necessárias.
        """

        if True in (condic.ativo for condic in self.condicionadores_essenciais):
            condics_ativos = [condic for condics in [self.condicionadores_essenciais, self.condicionadores] for condic in condics if condic.ativo]

            logger.debug("")
            if self.condicionadores_ativos == []:
                logger.debug(f"[SE]  Foram detectados Condicionadores ativos na Subestação!")

            else:
                logger.debug(f"[SE]  Ainda há Condicionadores ativos na Subestação!")

            for condic in condics_ativos:
                if condic.teste:
                    logger.debug(f"[SE]  Descrição: \"{condic.descricao}\", Gravidade: \"{CONDIC_STR_DCT[condic.gravidade] if condic.gravidade in CONDIC_STR_DCT else 'Desconhecida'}\", Obs.: \"TESTE\"")
                    continue

                elif condic in self.condicionadores_ativos:
                    logger.debug(f"[SE]  Descrição: \"{condic.descricao}\", Gravidade: \"{CONDIC_STR_DCT[condic.gravidade] if condic.gravidade in CONDIC_STR_DCT else 'Desconhecida'}\"")
                    continue

                else:
                    logger.warning(f"[SE]  Descrição: \"{condic.descricao}\", Gravidade: \"{CONDIC_STR_DCT[condic.gravidade] if condic.gravidade in CONDIC_STR_DCT else 'Desconhecida'}\"")
                    self.condicionadores_ativos.append(condic)
                    self.__bd.update_alarmes([
                        datetime.now(pytz.timezone("Brazil/East")).replace(tzinfo=None),
                        condic.gravidade,
                        condic.descricao
                    ])
                    sleep(1)

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

        if not self.l_seletora_52L_remoto.valor:
            logger.warning("[SE]  O Disjuntor 52L saiu do modo remoto. Favor verificar.")

        if self.l_falha_temp_oleo_te.valor:
            logger.warning("[SE]  Houve uma falha de leitura de temperatura do óleo do transformador elevador. Favor verificar.")

        if self.l_falha_ler_temp_enrola_te.valor:
            logger.warning("[SE]  Houve uma falha de leitura de temperatura do enrolamento do transformador elevador. Favor verificar.")

        if self.l_alarme_temp_oleo_te.valor and not dct.voip["TE_ALM_TEMPERATURA_OLEO"][0]:
            logger.warning("[SE]  A temperatura do óleo do transformador elevador está alta. Favor verificar.")
            dct.voip["TE_ALM_TEMPERATURA_OLEO"][0] = True
        elif not self.l_alarme_temp_oleo_te.valor and dct.voip["TE_ALM_TEMPERATURA_OLEO"][0]:
            dct.voip["TE_ALM_TEMPERATURA_OLEO"][0] = False

        if self.l_nv_muito_baixo_oleo_te.valor and not dct.voip["TE_NIVEL_OLEO_MUITO_BAIXO"][0]:
            logger.warning("[SE]  O nível de óleo do tranformador elevador está muito baixo. Favor verificar.")
            dct.voip["TE_NIVEL_OLEO_MUITO_BAIXO"][0] = True
        elif not self.l_nv_muito_baixo_oleo_te.valor and dct.voip["TE_NIVEL_OLEO_MUITO_BAIXO"][0]:
            dct.voip["TE_NIVEL_OLEO_MUITO_BAIXO"][0] = False

        if self.l_alarme_temp_oleo_te.valor and not dct.voip["TE_ALARME_TEMPERATURA_OLEO"][0]:
            logger.warning("[SE]  A temperatura do óleo do transformador elevador está alta. Favor verificar.")
            dct.voip["TE_ALARME_TEMPERATURA_OLEO"][0] = True
        elif not self.l_alarme_temp_oleo_te.valor and dct.voip["TE_ALARME_TEMPERATURA_OLEO"][0]:
            dct.voip["TE_ALARME_TEMPERATURA_OLEO"][0] = False

        if self.l_alarme_temp_enrola_te.valor and not dct.voip["TE_ALARME_TEMPERATURA_ENROLAMENTO"][0]:
            logger.warning("[SE]  A temperatura do enrolamento do transformador elevador está alta. Favor verificar.")
            dct.voip["TE_ALARME_TEMPERATURA_ENROLAMENTO"][0] = True
        elif not self.l_alarme_temp_enrola_te.valor and dct.voip["TE_ALARME_TEMPERATURA_ENROLAMENTO"][0]:
            dct.voip["TE_ALARME_TEMPERATURA_ENROLAMENTO"][0] = False


    def carregar_leituras(self) -> "None":
        """
        Função para carregamento de leituras necessárias para a operação.
        """

        # CONDIÇÕES DE FECHAMENTO Dj52L
        self.secc_fechada = LeituraModbusBit(self.rele["SE"], REG_RELE["SE"]["SECC_FECHADA"], invertido=True, descricao="[SE][RELE] Seccionadora Fechada")
        self.l_trip_rele_te = LeituraModbusBit(self.rele["TE"], REG_RELE["TE"]["RELE_ESTADO_TRP"], descricao="[TE][RELE] Transformador Elevador Trip")
        self.l_barra_viva = LeituraModbusBit(self.rele["SE"], REG_RELE["SE"]["ID_BARRA_VIVA"], descricao="[SE]  Identificação de Barra Viva")
        self.l_mola_carregada = LeituraModbusBit(self.rele["SE"], REG_RELE["SE"]["DJL_MOLA_CARREGADA"], descricao="[SE]  Disjuntor Linha Mola Carregada")
        self.l_djL_remoto = LeituraModbusBit(self.clp["SA"], REG_CLP["SE"]["DJL_SELETORA_REMOTO"], descricao="[SE]  Disjuntor Linha Seletora Modo Remoto")
        self.l_alarme_gas_te = LeituraModbusBit(self.rele["SE"], REG_CLP["SE"]["TE_RELE_BUCHHOLZ_ALM"], descricao="[SE]  Transformador Elevador Alarme Relé Buchholz")
        self.condicionadores.append(c.CondicionadorBase(self.l_alarme_gas_te, CONDIC_INDISPONIBILIZAR))


        # CONDICIONADORES ESSENCIAIS
        self.l_rele_linha_atuado = LeituraModbusBit(self.rele["SE"], REG_CLP["SE"]["RELE_LINHA_ATUADO"], descricao="[SE]  Relé Linha Atuado")
        self.condicionadores_essenciais.append(c.CondicionadorBase(self.l_rele_linha_atuado, gravidade=CONDIC_NORMALIZAR))


        # CONDICIONADORES
        self.l_89L_fechada = LeituraModbusBit(self.clp["SA"], REG_CLP["SE"]["89L_FECHADA"], invertido=True, descricao="[SE]  89L Fechada")
        self.condicionadores.append(c.CondicionadorBase(self.l_89L_fechada, CONDIC_INDISPONIBILIZAR))

        self.l_86T_atuado = LeituraModbusBit(self.clp["SA"], REG_CLP["SE"]["86T_ATUADO"], invertido=True, descricao="[SE]  86T Atuado")
        self.condicionadores.append(c.CondicionadorBase(self.l_86T_atuado, CONDIC_INDISPONIBILIZAR))

        self.l_86BF_atuado = LeituraModbusBit(self.clp["SA"], REG_CLP["SE"]["86BF_ATUADO"], descricao="[SE]  86BF Atuado")
        self.condicionadores.append(c.CondicionadorBase(self.l_86BF_atuado, CONDIC_INDISPONIBILIZAR))

        self.l_trip_rele_buchholz = LeituraModbusBit(self.clp["SA"], REG_CLP["SE"]["TE_RELE_BUCHHOLZ_TRP"], descricao="[SE]  Transformador Elevador Trip Relé Buchholz")
        self.condicionadores.append(c.CondicionadorBase(self.l_trip_rele_buchholz, CONDIC_INDISPONIBILIZAR))

        self.l_trip_alivio_pressao = LeituraModbusBit(self.clp["SA"], REG_CLP["SE"]["TE_TRP_ALIVIO_PRESSAO"], descricao="[SE]  Transformador Elevador Trip Alívio Pressão")
        self.condicionadores.append(c.CondicionadorBase(self.l_trip_alivio_pressao, CONDIC_INDISPONIBILIZAR))

        self.l_trip_temp_oleo_te = LeituraModbusBit(self.clp["SA"], REG_CLP["SE"]["TE_TRP_TMP_OLEO"], descricao="[SE]  Transformador Elevador Trip Temperatura Óleo")
        self.condicionadores.append(c.CondicionadorBase(self.l_trip_temp_oleo_te, CONDIC_INDISPONIBILIZAR))

        self.l_rele_linha_bf_atuado = LeituraModbusBit(self.clp["SA"], REG_CLP["SE"]["RELE_LINHA_ATUACAO_BF"], descricao="[SE]  Relé Linha Atuação BF")
        self.condicionadores.append(c.CondicionadorBase(self.l_rele_linha_bf_atuado, CONDIC_INDISPONIBILIZAR))

        self.l_trip_temp_enrola_te = LeituraModbusBit(self.clp["SA"], REG_CLP["SE"]["TE_TRP_TMP_ENROL"], descricao="[SE]  Transformador Elevador Trip Temperatura Enrolamento")
        self.condicionadores.append(c.CondicionadorBase(self.l_trip_temp_enrola_te, CONDIC_INDISPONIBILIZAR))

        self.l_falha_cmd_abertura_52L = LeituraModbusBit(self.clp["SA"], REG_CLP["SE"]["DJL_FLH_CMD_ABERTURA"], descricao="[SE]  Disjuntor Linha Falha Comando Abertura")
        self.condicionadores.append(c.CondicionadorBase(self.l_falha_cmd_abertura_52L, CONDIC_INDISPONIBILIZAR))

        self.l_falha_cmd_fechamento_52L = LeituraModbusBit(self.clp["SA"], REG_CLP["SE"]["DJL_FLH_CMD_FECHAMENTO"], descricao="[SE]  Disjuntor Linha Falha Comando Fechamento")
        self.condicionadores.append(c.CondicionadorBase(self.l_falha_cmd_fechamento_52L, CONDIC_INDISPONIBILIZAR))


        # CONDICIONADORES RELÉS
        self.l_rele_falha_receb_rele_te = LeituraModbusBit(self.rele["SE"], REG_RELE["SE"]["RELE_TE_FLH_PARTIDA"],  descricao="[SE][RELE] Falha Partida Recebida Relé Transformador Elevador")
        self.condicionadores_essenciais.append(c.CondicionadorBase(self.l_rele_falha_receb_rele_te, CONDIC_INDISPONIBILIZAR))

        self.l_rele_falha_abertura_djB1 = LeituraModbusBit(self.rele["SE"], REG_RELE["SE"]["DJL_FLH_ABERTURA_B1"],  descricao="[SE][RELE] Disjuntor Linha Falha Abertura - BIT 01")
        self.condicionadores_essenciais.append(c.CondicionadorBase(self.l_rele_falha_abertura_djB1, CONDIC_INDISPONIBILIZAR))

        self.l_rele_falha_abertura_djB3 = LeituraModbusBit(self.rele["SE"], REG_RELE["SE"]["DJL_FLH_ABERTURA_B3"],  descricao="[SE][RELE] Disjuntor Linha Falha Abertura - BIT 03")
        self.condicionadores_essenciais.append(c.CondicionadorBase(self.l_rele_falha_abertura_djB3, CONDIC_INDISPONIBILIZAR))

        self.l_rele_falha_abertura_dB4 = LeituraModbusBit(self.rele["SE"], REG_RELE["SE"]["DJL_FLH_ABERTURA_B4"],  descricao="[SE][RELE] Disjuntor Linha Falha Abertura - BIT 04")
        self.condicionadores_essenciais.append(c.CondicionadorBase(self.l_rele_falha_abertura_dB4, CONDIC_INDISPONIBILIZAR))

        self.l_rele_sobrecorr_inst_seq_neg_Z1 = LeituraModbusBit(self.rele["SE"], REG_RELE["SE"]["Z1_SOBRECO_INST_SEQU_NEG"],  descricao="[SE][RELE] Sobrecorrente Instantânea Sequência Negativa Z1")
        self.condicionadores_essenciais.append(c.CondicionadorBase(self.l_rele_sobrecorr_inst_seq_neg_Z1, CONDIC_INDISPONIBILIZAR))

        self.l_rele_sobrecorr_inst_seq_neg_Z2 = LeituraModbusBit(self.rele["SE"], REG_RELE["SE"]["Z2_SOBRECO_INST_SEQU_NEG"],  descricao="[SE][RELE] Sobrecorrente Instantânea Sequência Negativa Z2")
        self.condicionadores_essenciais.append(c.CondicionadorBase(self.l_rele_sobrecorr_inst_seq_neg_Z2, CONDIC_INDISPONIBILIZAR))

        self.l_rele_sobrecorr_inst_seq_neg_Z3 = LeituraModbusBit(self.rele["SE"], REG_RELE["SE"]["Z3_SOBRECO_INST_SEQU_NEG"],  descricao="[SE][RELE] Sobrecorrente Instantânea Sequência Negativa Z3")
        self.condicionadores_essenciais.append(c.CondicionadorBase(self.l_rele_sobrecorr_inst_seq_neg_Z3, CONDIC_INDISPONIBILIZAR))

        self.l_rele_86T_atuado = LeituraModbusBit(self.rele["TE"], REG_RELE["TE"]["86T_ATUADO"],  descricao="[TE][RELE] Atua 86T")
        self.condicionadores_essenciais.append(c.CondicionadorBase(self.l_rele_86T_atuado, CONDIC_INDISPONIBILIZAR))

        self.l_rele_difer_com_restricao = LeituraModbusBit(self.rele["TE"], REG_RELE["TE"]["DIF_COM_RESTRICAO"], descricao="[TE][RELE] Diferencial Com Restrição")
        self.condicionadores_essenciais.append(c.CondicionadorBase(self.l_rele_difer_com_restricao, CONDIC_INDISPONIBILIZAR))

        self.l_rele_difer_sem_restricao = LeituraModbusBit(self.rele["TE"], REG_RELE["TE"]["DIF_SEM_RESTRICAO"], descricao="[TE][RELE] Diferencial Sem Restrição")
        self.condicionadores_essenciais.append(c.CondicionadorBase(self.l_rele_difer_sem_restricao, CONDIC_INDISPONIBILIZAR))

        self.l_rele_sobrecorr_temp_fase_enrola_prim = LeituraModbusBit(self.rele["TE"], REG_RELE["TE"]["ENROL_PRI_SOBRECO_TEMPO_FASE"],  descricao="[TE][RELE] Sobrecorrente Temperatura Fase Enrolamento Primário")
        self.condicionadores_essenciais.append(c.CondicionadorBase(self.l_rele_sobrecorr_temp_fase_enrola_prim, CONDIC_INDISPONIBILIZAR))

        self.l_rele_sobrecorr_temp_res_enrola_prim = LeituraModbusBit(self.rele["TE"], REG_RELE["TE"]["ENROL_PRI_SOBRECO_TEMPO_RES"],  descricao="[TE][RELE] Sobrecorrente Temperatura Residual Enrolamento Primário")
        self.condicionadores_essenciais.append(c.CondicionadorBase(self.l_rele_sobrecorr_temp_res_enrola_prim, CONDIC_INDISPONIBILIZAR))

        self.l_rele_sobrecorr_temp_fase_enrola_sec = LeituraModbusBit(self.rele["TE"], REG_RELE["TE"]["ENROL_SEC_SOBRECO_TEMPO_FASE"], descricao="[TE][RELE] Sobrecorrente Temperatura Fase Enrolamento Secundário")
        self.condicionadores_essenciais.append(c.CondicionadorBase(self.l_rele_sobrecorr_temp_fase_enrola_sec, CONDIC_INDISPONIBILIZAR))

        self.l_rele_sobrecorr_temp_res_enrola_sec = LeituraModbusBit(self.rele["TE"], REG_RELE["TE"]["ENROL_SEC_SOBRECO_TEMPO_RES"], descricao="[TE][RELE] Sobrecorremnte Temperatura Residual Enrolamento Secundário")
        self.condicionadores_essenciais.append(c.CondicionadorBase(self.l_rele_sobrecorr_temp_res_enrola_sec, CONDIC_INDISPONIBILIZAR))


        # LEITURA PERIÓDICA
        self.l_seletora_52L_remoto = LeituraModbusBit(self.rele["SE"], REG_CLP["SE"]["DJL_SELETORA_REMOTO"], invertido=True, descricao="[SE]  Disjuntor Linha Seletora Modo Remoto")
        self.l_alarme_temp_oleo_te = LeituraModbusBit(self.clp["SA"], REG_CLP["SE"]["TE_ALM_TMP_OLEO"], descricao="[SE]  Transformador Elevador Alarme Temperatura Óleo")
        self.l_falha_temp_oleo_te = LeituraModbusBit(self.clp["SA"], REG_CLP["SE"]["TE_FLH_LER_TMP_OLEO"], descricao="[SE]  Transformador Elevador Falha Leitura Temperatura Óleo")
        self.l_nv_muito_baixo_oleo_te = LeituraModbusBit(self.clp["SA"], REG_CLP["SE"]["TE_NV_OLEO_MUITO_BAIXO"], descricao="[SE]  Transformador Elevador Nível Óleo Muito Baixo")
        self.l_alarme_temp_oleo_te = LeituraModbusBit(self.clp["SA"], REG_CLP["SE"]["TE_ALM_TMP_OLEO"], descricao="[SE]  Transformador Elevador Alarme Temperatura Óleo")
        self.l_alarme_temp_enrola_te = LeituraModbusBit(self.clp["SA"], REG_CLP["SE"]["TE_ALM_TMP_ENROL"], descricao="[SE]  Transformador Elevador Alarme Temperatura Enrolamento")
        self.l_falha_ler_temp_enrola_te = LeituraModbusBit(self.clp["SA"], REG_CLP["SE"]["TE_FLH_LER_TMP_ENROL"], descricao="[SE]  Transformador Elevador Falha Leitura Temperatura Enrolamento")