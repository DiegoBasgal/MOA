__version__ = "0.1"
__author__ = "Diego Basgal", "Henrique Pfeifer"
__credits__ = ["Lucas Lavratti", ...]
__description__ = "Este módulo corresponde a implementação da operação da Subestação."

import logging
import traceback

import dicionarios.dict as dct

from funcoes.leitura import *
from dicionarios.const import *
from funcoes.condicionador import *

from usina import Usina
from bay import Bay as BAY
from conectores.servidores import Servidores
from funcoes.escrita import EscritaModBusBit as EMB

logger = logging.getLogger("logger")

class Subestacao(Usina):

    # ATRIBUIÇÃO DE VARIÁVEIS

    clp = Servidores.clp
    rele = Servidores.rele

    tensao_vs = LeituraModbus(
        clp[""], # TODO -> Adicionar Leitura de Tenão VS SE
    )
    tensao_vab = LeituraModbus(
        clp["SA"],
        REG_CLP["SE"]["LT_VAB"],
        descricao="[SE]  Leitura Tensão VAB"
    )
    tensao_vbc = LeituraModbus(
        clp["SA"],
        REG_CLP["SE"]["LT_VBC"],
        descricao="[SE]  Leitura Tensão VBC"
    )
    tensao_vca = LeituraModbus(
        clp["SA"],
        REG_CLP["SE"]["LT_VCA"],
        descricao="[SE]  Leitura Tensão VCA"
    )
    dj_linha_se = LeituraModbusBit(
        rele["SE"],
        REG_RELE["SE"]["DJ_LINHA_FECHADO"],
        bit=0,
        descricao="[SE][RELE] Disjuntor Linha Status"
    )

    dj_bay_aberto: "bool" = False

    condicionadores: "list[CondicionadorBase]" = []
    condicionadores_essenciais: "list[CondicionadorBase]" = []

    @classmethod
    def resetar_emergencia(cls) -> "bool":
        """
        Função para acionar comandos de reset de TRIPS/Alarmes
        """

        try:
            res = EMB.escrever_bit(cls.clp["SA"], REG_CLP["SE"]["CMD_SE_REARME_BLOQUEIO_GERAL"], bit=0, valor=1)
            res = EMB.escrever_bit(cls.clp["SA"], REG_CLP["SE"]["CMD_SE_REARME_86T"], bit=1, valor=1)
            res = EMB.escrever_bit(cls.clp["SA"], REG_CLP["SE"]["CMD_SE_REARME_86BF"], bit=2, valor=1)
            res = EMB.escrever_bit(cls.clp["SA"], REG_CLP["SE"]["REARME_86BF_86T"], bit=22, valor=1)
            res = EMB.escrever_bit(cls.clp["SA"], REG_CLP["SE"]["CMD_SE_RESET_REGISTROS"], bit=5, valor=1)
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
                if cls.verificar_dj_linha():
                    EMB.escrever_bit(cls.clp["SA"], REG_CLP["SE"]["CMD_SE_FECHA_52L"], bit=4, valor=1)
                    return DJL_FECHAMENTO_OK

                elif cls.dj_bay_aberto:
                    logger.info("[SE]  Foi identificado que o Disjuntor do BAY está aberto. Adicionando condição para fechamento...")
                    return DJL_DJBAY_ABERTO

                else:
                    logger.warning("[SE]  Não foi possível realizar o fechamento do Disjuntor de Linha.")
                    return DJL_FALHA_FECHAMENTO

            else:
                logger.debug("[SE]  O Disjuntor de Linha já está fechado")
                return DJL_FECHAMENTO_OK

        except Exception:
            logger.exception(f"[SE]  Houve um erro ao realizar o fechamento do Disjuntor de Linha.")
            logger.debug(f"[SE]  Traceback: {traceback.format_exc()}")
            return DJL_FALHA_FECHAMENTO

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
        logger.info("[SE]  Verificando condições de fechamento do Disjuntor de Linha...")

        try:
            if not BAY.dj_linha_bay.valor:
                logger.warning("[SE]  O Disjuntor do Bay está aberto!")
                cls.dj_bay_aberto = True
                flags += 1

            if cls.trip_rele_te.valor:
                logger.warning("[SE]  O sinal de trip do relé do transformador elevador está ativado!")
                flags += 1

            if not BAY.barra_morta.valor and BAY.barra_viva.valor:
                logger.warning("[SE]  Foi identificada leitura de corrente na barra do Bay!")
                flags += 1

            if not BAY.secc_fechada.valor:
                logger.warning("[SE]  A seccionadora do Bay está aberta!")
                flags += 1

            if cls.alarme_gas_te.valor:
                logger.warning("[SE]  Foi identificado sinal de alarme no Relé de Buchholz do Transformador Elevador!")
                flags += 1

            if not cls.mola_carregada.valor:
                logger.warning("[SE]  A mola do Disjuntor não está carregada!")
                flags += 1

            if not cls.dj52l_remoto.valor:
                logger.warning("[SE]  O Disjuntor não está em modo remoto!")
                flags += 1

            logger.warning(f"[SE]  Foram identificadas \"{flags}\" condições de bloqueio ao realizar fechamento do Disjuntor. Favor normalizar.") \
                if flags > 0 else logger.debug("[SE]  Condições de fechamento do Disjuntor de Linha OK! Fechando disjuntor...")

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
    def verificar_condicionadores(cls) -> "list[CondicionadorBase]":
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

        if not cls.leitura_seletora_52l_remoto.valor:
            logger.warning("[SE]  O Disjuntor 52L saiu do modo remoto. Favor verificar.")

        if cls.leitura_falha_temp_oleo_te.valor:
            logger.warning("[SE]  Houve uma falha de leitura de temperatura do óleo do transformador elevador. Favor verificar.")

        if cls.leitura_falha_temp_enrolamento_te.valor:
            logger.warning("[SE]  Houve uma falha de leitura de temperatura do enrolamento do transformador elevador. Favor verificar.")

        if cls.leitura_alm_temperatura_oleo_te.valor and not dct.voip["TE_ALM_TEMPERATURA_OLEO"][0]:
            logger.warning("[SE]  A temperatura do óleo do transformador elevador está alta. Favor verificar.")
            dct.voip["TE_ALM_TEMPERATURA_OLEO"][0] = True
        elif not cls.leitura_alm_temperatura_oleo_te.valor and dct.voip["TE_ALM_TEMPERATURA_OLEO"][0]:
            dct.voip["TE_ALM_TEMPERATURA_OLEO"][0] = False

        if cls.leitura_nivel_oleo_muito_alto_te.valor and not dct.voip["TE_NIVEL_OLEO_MUITO_ALTO"][0]:
            logger.warning("[SE]  O nível do óleo do transformador elevador está muito alto. Favor verificar.")
            dct.voip["TE_NIVEL_OLEO_MUITO_ALTO"][0] = True
        elif not cls.leitura_nivel_oleo_muito_alto_te.valor and dct.voip["TE_NIVEL_OLEO_MUITO_ALTO"][0]:
            dct.voip["TE_NIVEL_OLEO_MUITO_ALTO"][0] = False

        if cls.leitura_nivel_oleo_muito_baixo_te.valor and not dct.voip["TE_NIVEL_OLEO_MUITO_BAIXO"][0]:
            logger.warning("[SE]  O nível de óleo do tranformador elevador está muito baixo. Favor verificar.")
            dct.voip["TE_NIVEL_OLEO_MUITO_BAIXO"][0] = True
        elif not cls.leitura_nivel_oleo_muito_baixo_te.valor and dct.voip["TE_NIVEL_OLEO_MUITO_BAIXO"][0]:
            dct.voip["TE_NIVEL_OLEO_MUITO_BAIXO"][0] = False

        if cls.leitura_alarme_temperatura_oleo_te.valor and not dct.voip["TE_ALARME_TEMPERATURA_OLEO"][0]:
            logger.warning("[SE]  A temperatura do óleo do transformador elevador está alta. Favor verificar.")
            dct.voip["TE_ALARME_TEMPERATURA_OLEO"][0] = True
        elif not cls.leitura_alarme_temperatura_oleo_te.valor and dct.voip["TE_ALARME_TEMPERATURA_OLEO"][0]:
            dct.voip["TE_ALARME_TEMPERATURA_OLEO"][0] = False

        if cls.leitura_alm_temp_enrolamento_te.valor and not dct.voip["TE_ALM_TEMPERATURA_ENROLAMENTO"][0]:
            logger.warning("[SE]  A temperatura do enrolamento do transformador elevador está alta. Favor verificar.")
            dct.voip["TE_ALM_TEMPERATURA_ENROLAMENTO"][0] = True
        elif not cls.leitura_alm_temp_enrolamento_te.valor and dct.voip["TE_ALM_TEMPERATURA_ENROLAMENTO"][0]:
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
        cls.trip_rele_te = LeituraModbusBit(cls.rele["TE"], REG_RELE["TE"]["RELE_ESTADO_TRIP"], bit=15, descricao="[TE][RELE] Transformador Elevador Trip")

        cls.mola_carregada = LeituraModbusBit(cls.clp["SA"], REG_CLP["SE"]["52L_MOLA_CARREGADA"], bit=16, descricao="[SE]  Disjuntor Linha Mola Carregada")
        cls.dj52l_remoto = LeituraModbusBit(cls.clp["SA"], REG_CLP["SE"]["52L_SELETORA_REMOTO"], bit=10, descricao="[SE]  Disjuntor Linha Seletora Modo Remoto")
        cls.alarme_gas_te = LeituraModbusBit(cls.clp["SA"], REG_CLP["SE"]["TE_ALARME_RELE_BUCHHOLZ"], bit=22, descricao="[SE]  Transformador Elevador Alarme Relé Buchholz")

        # CONDICIONADORES ESSENCIAIS
        # Normalizar
        cls.leitura_rele_linha_atuado = LeituraModbusBit(cls.clp["SA"], REG_CLP["SE"]["RELE_LINHA_ATUADO"], bit=14, descricao="[SE]  Relé Linha Atuado")
        cls.condicionadores_essenciais.append(CondicionadorBase(cls.leitura_rele_linha_atuado, CONDIC_NORMALIZAR))

        # CONDICIONADORES
        # Indisponibilizar
        cls.leitura_89l_fechada = LeituraModbusBit(cls.clp["SA"], REG_CLP["SE"]["89L_FECHADA"], bit=12, invertido=True, descricao="[SE]  89L Fechada")
        cls.condicionadores.append(CondicionadorBase(cls.leitura_89l_fechada, CONDIC_INDISPONIBILIZAR))

        cls.leitura_86t_atuado = LeituraModbusBit(cls.clp["SA"], REG_CLP["SE"]["86T_ATUADO"], bit=20, descricao="[SE]  86T Atuado")
        cls.condicionadores.append(CondicionadorBase(cls.leitura_86t_atuado, CONDIC_INDISPONIBILIZAR))

        cls.leitura_86bf_atuado = LeituraModbusBit(cls.clp["SA"], REG_CLP["SE"]["86BF_ATUADO"], bit=19, descricao="[SE]  86BF Atuado")
        cls.condicionadores.append(CondicionadorBase(cls.leitura_86bf_atuado, CONDIC_INDISPONIBILIZAR))

        cls.leitura_rele_te_atuado = LeituraModbusBit(cls.clp["SA"], REG_CLP["SE"]["TE_RELE_ATUADO"], bit=17, descricao="[SE]  Transformador Elevador Relé Atuado")
        cls.condicionadores.append(CondicionadorBase(cls.leitura_rele_te_atuado, CONDIC_INDISPONIBILIZAR))

        cls.leitura_trip_rele_buchholz = LeituraModbusBit(cls.clp["SA"], REG_CLP["SE"]["TE_TRIP_RELE_BUCHHOLZ"], bit=23, descricao="[SE]  Transformador Elevador Trip Relé Buchholz")
        cls.condicionadores.append(CondicionadorBase(cls.leitura_trip_rele_buchholz, CONDIC_INDISPONIBILIZAR))

        cls.leitura_trip_alivio_pressao = LeituraModbusBit(cls.clp["SA"], REG_CLP["SE"]["TE_TRIP_ALIVIO_PRESSAO"], bit=24, descricao="[SE]  Transformador Elevador Trip Alívio Pressão")
        cls.condicionadores.append(CondicionadorBase(cls.leitura_trip_alivio_pressao, CONDIC_INDISPONIBILIZAR))

        cls.leitura_trip_temp_oleo_te = LeituraModbusBit(cls.clp["SA"], REG_CLP["SE"]["TE_TRIP_TEMPERATURA_OLEO"], bit=19, descricao="[SE]  Transformador Elevador Trip Temperatura Óleo")
        cls.condicionadores.append(CondicionadorBase(cls.leitura_trip_temp_oleo_te, CONDIC_INDISPONIBILIZAR))

        cls.leitura_atuacao_rele_linha_bf = LeituraModbusBit(cls.clp["SA"], REG_CLP["SE"]["RELE_LINHA_ATUACAO_BF"], bit=16, descricao="[SE]  Relé Linha Atuação BF")
        cls.condicionadores.append(CondicionadorBase(cls.leitura_atuacao_rele_linha_bf, CONDIC_INDISPONIBILIZAR))

        cls.leitura_alarme_rele_buchholz = LeituraModbusBit(cls.clp["SA"], REG_CLP["SE"]["TE_ALARME_RELE_BUCHHOLZ"], bit=22, descricao="[SE]  Transformador Elevador Alarme Relé Buchholz")
        cls.condicionadores.append(CondicionadorBase(cls.leitura_alarme_rele_buchholz, CONDIC_INDISPONIBILIZAR))

        cls.leitura_trip_temp_enrol_te = LeituraModbusBit(cls.clp["SA"], REG_CLP["SE"]["TE_TRIP_TEMPERATURA_ENROLAMENTO"], bit=20, descricao="[SE]  Transformador Elevador Trip Temperatura Enrolamento")
        cls.condicionadores.append(CondicionadorBase(cls.leitura_trip_temp_enrol_te, CONDIC_INDISPONIBILIZAR))

        cls.leitura_falha_comando_abertura_52l = LeituraModbusBit(cls.clp["SA"], REG_CLP["SE"]["FALHA_COMANDO_ABERTURA_52L"], bit=1, descricao="[SE]  Disjuntor Linha Falha Comando Abertura")
        cls.condicionadores.append(CondicionadorBase(cls.leitura_falha_comando_abertura_52l, CONDIC_INDISPONIBILIZAR))

        cls.leitura_falha_comando_fechamento_52l = LeituraModbusBit(cls.clp["SA"], REG_CLP["SE"]["FALHA_COMANDO_FECHAMENTO_52L"], bit=2, descricao="[SE]  Disjuntor Linha Falha Comando Fechamento")
        cls.condicionadores.append(CondicionadorBase(cls.leitura_falha_comando_fechamento_52l, CONDIC_INDISPONIBILIZAR))

        cls.leitura_super_bobinas_reles_bloq = LeituraModbusBit(cls.clp["SA"], REG_CLP["SE"]["SUPERVISAO_BOBINAS_RELES_BLOQUEIOS"], bit=21, descricao="[SE]  Supervisão Bobinas, Relés e Bloqueios")
        cls.condicionadores.append(CondicionadorBase(cls.leitura_super_bobinas_reles_bloq, CONDIC_INDISPONIBILIZAR))

        # LEITURA PERIÓDICA
        cls.leitura_seletora_52l_remoto = LeituraModbusBit(cls.clp["SA"], REG_CLP["SE"]["52L_SELETORA_REMOTO"], bit=10, invertido=True, descricao="[SE]  Disjuntor Linha Seletora Modo Remoto")
        cls.leitura_alm_temperatura_oleo_te = LeituraModbusBit(cls.clp["SA"], REG_CLP["SE"]["TE_ALM_TEMPERATURA_OLEO"], bit=1, descricao="[SE]  Transformador Elevador Alarme Temperatura Óleo")
        cls.leitura_nivel_oleo_muito_alto_te = LeituraModbusBit(cls.clp["SA"], REG_CLP["SE"]["TE_NIVEL_OLEO_MUITO_ALTO"], bit=26, descricao="[SE]  Transformador Elevador Nível Óleo Muito Alto")
        cls.leitura_falha_temp_oleo_te = LeituraModbusBit(cls.clp["SA"], REG_CLP["SE"]["TE_FALHA_TEMPERATURA_OLEO"], bit=1, descricao="[SE]  Transformador Elevador Falha Leitura Temperatura Óleo")
        cls.leitura_nivel_oleo_muito_baixo_te = LeituraModbusBit(cls.clp["SA"], REG_CLP["SE"]["TE_NIVEL_OLEO_MUITO_BAIXO"], bit=27, descricao="[SE]  Transformador Elevador Nível Óleo Muito Baixo")
        cls.leitura_alarme_temperatura_oleo_te = LeituraModbusBit(cls.clp["SA"], REG_CLP["SE"]["TE_ALARME_TEMPERATURA_OLEO"], bit=18, descricao="[SE]  Transformador Elevador Alarme Temperatura Óleo")
        cls.leitura_alm_temp_enrolamento_te = LeituraModbusBit(cls.clp["SA"], REG_CLP["SE"]["TE_ALM_TEMPERATURA_ENROLAMENTO"], bit=2, descricao="[SE]  Transformador Elevador Alarme Temperatura Enrolamento")
        cls.leitura_alarme_temp_enrolamento_te = LeituraModbusBit(cls.clp["SA"], REG_CLP["SE"]["TE_ALARME_TEMPERATURA_ENROLAMENTO"], bit=20, descricao="[SE]  Transformador Elevador Alarme Temperatura Enrolamento")
        cls.leitura_falha_temp_enrolamento_te = LeituraModbusBit(cls.clp["SA"], REG_CLP["SE"]["TE_FALHA_TEMPERATURA_ENROLAMENTO"], bit=2, descricao="[SE]  Transformador Elevador Falha Leitura Temperatura Enrolamento")


        # CONDICIONADORES RELÉS
        cls.leitura_rele_falha_receb_rele_te = LeituraModbusBit(cls.rele["SE"], REG_RELE["SE"]["FALHA_PARTIDA_RECE_RELE_TE"], bit=2, descricao="[SE][RELE] Falha Partida Recebida Relé Transformador Elevador")
        cls.condicionadores_essenciais.append(CondicionadorBase(cls.leitura_rele_falha_receb_rele_te, CONDIC_INDISPONIBILIZAR))

        cls.leitura_rele_falha_abertura_dj_linha1 = LeituraModbusBit(cls.rele["SE"], REG_RELE["SE"]["FALHA_ABERTURA_DJ_LINHA"], bit=1, descricao="[SE][RELE] Disjuntor Linha Falha Abertura - BIT 01")
        cls.condicionadores_essenciais.append(CondicionadorBase(cls.leitura_rele_falha_abertura_dj_linha1, CONDIC_INDISPONIBILIZAR))

        cls.leitura_rele_falha_abertura_dj_linha2 = LeituraModbusBit(cls.rele["SE"], REG_RELE["SE"]["FALHA_ABERTURA_DJ_LINHA"], bit=3, descricao="[SE][RELE] Disjuntor Linha Falha Abertura - BIT 03")
        cls.condicionadores_essenciais.append(CondicionadorBase(cls.leitura_rele_falha_abertura_dj_linha2, CONDIC_INDISPONIBILIZAR))

        cls.leitura_rele_falha_abertura_dj_linha3 = LeituraModbusBit(cls.rele["SE"], REG_RELE["SE"]["FALHA_ABERTURA_DJ_LINHA"], bit=4, descricao="[SE][RELE] Disjuntor Linha Falha Abertura - BIT 04")
        cls.condicionadores_essenciais.append(CondicionadorBase(cls.leitura_rele_falha_abertura_dj_linha3, CONDIC_INDISPONIBILIZAR))

        cls.leitura_rele_sobrecorr_inst_seq_neg_z1 = LeituraModbusBit(cls.rele["SE"], REG_RELE["SE"]["SOBRECORR_INST_SEQUEN_NEG_Z1"], bit=3, descricao="[SE][RELE] Sobrecorrente Instantânea Sequência Negativa Z1")
        cls.condicionadores_essenciais.append(CondicionadorBase(cls.leitura_rele_sobrecorr_inst_seq_neg_z1, CONDIC_INDISPONIBILIZAR))

        cls.leitura_rele_sobrecorr_inst_seq_neg_z2 = LeituraModbusBit(cls.rele["SE"], REG_RELE["SE"]["SOBRECORR_INST_SEQUEN_NEG_Z2"], bit=2, descricao="[SE][RELE] Sobrecorrente Instantânea Sequência Negativa Z2")
        cls.condicionadores_essenciais.append(CondicionadorBase(cls.leitura_rele_sobrecorr_inst_seq_neg_z2, CONDIC_INDISPONIBILIZAR))

        cls.leitura_rele_sobrecorr_inst_seq_neg_z3 = LeituraModbusBit(cls.rele["SE"], REG_RELE["SE"]["SOBRECORR_INST_SEQUEN_NEG_Z3"], bit=1, descricao="[SE][RELE] Sobrecorrente Instantânea Sequência Negativa Z3")
        cls.condicionadores_essenciais.append(CondicionadorBase(cls.leitura_rele_sobrecorr_inst_seq_neg_z3, CONDIC_INDISPONIBILIZAR))

        cls.leitura_rele_86t_atuado = LeituraModbusBit(cls.rele["TE"], REG_RELE["TE"]["ATUA_86T"], bit=4, descricao="[TE][RELE] Atua 86T")
        cls.condicionadores_essenciais.append(CondicionadorBase(cls.leitura_rele_86t_atuado, CONDIC_INDISPONIBILIZAR))

        cls.leitura_rele_difer_com_restricao = LeituraModbusBit(cls.rele["TE"], REG_RELE["TE"]["DIFERENCIAL_COM_RESTRICAO"], bit=14, descricao="[TE][RELE] Diferencial Com Restrição")
        cls.condicionadores_essenciais.append(CondicionadorBase(cls.leitura_rele_difer_com_restricao, CONDIC_INDISPONIBILIZAR))

        cls.leitura_rele_difer_sem_restricao = LeituraModbusBit(cls.rele["TE"], REG_RELE["TE"]["DIFERENCIAL_SEM_RESTRICAO"], bit=15, descricao="[TE][RELE] Diferencial Sem Restrição")
        cls.condicionadores_essenciais.append(CondicionadorBase(cls.leitura_rele_difer_sem_restricao, CONDIC_INDISPONIBILIZAR))

        cls.leitura_rele_sobrecorr_temp_fase_enrol_prim = LeituraModbusBit(cls.rele["TE"], REG_RELE["TE"]["SOBRECORR_TEMP_FASE_ENROL_PRIM"], bit=3, descricao="[TE][RELE] Sobrecorrente Temperatura Fase Enrolamento Primário")
        cls.condicionadores_essenciais.append(CondicionadorBase(cls.leitura_rele_sobrecorr_temp_fase_enrol_prim, CONDIC_INDISPONIBILIZAR))

        cls.leitura_rele_sobrecorr_temp_res_enrol_prim = LeituraModbusBit(cls.rele["TE"], REG_RELE["TE"]["SOBRECORR_TEMP_RESIDUAL_ENROL_PRIM"], bit=4, descricao="[TE][RELE] Sobrecorrente Temperatura Residual Enrolamento Primário")
        cls.condicionadores_essenciais.append(CondicionadorBase(cls.leitura_rele_sobrecorr_temp_res_enrol_prim, CONDIC_INDISPONIBILIZAR))

        cls.leitura_rele_sobrecorr_temp_fase_enrol_sec = LeituraModbusBit(cls.rele["TE"], REG_RELE["TE"]["SOBRECORR_TEMP_FASE_ENROL_SEC"], bit=6, descricao="[TE][RELE] Sobrecorrente Temperatura Fase Enrolamento Secundário")
        cls.condicionadores_essenciais.append(CondicionadorBase(cls.leitura_rele_sobrecorr_temp_fase_enrol_sec, CONDIC_INDISPONIBILIZAR))

        cls.leitura_rele_sobrecorr_temp_res_enrol_sec = LeituraModbusBit(cls.rele["TE"], REG_RELE["TE"]["SOBRECORR_TEMP_RESIDUAL_ENROL_SEC"], bit=1, descricao="[TE][RELE] Sobrecorremnte Temperatura Residual Enrolamento Secundário")
        cls.condicionadores_essenciais.append(CondicionadorBase(cls.leitura_rele_sobrecorr_temp_res_enrol_sec, CONDIC_INDISPONIBILIZAR))