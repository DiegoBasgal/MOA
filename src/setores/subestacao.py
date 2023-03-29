__version__ = "0.1"
__author__ = "Diego Basgal"
__description__ = "Este módulo corresponde a implementação da operação da Subestação."

import logging
import threading

from time import time

from usina import *
from setores.bay import Bay

logger = logging.getLogger("__main__")

class Subestacao(Usina):
    def __init__(self, dicionario: dict | None = ..., conversor : NativoParaExterno | None = ...) -> ...:
        self.bay = Bay.__init__(self, conversor)

        self.__tensao_rs = LeituraOpc(OPC_UA["LT_VAB"])
        self.__tensao_st = LeituraOpc(OPC_UA["LT_VBC"])
        self.__tensao_tr = LeituraOpc(OPC_UA["LT_VCA"])

        self._condicionadores = []
        self._condicionadores_essenciais = []

        self.dct = dicionario
        self.escrita_opc: EscritaOpc | EscritaOpcBit = EscritaOpc()

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

    def fechar_Dj52L(self):
        """if not self.get_flag_falha52L():
            return False
        else:"""
        # utilizar o write_value_bool para o ambiente em produção e write_single_register para a simulação
        res = self.escrita_opc.escrever_bit(OPC_UA["SE"]["CMD_SE_FECHA_52L"], valor=1, bit=4)
        return res

    def resetar_emergencia(self) -> bool:
        try:
            res = 0
            res += 1 if self.escrita_opc.escrever_bit(OPC_UA["SE"]["CMD_SE_REARME_BLOQUEIO_GERAL"], valor=1, bit=0) else ...
            res += 1 if self.escrita_opc.escrever_bit(OPC_UA["SE"]["CMD_SE_REARME_86T"], valor=1, bit=1) else ...
            res += 1 if self.escrita_opc.escrever_bit(OPC_UA["SE"]["CMD_SE_REARME_86BF"], valor=1, bit=2) else ...
            res += 1 if self.escrita_opc.escrever_bit(OPC_UA["SE"]["REARME_86BF_86T"], valor=1, bit=22) else ...
            res += 1 if self.escrita_opc.escrever_bit(OPC_UA["SE"]["CMD_SE_RESET_REGISTROS"], valor=1, bit=5) else ...
            return True if res == 5 else False

        except Exception as e:
            logger.exception(f"[SE] Houve um erro ao realizar o reset geral. Exception: \"{repr(e)}\"")
            logger.exception(f"[SE] Traceback: {traceback.print_stack}")
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
            logger.exception(f"[SE] Houve um erro ao realizar a verificação da tensão na linha. Exception: \"{repr(e)}\"")
            logger.exception(f"[SE] Traceback: {traceback.print_stack}")

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

        if self.leitura_alm_temperatura_oleo_te and not self.dct["VOIP"]["TE_ALM_TEMPERATURA_OLEO"]:
            logger.warning("[SE] A temperatura do óleo do transformador elevador está alta. Favor verificar.")
            self.dct["VOIP"]["TE_ALM_TEMPERATURA_OLEO"] = True
            self.acionar_voip = True
        elif not self.leitura_alm_temperatura_oleo_te and self.dct["VOIP"]["TE_ALM_TEMPERATURA_OLEO"]:
            self.dct["VOIP"]["TE_ALM_TEMPERATURA_OLEO"] = False

        if self.leitura_nivel_oleo_muito_alto_te and not self.dct["VOIP"]["TE_NIVEL_OLEO_MUITO_ALTO"]:
            logger.warning("[SE] O nível do óleo do transformador elevador está muito alto. Favor verificar.")
            self.dct["VOIP"]["TE_NIVEL_OLEO_MUITO_ALTO"] = True
            self.acionar_voip = True
        elif not self.leitura_nivel_oleo_muito_alto_te and self.dct["VOIP"]["TE_NIVEL_OLEO_MUITO_ALTO"]:
            self.dct["VOIP"]["TE_NIVEL_OLEO_MUITO_ALTO"] = False
        
        if self.leitura_nivel_oleo_muito_baixo_te and not self.dct["VOIP"]["TE_NIVEL_OLEO_MUITO_BAIXO"]:
            logger.warning("[SE] O nível de óleo do tranformador elevador está muito baixo. Favor verificar.")
            self.dct["VOIP"]["TE_NIVEL_OLEO_MUITO_BAIXO"] = True
            self.acionar_voip = True
        elif not self.leitura_nivel_oleo_muito_baixo_te and self.dct["VOIP"]["TE_NIVEL_OLEO_MUITO_BAIXO"]:
            self.dct["VOIP"]["TE_NIVEL_OLEO_MUITO_BAIXO"] = False

        if self.leitura_alarme_temperatura_oleo_te and not self.dct["VOIP"]["TE_ALARME_TEMPERATURA_OLEO"]:
            logger.warning("[SE] A temperatura do óleo do transformador elevador está alta. Favor verificar.")
            self.dct["VOIP"]["TE_ALARME_TEMPERATURA_OLEO"] = True
            self.acionar_voip = True
        elif not self.leitura_alarme_temperatura_oleo_te and self.dct["VOIP"]["TE_ALARME_TEMPERATURA_OLEO"]:
            self.dct["VOIP"]["TE_ALARME_TEMPERATURA_OLEO"] = False

        if self.leitura_alm_temp_enrolamento_te and not self.dct["VOIP"]["TE_ALM_TEMPERATURA_ENROLAMENTO"]:
            logger.warning("[SE] A temperatura do enrolamento do transformador elevador está alta. Favor verificar.")
            self.dct["VOIP"]["TE_ALM_TEMPERATURA_ENROLAMENTO"] = True
            self.acionar_voip = True
        elif not self.leitura_alm_temp_enrolamento_te and self.dct["VOIP"]["TE_ALM_TEMPERATURA_ENROLAMENTO"]:
            self.dct["VOIP"]["TE_ALM_TEMPERATURA_ENROLAMENTO"] = False
        
        if self.leitura_alarme_temp_enrolamento_te and not self.dct["VOIP"]["TE_ALARME_TEMPERATURA_ENROLAMENTO"]:
            logger.warning("[SE] A temperatura do enrolamento do transformador elevador está alta. Favor verificar.")
            self.dct["VOIP"]["TE_ALARME_TEMPERATURA_ENROLAMENTO"] = True
            self.acionar_voip = True
        elif not self.leitura_alarme_temp_enrolamento_te and self.dct["VOIP"]["TE_ALARME_TEMPERATURA_ENROLAMENTO"]:
            self.dct["VOIP"]["TE_ALARME_TEMPERATURA_ENROLAMENTO"] = False


    def iniciar_leituras_condicionadores(self) -> None:
        # CONDICIONADORES ESSENCIAIS
        # Normalizar
            # Bit Normal
        self.leitura_rele_linha_atuado = LeituraOpcBit(OPC_UA["SE"]["RELE_LINHA_ATUADO"], 14)
        self.condicionadores_essenciais.append(CondicionadorBase(self.leitura_rele_linha_atuado, CONDIC_NORMALIZAR))

        # CONDICIONADORES
        # Indisponibilizar
            # Bit Invertido
        self.leitura_89l_fechada = LeituraOpcBit(OPC_UA["SE"]["89L_FECHADA"], 12, True)
        self.condicionadores.append(CondicionadorBase(self.leitura_89l_fechada, CONDIC_INDISPONIBILIZAR))

            # Bit Normal
        self.leitura_86t_atuado = LeituraOpcBit(OPC_UA["SE"]["86T_ATUADO"], 20)
        self.condicionadores.append(CondicionadorBase(self.leitura_86t_atuado, CONDIC_INDISPONIBILIZAR))
        
        self.leitura_86bf_atuado = LeituraOpcBit(OPC_UA["SE"]["86BF_ATUADO"], 19)
        self.condicionadores.append(CondicionadorBase(self.leitura_86bf_atuado, CONDIC_INDISPONIBILIZAR))

        self.leitura_rele_te_atuado = LeituraOpcBit(OPC_UA["SE"]["TE_RELE_ATUADO"], 17)
        self.condicionadores.append(CondicionadorBase(self.leitura_rele_te_atuado, CONDIC_INDISPONIBILIZAR))

        self.leitura_trip_rele_buchholz = LeituraOpcBit(OPC_UA["SE"]["TE_TRIP_RELE_BUCHHOLZ"], 23)
        self.condicionadores.append(CondicionadorBase(self.leitura_trip_rele_buchholz, CONDIC_INDISPONIBILIZAR))

        self.leitura_trip_alivio_pressao = LeituraOpcBit(OPC_UA["SE"]["TE_TRIP_ALIVIO_PRESSAO"], 24)
        self.condicionadores.append(CondicionadorBase(self.leitura_trip_alivio_pressao, CONDIC_INDISPONIBILIZAR))

        self.leitura_trip_temp_oleo_te = LeituraOpcBit(OPC_UA["SE"]["TE_TRIP_TEMPERATURA_OLEO"], 19)
        self.condicionadores.append(CondicionadorBase(self.leitura_trip_temp_oleo_te, CONDIC_INDISPONIBILIZAR))

        self.leitura_atuacao_rele_linha_bf = LeituraOpcBit(OPC_UA["SE"]["RELE_LINHA_ATUACAO_BF"], 16)
        self.condicionadores.append(CondicionadorBase(self.leitura_atuacao_rele_linha_bf, CONDIC_INDISPONIBILIZAR))

        self.leitura_alarme_rele_buchholz = LeituraOpcBit(OPC_UA["SE"]["TE_ALARME_RELE_BUCHHOLZ"], 22)
        self.condicionadores.append(CondicionadorBase(self.leitura_alarme_rele_buchholz, CONDIC_INDISPONIBILIZAR))

        self.leitura_trip_temp_enrol_te = LeituraOpcBit(OPC_UA["SE"]["TE_TRIP_TEMPERATURA_ENROLAMENTO"], 20)
        self.condicionadores.append(CondicionadorBase(self.leitura_trip_temp_enrol_te, CONDIC_INDISPONIBILIZAR))

        self.leitura_falha_comando_abertura_52l = LeituraOpcBit(OPC_UA["SE"]["FALHA_COMANDO_ABERTURA_52L"], 1)
        self.condicionadores.append(CondicionadorBase(self.leitura_falha_comando_abertura_52l, CONDIC_INDISPONIBILIZAR))

        self.leitura_falha_comando_fechamento_52l = LeituraOpcBit(OPC_UA["SE"]["FALHA_COMANDO_FECHAMENTO_52L"], 2)
        self.condicionadores.append(CondicionadorBase(self.leitura_falha_comando_fechamento_52l, CONDIC_INDISPONIBILIZAR))

        self.leitura_super_bobinas_reles_bloq = LeituraOpcBit(OPC_UA["SE"]["SUPERVISAO_BOBINAS_RELES_BLOQUEIOS"], 21)
        self.condicionadores.append(CondicionadorBase(self.leitura_super_bobinas_reles_bloq, CONDIC_INDISPONIBILIZAR))

        # LEITURAS PARA LEITURA PERIÓDICA
        # Telegram
            # Bit Invertido
        self.leitura_seletora_52l_remoto = LeituraOpcBit(OPC_UA["SE"]["52L_SELETORA_REMOTO"], 10, True)

            # Bit Normal
        self.leitura_falha_temp_oleo_te = LeituraOpcBit(OPC_UA["SE"]["TE_FALHA_TEMPERATURA_OLEO"], 1)
        self.leitura_falha_temp_enrolamento_te = LeituraOpcBit(OPC_UA["SE"]["TE_FALHA_TEMPERATURA_ENROLAMENTO"], 2)

        # Telegram + Voip
            # Bit Normal
        self.leitura_alm_temperatura_oleo_te = LeituraOpcBit(OPC_UA["SE"]["TE_ALM_TEMPERATURA_OLEO"], 1)
        self.leitura_nivel_oleo_muito_alto_te = LeituraOpcBit(OPC_UA["SE"]["TE_NIVEL_OLEO_MUITO_ALTO"], 26)
        self.leitura_nivel_oleo_muito_baixo_te = LeituraOpcBit(OPC_UA["SE"]["TE_NIVEL_OLEO_MUITO_BAIXO"], 27)
        self.leitura_alm_temp_enrolamento_te = LeituraOpcBit(OPC_UA["SE"]["TE_ALM_TEMPERATURA_ENROLAMENTO"], 2)
        self.leitura_alarme_temperatura_oleo_te = LeituraOpcBit(OPC_UA["SE"]["TE_ALARME_TEMPERATURA_OLEO"], 18)
        self.leitura_alarme_temp_enrolamento_te = LeituraOpcBit(OPC_UA["SE"]["TE_ALARME_TEMPERATURA_ENROLAMENTO"], 20)