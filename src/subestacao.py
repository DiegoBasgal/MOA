__version__ = "0.1"
__author__ = "Diego Basgal", "Henrique Pfeifer"
__credits__ = ["Lucas Lavratti", ...]
__description__ = "Este módulo corresponde a implementação da operação da Subestação."

import logging
import traceback

import src.bay as bay
import src.dicionarios.dict as dct
import src.funcoes.condicionadores as c

from src.funcoes.leitura import *
from src.dicionarios.const import *

from src.conectores.servidores import Servidores
from src.funcoes.escrita import EscritaModBusBit as EMB

logger = logging.getLogger("logger")

class Subestacao:

    # ATRIBUIÇÃO DE VARIÁVEIS

    clp = Servidores.clp
    rele = Servidores.rele

    tensao_vs = LeituraModbus(
        clp["SA"], # TODO -> Adicionar Leitura de Tenão VS SE
        REG_CLP["SE"]["LT_VAB"],
    )
    tensao_vab = LeituraModbus(
        clp["SA"],
        REG_CLP["SE"]["LT_VAB"],
        escala=1000,
        descricao="[SE]  Leitura Tensão VAB"
    )
    tensao_vbc = LeituraModbus(
        clp["SA"],
        REG_CLP["SE"]["LT_VBC"],
        escala=1000,
        descricao="[SE]  Leitura Tensão VBC"
    )
    tensao_vca = LeituraModbus(
        clp["SA"],
        REG_CLP["SE"]["LT_VCA"],
        escala=1000,
        descricao="[SE]  Leitura Tensão VCA"
    )
    dj_linha_se = LeituraModbusBit(
        rele["SE"],
        REG_RELE["SE"]["DJL_FECHADO"],
        descricao="[SE][RELE] Disjuntor Linha Status"
    )

    dj_bay_aberto: "bool" = False

    condicionadores: "list[c.CondicionadorBase]" = []
    condicionadores_essenciais: "list[c.CondicionadorBase]" = []

    @classmethod
    def resetar_emergencia(cls) -> "bool":
        """
        Função para acionar comandos de reset de TRIPS/Alarmes
        """

        try:
            res = EMB.escrever_bit(cls.clp["SA"], REG_CLP["SE"]["BLQ_GERAL_CMD_REARME"], valor=1)
            res = EMB.escrever_bit(cls.clp["SA"], REG_CLP["SE"]["86T_CMD_REARME"], valor=1)
            res = EMB.escrever_bit(cls.clp["SA"], REG_CLP["SE"]["86BF_CMD_REARME"], valor=1)
            # res = EMB.escrever_bit(cls.clp["SA"], REG_CLP["SE"]["86BF_86T_CMD_REARME"], valor=1)
            res = EMB.escrever_bit(cls.clp["SA"], REG_CLP["SE"]["REGISTROS_CMD_RST"], valor=1)
            res = EMB.escrever_bit(cls.rele["SE"], REG_CLP["SE"]["RELE_LINHA_ATUADO"], valor=0) # SIMULADOR
            return res

        except Exception:
            logger.exception(f"[SE]  Houve um erro ao realizar o Reset de Emergência.")
            logger.debug(f"[SE]  Traceback: {traceback.format_exc()}")
            return False

    @classmethod
    def fechar_dj_linha(cls) -> "int":
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
            if not cls.dj_linha_se.valor:
                logger.info("[SE]  O Disjuntor da Subestação está aberto!")
                if cls.verificar_dj_linha():
                    logger.debug(f"[SE]  Enviando comando:                   \"FECHAR DISJUNTOR\"")
                    logger.debug("")
                    EMB.escrever_bit(cls.clp["SA"], REG_CLP["SE"]["DJL_CMD_FECHAR"],  valor=1)
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

    @classmethod
    def verificar_dj_linha(cls) -> "bool":
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
            # ADICIONAR SECCIONADORA
            if not cls.l_djL_remoto.valor:
                logger.warning("[SE]  O Disjuntor não está em modo remoto!")
                flags += 1

            if not bay.Bay.dj_linha_bay.valor:
                logger.warning("[SE]  O Disjuntor do Bay está aberto!")
                cls.dj_bay_aberto = True
                flags += 1

            if not bay.Bay.barra_morta.valor and bay.Bay.barra_viva.valor: # BARRA DOS GERADORES
                logger.warning("[SE]  Foi identificada leitura de corrente na barra do Bay!")
                flags += 1

            if cls.l_trip_rele_te.valor:
                logger.warning("[SE]  O sinal de trip do relé do transformador elevador está ativado!")
                flags += 1

            if cls.l_alarme_gas_te.valor:
                logger.warning("[SE]  Foi identificado sinal de alarme no Relé de Buchholz do Transformador Elevador!")
                flags += 1

            if not cls.l_mola_carregada.valor:
                logger.warning("[SE]  A mola do Disjuntor não está carregada!")
                flags += 1

            logger.warning(f"[SE]  Foram identificadas \"{flags}\" condições de bloqueio ao realizar fechamento do Disjuntor. Favor normalizar.") \
                if flags > 0 else logger.debug("[SE]  Condições de Fechamento Validadas.")

            return False if flags > 0 else True

        except Exception:
            logger.exception(f"[SE]  Houve um erro ao verificar as pré-condições de fechameto do Dijuntor de Linha.")
            logger.debug(f"[SE]  Traceback: {traceback.format_exc()}")
            return False

    @classmethod
    def verificar_tensao_trifasica(cls) -> "bool":
        """
        Função para verificação de Tensão na linha da Subestação.
        """

        try:
            if (TENSAO_LINHA_BAIXA < cls.tensao_vab.valor < TENSAO_LINHA_ALTA) \
                and (TENSAO_LINHA_BAIXA < cls.tensao_vbc.valor < TENSAO_LINHA_ALTA) \
                and (TENSAO_LINHA_BAIXA < cls.tensao_vca.valor < TENSAO_LINHA_ALTA):
                return True
            else:
                logger.warning("[SE]  Tensão da linha fora do limite.")
                return False

        except Exception:
            logger.exception(f"[SE]  Houve um erro ao realizar a verificação da tensão na linha.")
            logger.debug(f"[SE]  Traceback: {traceback.format_exc()}")
            return False

    @classmethod
    def verificar_condicionadores(cls) -> "list[c.CondicionadorBase]":
        """
        Função para verificação de TRIPS/Alarmes.

        Verifica os condicionadores ativos e retorna lista com os mesmos para a função de verificação
        da Classe da Usina determinar as ações necessárias.
        """

        if True in (condic.ativo for condic in cls.condicionadores_essenciais):
            condics_ativos = [condic for condics in [cls.condicionadores_essenciais, cls.condicionadores] for condic in condics if condic.ativo]

            logger.debug("")
            logger.info("[SE]  Foram detectados condicionadores ativos!")
            [logger.info(f"[SE]  Descrição: \"{condic.descricao}\", Gravidade: \"{CONDIC_STR_DCT[condic.gravidade]}\".") for condic in condics_ativos]
            logger.debug("")

            return condics_ativos
        else:
            return []

    @classmethod
    def verificar_leituras(cls) -> "None":
        """
        Função para verificação de leituras por acionamento temporizado.

        Verifica leituras específcas para acionamento da manuteção. As leituras são disparadas
        em períodos separados por um tempo pré-definido.
        """
        return

        if not cls.l_seletora_52L_remoto.valor:
            logger.warning("[SE]  O Disjuntor 52L saiu do modo remoto. Favor verificar.")

        if cls.l_falha_temp_oleo_te.valor:
            logger.warning("[SE]  Houve uma falha de leitura de temperatura do óleo do transformador elevador. Favor verificar.")

        if cls.l_falha_ler_temp_enrola_te.valor:
            logger.warning("[SE]  Houve uma falha de leitura de temperatura do enrolamento do transformador elevador. Favor verificar.")

        if cls.l_alarme_temp_oleo_te.valor and not dct.voip["TE_ALM_TEMPERATURA_OLEO"][0]:
            logger.warning("[SE]  A temperatura do óleo do transformador elevador está alta. Favor verificar.")
            dct.voip["TE_ALM_TEMPERATURA_OLEO"][0] = True
        elif not cls.l_alarme_temp_oleo_te.valor and dct.voip["TE_ALM_TEMPERATURA_OLEO"][0]:
            dct.voip["TE_ALM_TEMPERATURA_OLEO"][0] = False

        if cls.l_nv_muito_alto_oleo_te.valor and not dct.voip["TE_NIVEL_OLEO_MUITO_ALTO"][0]:
            logger.warning("[SE]  O nível do óleo do transformador elevador está muito alto. Favor verificar.")
            dct.voip["TE_NIVEL_OLEO_MUITO_ALTO"][0] = True
        elif not cls.l_nv_muito_alto_oleo_te.valor and dct.voip["TE_NIVEL_OLEO_MUITO_ALTO"][0]:
            dct.voip["TE_NIVEL_OLEO_MUITO_ALTO"][0] = False

        if cls.l_nv_muito_baixo_oleo_te.valor and not dct.voip["TE_NIVEL_OLEO_MUITO_BAIXO"][0]:
            logger.warning("[SE]  O nível de óleo do tranformador elevador está muito baixo. Favor verificar.")
            dct.voip["TE_NIVEL_OLEO_MUITO_BAIXO"][0] = True
        elif not cls.l_nv_muito_baixo_oleo_te.valor and dct.voip["TE_NIVEL_OLEO_MUITO_BAIXO"][0]:
            dct.voip["TE_NIVEL_OLEO_MUITO_BAIXO"][0] = False

        if cls.l_alarme_temp_oleo_te.valor and not dct.voip["TE_ALARME_TEMPERATURA_OLEO"][0]:
            logger.warning("[SE]  A temperatura do óleo do transformador elevador está alta. Favor verificar.")
            dct.voip["TE_ALARME_TEMPERATURA_OLEO"][0] = True
        elif not cls.l_alarme_temp_oleo_te.valor and dct.voip["TE_ALARME_TEMPERATURA_OLEO"][0]:
            dct.voip["TE_ALARME_TEMPERATURA_OLEO"][0] = False

        if cls.l_alarme_temp_enrola_te.valor and not dct.voip["TE_ALM_TEMPERATURA_ENROLAMENTO"][0]:
            logger.warning("[SE]  A temperatura do enrolamento do transformador elevador está alta. Favor verificar.")
            dct.voip["TE_ALM_TEMPERATURA_ENROLAMENTO"][0] = True
        elif not cls.l_alarme_temp_enrola_te.valor and dct.voip["TE_ALM_TEMPERATURA_ENROLAMENTO"][0]:
            dct.voip["TE_ALM_TEMPERATURA_ENROLAMENTO"][0] = False

        if cls.leitura_alarme_temp_enrolamento_te.valor and not dct.voip["TE_ALARME_TEMPERATURA_ENROLAMENTO"][0]:
            logger.warning("[SE]  A temperatura do enrolamento do transformador elevador está alta. Favor verificar.")
            dct.voip["TE_ALARME_TEMPERATURA_ENROLAMENTO"][0] = True
        elif not cls.leitura_alarme_temp_enrolamento_te.valor and dct.voip["TE_ALARME_TEMPERATURA_ENROLAMENTO"][0]:
            dct.voip["TE_ALARME_TEMPERATURA_ENROLAMENTO"][0] = False

    @classmethod
    def carregar_leituras(cls) -> "None":
        """
        Função para carregamento de leituras necessárias para a operação.
        """

        # Pré-condições de fechamento do Dj52L
        cls.l_trip_rele_te = LeituraModbusBit(cls.rele["TE"], REG_RELE["TE"]["RELE_ESTADO_TRP"], descricao="[TE][RELE] Transformador Elevador Trip")

        cls.l_mola_carregada = LeituraModbusBit(cls.clp["SA"], REG_RELE["SE"]["DJL_MOLA_CARREGADA"], descricao="[SE]  Disjuntor Linha Mola Carregada")
        cls.l_djL_remoto = LeituraModbusBit(cls.clp["SA"], REG_CLP["SE"]["DJL_SELETORA_REMOTO"], descricao="[SE]  Disjuntor Linha Seletora Modo Remoto")
        cls.l_alarme_gas_te = LeituraModbusBit(cls.clp["SA"], REG_CLP["SE"]["TE_RELE_BUCHHOLZ_ALM"], descricao="[SE]  Transformador Elevador Alarme Relé Buchholz")

        ### CONDICIONADORES ESSENCIAIS
        ## NORMALIZAR

        cls.l_rele_linha_atuado = LeituraModbusBit(cls.clp["SA"], REG_CLP["SE"]["RELE_LINHA_ATUADO"], descricao="[SE]  Relé Linha Atuado")
        cls.condicionadores_essenciais.append(c.CondicionadorBase(cls.l_rele_linha_atuado, gravidade=CONDIC_NORMALIZAR))
        return

        ### CONDICIONADORES
        ## INDISPONIBILIZAR

        cls.l_89L_fechada = LeituraModbusBit(cls.clp["SA"], REG_CLP["SE"]["89L_FECHADA"], invertido=True, descricao="[SE]  89L Fechada")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_89L_fechada, CONDIC_INDISPONIBILIZAR))

        cls.l_86T_atuado = LeituraModbusBit(cls.clp["SA"], REG_CLP["SE"]["86T_ATUADO"], descricao="[SE]  86T Atuado")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_86T_atuado, CONDIC_INDISPONIBILIZAR))

        cls.l_86BF_atuado = LeituraModbusBit(cls.clp["SA"], REG_CLP["SE"]["86BF_ATUADO"], descricao="[SE]  86BF Atuado")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_86BF_atuado, CONDIC_INDISPONIBILIZAR))

        cls.l_rele_te_atuado = LeituraModbusBit(cls.clp["SA"], REG_CLP["SE"]["TE_RELE_ATUADO"], descricao="[SE]  Transformador Elevador Relé Atuado")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_rele_te_atuado, CONDIC_INDISPONIBILIZAR))

        cls.l_trip_rele_buchholz = LeituraModbusBit(cls.clp["SA"], REG_CLP["SE"]["TE_RELE_BUCHHOLZ_TRP"], descricao="[SE]  Transformador Elevador Trip Relé Buchholz")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_trip_rele_buchholz, CONDIC_INDISPONIBILIZAR))

        cls.l_trip_alivio_pressao = LeituraModbusBit(cls.clp["SA"], REG_CLP["SE"]["TE_TRP_ALIVIO_PRESSAO"], descricao="[SE]  Transformador Elevador Trip Alívio Pressão")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_trip_alivio_pressao, CONDIC_INDISPONIBILIZAR))

        cls.l_trip_temp_oleo_te = LeituraModbusBit(cls.clp["SA"], REG_CLP["SE"]["TE_TRP_TMP_OLEO"], descricao="[SE]  Transformador Elevador Trip Temperatura Óleo")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_trip_temp_oleo_te, CONDIC_INDISPONIBILIZAR))

        cls.l_rele_linha_bf_atuado = LeituraModbusBit(cls.clp["SA"], REG_CLP["SE"]["RELE_LINHA_ATUACAO_BF"], descricao="[SE]  Relé Linha Atuação BF")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_rele_linha_bf_atuado, CONDIC_INDISPONIBILIZAR))

        cls.l_alarme_rele_bulchholz_te = LeituraModbusBit(cls.clp["SA"], REG_CLP["SE"]["TE_RELE_BUCHHOLZ_ALM"], descricao="[SE]  Transformador Elevador Alarme Relé Buchholz")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alarme_rele_bulchholz_te, CONDIC_INDISPONIBILIZAR))

        cls.l_trip_temp_enrola_te = LeituraModbusBit(cls.clp["SA"], REG_CLP["SE"]["TE_TRP_TMP_ENROL"], descricao="[SE]  Transformador Elevador Trip Temperatura Enrolamento")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_trip_temp_enrola_te, CONDIC_INDISPONIBILIZAR))

        cls.l_falha_cmd_abertura_52L = LeituraModbusBit(cls.clp["SA"], REG_CLP["SE"]["DJL_FLH_CMD_ABERTURA"], descricao="[SE]  Disjuntor Linha Falha Comando Abertura")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_falha_cmd_abertura_52L, CONDIC_INDISPONIBILIZAR))

        cls.l_falha_cmd_fechamento_52L = LeituraModbusBit(cls.clp["SA"], REG_CLP["SE"]["DJL_FLH_CMD_FECHAMENTO"], descricao="[SE]  Disjuntor Linha Falha Comando Fechamento")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_falha_cmd_fechamento_52L, CONDIC_INDISPONIBILIZAR))

        # cls.leitura_super_bobinas_reles_bloq = LeituraModbusBit(cls.clp["SA"], REG_CLP["SE"]["SUPERVISAO_BOBINAS_RELES_BLOQUEIOS"], , descricao="[SE]  Supervisão Bobinas, Relés e Bloqueios")
        # cls.condicionadores.append(c.CondicionadorBase(cls.leitura_super_bobinas_reles_bloq, CONDIC_INDISPONIBILIZAR))

        # LEITURA PERIÓDICA
        cls.l_seletora_52L_remoto = LeituraModbusBit(cls.clp["SA"], REG_CLP["SE"]["DJL_SELETORA_REMOTO"], invertido=True, descricao="[SE]  Disjuntor Linha Seletora Modo Remoto")
        cls.l_alarme_temp_oleo_te = LeituraModbusBit(cls.clp["SA"], REG_CLP["SE"]["TE_ALM_TMP_OLEO"], descricao="[SE]  Transformador Elevador Alarme Temperatura Óleo")
        cls.l_nv_muito_alto_oleo_te = LeituraModbusBit(cls.clp["SA"], REG_CLP["SE"]["TE_NV_OLEO_MUITO_ALTO"], descricao="[SE]  Transformador Elevador Nível Óleo Muito Alto")
        cls.l_falha_temp_oleo_te = LeituraModbusBit(cls.clp["SA"], REG_CLP["SE"]["TE_FLH_LER_TMP_OLEO"], descricao="[SE]  Transformador Elevador Falha Leitura Temperatura Óleo")
        cls.l_nv_muito_baixo_oleo_te = LeituraModbusBit(cls.clp["SA"], REG_CLP["SE"]["TE_NV_OLEO_MUITO_BAIXO"], descricao="[SE]  Transformador Elevador Nível Óleo Muito Baixo")
        cls.l_alarme_temp_oleo_te = LeituraModbusBit(cls.clp["SA"], REG_CLP["SE"]["TE_ALM_TMP_OLEO"], descricao="[SE]  Transformador Elevador Alarme Temperatura Óleo")
        cls.l_alarme_temp_enrola_te = LeituraModbusBit(cls.clp["SA"], REG_CLP["SE"]["TE_ALM_TMP_ENROL"], descricao="[SE]  Transformador Elevador Alarme Temperatura Enrolamento")
        cls.l_falha_ler_temp_enrola_te = LeituraModbusBit(cls.clp["SA"], REG_CLP["SE"]["TE_FLH_LER_TMP_ENROL"], descricao="[SE]  Transformador Elevador Falha Leitura Temperatura Enrolamento")


        # CONDICIONADORES RELÉS
        cls.l_rele_falha_receb_rele_te = LeituraModbusBit(cls.rele["SE"], REG_RELE["SE"]["RELE_TE_FLH_PARTIDA"],  descricao="[SE][RELE] Falha Partida Recebida Relé Transformador Elevador")
        cls.condicionadores_essenciais.append(c.CondicionadorBase(cls.l_rele_falha_receb_rele_te, CONDIC_INDISPONIBILIZAR))

        cls.l_rele_falha_abertura_djB1 = LeituraModbusBit(cls.rele["SE"], REG_RELE["SE"]["DJL_FLH_ABERTURA_B1"],  descricao="[SE][RELE] Disjuntor Linha Falha Abertura - BIT 01")
        cls.condicionadores_essenciais.append(c.CondicionadorBase(cls.l_rele_falha_abertura_djB1, CONDIC_INDISPONIBILIZAR))

        cls.l_rele_falha_abertura_djB3 = LeituraModbusBit(cls.rele["SE"], REG_RELE["SE"]["DJL_FLH_ABERTURA_B3"],  descricao="[SE][RELE] Disjuntor Linha Falha Abertura - BIT 03")
        cls.condicionadores_essenciais.append(c.CondicionadorBase(cls.l_rele_falha_abertura_djB3, CONDIC_INDISPONIBILIZAR))

        cls.l_rele_falha_abertura_dB4 = LeituraModbusBit(cls.rele["SE"], REG_RELE["SE"]["DJL_FLH_ABERTURA_B4"],  descricao="[SE][RELE] Disjuntor Linha Falha Abertura - BIT 04")
        cls.condicionadores_essenciais.append(c.CondicionadorBase(cls.l_rele_falha_abertura_dB4, CONDIC_INDISPONIBILIZAR))

        cls.l_rele_sobrecorr_inst_seq_neg_Z1 = LeituraModbusBit(cls.rele["SE"], REG_RELE["SE"]["Z1_SOBRECO_INST_SEQU_NEG"],  descricao="[SE][RELE] Sobrecorrente Instantânea Sequência Negativa Z1")
        cls.condicionadores_essenciais.append(c.CondicionadorBase(cls.l_rele_sobrecorr_inst_seq_neg_Z1, CONDIC_INDISPONIBILIZAR))

        cls.l_rele_sobrecorr_inst_seq_neg_Z2 = LeituraModbusBit(cls.rele["SE"], REG_RELE["SE"]["Z2_SOBRECO_INST_SEQU_NEG"],  descricao="[SE][RELE] Sobrecorrente Instantânea Sequência Negativa Z2")
        cls.condicionadores_essenciais.append(c.CondicionadorBase(cls.l_rele_sobrecorr_inst_seq_neg_Z2, CONDIC_INDISPONIBILIZAR))

        cls.l_rele_sobrecorr_inst_seq_neg_Z3 = LeituraModbusBit(cls.rele["SE"], REG_RELE["SE"]["Z3_SOBRECO_INST_SEQU_NEG"],  descricao="[SE][RELE] Sobrecorrente Instantânea Sequência Negativa Z3")
        cls.condicionadores_essenciais.append(c.CondicionadorBase(cls.l_rele_sobrecorr_inst_seq_neg_Z3, CONDIC_INDISPONIBILIZAR))

        cls.l_rele_86T_atuado = LeituraModbusBit(cls.rele["TE"], REG_RELE["TE"]["86T_ATUADO"],  descricao="[TE][RELE] Atua 86T")
        cls.condicionadores_essenciais.append(c.CondicionadorBase(cls.l_rele_86T_atuado, CONDIC_INDISPONIBILIZAR))

        cls.l_rele_difer_com_restricao = LeituraModbusBit(cls.rele["TE"], REG_RELE["TE"]["DIF_COM_RESTRICAO"], descricao="[TE][RELE] Diferencial Com Restrição")
        cls.condicionadores_essenciais.append(c.CondicionadorBase(cls.l_rele_difer_com_restricao, CONDIC_INDISPONIBILIZAR))

        cls.l_rele_difer_sem_restricao = LeituraModbusBit(cls.rele["TE"], REG_RELE["TE"]["DIF_SEM_RESTRICAO"], descricao="[TE][RELE] Diferencial Sem Restrição")
        cls.condicionadores_essenciais.append(c.CondicionadorBase(cls.l_rele_difer_sem_restricao, CONDIC_INDISPONIBILIZAR))

        cls.l_rele_sobrecorr_temp_fase_enrola_prim = LeituraModbusBit(cls.rele["TE"], REG_RELE["TE"]["ENROL_PRI_SOBRECO_TEMPO_FASE"],  descricao="[TE][RELE] Sobrecorrente Temperatura Fase Enrolamento Primário")
        cls.condicionadores_essenciais.append(c.CondicionadorBase(cls.l_rele_sobrecorr_temp_fase_enrola_prim, CONDIC_INDISPONIBILIZAR))

        cls.l_rele_sobrecorr_temp_res_enrola_prim = LeituraModbusBit(cls.rele["TE"], REG_RELE["TE"]["ENROL_PRI_SOBRECO_TEMPO_RES"],  descricao="[TE][RELE] Sobrecorrente Temperatura Residual Enrolamento Primário")
        cls.condicionadores_essenciais.append(c.CondicionadorBase(cls.l_rele_sobrecorr_temp_res_enrola_prim, CONDIC_INDISPONIBILIZAR))

        cls.l_rele_sobrecorr_temp_fase_enrola_sec = LeituraModbusBit(cls.rele["TE"], REG_RELE["TE"]["ENRO_SEC_SOBRECO_TEMPO_FASE"],  descricao="[TE][RELE] Sobrecorrente Temperatura Fase Enrolamento Secundário")
        cls.condicionadores_essenciais.append(c.CondicionadorBase(cls.l_rele_sobrecorr_temp_fase_enrola_sec, CONDIC_INDISPONIBILIZAR))

        cls.l_rele_sobrecorr_temp_res_enrola_sec = LeituraModbusBit(cls.rele["TE"], REG_RELE["TE"]["ENRO_SEC_SOBRECO_TEMPO_RES"],  descricao="[TE][RELE] Sobrecorremnte Temperatura Residual Enrolamento Secundário")
        cls.condicionadores_essenciais.append(c.CondicionadorBase(cls.la_rele_sobrecorr_temp_res_enroal_sec, CONDIC_INDISPONIBILIZAR))