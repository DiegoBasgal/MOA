
from leitura import *
from dicionarios.reg import *
from dicionarios.dict import *
from dicionarios.const import *

class Comportas:
    def __init__(self) -> None:
        pass

    @property
    def etapa_comporta(self) -> int:
        try:
            aberta = LeituraOPCBit(self.client, REG_OPC["TDA"]["CP{}_ABERTA".format(self.id)], 17).valor
            fechada = LeituraOPCBit(self.client, REG_OPC["TDA"]["CP{}_FECHADA".format(self.id)], 18).valor
            cracking = LeituraOPCBit(self.client, REG_OPC["TDA"]["CP{}_CRACKING".format(self.id)], 25).valor
            remoto = LeituraOPCBit(self.client, REG_OPC["TDA"]["CP{}_REMOTO".format(self.id)], 22).valor

            if fechada:
                return COMPORTA_FECHADA
            elif aberta:
                return COMPORTA_ABERTA
            elif cracking:
                return COMPORTA_CRACKING
            elif remoto:
                return COMPORTA_REMOTO
            else:
                self.logger.debug("[UG{}] Comporta em etapa inconsistente".format(self.id))
                return False
        except Exception as e:
            raise(e)

    @property
    def permissao_comporta(self) -> bool:
        try:
            response = LeituraOPCBit(self.client, REG_OPC["TDA"]["CP{}_PERMISSIVOS_OK".format(self.id)], 31, True).valor
        except Exception as e:
            raise(e)
        else:
            return response

    @property
    def bloqueio_comporta(self) -> bool:
        try:
            response = LeituraOPCBit(self.client, REG_OPC["TDA"]["CP{}_BLOQUEIO_ATUADO".format(self.id)], 31, True).valor
        except Exception as e:
            raise(e)
        else:
            return response

    @property
    def status_comporta(self) -> int:
        try:
            response = LeituraOPC(self.client, REG_OPC["TDA"]["CP{}_COMPORTA_OPERANDO".format(self.id)]).valor
        except Exception as e:
            raise(e)
        else:
            return response

    @property
    def status_outra_comporta(self) -> int:
        try:
            response = LeituraOPC(self.client, REG_OPC["TDA"]["CP{}_COMPORTA_OPERANDO".format(2 if self.id == 1 else 1)]).valor
        except Exception as e:
            raise(e)
        else:
            return response

    @property
    def status_limpa_grades(self) -> int:
        try:
            response = LeituraOPC(self.client, REG_OPC["TDA"]["LG_OPERACAO_MANUAL"]).valor
        except Exception as e:
            raise (e)
        else:
            return response

    @property
    def status_valvula_borboleta(self) -> int:
        try:
            response = LeituraOPC(self.client, REG_OPC["TDA"]["VB_FECHANDO"]).valor
        except Exception as e:
            raise(e)
        else:
            return response

    @property
    def status_unidade_hidraulica(self) -> bool:
        try:
            response = LeituraOPCBit(self.client, REG_OPC["TDA"]["UH_UNIDADE_HIDRAULICA_DISPONIVEL"], 1).valor
        except Exception as e:
            raise(e)
        else:
            return response