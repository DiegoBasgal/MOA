__author__ = "Lucas Lavratti", "Diego Basgal"
__credits__ = "Lucas Lavratti" , "Diego Basgal"

__version__ = "0.2"
__status__ = "Development"
__maintainer__ = "Diego Basgal"
__email__ = "diego.garcia@ritmoenergia.com.br"
__description__ = "Este módulo corresponde a implementação de conexão com setores de campo (TDA, BAY, SE...)."



import logging
import threading

from time import sleep

from escrita import *
from leitura import *

from dicionarios.reg import *
from conversor_protocolo.conversor import *

from clients import ClientsUsn
from comporta import Comporta

logger = logging.getLogger("__main__")


class ServicoAuxiliar:
    ...

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

        self.opc = client

        self.dict = dicionario

        self.escrita_opc = escritas[0]
        self.escrita_opc_bit = escritas[1]

        self.cp1 = Comporta(1, self.opc, escritas)
        self.cp2 = Comporta(2, self.opc, escritas)
        Comporta.lista_comportas = [self.cp1, self.cp2]

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

    def resetar_emergencia(self):
        if not self.dict["GLB"]["tda_offline"]:
            self.escrita_opc_bit.escrever(OPC_UA["TDA"]["CP1_CMD_REARME_FALHAS"], valor=1, bit=0)
            self.escrita_opc_bit.escrever(OPC_UA["TDA"]["CP2_CMD_REARME_FALHAS"], valor=1, bit=0)
        else:
            logger.debug("[TDA] Não é possível resetar a emergência pois o CLP da TDA se encontra offline")

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

        self.opc = client

        self.escrita_opc = escritas[0]
        self.escrita_opc_bit = escritas[1]

    @property
    def tensao_rs(self) -> int | float:
        return self.__tensao_rs.valor

    @property
    def tensao_st(self) -> int | float:
        return self.__tensao_st.valor

    @property
    def tensao_tr(self) -> int | float:
        return self.__tensao_tr.valor

    def fechar_Dj52L(self):
        """if not self.get_flag_falha52L():
            return False
        else:"""
        # utilizar o write_value_bool para o ambiente em produção e write_single_register para a simulação
        res = self.escrita_opc_bit.escrever(OPC_UA["SE"]["CMD_SE_FECHA_52L"], valor=1, bit=4)
        return res

    def resetar_emergencia(self) -> bool:
        try:
            res = self.escrita_opc_bit.escrever(OPC_UA["UG"]["UG1_CMD_RESET_FALHAS_PASSOS"], valor=1, bit=0)
            res = self.escrita_opc_bit.escrever(OPC_UA["UG"]["UG1_CMD_REARME_BLOQUEIO_86M"], valor=1, bit=1)
            res = self.escrita_opc_bit.escrever(OPC_UA["UG"]["UG1_CMD_REARME_BLOQUEIO_86E"], valor=1, bit=2)
            res = self.escrita_opc_bit.escrever(OPC_UA["UG"]["UG1_CMD_REARME_BLOQUEIO_86H"], valor=1, bit=3)
            res = self.escrita_opc_bit.escrever(OPC_UA["UG"]["UG1_CMD_UHRV_REARME_FALHAS"], valor=1, bit=0)
            res = self.escrita_opc_bit.escrever(OPC_UA["UG"]["UG1_CMD_UHLM_REARME_FALHAS"], valor=1, bit=16)
            res = self.escrita_opc_bit.escrever(OPC_UA["UG"]["UG2_CMD_RESET_FALHAS_PASSOS"], valor=1, bit=0)
            res = self.escrita_opc_bit.escrever(OPC_UA["UG"]["UG2_CMD_REARME_BLOQUEIO_86M"], valor=1, bit=1)
            res = self.escrita_opc_bit.escrever(OPC_UA["UG"]["UG2_CMD_REARME_BLOQUEIO_86E"], valor=1, bit=2)
            res = self.escrita_opc_bit.escrever(OPC_UA["UG"]["UG2_CMD_REARME_BLOQUEIO_86H"], valor=1, bit=3)
            res = self.escrita_opc_bit.escrever(OPC_UA["UG"]["UG2_CMD_UHRV_REARME_FALHAS"], valor=1, bit=0)
            res = self.escrita_opc_bit.escrever(OPC_UA["UG"]["UG2_CMD_UHLM_REARME_FALHAS"], valor=1, bit=16)

            res = self.escrita_opc_bit.escrever(OPC_UA["SA"]["RESET_FALHAS_BARRA_CA"], valor=1, bit=0)
            res = self.escrita_opc_bit.escrever(OPC_UA["SA"]["RESET_FALHAS_SISTEMA_AGUA"], valor=1, bit=1)
            res = self.escrita_opc_bit.escrever(OPC_UA["SA"]["REARME_BLOQUEIO_GERAL_E_FALHAS_SA"], valor=1, bit=23)

            res = self.escrita_opc_bit.escrever(OPC_UA["SE"]["CMD_SE_REARME_BLOQUEIO_GERAL"], valor=1, bit=0)
            res = self.escrita_opc_bit.escrever(OPC_UA["SE"]["CMD_SE_REARME_86T"], valor=1, bit=1)
            res = self.escrita_opc_bit.escrever(OPC_UA["SE"]["CMD_SE_REARME_86BF"], valor=1, bit=2)
            res = self.escrita_opc_bit.escrever(OPC_UA["SE"]["REARME_86BF_86T"], valor=1, bit=22)
            res = self.escrita_opc_bit.escrever(OPC_UA["SE"]["CMD_SE_RESET_REGISTROS"], valor=1, bit=5)
            return res

        except Exception as e:
            logger.exception(f"[CON-SUB] Houve um erro ao realizar o reset geral. Exception: \"{repr(e)}\"")
            logger.exception(f"[CON-SUB] Traceback: {traceback.print_stack}")
            return False

    def verificar_tensao(self) -> bool:
        try:
            if (TENSAO_LINHA_BAIXA < self.tensao_rs < TENSAO_LINHA_ALTA) \
                and (TENSAO_LINHA_BAIXA < self.tensao_st < TENSAO_LINHA_ALTA) \
                and (TENSAO_LINHA_BAIXA < self.tensao_tr < TENSAO_LINHA_ALTA):
                return True
            else:
                logger.warning("[USN] Tensão da linha fora do limite.")
                return False

        except Exception as e:
            logger.exception(f"[USN] Houve um erro ao realizar a verificação da tensão na linha. Exception: \"{repr(e)}\"")
            logger.exception(f"[USN] Traceback: {traceback.print_stack}")

    def aguardar_tensao(self) -> bool:
        if self.status_tensao == 0:
            self.status_tensao = 1
            logger.debug("[USN] Iniciando o timer para a normalização da tensão na linha.")
            threading.Thread(target=lambda: self.timeout_tensao(600)).start()

        elif self.status_tensao == 2:
            logger.info("[USN] Tensão na linha reestabelecida.")
            self.status_tensao = 0
            return True

        elif self.status_tensao == 3:
            logger.critical("[USN] Não foi possível reestabelecer a tensão na linha. Acionando emergência")
            self.status_tensao = 0
            return False

        else:
            logger.debug("[USN] A tensão na linha ainda está fora.")

    def timeout_tensao(self, delay) -> None:
        while time() <= time() + delay:
            if self.verificar_tensao():
                self.status_tensao = 2
                return
            sleep(time() - (time() - 15))
        self.status_tensao = 3

    # TODO verificar flags de falha dj XAV
    """def get_flag_falha52L(self):
        # adicionar estado do disjuntor
        if LeituraOPC(self.opc, OPC_UA["REG_SA_EntradasDigitais_MXI_SA_DisjDJ1_SuperBobAbert1"]) == 0:
            logger.info("DisjDJ1_SuperBobAbert1")
            return True

        if LeituraOPC(self.opc, OPC_UA["REG_SA_EntradasDigitais_MXI_SA_DisjDJ1_SuperBobAbert2"]) == 0:
            logger.info("DisjDJ1_SuperBobAbert2")
            return True

        if LeituraOPC(self.opc, OPC_UA["REG_SA_EntradasDigitais_MXI_SA_DisjDJ1_Super125VccCiMot"]) == 0:
            logger.info("DisjDJ1_Super125VccCiMot")
            return True

        if LeituraOPC(self.opc, OPC_UA["REG_SA_EntradasDigitais_MXI_SA_DisjDJ1_Super125VccCiCom"]) == 0:
            logger.info("DisjDJ1_Super125VccCiCom")
            return True

        if LeituraOPC(self.opc, OPC_UA["REG_SA_EntradasDigitais_MXI_SA_DisjDJ1_AlPressBaixa"]) == 1:
            logger.info("DisjDJ1_AlPressBaixa")
            return True

        if LeituraOPC(self.opc, OPC_UA["REG_SA_RetornosDigitais_MXR_DJ1_FalhaInt"]) == 1:
            logger.info("MXR_DJ1_FalhaInt")
            return True

        if LeituraOPC(self.opc, OPC_UA["REG_SA_EntradasDigitais_MXI_SA_DisjDJ1_BloqPressBaixa"]) == 1:
            logger.info("DisjDJ1_BloqPressBaixa")
            return True

        if LeituraOPC(self.opc, OPC_UA["REG_SA_EntradasDigitais_MXI_SA_DisjDJ1_Sup125VccBoFeAb1"]) == 0:
            logger.info("DisjDJ1_Sup125VccBoFeAb1")
            return True

        if LeituraOPC(self.opc, OPC_UA["REG_SA_EntradasDigitais_MXI_SA_DisjDJ1_Sup125VccBoFeAb2"]) == 0:
            logger.info("DisjDJ1_Sup125VccBoFeAb2")
            return True

        if LeituraOPC(self.opc, OPC_UA["REG_SA_EntradasDigitais_MXI_SA_DisjDJ1_Local"])[0] == 1:
            logger.info("DisjDJ1_Local")
            return True

        if LeituraOPC(self.opc, OPC_UA["REG_SA_EntradasDigitais_MXI_SA_DisjDJ1_MolaDescarregada"])[0] == 1:
            logger.info("DisjDJ1_MolaDescarregada")
            return True

        return False"""

