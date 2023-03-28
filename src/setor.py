__version__ = "0.2"
__authors__ = "Diego Basgal", "Henrique Pfeifer"
__credits__ = ["Lucas Lavratti", ...]
__description__ = "Este módulo corresponde a implementação dos setores da Usina."


import logging
import threading

from time import sleep, time

from escrita import *
from leitura import *
from comporta import *
from condicionador import *
from dicionarios.reg import *
from conversor_protocolo.conversor import *

logger = logging.getLogger("__main__")

class Bay:
    def __init__(
            self,
            conversor: NativoParaExterno | None = ...
        ) -> ...:

        if None in (conversor):
            logger.warning("[BAY] Erro ao carregar argumentos da classe \"ConectorBay\".")
            raise ImportError
        else:
            self.cnv = conversor

    def verificar_status_DJs(self) -> bool: 
        return
    
    def resetar_emergencia(self) -> bool:
        return



class Subestacao:
    def __init__(
            self,
            dicionario: dict | None = ...,
            client: OpcClient | None = ...,
            escritas: list[EscritaBase] | None = ...
        ) -> ...:

        self.__tensao_rs = LeituraOpc(self.opc, OPC_UA["LT_VAB"])
        self.__tensao_st = LeituraOpc(self.opc, OPC_UA["LT_VBC"])
        self.__tensao_tr = LeituraOpc(self.opc, OPC_UA["LT_VCA"])

        self._condicionadores = []
        self._condicionadores_essenciais = []

        self.opc = client
        self.dct = dicionario

        self.e_opc = escritas[0]
        self.e_opc_bit = escritas[1]

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
        res = self.e_opc_bit.escrever(OPC_UA["SE"]["CMD_SE_FECHA_52L"], valor=1, bit=4)
        return res

    def resetar_emergencia(self) -> bool:
        try:
            res = 0
            res += 1 if self.e_opc_bit.escrever(OPC_UA["SE"]["CMD_SE_REARME_BLOQUEIO_GERAL"], valor=1, bit=0) else ...
            res += 1 if self.e_opc_bit.escrever(OPC_UA["SE"]["CMD_SE_REARME_86T"], valor=1, bit=1) else ...
            res += 1 if self.e_opc_bit.escrever(OPC_UA["SE"]["CMD_SE_REARME_86BF"], valor=1, bit=2) else ...
            res += 1 if self.e_opc_bit.escrever(OPC_UA["SE"]["REARME_86BF_86T"], valor=1, bit=22) else ...
            res += 1 if self.e_opc_bit.escrever(OPC_UA["SE"]["CMD_SE_RESET_REGISTROS"], valor=1, bit=5) else ...
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
        self.leitura_rele_linha_atuado = LeituraOpcBit(self.opc, OPC_UA["SE"]["RELE_LINHA_ATUADO"], 14)
        self.condicionadores_essenciais.append(CondicionadorBase(self.leitura_rele_linha_atuado, CONDIC_NORMALIZAR))

        # CONDICIONADORES
        # Indisponibilizar
            # Bit Invertido
        self.leitura_89l_fechada = LeituraOpcBit(self.opc, OPC_UA["SE"]["89L_FECHADA"], 12, True)
        self.condicionadores.append(CondicionadorBase(self.leitura_89l_fechada, CONDIC_INDISPONIBILIZAR))

            # Bit Normal
        self.leitura_86t_atuado = LeituraOpcBit(self.opc, OPC_UA["SE"]["86T_ATUADO"], 20)
        self.condicionadores.append(CondicionadorBase(self.leitura_86t_atuado, CONDIC_INDISPONIBILIZAR))
        
        self.leitura_86bf_atuado = LeituraOpcBit(self.opc, OPC_UA["SE"]["86BF_ATUADO"], 19)
        self.condicionadores.append(CondicionadorBase(self.leitura_86bf_atuado, CONDIC_INDISPONIBILIZAR))

        self.leitura_rele_te_atuado = LeituraOpcBit(self.opc, OPC_UA["SE"]["TE_RELE_ATUADO"], 17)
        self.condicionadores.append(CondicionadorBase(self.leitura_rele_te_atuado, CONDIC_INDISPONIBILIZAR))

        self.leitura_trip_rele_buchholz = LeituraOpcBit(self.opc, OPC_UA["SE"]["TE_TRIP_RELE_BUCHHOLZ"], 23)
        self.condicionadores.append(CondicionadorBase(self.leitura_trip_rele_buchholz, CONDIC_INDISPONIBILIZAR))

        self.leitura_trip_alivio_pressao = LeituraOpcBit(self.opc, OPC_UA["SE"]["TE_TRIP_ALIVIO_PRESSAO"], 24)
        self.condicionadores.append(CondicionadorBase(self.leitura_trip_alivio_pressao, CONDIC_INDISPONIBILIZAR))

        self.leitura_trip_temp_oleo_te = LeituraOpcBit(self.opc, OPC_UA["SE"]["TE_TRIP_TEMPERATURA_OLEO"], 19)
        self.condicionadores.append(CondicionadorBase(self.leitura_trip_temp_oleo_te, CONDIC_INDISPONIBILIZAR))

        self.leitura_atuacao_rele_linha_bf = LeituraOpcBit(self.opc, OPC_UA["SE"]["RELE_LINHA_ATUACAO_BF"], 16)
        self.condicionadores.append(CondicionadorBase(self.leitura_atuacao_rele_linha_bf, CONDIC_INDISPONIBILIZAR))

        self.leitura_alarme_rele_buchholz = LeituraOpcBit(self.opc, OPC_UA["SE"]["TE_ALARME_RELE_BUCHHOLZ"], 22)
        self.condicionadores.append(CondicionadorBase(self.leitura_alarme_rele_buchholz, CONDIC_INDISPONIBILIZAR))

        self.leitura_trip_temp_enrol_te = LeituraOpcBit(self.opc, OPC_UA["SE"]["TE_TRIP_TEMPERATURA_ENROLAMENTO"], 20)
        self.condicionadores.append(CondicionadorBase(self.leitura_trip_temp_enrol_te, CONDIC_INDISPONIBILIZAR))

        self.leitura_falha_comando_abertura_52l = LeituraOpcBit(self.opc, OPC_UA["SE"]["FALHA_COMANDO_ABERTURA_52L"], 1)
        self.condicionadores.append(CondicionadorBase(self.leitura_falha_comando_abertura_52l, CONDIC_INDISPONIBILIZAR))

        self.leitura_falha_comando_fechamento_52l = LeituraOpcBit(self.opc, OPC_UA["SE"]["FALHA_COMANDO_FECHAMENTO_52L"], 2)
        self.condicionadores.append(CondicionadorBase(self.leitura_falha_comando_fechamento_52l, CONDIC_INDISPONIBILIZAR))

        self.leitura_super_bobinas_reles_bloq = LeituraOpcBit(self.opc, OPC_UA["SE"]["SUPERVISAO_BOBINAS_RELES_BLOQUEIOS"], 21)
        self.condicionadores.append(CondicionadorBase(self.leitura_super_bobinas_reles_bloq, CONDIC_INDISPONIBILIZAR))

        # LEITURAS PARA LEITURA PERIÓDICA
        # Telegram
            # Bit Invertido
        self.leitura_seletora_52l_remoto = LeituraOpcBit(self.opc, OPC_UA["SE"]["52L_SELETORA_REMOTO"], 10, True)

            # Bit Normal
        self.leitura_falha_temp_oleo_te = LeituraOpcBit(self.opc, OPC_UA["SE"]["TE_FALHA_TEMPERATURA_OLEO"], 1)
        self.leitura_falha_temp_enrolamento_te = LeituraOpcBit(self.opc, OPC_UA["SE"]["TE_FALHA_TEMPERATURA_ENROLAMENTO"], 2)

        # Telegram + Voip
            # Bit Normal
        self.leitura_alm_temperatura_oleo_te = LeituraOpcBit(self.opc, OPC_UA["SE"]["TE_ALM_TEMPERATURA_OLEO"], 1)
        self.leitura_nivel_oleo_muito_alto_te = LeituraOpcBit(self.opc, OPC_UA["SE"]["TE_NIVEL_OLEO_MUITO_ALTO"], 26)
        self.leitura_nivel_oleo_muito_baixo_te = LeituraOpcBit(self.opc, OPC_UA["SE"]["TE_NIVEL_OLEO_MUITO_BAIXO"], 27)
        self.leitura_alm_temp_enrolamento_te = LeituraOpcBit(self.opc, OPC_UA["SE"]["TE_ALM_TEMPERATURA_ENROLAMENTO"], 2)
        self.leitura_alarme_temperatura_oleo_te = LeituraOpcBit(self.opc, OPC_UA["SE"]["TE_ALARME_TEMPERATURA_OLEO"], 18)
        self.leitura_alarme_temp_enrolamento_te = LeituraOpcBit(self.opc, OPC_UA["SE"]["TE_ALARME_TEMPERATURA_ENROLAMENTO"], 20)



