
from leitura import *
from dicionarios.reg import *
from dicionarios.dict import *
from dicionarios.const import *

class Comportas:
    def __init__(self, id: int) -> None:
        pass

    @property
    def etapa_comporta(self) -> int:
        try:
            aberta = LeituraOPCBit(self.client, OPC_UA["TDA"][f"CP{self.id}_ABERTA"], 17).valor
            fechada = LeituraOPCBit(self.client, OPC_UA["TDA"][f"CP{self.id}_FECHADA"], 18).valor
            cracking = LeituraOPCBit(self.client, OPC_UA["TDA"][f"CP{self.id}_CRACKING"], 25).valor
            remoto = LeituraOPCBit(self.client, OPC_UA["TDA"][f"CP{self.id}_REMOTO"], 22).valor

            if fechada:
                return CP_FECHADA
            elif aberta:
                return CP_ABERTA
            elif cracking:
                return CP_CRACKING
            elif remoto:
                return CP_REMOTO
            else:
                self.logger.debug("[UG{}] Comporta em etapa inconsistente")
                return False
        except Exception as e:
            raise(e)

    @property
    def permissao_comporta(self) -> bool:
        try:
            response = LeituraOPCBit(self.client, OPC_UA["TDA"][f"CP{self.id}_PERMISSIVOS_OK"], 31, True).valor
        except Exception as e:
            raise(e)
        else:
            return response

    @property
    def bloqueio_comporta(self) -> bool:
        try:
            response = LeituraOPCBit(self.client, OPC_UA["TDA"][f"CP{self.id}_BLOQUEIO_ATUADO"], 31, True).valor
        except Exception as e:
            raise(e)
        else:
            return response

    @property
    def status_comporta(self) -> int:
        try:
            response = LeituraOPC(self.client, OPC_UA["TDA"][f"CP{self.id}_COMPORTA_OPERANDO"]).valor
        except Exception as e:
            raise(e)
        else:
            return response

    @property
    def status_outra_comporta(self) -> int:
        try:
            response = LeituraOPC(self.client, OPC_UA["TDA"][f"CP{self.id}_COMPORTA_OPERANDO".format(2 if self.id == 1 else 1)]).valor
        except Exception as e:
            raise(e)
        else:
            return response

    @property
    def status_limpa_grades(self) -> int:
        try:
            response = LeituraOPC(self.client, OPC_UA["TDA"]["LG_OPERACAO_MANUAL"]).valor
        except Exception as e:
            raise (e)
        else:
            return response

    @property
    def status_valvula_borboleta(self) -> int:
        try:
            response = LeituraOPC(self.client, OPC_UA["TDA"]["VB_FECHANDO"]).valor
        except Exception as e:
            raise(e)
        else:
            return response

    @property
    def status_unidade_hidraulica(self) -> bool:
        try:
            response = LeituraOPCBit(self.client, OPC_UA["TDA"]["UH_UNIDADE_HIDRAULICA_DISPONIVEL"], 1).valor
        except Exception as e:
            raise(e)
        else:
            return response
    
    def rearme_falhas_comporta(self) -> bool:
        try:
            response = EscritaOPCBit(self.client, OPC_UA["TDA"][f"CP{self.id}_CMD_REARME_FALHAS"], 0, 1)
        except Exception as e:
            raise(e)
        else:
            return response

    def verificar_precondicoes_comporta(self) -> bool:
        self.rearme_falhas_comporta()
        try:
            if self.status_unidade_hidraulica and not self.permissao_comporta and not self.bloqueio_comporta:
                if self.status_outra_comporta == (2 or 4 or 32) or self.status_valvula_borboleta != 0 or self.status_limpa_grades != 0:
                    self.logger.debug("[UG{0}] Não há condições para operar a comporta {0}")
                    if self.status_outra_comporta != 0:
                        self.logger.debug("[UG{}] A comporta {} está repondo".format(self.id, 2 if self.id == 1 else 1)) if self.status_outra_comporta == 2 else None
                        self.logger.debug("[UG{}] A comporta {} está abrindo".format(self.id, 2 if self.id == 1 else 1)) if self.status_outra_comporta == 4 else None
                        self.logger.debug("[UG{}] A comporta {} está em cracking".format(self.id, 2 if self.id == 1 else 1)) if self.status_outra_comporta == 32 else None
                        return False
                    elif self.status_limpa_grades != 0:
                        self.logger.debug("[UG{}] O limpa grades está em operação")
                        return False
                    elif self.status_valvula_borboleta != 0:
                        self.logger.debug("[UG{}] A válvula borboleta está em operação")
                        return False
                    else:
                        self.logger.debug("[UG{}] Favor aguardar normalização")
                        return False
            elif not self.status_unidade_hidraulica:
                self.logger.debug("[UG{}] A Unidade Hidráulica ainda não está disponível")
                return False
            elif self.bloqueio_comporta:
                self.logger.debug("[UG{0}] A comporta {0} ainda possui bloqueios ativados")
                return False
            elif self.permissao_comporta:
                self.logger.debug("[UG{0}] A permissão da comporta {0} ainda não foi concedida")
                return False
        except Exception as e:
            raise(e)
        else:
            return True

    def abrir_comporta(self) -> bool:
        try:
            if self.etapa_comporta == COMPORTA_ABERTA:
                self.logger.debug("[UG{0}] A comporta {0} já está aberta")
                return True
            elif self.verificar_precondicoes_comporta():
                press_equalizada = LeituraOPCBit(self.client, OPC_UA["TDA"][f"CP{self.id}_PRESSAO_EQUALIZADA"], 4)
                aguardando_cmd_abert = LeituraOPCBit(self.client, OPC_UA["TDA"][f"CP{self.id}_AGUARDANDO_COMANDO_ABERTURA"], 3)
                if press_equalizada.valor and aguardando_cmd_abert.valor:
                    self.logger.debug("[UG{0}] Enviando comando de abertura para a comporta {0}")
                    response = EscritaOPCBit(self.client, OPC_UA["TDA"][f"CP{self.id}_CMD_ABERTURA_TOTAL"], 1, 1)
                else:
                    return False
            else:
                return False
        except Exception as e:
            raise(e)
        else:
            return response
    
    def fechar_comporta(self) -> bool:
        try:
            if self.etapa_comporta == CP_FECHADA:
                self.logger.debug("[UG{0}] A comporta {0} já está fechada")
                return True
            else:
                response = EscritaOPCBit(self.client, OPC_UA["TDA"][f"CP{self.id}_CMD_FECHAMENTO"], 3, 1)
        except Exception as e:
            raise(e)
        else:
            return response

    def cracking_comporta(self) -> bool:
        try:
            if self.etapa_comporta == COMPORTA_CRACKING:
                self.logger.debug("[UG{0}] A comporta {} já está em cracking")
                return True
            elif self.verificar_precondicoes_comporta():
                self.logger.debug("[UG{0}] Enviando comando de cracking para a comporta {0}")
                response = EscritaOPCBit(self.client, OPC_UA["TDA"][f"CP{self.id}_CMD_ABERTURA_CRACKING"], 1, 1)
            else:
                return False
        except Exception as e:
            raise(e)
        else:
            return response