__version__ = "0.1"
__author__ = "Diego Basgal"
__description__ = "Este módulo corresponde a implementação da operação da Subestação."

import logging
import threading

from time import time

from usina import *
from bay import Bay

logger = logging.getLogger("__main__")

class Subestacao(Usina):
    def __init__(self, *args, **kwargs) -> ...:
        super().__init__(self, *args, **kwargs)

        self.__tensao_rs = LeituraModbus(self.clp["SA"], REG_CLP["SE"]["LT_VAB"], descricao="SE_LT_VAB")
        self.__tensao_st = LeituraModbus(self.clp["SA"], REG_CLP["SE"]["LT_VBC"], descricao="SE_LT_VBC")
        self.__tensao_tr = LeituraModbus(self.clp["SA"], REG_CLP["SE"]["LT_VCA"], descricao="SE_LT_VCA")

        self._condicionadores = []
        self._condicionadores_essenciais = []

    @property
    def tensao_rs(self) -> float:
        return self.__tensao_rs.valor

    @property
    def tensao_st(self) -> float:
        return self.__tensao_st.valor

    @property
    def tensao_tr(self) -> float:
        return self.__tensao_tr.valor

    @property
    def condicionadores(self) -> "list[CondicionadorBase]":
        return self._condicionadores

    @condicionadores.setter
    def condicionadores(self, var: "list[CondicionadorBase]") -> None:
        self._condicionadores = var

    @property
    def condicionadores_essenciais(self) -> "list[CondicionadorBase]":
        return self._condicionadores_essenciais

    @condicionadores_essenciais.setter
    def condicionadores_essenciais(self, var: "list[CondicionadorBase]") -> None:
        self._condicionadores_essenciais = var


    def verificar_condicionadores(self) -> int:
        if [condic.ativo for condic in self.condicionadores_essenciais]:
            condics_ativos = [condic for condics in [self.condicionadores_essenciais, self.condicionadores] for condic in condics if condic.ativo]
            condic_flag = [CONDIC_NORMALIZAR for condic in condics_ativos if condic.gravidade == CONDIC_NORMALIZAR]
            condic_flag = [CONDIC_INDISPONIBILIZAR for condic in condics_ativos if condic.gravidade == CONDIC_INDISPONIBILIZAR]

            if condic_flag in (CONDIC_NORMALIZAR, CONDIC_INDISPONIBILIZAR):
                logger.info("[SE] Foram detectados condicionadores ativos!")
                [logger.info(f"[SE] Condicionador: \"{condic.descr}\", Gravidade: \"{condic.gravidade}\".") for condic in condics_ativos]
        return condic_flag

    def fechar_Dj52L(self) -> bool:
        try:
            if self.verificar_condicoes_Dj52L():
                res = EscritaModBusBit.escrever_bit(self.clp["SA"], REG_CLP["SE"]["CMD_SE_FECHA_52L"], bit=4, valor=1)
                return res
            
        except Exception as e:
            logger.exception(f"[SE] Houve um erro ao realizar o fechamento do Disjuntor 52L. Exception: \"{repr(e)}\"")
            logger.debug(f"[SE] Traceback: {traceback.format_exc()}")

    def verificar_condicoes_Dj52L(self) -> bool:
        try:
            flags = 0

            if not self.dj_bay_fechado.valor:
                logger.warning("[SE] O disjuntor do Bay está aberto!")
                flags += 1

            if self.trip_rele_te.valor:
                logger.warning("[SE] O sinal de trip do relé do transformador elevador está ativado!")
                flags += 1

            if not self.barra_bay_morta.valor and self.barra_bay_viva.valor:
                logger.warning("[SE] Foi identificada leitura de corrente na barra do Bay!")
                flags += 1

            if not self.secc_bay_fechada.valor:
                logger.warning("[SE] A seccionadora do Bay está aberta!")
                flags += 1

            if self.alarme_gas_te.valor:
                logger.warning("[SE] Foi identificado sinal de alarme no Relé de Buchholz do Transformador Elevador!")
                flags += 1

            if not self.mola_carregada.valor:
                logger.warning("[SE] A mola do Disjuntor não está carregada!")
                flags += 1

            if not self.dj52l_remoto.valor:
                logger.warning("[SE] O Disjuntor não está em modo remoto!")
                flags += 1

            logger.warning(f"[SE] Foram identificadas \"{flags}\" condições de bloqueio ao realizar fechamento do Disjuntor. Favor normalizar.") \
                if flags > 0 else logger.debug("[SE] Condições de fechamento Dj52L OK! Fechando disjuntor...")

            return False if flags > 0 else True

        except Exception as e:
            logger.exception(f"[SE] Houve um erro ao verificar as pré-condições de fechameto do Dijuntor 52L. Exception: \"{repr(e)}\"")
            logger.debug(f"[SE] Traceback: {traceback.format_exc()}")
            return False

    def resetar_emergencia(self) -> bool:
        try:
            res = EscritaModBusBit.escrever_bit(self.clp["SA"], REG_CLP["SE"]["CMD_SE_REARME_BLOQUEIO_GERAL"], bit=0, valor=1)
            res = EscritaModBusBit.escrever_bit(self.clp["SA"], REG_CLP["SE"]["CMD_SE_REARME_86T"], bit=1, valor=1)
            res = EscritaModBusBit.escrever_bit(self.clp["SA"], REG_CLP["SE"]["CMD_SE_REARME_86BF"], bit=2, valor=1)
            res = EscritaModBusBit.escrever_bit(self.clp["SA"], REG_CLP["SE"]["REARME_86BF_86T"], bit=22, valor=1)
            res = EscritaModBusBit.escrever_bit(self.clp["SA"], REG_CLP["SE"]["CMD_SE_RESET_REGISTROS"], bit=5, valor=1)
            return res

        except Exception as e:
            logger.error(f"[SE] Houve um erro ao realizar o reset geral. Exception: \"{repr(e)}\"")
            logger.debug(f"[SE] Traceback: {traceback.format_exc()}")
            return False

    def verificar_tensao(self) -> bool:
        try:
            if (TENSAO_LINHA_BAIXA < self.tensao_rs < TENSAO_LINHA_ALTA) \
                and (TENSAO_LINHA_BAIXA < self.tensao_st < TENSAO_LINHA_ALTA) \
                and (TENSAO_LINHA_BAIXA < self.tensao_tr < TENSAO_LINHA_ALTA):
                return True
            else:
                logger.warning("[SE] Tensão da linha fora do limite.")
                return False

        except Exception as e:
            logger.error(f"[SE] Houve um erro ao realizar a verificação da tensão na linha. Exception: \"{repr(e)}\"")
            logger.debug(f"[SE] Traceback: {traceback.format_exc()}")
            return False

    def aguardar_tensao(self) -> bool:
        if self.status_tensao == TENSAO_VERIFICAR:
            self.status_tensao = TENSAO_AGUARDO
            logger.debug("[SE] Iniciando o timer para a normalização da tensão na linha.")
            threading.Thread(target=lambda: self.timeout_tensao(600)).start()

        elif self.status_tensao == TENSAO_REESTABELECIDA:
            logger.info("[SE] Tensão na linha reestabelecida.")
            self.status_tensao = TENSAO_VERIFICAR
            return True

        elif self.status_tensao == TENSAO_FORA:
            logger.critical("[SE] Não foi possível reestabelecer a tensão na linha. Acionando emergência")
            self.status_tensao = TENSAO_VERIFICAR
            return False

        else:
            logger.debug("[SE] A tensão na linha ainda está fora.")

    def timeout_tensao(self, delay) -> None:
        while time() <= time() + delay:
            if self.verificar_tensao():
                self.status_tensao = TENSAO_REESTABELECIDA
                return
            sleep(time() - (time() - 15))
        self.status_tensao = TENSAO_FORA

    def leitura_periodica(self) -> None:
        if not self.leitura_seletora_52l_remoto.valor:
            logger.warning("[SE] O Disjuntor 52L saiu do modo remoto. Favor verificar.")

        if self.leitura_falha_temp_oleo_te.valor:
            logger.warning("[SE] Houve uma falha de leitura de temperatura do óleo do transformador elevador. Favor verificar.")

        if self.leitura_falha_temp_enrolamento_te.valor:
            logger.warning("[SE] Houve uma falha de leitura de temperatura do enrolamento do transformador elevador. Favor verificar.")

        if self.leitura_alm_temperatura_oleo_te.valor and not Dicionarios.voip["TE_ALM_TEMPERATURA_OLEO"][0]:
            logger.warning("[SE] A temperatura do óleo do transformador elevador está alta. Favor verificar.")
            Dicionarios.voip["TE_ALM_TEMPERATURA_OLEO"][0] = True
        elif not self.leitura_alm_temperatura_oleo_te.valor and Dicionarios.voip["TE_ALM_TEMPERATURA_OLEO"][0]:
            Dicionarios.voip["TE_ALM_TEMPERATURA_OLEO"][0] = False

        if self.leitura_nivel_oleo_muito_alto_te.valor and not Dicionarios.voip["TE_NIVEL_OLEO_MUITO_ALTO"][0]:
            logger.warning("[SE] O nível do óleo do transformador elevador está muito alto. Favor verificar.")
            Dicionarios.voip["TE_NIVEL_OLEO_MUITO_ALTO"][0] = True
        elif not self.leitura_nivel_oleo_muito_alto_te.valor and Dicionarios.voip["TE_NIVEL_OLEO_MUITO_ALTO"][0]:
            Dicionarios.voip["TE_NIVEL_OLEO_MUITO_ALTO"][0] = False

        if self.leitura_nivel_oleo_muito_baixo_te.valor and not Dicionarios.voip["TE_NIVEL_OLEO_MUITO_BAIXO"][0]:
            logger.warning("[SE] O nível de óleo do tranformador elevador está muito baixo. Favor verificar.")
            Dicionarios.voip["TE_NIVEL_OLEO_MUITO_BAIXO"][0] = True
        elif not self.leitura_nivel_oleo_muito_baixo_te.valor and Dicionarios.voip["TE_NIVEL_OLEO_MUITO_BAIXO"][0]:
            Dicionarios.voip["TE_NIVEL_OLEO_MUITO_BAIXO"][0] = False

        if self.leitura_alarme_temperatura_oleo_te.valor and not Dicionarios.voip["TE_ALARME_TEMPERATURA_OLEO"][0]:
            logger.warning("[SE] A temperatura do óleo do transformador elevador está alta. Favor verificar.")
            Dicionarios.voip["TE_ALARME_TEMPERATURA_OLEO"][0] = True
        elif not self.leitura_alarme_temperatura_oleo_te.valor and Dicionarios.voip["TE_ALARME_TEMPERATURA_OLEO"][0]:
            Dicionarios.voip["TE_ALARME_TEMPERATURA_OLEO"][0] = False

        if self.leitura_alm_temp_enrolamento_te.valor and not Dicionarios.voip["TE_ALM_TEMPERATURA_ENROLAMENTO"][0]:
            logger.warning("[SE] A temperatura do enrolamento do transformador elevador está alta. Favor verificar.")
            Dicionarios.voip["TE_ALM_TEMPERATURA_ENROLAMENTO"][0] = True
        elif not self.leitura_alm_temp_enrolamento_te.valor and Dicionarios.voip["TE_ALM_TEMPERATURA_ENROLAMENTO"][0]:
            Dicionarios.voip["TE_ALM_TEMPERATURA_ENROLAMENTO"][0] = False

        if self.leitura_alarme_temp_enrolamento_te.valor and not Dicionarios.voip["TE_ALARME_TEMPERATURA_ENROLAMENTO"][0]:
            logger.warning("[SE] A temperatura do enrolamento do transformador elevador está alta. Favor verificar.")
            Dicionarios.voip["TE_ALARME_TEMPERATURA_ENROLAMENTO"][0] = True
        elif not self.leitura_alarme_temp_enrolamento_te.valor and Dicionarios.voip["TE_ALARME_TEMPERATURA_ENROLAMENTO"][0]:
            Dicionarios.voip["TE_ALARME_TEMPERATURA_ENROLAMENTO"][0] = False


    def iniciar_leituras_condicionadores(self) -> None:
        # Satatus Disjuntor 52L
        self.dj_se = LeituraModbusBit(self.rele["SE"], REG_RELE["SE"]["DJ_LINHA_FECHADO"], bit=0, descricao="BAY_DJ_LINHA_FECHADO")
        
        # Pré-condições de fechamento do Dj52L
        self.trip_rele_te = LeituraModbusBit(self.rele["TE"], REG_RELE["TE"]["RELE_ESTADO_TRIP"], bit=15, descricao="TE_RELE_ESTADO_TRIP")
        self.dj_bay_fechado = LeituraModbusBit(self.rele["BAY"], REG_RELE["BAY"]["DJ_LINHA_FECHADO"], bit=0, descricao="BAY_DJ_LINHA_FECHADO")
        self.barra_bay_morta = LeituraModbusBit(self.rele["BAY"], REG_RELE["BAY"]["ID_BARRA_MORTA"], bit=7, descricao="BAY_ID_BARRA_MORTA")
        self.barra_bay_viva = LeituraModbusBit(self.rele["BAY"], REG_RELE["BAY"]["ID_BARRA_VIVA"], bit=1, descricao="BAY_ID_BARRA_VIVA")
        self.secc_bay_fechada = LeituraModbusBit(self.rele["BAY"], REG_RELE["BAY"]["SECC_FECHADA"], bit=4, descricao="BAY_SECC_FECHADA")
        self.alarme_gas_te = LeituraModbusBit(self.clp["SA"], REG_CLP["SE"]["TE_ALARME_RELE_BUCHHOLZ"], bit=22, descricao="TE_ALARME_RELE_BUCHHOLZ")
        self.mola_carregada = LeituraModbusBit(self.clp["SA"], REG_CLP["SE"]["52L_MOLA_CARREGADA"], bit=16, descricao="52L_MOLA_CARREGADA")
        self.dj52l_remoto = LeituraModbusBit(self.clp["SA"], REG_CLP["SE"]["52L_SELETORA_REMOTO"], bit=10, descricao="52L_SELETORA_REMOTO")

        # CONDICIONADORES ESSENCIAIS
        # Normalizar
            # Bit Normal
        self.leitura_rele_linha_atuado = LeituraModbusBit(self.clp["SA"], REG_CLP["SE"]["RELE_LINHA_ATUADO"], bit=14, descricao="SE_RELE_LINHA_ATUADO")
        self.condicionadores_essenciais.append(CondicionadorBase(self.leitura_rele_linha_atuado, CONDIC_NORMALIZAR))

        # CONDICIONADORES
        # Indisponibilizar
            # Bit Invertido
        self.leitura_89l_fechada = LeituraModbusBit(self.clp["SA"], REG_CLP["SE"]["89L_FECHADA"], bit=12, invertido=True, descricao="SE_89L_FECHADA")
        self.condicionadores.append(CondicionadorBase(self.leitura_89l_fechada, CONDIC_INDISPONIBILIZAR))

            # Bit Normal
        self.leitura_86t_atuado = LeituraModbusBit(self.clp["SA"], REG_CLP["SE"]["86T_ATUADO"], bit=20, descricao="SE_86T_ATUADO")
        self.condicionadores.append(CondicionadorBase(self.leitura_86t_atuado, CONDIC_INDISPONIBILIZAR))

        self.leitura_86bf_atuado = LeituraModbusBit(self.clp["SA"], REG_CLP["SE"]["86BF_ATUADO"], bit=19, descricao="SE_86BF_ATUADO")
        self.condicionadores.append(CondicionadorBase(self.leitura_86bf_atuado, CONDIC_INDISPONIBILIZAR))

        self.leitura_rele_te_atuado = LeituraModbusBit(self.clp["SA"], REG_CLP["SE"]["TE_RELE_ATUADO"], bit=17, descricao="SE_TE_RELE_ATUADO")
        self.condicionadores.append(CondicionadorBase(self.leitura_rele_te_atuado, CONDIC_INDISPONIBILIZAR))

        self.leitura_trip_rele_buchholz = LeituraModbusBit(self.clp["SA"], REG_CLP["SE"]["TE_TRIP_RELE_BUCHHOLZ"], bit=23, descricao="SE_TE_TRIP_RELE_BUCHHOLZ")
        self.condicionadores.append(CondicionadorBase(self.leitura_trip_rele_buchholz, CONDIC_INDISPONIBILIZAR))

        self.leitura_trip_alivio_pressao = LeituraModbusBit(self.clp["SA"], REG_CLP["SE"]["TE_TRIP_ALIVIO_PRESSAO"], bit=24, descricao="SE_TE_TRIP_ALIVIO_PRESSAO")
        self.condicionadores.append(CondicionadorBase(self.leitura_trip_alivio_pressao, CONDIC_INDISPONIBILIZAR))

        self.leitura_trip_temp_oleo_te = LeituraModbusBit(self.clp["SA"], REG_CLP["SE"]["TE_TRIP_TEMPERATURA_OLEO"], bit=19, descricao="SE_TE_TRIP_TEMPERATURA_OLEO")
        self.condicionadores.append(CondicionadorBase(self.leitura_trip_temp_oleo_te, CONDIC_INDISPONIBILIZAR))

        self.leitura_atuacao_rele_linha_bf = LeituraModbusBit(self.clp["SA"], REG_CLP["SE"]["RELE_LINHA_ATUACAO_BF"], bit=16, descricao="SE_RELE_LINHA_ATUACAO_BF")
        self.condicionadores.append(CondicionadorBase(self.leitura_atuacao_rele_linha_bf, CONDIC_INDISPONIBILIZAR))

        self.leitura_alarme_rele_buchholz = LeituraModbusBit(self.clp["SA"], REG_CLP["SE"]["TE_ALARME_RELE_BUCHHOLZ"], bit=22, descricao="SE_TE_ALARME_RELE_BUCHHOLZ")
        self.condicionadores.append(CondicionadorBase(self.leitura_alarme_rele_buchholz, CONDIC_INDISPONIBILIZAR))

        self.leitura_trip_temp_enrol_te = LeituraModbusBit(self.clp["SA"], REG_CLP["SE"]["TE_TRIP_TEMPERATURA_ENROLAMENTO"], bit=20, descricao="SE_TE_TRIP_TEMPERATURA_ENROLAMENTO")
        self.condicionadores.append(CondicionadorBase(self.leitura_trip_temp_enrol_te, CONDIC_INDISPONIBILIZAR))

        self.leitura_falha_comando_abertura_52l = LeituraModbusBit(self.clp["SA"], REG_CLP["SE"]["FALHA_COMANDO_ABERTURA_52L"], bit=1, descricao="SE_FALHA_COMANDO_ABERTURA_52L")
        self.condicionadores.append(CondicionadorBase(self.leitura_falha_comando_abertura_52l, CONDIC_INDISPONIBILIZAR))

        self.leitura_falha_comando_fechamento_52l = LeituraModbusBit(self.clp["SA"], REG_CLP["SE"]["FALHA_COMANDO_FECHAMENTO_52L"], bit=2, descricao="SE_FALHA_COMANDO_FECHAMENTO_52L")
        self.condicionadores.append(CondicionadorBase(self.leitura_falha_comando_fechamento_52l, CONDIC_INDISPONIBILIZAR))

        self.leitura_super_bobinas_reles_bloq = LeituraModbusBit(self.clp["SA"], REG_CLP["SE"]["SUPERVISAO_BOBINAS_RELES_BLOQUEIOS"], bit=21, descricao="SE_SUPERVISAO_BOBINAS_RELES_BLOQUEIOS")
        self.condicionadores.append(CondicionadorBase(self.leitura_super_bobinas_reles_bloq, CONDIC_INDISPONIBILIZAR))

        # LEITURAS PARA LEITURA PERIÓDICA
        # Telegram
            # Bit Invertido
        self.leitura_seletora_52l_remoto = LeituraModbusBit(self.clp["SA"], REG_CLP["SE"]["52L_SELETORA_REMOTO"], bit=10, invertido=True, descricao="SE_52L_SELETORA_REMOTO")

            # Bit Normal
        self.leitura_falha_temp_oleo_te = LeituraModbusBit(self.clp["SA"], REG_CLP["SE"]["TE_FALHA_TEMPERATURA_OLEO"], bit=1, descricao="TE_FALHA_TEMPERATURA_OLEO")
        self.leitura_falha_temp_enrolamento_te = LeituraModbusBit(self.clp["SA"], REG_CLP["SE"]["TE_FALHA_TEMPERATURA_ENROLAMENTO"], bit=2, descricao="TE_FALHA_TEMPERATURA_ENROLAMENTO")

        # Telegram + Voip
            # Bit Normal
        self.leitura_alm_temperatura_oleo_te = LeituraModbusBit(self.clp["SA"], REG_CLP["SE"]["TE_ALM_TEMPERATURA_OLEO"], bit=1, descricao="TE_ALM_TEMPERATURA_OLEO")
        self.leitura_nivel_oleo_muito_alto_te = LeituraModbusBit(self.clp["SA"], REG_CLP["SE"]["TE_NIVEL_OLEO_MUITO_ALTO"], bit=26, descricao="TE_NIVEL_OLEO_MUITO_ALTO")
        self.leitura_nivel_oleo_muito_baixo_te = LeituraModbusBit(self.clp["SA"], REG_CLP["SE"]["TE_NIVEL_OLEO_MUITO_BAIXO"], bit=27, descricao="TE_NIVEL_OLEO_MUITO_BAIXO")
        self.leitura_alm_temp_enrolamento_te = LeituraModbusBit(self.clp["SA"], REG_CLP["SE"]["TE_ALM_TEMPERATURA_ENROLAMENTO"], bit=2, descricao="TE_ALM_TEMPERATURA_ENROLAMENTO")
        self.leitura_alarme_temperatura_oleo_te = LeituraModbusBit(self.clp["SA"], REG_CLP["SE"]["TE_ALARME_TEMPERATURA_OLEO"], bit=18, descricao="TE_ALARME_TEMPERATURA_OLEO")
        self.leitura_alarme_temp_enrolamento_te = LeituraModbusBit(self.clp["SA"], REG_CLP["SE"]["TE_ALARME_TEMPERATURA_ENROLAMENTO"], bit=20, descricao="TE_ALARME_TEMPERATURA_ENROLAMENTO")


        # CONDICIONADORES RELÉS
        self.leitura_rele_falha_receb_rele_te = LeituraModbusBit(self.rele["SE"], REG_RELE["SE"]["FALHA_PARTIDA_RECE_RELE_TE"], bit=2, descricao="RELE_SE_FALHA_PARTIDA_RECE_RELE_TE")
        self.condicionadores_essenciais.append(CondicionadorBase(self.leitura_rele_falha_receb_rele_te, CONDIC_INDISPONIBILIZAR))
                
        self.leitura_rele_falha_abertura_dj_linha1 = LeituraModbusBit(self.rele["SE"], REG_RELE["SE"]["FALHA_ABERTURA_DJ_LINHA"], bit=1, descricao="RELE_SE_FALHA_ABERTURA_DJ_LINHA - bit 01")
        self.condicionadores_essenciais.append(CondicionadorBase(self.leitura_rele_falha_abertura_dj_linha1, CONDIC_INDISPONIBILIZAR))
        
        self.leitura_rele_falha_abertura_dj_linha2 = LeituraModbusBit(self.rele["SE"], REG_RELE["SE"]["FALHA_ABERTURA_DJ_LINHA"], bit=3, descricao="RELE_SE_FALHA_ABERTURA_DJ_LINHA - bit 03")
        self.condicionadores_essenciais.append(CondicionadorBase(self.leitura_rele_falha_abertura_dj_linha2, CONDIC_INDISPONIBILIZAR))
        
        self.leitura_rele_falha_abertura_dj_linha3 = LeituraModbusBit(self.rele["SE"], REG_RELE["SE"]["FALHA_ABERTURA_DJ_LINHA"], bit=4, descricao="RELE_SE_FALHA_ABERTURA_DJ_LINHA - bit 04")
        self.condicionadores_essenciais.append(CondicionadorBase(self.leitura_rele_falha_abertura_dj_linha3, CONDIC_INDISPONIBILIZAR))
        
        self.leitura_rele_sobrecorr_inst_seq_neg_z1 = LeituraModbusBit(self.rele["SE"], REG_RELE["SE"]["SOBRECORR_INST_SEQUEN_NEG_Z1"], bit=3, descricao="RELE_SE_SOBRECORR_INST_SEQUEN_NEG_Z1")
        self.condicionadores_essenciais.append(CondicionadorBase(self.leitura_rele_sobrecorr_inst_seq_neg_z1, CONDIC_INDISPONIBILIZAR))
        
        self.leitura_rele_sobrecorr_inst_seq_neg_z2 = LeituraModbusBit(self.rele["SE"], REG_RELE["SE"]["SOBRECORR_INST_SEQUEN_NEG_Z2"], bit=2, descricao="RELE_SE_SOBRECORR_INST_SEQUEN_NEG_Z2")
        self.condicionadores_essenciais.append(CondicionadorBase(self.leitura_rele_sobrecorr_inst_seq_neg_z2, CONDIC_INDISPONIBILIZAR))
        
        self.leitura_rele_sobrecorr_inst_seq_neg_z3 = LeituraModbusBit(self.rele["SE"], REG_RELE["SE"]["SOBRECORR_INST_SEQUEN_NEG_Z3"], bit=1, descricao="RELE_SE_SOBRECORR_INST_SEQUEN_NEG_Z3")
        self.condicionadores_essenciais.append(CondicionadorBase(self.leitura_rele_sobrecorr_inst_seq_neg_z3, CONDIC_INDISPONIBILIZAR))

        self.leitura_rele_86t_atuado = LeituraModbusBit(self.rele["TE"], REG_RELE["TE"]["ATUA_86T"], bit=4, descricao="RELE_TE_ATUA_86T")
        self.condicionadores_essenciais.append(CondicionadorBase(self.leitura_rele_86t_atuado, CONDIC_INDISPONIBILIZAR))

        self.leitura_rele_difer_com_restricao = LeituraModbusBit(self.rele["TE"], REG_RELE["TE"]["DIFERENCIAL_COM_RESTRICAO"], bit=14, descricao="RELE_TE_DIFERENCIAL_COM_RESTRICAO")
        self.condicionadores_essenciais.append(CondicionadorBase(self.leitura_rele_difer_com_restricao, CONDIC_INDISPONIBILIZAR))

        self.leitura_rele_difer_sem_restricao = LeituraModbusBit(self.rele["TE"], REG_RELE["TE"]["DIFERENCIAL_SEM_RESTRICAO"], bit=15, descricao="RELE_TE_DIFERENCIAL_SEM_RESTRICAO")
        self.condicionadores_essenciais.append(CondicionadorBase(self.leitura_rele_difer_sem_restricao, CONDIC_INDISPONIBILIZAR))

        self.leitura_rele_sobrecorr_temp_fase_enrol_prim = LeituraModbusBit(self.rele["TE"], REG_RELE["TE"]["SOBRECORR_TEMP_FASE_ENROL_PRIM"], bit=3, descricao="RELE_TE_SOBRECORR_TEMP_FASE_ENROL_PRIM")
        self.condicionadores_essenciais.append(CondicionadorBase(self.leitura_rele_sobrecorr_temp_fase_enrol_prim, CONDIC_INDISPONIBILIZAR))

        self.leitura_rele_sobrecorr_temp_res_enrol_prim = LeituraModbusBit(self.rele["TE"], REG_RELE["TE"]["SOBRECORR_TEMP_RESIDUAL_ENROL_PRIM"], bit=4, descricao="RELE_TE_SOBRECORR_TEMP_RESIDUAL_ENROL_PRIM")
        self.condicionadores_essenciais.append(CondicionadorBase(self.leitura_rele_sobrecorr_temp_res_enrol_prim, CONDIC_INDISPONIBILIZAR))

        self.leitura_rele_sobrecorr_temp_fase_enrol_sec = LeituraModbusBit(self.rele["TE"], REG_RELE["TE"]["SOBRECORR_TEMP_FASE_ENROL_SEC"], bit=6, descricao="RELE_TE_SOBRECORR_TEMP_FASE_ENROL_SEC")
        self.condicionadores_essenciais.append(CondicionadorBase(self.leitura_rele_sobrecorr_temp_fase_enrol_sec, CONDIC_INDISPONIBILIZAR))

        self.leitura_rele_sobrecorr_temp_res_enrol_sec = LeituraModbusBit(self.rele["TE"], REG_RELE["TE"]["SOBRECORR_TEMP_RESIDUAL_ENROL_SEC"], bit=1, descricao="RELE_TE_SOBRECORR_TEMP_RESIDUAL_ENROL_SEC")
        self.condicionadores_essenciais.append(CondicionadorBase(self.leitura_rele_sobrecorr_temp_res_enrol_sec, CONDIC_INDISPONIBILIZAR))