class TomadaAgua:
    def __init__(
            self,
            dicionario: dict | None = ...,
            client: OpcClient | None = ...,
            escritas: list[EscritaBase] | None = ...
        ) -> ...:

        self.__nv_montante = LeituraOpc(self.opc, OPC_UA["TDA"]["NIVEL_MONTANTE"])
        self.__status_lp = LeituraOpc(self.opc, OPC_UA["TDA"]["LG_OPERACAO_MANUAL"])
        self.__status_vb = LeituraOpc(self.opc, OPC_UA["TDA"]["VB_FECHANDO"])
        self.__status_uh = LeituraOpcBit(self.opc, OPC_UA["TDA"]["UH_UNIDADE_HIDRAULICA_DISPONIVEL"], 1)

        self._condicionadores = []
        self._condicionadores_essenciais = []

        self.opc = client
        self.dct = dicionario

        self.e_opc = escritas[0]
        self.e_opc_bit = escritas[1]

        self.cp1: Comporta = Comporta.__init__(1)
        self.cp2: Comporta = Comporta.__init__(2)

        self.cps = [self.cp1, self.cp2]
        self.cp1.lista_comportas = self.cps
        self.cp2.lista_comportas = self.cps

    @property
    def nv_montante(self) -> int | float:
        return self.__nv_montante.valor

    @property
    def limpa_grades(self) -> int:
        try:
            return self.__status_lp.valor
        except ValueError(f"[TDA] O limpa grades retornou valor de status inválido.") \
            or ConnectionError(f"[TDA] Falha na comunicação com o limpa grades."):
            return 99

    @property
    def valvula_borboleta(self) -> int:
        try:
            return self.__status_vb.valor
        except ValueError(f"[TDA] O limpa grades retornou valor de status inválido.") \
            or ConnectionError(f"[TDA] Falha na comunicação com o limpa grades."):
            return 99

    @property
    def unidade_hidraulica(self) -> int:
        try:
            return self.__status_uh.valor
        except ValueError(f"[TDA] A unidade hidráulica retornou valor de status inválido.") \
            or ConnectionError(f"[TDA] Falha na comunicação com a unidade hidráulica."):
            return 99

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


    def resetar_emergencia(self):
        if not self.dct["GLB"]["tda_offline"]:
            [self.e_opc_bit.escrever(OPC_UA["TDA"][f"CP{cp.id}_CMD_REARME_FALHAS"], valor=1, bit=0) for cp in self.cps]
        else:
            logger.debug("[TDA] Não é possível resetar a emergência pois o CLP da TDA se encontra offline")

    def leitura_periodica(self) -> None:
        if not self.leitura_filtro_limpo_uh:
            logger.warning("[TDA] O filtro da UH da TDA está sujo. Favor realizar limpeza/troca.")

        if self.leitura_nivel_jusante_comporta_1:
            logger.warning("[TDA] Houve uma falha no sensor de nível jusante da comporta 1. Favor verificar.")

        if self.leitura_nivel_jusante_comporta_2:
            logger.warning("[TDA] Houve uma falha no sensor de nível jusante da comporta 2. Favor verificar.")

        if not self.leitura_ca_com_tensao:
            logger.warning("[TDA] Foi dentificado que o CA da tomada da água está sem tensão. Favor verificar.")

        if self.leitura_lg_operacao_manual:
            logger.warning("[TDA] Foi identificado que o Limpa Grades entrou em operação manual. Favor verificar.")

        if self.leitura_nivel_jusante_grade_comporta_1:
            logger.warning("[TDA] Houve uma falha no sensor de nível jusante grade da comporta 1. Favor verificar.")

        if self.leitura_nivel_jusante_grade_comporta_2:
            logger.warning("[TDA] Houve uma falha no sensor de nível jusante grade da comporta 2. Favor verificar.")


        if self.leitura_falha_atuada_lg and not self.dct["VOIP"]["LG_FALHA_ATUADA"]:
            logger.warning("[TDA] Foi identificado que o limpa grades está em falha. Favor verificar.")
            self.dct["VOIP"]["LG_FALHA_ATUADA"] = True
            self.acionar_voip = True
        elif not self.leitura_falha_atuada_lg and self.dct["VOIP"]["LG_FALHA_ATUADA"]:
            self.dct["VOIP"]["LG_FALHA_ATUADA"] = False

        if self.leitura_falha_nivel_montante and not self.dct["VOIP"]["FALHA_NIVEL_MONTANTE"]:
            logger.warning("[TDA] Houve uma falha na leitura de nível montante. Favor verificar.")
            self.dct["VOIP"]["FALHA_NIVEL_MONTANTE"] = True
            self.acionar_voip = True
        elif not self.leitura_falha_nivel_montante and self.dct["VOIP"]["FALHA_NIVEL_MONTANTE"]:
            self.dct["VOIP"]["FALHA_NIVEL_MONTANTE"] = False

    def iniciar_leituras_condicionadores(self) -> None:
        # CONDICIONADORES ESSENCIAIS
        # Normalizar
            # Bit Invertido
        self.leitura_sem_emergencia_tda = LeituraOpcBit(self.opc, OPC_UA["TDA"]["SEM_EMERGENCIA"], 24, True)
        self.condicionadores_essenciais.append(CondicionadorBase(self.leitura_sem_emergencia_tda, CONDIC_NORMALIZAR))

        # CONDICIONADORES
        # Normalizar
            # Bit Invertido
        self.leitura_ca_com_tensao = LeituraOpcBit(self.opc, OPC_UA["TDA"]["COM_TENSAO_CA"], 11, True)
        self.condicionadores.append(CondicionadorBase(self.leitura_ca_com_tensao, CONDIC_NORMALIZAR))

            # Bit Normal
        self.leitura_falha_ligar_bomba_uh = LeituraOpcBit(self.opc, OPC_UA["TDA"]["UH_FALHA_LIGAR_BOMBA"], 2)
        self.condicionadores.append(CondicionadorBase(self.leitura_falha_ligar_bomba_uh, CONDIC_NORMALIZAR))


        # LEITURAS PARA LEITURA PERIÓDICA
        # Telegram
            # Bit Invertido
        self.leitura_ca_com_tensao = LeituraOpcBit(self.opc, OPC_UA["TDA"]["COM_TENSAO_CA"], 11, True)
        self.leitura_filtro_limpo_uh = LeituraOpcBit(self.opc, OPC_UA["TDA"]["UH_FILTRO_LIMPO"], 13, True)

            # Bit Normal
        self.leitura_lg_operacao_manual = LeituraOpcBit(self.opc, OPC_UA["TDA"]["LG_OPERACAO_MANUAL"], 0)
        self.leitura_nivel_jusante_comporta_1 = LeituraOpcBit(self.opc, OPC_UA["TDA"]["NIVEL_JUSANTE_COMPORTA_1"], 2)
        self.leitura_nivel_jusante_comporta_2 = LeituraOpcBit(self.opc, OPC_UA["TDA"]["NIVEL_JUSANTE_COMPORTA_2"], 4)
        self.leitura_nivel_jusante_grade_comporta_1 = LeituraOpcBit(self.opc, OPC_UA["TDA"]["FALHA_NIVEL_JUSANTE_GRADE_COMPORTA_1"], 1)
        self.leitura_nivel_jusante_grade_comporta_2 = LeituraOpcBit(self.opc, OPC_UA["TDA"]["FALHA_NIVEL_JUSANTE_GRADE_COMPORTA_2"], 3)

        # Telegram + Voip
            # Bit Normal
        self.leitura_falha_atuada_lg = LeituraOpcBit(self.opc, OPC_UA["TDA"]["LG_FALHA_ATUADA"], 31)
        self.leitura_falha_nivel_montante = LeituraOpcBit(self.opc, OPC_UA["TDA"]["FALHA_NIVEL_MONTANTE"], 0)



