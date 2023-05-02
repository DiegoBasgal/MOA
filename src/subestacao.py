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

        self.__tensao_rs = LeituraModbus(OPC_UA["SE"]["LT_VAB"])
        self.__tensao_st = LeituraModbus(OPC_UA["SE"]["LT_VBC"])
        self.__tensao_tr = LeituraModbus(OPC_UA["SE"]["LT_VCA"])

        self._condicionadores = []
        self._condicionadores_essenciais = []

    @property
    def tensao_rs(self) -> int | float:
        return self.__tensao_rs.valor

    @property
    def tensao_st(self) -> int | float:
        return self.__tensao_st.valor

    @property
    def tensao_tr(self) -> int | float:
        return self.__tensao_tr.valor

    @property
    def condicionadores(self) -> list[CondicionadorBase]:
        return self._condicionadores

    @condicionadores.setter
    def condicionadores(self, var: list[CondicionadorBase]) -> None:
        self._condicionadores = var

    @property
    def condicionadores_essenciais(self) -> list[CondicionadorBase]:
        return self._condicionadores_essenciais

    @condicionadores_essenciais.setter
    def condicionadores_essenciais(self, var: list[CondicionadorBase]) -> None:
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

    def fechar_Dj52L(self):
        return EscritaModBusBit.escrever_bit(self.clp["SA"], OPC_UA["SE"]["CMD_SE_FECHA_52L"], valor=1, bit=4)

    def resetar_emergencia(self) -> bool:
        try:
            res = 0
            res += 1 if EscritaModBusBit.escrever_bit(self.clp["SA"], OPC_UA["SE"]["CMD_SE_REARME_BLOQUEIO_GERAL"], valor=1, bit=0) else ...
            res += 1 if EscritaModBusBit.escrever_bit(self.clp["SA"], OPC_UA["SE"]["CMD_SE_REARME_86T"], valor=1, bit=1) else ...
            res += 1 if EscritaModBusBit.escrever_bit(self.clp["SA"], OPC_UA["SE"]["CMD_SE_REARME_86BF"], valor=1, bit=2) else ...
            res += 1 if EscritaModBusBit.escrever_bit(self.clp["SA"], OPC_UA["SE"]["REARME_86BF_86T"], valor=1, bit=22) else ...
            res += 1 if EscritaModBusBit.escrever_bit(self.clp["SA"], OPC_UA["SE"]["CMD_SE_RESET_REGISTROS"], valor=1, bit=5) else ...
            return True if res == 5 else False

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

    def aguardar_tensao(self) -> bool:
        if self.status_tensao == 0:
            self.status_tensao = 1
            logger.debug("[SE] Iniciando o timer para a normalização da tensão na linha.")
            threading.Thread(target=lambda: self.timeout_tensao(600)).start()

        elif self.status_tensao == 2:
            logger.info("[SE] Tensão na linha reestabelecida.")
            self.status_tensao = 0
            return True

        elif self.status_tensao == 3:
            logger.critical("[SE] Não foi possível reestabelecer a tensão na linha. Acionando emergência")
            self.status_tensao = 0
            return False

        else:
            logger.debug("[SE] A tensão na linha ainda está fora.")

    def timeout_tensao(self, delay) -> None:
        while time() <= time() + delay:
            if self.verificar_tensao():
                self.status_tensao = 2
                return
            sleep(time() - (time() - 15))
        self.status_tensao = 3

    def leitura_periodica(self) -> None:
        if not self.leitura_seletora_52l_remoto:
            logger.warning("[SE] O Disjuntor 52L saiu do modo remoto. Favor verificar.")

        if self.leitura_falha_temp_oleo_te:
            logger.warning("[SE] Houve uma falha de leitura de temperatura do óleo do transformador elevador. Favor verificar.")

        if self.leitura_falha_temp_enrolamento_te:
            logger.warning("[SE] Houve uma falha de leitura de temperatura do enrolamento do transformador elevador. Favor verificar.")

        if self.leitura_alm_temperatura_oleo_te and not Dicionarios.voip["TE_ALM_TEMPERATURA_OLEO"][0]:
            logger.warning("[SE] A temperatura do óleo do transformador elevador está alta. Favor verificar.")
            Dicionarios.voip["TE_ALM_TEMPERATURA_OLEO"][0] = True
        elif not self.leitura_alm_temperatura_oleo_te and Dicionarios.voip["TE_ALM_TEMPERATURA_OLEO"][0]:
            Dicionarios.voip["TE_ALM_TEMPERATURA_OLEO"][0] = False

        if self.leitura_nivel_oleo_muito_alto_te and not Dicionarios.voip["TE_NIVEL_OLEO_MUITO_ALTO"][0]:
            logger.warning("[SE] O nível do óleo do transformador elevador está muito alto. Favor verificar.")
            Dicionarios.voip["TE_NIVEL_OLEO_MUITO_ALTO"][0] = True
        elif not self.leitura_nivel_oleo_muito_alto_te and Dicionarios.voip["TE_NIVEL_OLEO_MUITO_ALTO"][0]:
            Dicionarios.voip["TE_NIVEL_OLEO_MUITO_ALTO"][0] = False
        
        if self.leitura_nivel_oleo_muito_baixo_te and not Dicionarios.voip["TE_NIVEL_OLEO_MUITO_BAIXO"][0]:
            logger.warning("[SE] O nível de óleo do tranformador elevador está muito baixo. Favor verificar.")
            Dicionarios.voip["TE_NIVEL_OLEO_MUITO_BAIXO"][0] = True
        elif not self.leitura_nivel_oleo_muito_baixo_te and Dicionarios.voip["TE_NIVEL_OLEO_MUITO_BAIXO"][0]:
            Dicionarios.voip["TE_NIVEL_OLEO_MUITO_BAIXO"][0] = False

        if self.leitura_alarme_temperatura_oleo_te and not Dicionarios.voip["TE_ALARME_TEMPERATURA_OLEO"][0]:
            logger.warning("[SE] A temperatura do óleo do transformador elevador está alta. Favor verificar.")
            Dicionarios.voip["TE_ALARME_TEMPERATURA_OLEO"][0] = True
        elif not self.leitura_alarme_temperatura_oleo_te and Dicionarios.voip["TE_ALARME_TEMPERATURA_OLEO"][0]:
            Dicionarios.voip["TE_ALARME_TEMPERATURA_OLEO"][0] = False

        if self.leitura_alm_temp_enrolamento_te and not Dicionarios.voip["TE_ALM_TEMPERATURA_ENROLAMENTO"][0]:
            logger.warning("[SE] A temperatura do enrolamento do transformador elevador está alta. Favor verificar.")
            Dicionarios.voip["TE_ALM_TEMPERATURA_ENROLAMENTO"][0] = True
        elif not self.leitura_alm_temp_enrolamento_te and Dicionarios.voip["TE_ALM_TEMPERATURA_ENROLAMENTO"][0]:
            Dicionarios.voip["TE_ALM_TEMPERATURA_ENROLAMENTO"][0] = False
        
        if self.leitura_alarme_temp_enrolamento_te and not Dicionarios.voip["TE_ALARME_TEMPERATURA_ENROLAMENTO"][0]:
            logger.warning("[SE] A temperatura do enrolamento do transformador elevador está alta. Favor verificar.")
            Dicionarios.voip["TE_ALARME_TEMPERATURA_ENROLAMENTO"][0] = True
        elif not self.leitura_alarme_temp_enrolamento_te and Dicionarios.voip["TE_ALARME_TEMPERATURA_ENROLAMENTO"][0]:
            Dicionarios.voip["TE_ALARME_TEMPERATURA_ENROLAMENTO"][0] = False


    def iniciar_leituras_condicionadores(self) -> None:
        # CONDICIONADORES ESSENCIAIS
        # Normalizar
            # Bit Normal
        self.leitura_rele_linha_atuado = LeituraModbusBit(OPC_UA["SE"]["RELE_LINHA_ATUADO"], 14, "SE_RELE_LINHA_ATUADO")
        self.condicionadores_essenciais.append(CondicionadorBase(self.leitura_rele_linha_atuado, CONDIC_NORMALIZAR))

        # CONDICIONADORES
        # Indisponibilizar
            # Bit Invertido
        self.leitura_89l_fechada = LeituraModbusBit(OPC_UA["SE"]["89L_FECHADA"], 12, True, "SE_89L_FECHADA")
        self.condicionadores.append(CondicionadorBase(self.leitura_89l_fechada, CONDIC_INDISPONIBILIZAR))

            # Bit Normal
        self.leitura_86t_atuado = LeituraModbusBit(OPC_UA["SE"]["86T_ATUADO"], 20, "SE_86T_ATUADO")
        self.condicionadores.append(CondicionadorBase(self.leitura_86t_atuado, CONDIC_INDISPONIBILIZAR))
        
        self.leitura_86bf_atuado = LeituraModbusBit(OPC_UA["SE"]["86BF_ATUADO"], 19, "SE_86BF_ATUADO")
        self.condicionadores.append(CondicionadorBase(self.leitura_86bf_atuado, CONDIC_INDISPONIBILIZAR))

        self.leitura_rele_te_atuado = LeituraModbusBit(OPC_UA["SE"]["TE_RELE_ATUADO"], 17, "SE_TE_RELE_ATUADO")
        self.condicionadores.append(CondicionadorBase(self.leitura_rele_te_atuado, CONDIC_INDISPONIBILIZAR))

        self.leitura_trip_rele_buchholz = LeituraModbusBit(OPC_UA["SE"]["TE_TRIP_RELE_BUCHHOLZ"], 23, "SE_TE_TRIP_RELE_BUCHHOLZ")
        self.condicionadores.append(CondicionadorBase(self.leitura_trip_rele_buchholz, CONDIC_INDISPONIBILIZAR))

        self.leitura_trip_alivio_pressao = LeituraModbusBit(OPC_UA["SE"]["TE_TRIP_ALIVIO_PRESSAO"], 24, "SE_TE_TRIP_ALIVIO_PRESSAO")
        self.condicionadores.append(CondicionadorBase(self.leitura_trip_alivio_pressao, CONDIC_INDISPONIBILIZAR))

        self.leitura_trip_temp_oleo_te = LeituraModbusBit(OPC_UA["SE"]["TE_TRIP_TEMPERATURA_OLEO"], 19, "SE_TE_TRIP_TEMPERATURA_OLEO")
        self.condicionadores.append(CondicionadorBase(self.leitura_trip_temp_oleo_te, CONDIC_INDISPONIBILIZAR))

        self.leitura_atuacao_rele_linha_bf = LeituraModbusBit(OPC_UA["SE"]["RELE_LINHA_ATUACAO_BF"], 16, "SE_RELE_LINHA_ATUACAO_BF")
        self.condicionadores.append(CondicionadorBase(self.leitura_atuacao_rele_linha_bf, CONDIC_INDISPONIBILIZAR))

        self.leitura_alarme_rele_buchholz = LeituraModbusBit(OPC_UA["SE"]["TE_ALARME_RELE_BUCHHOLZ"], 22, "SE_TE_ALARME_RELE_BUCHHOLZ")
        self.condicionadores.append(CondicionadorBase(self.leitura_alarme_rele_buchholz, CONDIC_INDISPONIBILIZAR))

        self.leitura_trip_temp_enrol_te = LeituraModbusBit(OPC_UA["SE"]["TE_TRIP_TEMPERATURA_ENROLAMENTO"], 20, "SE_TE_TRIP_TEMPERATURA_ENROLAMENTO")
        self.condicionadores.append(CondicionadorBase(self.leitura_trip_temp_enrol_te, CONDIC_INDISPONIBILIZAR))

        self.leitura_falha_comando_abertura_52l = LeituraModbusBit(OPC_UA["SE"]["FALHA_COMANDO_ABERTURA_52L"], 1, "SE_FALHA_COMANDO_ABERTURA_52L")
        self.condicionadores.append(CondicionadorBase(self.leitura_falha_comando_abertura_52l, CONDIC_INDISPONIBILIZAR))

        self.leitura_falha_comando_fechamento_52l = LeituraModbusBit(OPC_UA["SE"]["FALHA_COMANDO_FECHAMENTO_52L"], 2, "SE_FALHA_COMANDO_FECHAMENTO_52L")
        self.condicionadores.append(CondicionadorBase(self.leitura_falha_comando_fechamento_52l, CONDIC_INDISPONIBILIZAR))

        self.leitura_super_bobinas_reles_bloq = LeituraModbusBit(OPC_UA["SE"]["SUPERVISAO_BOBINAS_RELES_BLOQUEIOS"], 21, "SE_SUPERVISAO_BOBINAS_RELES_BLOQUEIOS")
        self.condicionadores.append(CondicionadorBase(self.leitura_super_bobinas_reles_bloq, CONDIC_INDISPONIBILIZAR))

        # LEITURAS PARA LEITURA PERIÓDICA
        # Telegram
            # Bit Invertido
        self.leitura_seletora_52l_remoto = LeituraModbusBit(OPC_UA["SE"]["52L_SELETORA_REMOTO"], 10, True)

            # Bit Normal
        self.leitura_falha_temp_oleo_te = LeituraModbusBit(OPC_UA["SE"]["TE_FALHA_TEMPERATURA_OLEO"], 1)
        self.leitura_falha_temp_enrolamento_te = LeituraModbusBit(OPC_UA["SE"]["TE_FALHA_TEMPERATURA_ENROLAMENTO"], 2)

        # Telegram + Voip
            # Bit Normal
        self.leitura_alm_temperatura_oleo_te = LeituraModbusBit(OPC_UA["SE"]["TE_ALM_TEMPERATURA_OLEO"], 1)
        self.leitura_nivel_oleo_muito_alto_te = LeituraModbusBit(OPC_UA["SE"]["TE_NIVEL_OLEO_MUITO_ALTO"], 26)
        self.leitura_nivel_oleo_muito_baixo_te = LeituraModbusBit(OPC_UA["SE"]["TE_NIVEL_OLEO_MUITO_BAIXO"], 27)
        self.leitura_alm_temp_enrolamento_te = LeituraModbusBit(OPC_UA["SE"]["TE_ALM_TEMPERATURA_ENROLAMENTO"], 2)
        self.leitura_alarme_temperatura_oleo_te = LeituraModbusBit(OPC_UA["SE"]["TE_ALARME_TEMPERATURA_OLEO"], 18)
        self.leitura_alarme_temp_enrolamento_te = LeituraModbusBit(OPC_UA["SE"]["TE_ALARME_TEMPERATURA_ENROLAMENTO"], 20)