class Bay:
    def __init__(
            self,
            dados: dict | None = ...,
            conversor: NativoParaExterno | None = ...
        ) -> ...:

        if None in (conversor, dados):
            logger.warning("[CON-BAY] Erro ao carregar argumentos da classe \"ConectorBay\".")
            raise ImportError
        else:
            self.dados = dados
            self.conv = conversor

    def verificar_status_DJs(self) -> bool: 
        return


class Conector(TomadaAgua, Subestacao, Bay, ):
    def __init__(
            self,
            dicionario: dict | None = ...,
            clients: ClientsUsn | None = ...,
            escritas: list[EscritaBase] | None = ...
        ) -> ...:

        if not dicionario:
            logger.warning("[CON] Não foi possível carregar o arquivo com dicionário compartilhado (\"shared_dict\").")
        else:
            self.dict = dicionario

        if not clients:
            raise ConnectionError("[CON] Não foi possível carregar classe de conexão com Clients.")
        else:
            self.opc = clients.opc_client
            self.clp_ug1 = clients.clp_dict[1]
            self.clp_ug2 = clients.clp_dict[2]

        if not escritas:
            raise ValueError("[CON] Não foi possível carregar lista com classes de Escrita.")
        else:
            self.escrita_opc = escritas[0]
            self.escrita_opc_bit = escritas[1]
        
        TomadaAgua.__init__(self, self.dict, self.)


    def normalizar_emergencia(self) -> None:
        logger.info("[CON] Normalizando emergência.")
        self.resetar_emergencia()
        return

    def reconhecer_emergencia(self):
        logger.debug("XAV possui apenas reconhecimento interno de alarmes")

    def acionar_emergencia(self) -> None:
        logger.warning("FC: Acionando emergencia")
        try:
            self.escrita_opc_bit.escrever(OPC_UA["UG"]["UG1_CMD_PARADA_EMERGENCIA"], valor=1, bit=4)
            self.escrita_opc_bit.escrever(OPC_UA["UG"]["UG2_CMD_PARADA_EMERGENCIA"], valor=1, bit=4)
            sleep(5)
            self.escrita_opc_bit.escrever(OPC_UA["UG"]["UG1_CMD_PARADA_EMERGENCIA"], valor=0, bit=4)
            self.escrita_opc_bit.escrever(OPC_UA["UG"]["UG2_CMD_PARADA_EMERGENCIA"], valor=0, bit=4)

        except Exception as e:
            logger.exception(f"[CON] Houve um erro ao realizar acionar a emergência. Exception: \"{repr(e)}\"")
            logger.exception(f"[CON] Traceback: {traceback.print_stack}")
            return False