class ServicoAuxiliar:
    def __init__(
            self,
            dicionario: dict | None = ...,
            client: OpcClient | None = ...,
            escritas: list[EscritaBase] | None = ...
        ) -> ...:

        self.opc = client
        self.dct = dicionario

        self.e_opc = escritas[0]
        self.e_opc_bit = escritas[1]

        self._condicionadores = []
        self._condicionadores_essenciais = []

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

    def resetar_emergencia(self) -> bool:
        try:
            res = self.e_opc_bit.escrever(OPC_UA["SA"]["RESET_FALHAS_BARRA_CA"], valor=1, bit=0)
            res = self.e_opc_bit.escrever(OPC_UA["SA"]["RESET_FALHAS_SISTEMA_AGUA"], valor=1, bit=1)
            res = self.e_opc_bit.escrever(OPC_UA["SA"]["REARME_BLOQUEIO_GERAL_E_FALHAS_SA"], valor=1, bit=23)
            return res

        except Exception as e:
            logger.exception(f"[SA] Houve um erro ao realizar o reset geral. Exception: \"{repr(e)}\"")
            logger.exception(f"[SA] Traceback: {traceback.print_stack}")
            return False

    def leitura_periodica(self) -> None:
        if self.leitura_falha_bomba_drenagem_1:
            logger.warning("[SA] Houve uma falha na bomba 1 do poço de drenagem. Favor verificar.")
        
        if self.leitura_falha_bomba_drenagem_2:
            logger.warning("[SA] Houve uma falha na bomba 2 do poço de drenagem. Favor verificar.")

        if self.leitura_falha_bomba_drenagem_3:
            logger.warning("[SA] Houve uma falha na bomba 3 do poço de drenagem. Favor verificar.")

        if self.leitura_falha_ligar_bomba_sis_agua:
            logger.warning("[SA] Houve uma falha ao ligar a bomba do sistema de água. Favor verificar.")

        if self.leitura_djs_barra_seletora_remoto:
            logger.warning("[SA] Os disjuntores da barra seletora saíram do modo remoto. Favor verificar.")

        if not self.leitura_bomba_sis_agua_disp:
            logger.warning("[SA] Foi identificado que a bomba do sistema de água está indisponível. Favor verificar.")

        if self.leitura_discrepancia_boia_poco_drenagem:
            logger.warning("[SA] Foram identificados sinais inconsistentes nas boias do poço de drenagem. Favor verificar.")


        if self.leitura_falha_partir_gmg and not self.dct["VOIP"]["GMG_FALHA_PARTIR"]:
            logger.warning("[SA] Houve uma falha ao partir o Gerador Diesel. Favor verificar.")
            self.dct["VOIP"]["GMG_FALHA_PARTIR"] = True
            self.acionar_voip = True
        elif not self.leitura_falha_partir_gmg and self.dct["VOIP"]["GMG_FALHA_PARTIR"]:
            self.dct["VOIP"]["GMG_FALHA_PARTIR"] = False

        if self.leitura_falha_parar_gmg and not self.dct["VOIP"]["GMG_FALHA_PARAR"]:
            logger.warning("[SA] Houve uma falha ao parar o Gerador Diesel. Favor verificar.")
            self.dct["VOIP"]["GMG_FALHA_PARAR"] = True
            self.acionar_voip = True
        elif not self.leitura_falha_parar_gmg and self.dct["VOIP"]["GMG_FALHA_PARAR"]:
            self.dct["VOIP"]["GMG_FALHA_PARAR"] = False

        if self.leitura_operacao_manual_gmg and not self.dct["VOIP"]["GMG_OPERACAO_MANUAL"]:
            logger.warning("[SA] O Gerador Diesel saiu do modo remoto. Favor verificar.")
            self.dct["VOIP"]["GMG_OPERACAO_MANUAL"] = True
            self.acionar_voip = True
        elif not self.leitura_operacao_manual_gmg and self.dct["VOIP"]["GMG_OPERACAO_MANUAL"]:
            self.dct["VOIP"]["GMG_OPERACAO_MANUAL"] = False

        if not self.leitura_sem_falha_52sa1 and not self.dct["VOIP"]["52SA1_SEM_FALHA"]:
            logger.warning("[SA] Houve uma falha com o disjuntor 52SA1 do transformador do SA. Favor verificar.")
            self.dct["VOIP"]["52SA1_SEM_FALHA"] = True
        elif self.leitura_sem_falha_52sa1 and self.dct["VOIP"]["52SA1_SEM_FALHA"]:
            self.dct["VOIP"]["52SA1_SEM_FALHA"] = False

        if not self.leitura_sem_falha_52sa2 and not self.dct["VOIP"]["52SA2_SEM_FALHA"]:
            logger.warning("[SA] Houve uma falha com o disjuntor 52SA2 do Gerador Diesel. Favor verificar.")
            self.dct["VOIP"]["52SA2_SEM_FALHA"] = True
            self.acionar_voip = True
        elif self.leitura_sem_falha_52sa2 and self.dct["VOIP"]["52SA2_SEM_FALHA"]:
            self.dct["VOIP"]["52SA2_SEM_FALHA"] = False

        if not self.leitura_sem_falha_52sa3 and not self.dct["VOIP"]["52SA3_SEM_FALHA"]:
            logger.warning("[SA] Houve uma falha com o disjuntor 52SA3 do barramento de cargas não essenciais. Favor verificar.")
            self.dct["VOIP"]["52SA3_SEM_FALHA"] = True
            self.acionar_voip = True
        elif self.leitura_sem_falha_52sa3 and self.dct["VOIP"]["52SA3_SEM_FALHA"]:
            self.dct["VOIP"]["52SA3_SEM_FALHA"] = False

        if self.leitura_falha_bomba_filtragem and not self.dct["VOIP"]["FILTRAGEM_BOMBA_FALHA"]:
            logger.warning("[SA] Houve uma falha na bomba de filtragem. Favor verificar.")
            self.dct["VOIP"]["FILTRAGEM_BOMBA_FALHA"] = True
            self.acionar_voip = True
        elif not self.leitura_falha_bomba_filtragem and self.dct["VOIP"]["FILTRAGEM_BOMBA_FALHA"]:
            self.dct["VOIP"]["FILTRAGEM_BOMBA_FALHA"] = False

        if self.leitura_nivel_alto_poco_drenagem and not self.dct["VOIP"]["POCO_DRENAGEM_NIVEL_ALTO"]:
            logger.warning("[SA] Nível do poço de drenagem alto. Favor verificar.")
            self.dct["VOIP"]["POCO_DRENAGEM_NIVEL_ALTO"] = True
            self.acionar_voip = True
        elif not self.leitura_nivel_alto_poco_drenagem and self.dct["VOIP"]["POCO_DRENAGEM_NIVEL_ALTO"]:
            self.dct["VOIP"]["POCO_DRENAGEM_NIVEL_ALTO"] = False

        if self.leitura_falha_bomba_drenagem_uni and not self.dct["VOIP"]["DRENAGEM_UNIDADES_BOMBA_FALHA"]:
            logger.warning("[SA] Houve uma falha na bomba de drenagem. Favor verificar.")
            self.dct["VOIP"]["DRENAGEM_UNIDADES_BOMBA_FALHA"] = True
            self.acionar_voip = True
        elif not self.leitura_falha_bomba_drenagem_uni and self.dct["VOIP"]["DRENAGEM_UNIDADES_BOMBA_FALHA"]:
            self.dct["VOIP"]["DRENAGEM_UNIDADES_BOMBA_FALHA"] = False

        if self.leitura_nivel_muito_alto_poco_drenagem and not self.dct["VOIP"]["POCO_DRENAGEM_NIVEL_MUITO_ALTO"]:
            logger.warning("[SA] Nível do poço de drenagem está muito alto. Favor verificar.")
            self.dct["VOIP"]["POCO_DRENAGEM_NIVEL_MUITO_ALTO"] = True
            self.acionar_voip = True
        elif not self.leitura_nivel_muito_alto_poco_drenagem and self.dct["VOIP"]["POCO_DRENAGEM_NIVEL_MUITO_ALTO"]:
            self.dct["VOIP"]["POCO_DRENAGEM_NIVEL_MUITO_ALTO"] = False

        if self.leitura_alarme_sistema_incendio_atuado and not self.dct["VOIP"]["SISTEMA_INCENDIO_ALARME_ATUADO"]:
            logger.warning("[SA] O alarme do sistema de incêndio foi acionado. Favor verificar.")
            self.dct["VOIP"]["SISTEMA_INCENDIO_ALARME_ATUADO"] = True
            self.acionar_voip = True
        elif not self.leitura_alarme_sistema_incendio_atuado and self.dct["VOIP"]["SISTEMA_INCENDIO_ALARME_ATUADO"]:
            self.dct["VOIP"]["SISTEMA_INCENDIO_ALARME_ATUADO"] = False

        if self.leitura_alarme_sistema_seguraca_atuado and not self.dct["VOIP"]["SISTEMA_SEGURANCA_ALARME_ATUADO"]:
            logger.warning("[SA] O alarme do sistem de seguraça foi acionado. Favor verificar.")
            self.dct["VOIP"]["SISTEMA_SEGURANCA_ALARME_ATUADO"] = True
            self.acionar_voip = True
        elif not self.leitura_alarme_sistema_seguraca_atuado and self.dct["VOIP"]["SISTEMA_SEGURANCA_ALARME_ATUADO"]:
            self.dct["VOIP"]["SISTEMA_SEGURANCA_ALARME_ATUADO"] = False
            
        if self.leitura_falha_tubo_succao_bomba_recalque and not self.dct["VOIP"]["BOMBA_RECALQUE_TUBO_SUCCAO_FALHA"]:
            logger.warning("[SA] Houve uma falha na sucção da bomba de recalque. Favor verificar.")
            self.dct["VOIP"]["BOMBA_RECALQUE_TUBO_SUCCAO_FALHA"] = True
            self.acionar_voip = True
        elif not self.leitura_falha_tubo_succao_bomba_recalque and self.dct["VOIP"]["BOMBA_RECALQUE_TUBO_SUCCAO_FALHA"]:
            self.dct["VOIP"]["BOMBA_RECALQUE_TUBO_SUCCAO_FALHA"] = False

    def iniciar_leituras_condicionadores(self) -> None:
        # CONDICIONADORES ESSENCIAIS
        # MOA -> Indisponibilizar
        self.leitura_in_emergencia = self.clp_moa.read_coils(MB["MOA"]["IN_EMERG"])[0]
        self.condicionadores_essenciais.append(CondicionadorBase(self.leitura_in_emergencia, CONDIC_INDISPONIBILIZAR))

        # Normalizar
            # Bit Invertido
        self.leitura_sem_emergencia_sa = LeituraOpcBit(self.opc, OPC_UA["SA"]["SEM_EMERGENCIA"], 13, True)
        self.condicionadores_essenciais.append(CondicionadorBase(self.leitura_sem_emergencia_sa, CONDIC_NORMALIZAR))

        # CONDICIONADORES
        # Normalizar
            # Bit Normal
        self.leitura_retificador_subtensao = LeituraOpcBit(self.opc, OPC_UA["SA"]["RETIFICADOR_SUBTENSAO"], 31)
        self.condicionadores.append(CondicionadorBase(self.leitura_retificador_subtensao, CONDIC_NORMALIZAR))

        self.leitura_retificador_sobretensao = LeituraOpcBit(self.opc, OPC_UA["SA"]["RETIFICADOR_SOBRETENSAO"], 30)
        self.condicionadores.append(CondicionadorBase(self.leitura_retificador_sobretensao, CONDIC_NORMALIZAR))

        self.leitura_retificador_sobrecorrente_saida = LeituraOpcBit(self.opc, OPC_UA["SA"]["RETIFICADOR_SOBRECORRENTE_SAIDA"], 0)
        self.condicionadores.append(CondicionadorBase(self.leitura_retificador_sobrecorrente_saida, CONDIC_NORMALIZAR))

        self.leitura_retificador_sobrecorrente_baterias = LeituraOpcBit(self.opc, OPC_UA["SA"]["RETIFICADOR_SOBRECORRENTE_BATERIAS"], 1)
        self.condicionadores.append(CondicionadorBase(self.leitura_retificador_sobrecorrente_baterias, CONDIC_NORMALIZAR))

        self.leitura_falha_sistema_agua_pressurizar_fa = LeituraOpcBit(self.opc, OPC_UA["SA"]["SISTEMA_AGUA_FALHA_PRESSURIZAR_FILTRO_A"], 3)
        self.condicionadores.append(CondicionadorBase(self.leitura_falha_sistema_agua_pressurizar_fa, CONDIC_NORMALIZAR))

        self.leitura_falha_sistema_agua_pressostato_fa = LeituraOpcBit(self.opc, OPC_UA["SA"]["SISTEMA_AGUA_FALHA_PRESSOSTATO_FILTRO_A"], 4)
        self.condicionadores.append(CondicionadorBase(self.leitura_falha_sistema_agua_pressostato_fa, CONDIC_NORMALIZAR))

        self.leitura_falha_sistema_agua_pressurizar_fb = LeituraOpcBit(self.opc, OPC_UA["SA"]["SISTEMA_AGUA_FALHA_PRESSURIZAR_FILTRO_B"], 5)
        self.condicionadores.append(CondicionadorBase(self.leitura_falha_sistema_agua_pressurizar_fb, CONDIC_NORMALIZAR))

        self.leitura_falha_sistema_agua_pressostato_fb = LeituraOpcBit(self.opc, OPC_UA["SA"]["SISTEMA_AGUA_FALHA_PRESSOSTATO_FILTRO_B"], 6)
        self.condicionadores.append(CondicionadorBase(self.leitura_falha_sistema_agua_pressostato_fb, CONDIC_NORMALIZAR))

        # Indisponibilizar
            # Bit Invertido
        self.leitura_52sa1_sem_falha = LeituraOpcBit(self.opc, OPC_UA["SA"]["52SA1_SEM_FALHA"], 31, True)
        self.condicionadores.append(CondicionadorBase(self.leitura_52sa1_sem_falha, CONDIC_INDISPONIBILIZAR))

        self.leitura_sa_72sa1_fechado = LeituraOpcBit(self.opc, OPC_UA["SA"]["SA_72SA1_FECHADO"], 10, True)
        self.condicionadores.append(CondicionadorBase(self.leitura_sa_72sa1_fechado, CONDIC_INDISPONIBILIZAR))

        self.leitura_disj_24vcc_fechados = LeituraOpcBit(self.opc, OPC_UA["SA"]["DISJUNTORES_24VCC_FECHADOS"], 12, True)
        self.condicionadores.append(CondicionadorBase(self.leitura_disj_24vcc_fechados, CONDIC_INDISPONIBILIZAR))

        self.leitura_disj_125vcc_fechados = LeituraOpcBit(self.opc, OPC_UA["SA"]["DISJUNTORES_125VCC_FECHADOS"], 11, True)
        self.condicionadores.append(CondicionadorBase(self.leitura_disj_125vcc_fechados, CONDIC_INDISPONIBILIZAR))
        
        self.leitura_comando_24vcc_com_tensao = LeituraOpcBit(self.opc, OPC_UA["SA"]["COM_TENSAO_COMANDO_24VCC"], 15, True)
        self.condicionadores.append(CondicionadorBase(self.leitura_comando_24vcc_com_tensao, CONDIC_INDISPONIBILIZAR))
        
        self.leitura_comando_125vcc_com_tensao = LeituraOpcBit(self.opc, OPC_UA["SA"]["COM_TENSAO_COMANDO_125VCC"], 14, True)
        self.condicionadores.append(CondicionadorBase(self.leitura_comando_125vcc_com_tensao, CONDIC_INDISPONIBILIZAR))
        
        self.leitura_alimentacao_125vcc_com_tensao = LeituraOpcBit(self.opc, OPC_UA["SA"]["COM_TENSAO_ALIMENTACAO_125VCC"], 13, True)
        self.condicionadores.append(CondicionadorBase(self.leitura_alimentacao_125vcc_com_tensao, CONDIC_INDISPONIBILIZAR))

            # Bit normal
        self.leitura_falha_abrir_52sa1 = LeituraOpcBit(self.opc, OPC_UA["SA"]["FALHA_ABRIR_52SA1"], 0)
        self.condicionadores.append(CondicionadorBase(self.leitura_falha_abrir_52sa1, CONDIC_INDISPONIBILIZAR))

        self.leitura_falha_fechar_52sa1 = LeituraOpcBit(self.opc, OPC_UA["SA"]["FALHA_FECHAR_52SA1"], 1)
        self.condicionadores.append(CondicionadorBase(self.leitura_falha_fechar_52sa1, CONDIC_INDISPONIBILIZAR))

        self.leitura_falha_abrir_52sa2 = LeituraOpcBit(self.opc, OPC_UA["SA"]["FALHA_ABRIR_52SA2"], 3)
        self.condicionadores.append(CondicionadorBase(self.leitura_falha_abrir_52sa2, CONDIC_INDISPONIBILIZAR))

        self.leitura_falha_fechar_52sa2 = LeituraOpcBit(self.opc, OPC_UA["SA"]["FALHA_FECHAR_52SA2"], 4)
        self.condicionadores.append(CondicionadorBase(self.leitura_falha_fechar_52sa2, CONDIC_INDISPONIBILIZAR))

        self.leitura_falha_abrir_52sa3 = LeituraOpcBit(self.opc, OPC_UA["SA"]["FALHA_ABRIR_52SA3"], 5)
        self.condicionadores.append(CondicionadorBase(self.leitura_falha_abrir_52sa3, CONDIC_INDISPONIBILIZAR))

        self.leitura_falha_fechar_52sa3 = LeituraOpcBit(self.opc, OPC_UA["SA"]["FALHA_FECHAR_52SA3"], 6)
        self.condicionadores.append(CondicionadorBase(self.leitura_falha_fechar_52sa3, CONDIC_INDISPONIBILIZAR))

        self.leitura_fusivel_queimado_retificador = LeituraOpcBit(self.opc, OPC_UA["SA"]["RETIFICADOR_FUSIVEL_QUEIMADO"], 2)
        self.condicionadores.append(CondicionadorBase(self.leitura_fusivel_queimado_retificador, CONDIC_INDISPONIBILIZAR))

        self.leitura_fuga_terra_positivo_retificador = LeituraOpcBit(self.opc, OPC_UA["SA"]["RETIFICADOR_FUGA_TERRA_POSITIVO"], 5)
        self.condicionadores.append(CondicionadorBase(self.leitura_fuga_terra_positivo_retificador, CONDIC_INDISPONIBILIZAR))

        self.leitura_fuga_terra_negativo_retificador = LeituraOpcBit(self.opc, OPC_UA["SA"]["RETIFICADOR_FUGA_TERRA_NEGATIVO"], 6)
        self.condicionadores.append(CondicionadorBase(self.leitura_fuga_terra_negativo_retificador, CONDIC_INDISPONIBILIZAR))

        # LEITURAS PARA LEITURA PERIODICA
        # Telegram
            # Bit Invertido
        self.leitura_bomba_sis_agua_disp = LeituraOpcBit(self.opc, OPC_UA["SA"]["SISTEMA_AGUA_BOMBA_DISPONIVEL"], 0, True)

            # Bit Normal
        self.leitura_falha_bomba_drenagem_1 = LeituraOpcBit(self.opc, OPC_UA["SA"]["DRENAGEM_BOMBA_1_FALHA"], 0)
        self.leitura_falha_bomba_drenagem_2 = LeituraOpcBit(self.opc, OPC_UA["SA"]["DRENAGEM_BOMBA_2_FALHA"], 2)
        self.leitura_falha_bomba_drenagem_3 = LeituraOpcBit(self.opc, OPC_UA["SA"]["DRENAGEM_BOMBA_3_FALHA"], 4)
        self.leitura_falha_ligar_bomba_sis_agua = LeituraOpcBit(self.opc, OPC_UA["SA"]["SISTEMA_AGUA_FALHA_LIGA_BOMBA"], 1)
        self.leitura_djs_barra_seletora_remoto = LeituraOpcBit(self.opc, OPC_UA["SA"]["DISJUNTORES_BARRA_SELETORA_REMOTO"], 9)
        self.leitura_discrepancia_boia_poco_drenagem = LeituraOpcBit(self.opc, OPC_UA["SA"]["DRENAGEM_DISCREPANCIA_BOIAS_POCO"], 9)

        # Telegram + Voip
            # Bit Invertido
        self.leitura_sem_falha_52sa3 = LeituraOpcBit(self.opc, OPC_UA["SA"]["52SA3_SEM_FALHA"], 3, True)
        self.leitura_sem_falha_52sa2 = LeituraOpcBit(self.opc, OPC_UA["SA"]["52SA2_SEM_FALHA"], 1, True)
        self.leitura_sem_falha_52sa1 = LeituraOpcBit(self.opc, OPC_UA["SA"]["52SA1_SEM_FALHA"], 31, True)

            # Bit Normal
        self.leitura_falha_parar_gmg = LeituraOpcBit(self.opc, OPC_UA["SA"]["GMG_FALHA_PARAR"], 7)
        self.leitura_falha_partir_gmg = LeituraOpcBit(self.opc, OPC_UA["SA"]["GMG_FALHA_PARTIR"], 6)
        self.leitura_operacao_manual_gmg = LeituraOpcBit(self.opc, OPC_UA["SA"]["GMG_OPERACAO_MANUAL"], 10)
        self.leitura_falha_bomba_filtragem = LeituraOpcBit(self.opc, OPC_UA["SA"]["FILTRAGEM_BOMBA_FALHA"], 6)
        self.leitura_nivel_alto_poco_drenagem = LeituraOpcBit(self.opc, OPC_UA["SA"]["POCO_DRENAGEM_NIVEL_ALTO"], 26)
        self.leitura_falha_bomba_drenagem_uni = LeituraOpcBit(self.opc, OPC_UA["SA"]["DRENAGEM_UNIDADES_BOMBA_FALHA"], 12)
        self.leitura_alarme_sistema_incendio_atuado = LeituraOpcBit(self.opc, OPC_UA["SA"]["SISTEMA_INCENDIO_ALARME_ATUADO"], 6)
        self.leitura_alarme_sistema_seguraca_atuado = LeituraOpcBit(self.opc, OPC_UA["SA"]["SISTEMA_SEGURANCA_ALARME_ATUADO"], 7)
        self.leitura_nivel_muito_alto_poco_drenagem = LeituraOpcBit(self.opc, OPC_UA["SA"]["POCO_DRENAGEM_NIVEL_MUITO_ALTO"], 25)
        self.leitura_falha_tubo_succao_bomba_recalque = LeituraOpcBit(self.opc, OPC_UA["SA"]["BOMBA_RECALQUE_TUBO_SUCCAO_FALHA"], 14)