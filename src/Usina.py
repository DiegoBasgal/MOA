__version__ = "0.2"
__authors__ = "Lucas Lavratti", " Henrique Pfeifer"
__credits__ = ["Diego Basgal", ...]
__description__ = "Este módulo corresponde a implementação da operação da Usina."


import pytz
import logging

import mensageiro.voip as voip

from time import sleep, time
from datetime import  datetime

from leitura import *
from setor import *
from condicionador import *
from dicionarios.reg import *
from dicionarios.dict import *
from dicionarios.const import *

from conector import ClientsUsn
from banco_dados import BancoDados
from agendamentos import Agendamentos
from unidade_geracao import UnidadeGeracao

logger = logging.getLogger("__main__")

class Usina(UnidadeGeracao, ServicoAuxiliar, TomadaAgua, Subestacao, Bay):
    def __init__(
            self,
            config: dict | None = ...,
            dicionario: dict | None = ...,
            clients: ClientsUsn | None = ...,
            conversor: Conversor | None = ...,
            banco_dados: BancoDados | None = ...
        ):

        # VERIFICAÇÃO DE ARGUMENTOS
        if None in (config, dicionario):
            raise ValueError("[USN] Não foi possível carregar os arquivos de configuração (\"cfg.json\") e(ou) dicionário compartilhado (\"dicionário\").")
        else:
            self.cfg = config
            self.dct - dicionario

        if None in (clients, banco_dados):
            raise ConnectionError("[USN] Não foi possível carregar as classes de conexão com Clients e banco de dados.")
        else:
            self.bd = banco_dados
            self.cln = clients
            self.opc = clients.opc_client
            self.clp_moa = clients.clp_moa
            self.clp_ug1 = clients.clp_ug1
            self.clp_ug2 = clients.clp_ug2

        if not conversor:
            raise ValueError("[USN] Não foi possível carregar o conversor de dados \"Opc UA\" -> \"Opc DA\".")

        # INCIALIZAÇÃO DE OBJETOS DA USINA
        # Classes de Escrita Opc

        self.e_opc = EscritaOpc(self.opc)
        self.e_opc_bit = EscritaOpcBit(self.opc)
        self.es_opc = [self.e_opc, self.e_opc_bit]

        # Setores da Usina
        self.bay: Bay = Bay.__init__(self, conversor)
        self.se: Subestacao = Subestacao.__init__(self, self.dct, self.opc, self.es_opc)
        self.tda: TomadaAgua = TomadaAgua.__init__(self, self.dct, self.opc, self.es_opc)
        self.sa: ServicoAuxiliar = ServicoAuxiliar.__init__(self, self.dct, self.opc, self.es_opc)

        # Unidades de Geração
        self.ug1: UnidadeGeracao = UnidadeGeracao.__init__(self, 1, self.cfg, self.bd, self.es_opc, [self.opc, self.clp_ug1, self.clp_moa])
        self.ug2: UnidadeGeracao = UnidadeGeracao.__init__(self, 2, self.cfg, self.bd, self.es_opc, [self.opc, self.clp_ug2, self.clp_moa])

        self.ugs = [self.ug1, self.ug2]
        self.ug1.lista_ugs = self.ugs
        self.ug2.lista_ugs = self.ugs

        self.agn: Agendamentos = Agendamentos()


        # ATRIBUIÇÃO DE VARIÀVEIS PRIVADAS
        self.__split1: bool = False
        self.__split2: bool = False

        # self.__condicionadores = [condic for condics in [self.]]

        self.__potencia_ativa_kW = LeituraOpc(self.opc, "...")


        # ATRIBUIÇÃO DE VARIÁVEIS PROTEGIDAS
        # Numéricas
        self._tentativas_normalizar: int = 0
        self._potencia_alvo_anterior: int = -1

        # Booleanas
        self._modo_autonomo: bool = False


        # ATRIBUIÇÃO DE VARIÁVEIS PÚBLICAS
        # Numéricas
        self.estado_moa: int = 0

        self.pot_disp: int = 0
        self.ug_operando: int = 0

        self.bd_emergencia_acionada: int = 0
        self.modo_de_escolha_das_ugs: int = 0

        self.aguardando_reservatorio: int = 0

        self.controle_p: int | float = 0
        self.controle_i: int | float = 0
        self.controle_d: int | float = 0
        self.pot_alvo_anterior: int | float = -1

        self.erro_nv: int | float = 0
        self.erro_nv_anterior: int | float = 0
        self.nv_montante_recente: int | float = 0
        self.nv_montante_anterior: int | float = 0

        # Booleanas
        self.borda_emerg: bool = False
        self.acionar_voip: bool = False
        self.clp_emergencia: bool = False
        self.normalizar_forcado: bool = False


        # FINALIZAÇÃO DO __INIT__
        self.ler_valores()
        self.ajustar_unidades_inicializacao()
        self.normalizar_usina()
        self.escrever_valores()


    # Getters de variáveis PRIVADAS
    @property
    def potencia_ativa_kW(self) -> int | float:
        return self.__potencia_ativa_kW.valor


    # Getters e Setters de variáveis PROTEGIDAS
    @property
    def modo_autonomo(self) -> bool:
        return self._modo_autonomo

    @modo_autonomo.setter
    def modo_autonomo(self, var: bool) -> None:
        self._modo_autonomo = var
        self.bd.update_modo_moa(self._modo_autonomo)

    @property
    def tentativas_normalizar(self) -> int:
        return self._tentativas_normalizar

    @tentativas_normalizar.setter
    def tentativas_normalizar(self, var: int) -> None:
        self._tentativas_normalizar = var

    @property
    def pot_alvo_anterior(self) -> int | float:
        return self._potencia_alvo_anterior

    @pot_alvo_anterior.setter
    def pot_alvo_anterior(self, var: int | float):
        self._potencia_alvo_anterior = var


    def get_time(self) -> datetime:
        return datetime.now(pytz.timezone("Brazil/East")).replace(tzinfo=None)

    def ajustar_ie_padrao(self) -> int:
        return ([sum(ug.leitura_potencia) for ug in self.ugs] / self.cfg["pot_maxima_alvo"]) / self.ug_operando

    def ajustar_unidades_inicializacao(self) -> None:
        self.ug_operando += [1 for ug in self.ugs if ug.etapa_atual == UG_SINCRONIZADA]

        self.__split1 = True if self.ug_operando == 1 else False
        self.__split2 = True if self.ug_operando == 2 else False

        self.controle_ie = self.ajustar_ie_padrao()

    def verificar_condicionadores(self) -> int:
        if self.dct["GLB"]["avisado_eletrica"] or [condic.ativo for condic in self.condicionadores_essenciais]:
            condics_ativos = [condic for condics in [self.condicionadores_essenciais, self.condicionadores] for condic in condics if condic.ativo]
            condic_flag = [CONDIC_NORMALIZAR for condic in condics_ativos if condic.gravidade == CONDIC_NORMALIZAR]
            condic_flag = [CONDIC_INDISPONIBILIZAR for condic in condics_ativos if condic.gravidade == CONDIC_INDISPONIBILIZAR]

            if condic_flag in (CONDIC_NORMALIZAR, CONDIC_INDISPONIBILIZAR):
                logger.info("[USN] Foram detectados condicionadores ativos!")
                [logger.info(f"[USN] Condicionador: \"{condic.descr}\", Gravidade: \"{condic.gravidade}\".") for condic in condics_ativos]

    def acionar_emergencia(self):
        try:
            self.clp_emergencia = True
            [self.e_opc_bit.escrever(OPC_UA["UG"][f"UG{ug.id}_CMD_PARADA_EMERGENCIA"], valor=1, bit=4) for ug in self.ugs]
            sleep(5)
            [self.e_opc_bit.escrever(OPC_UA["UG"][f"UG{ug.id}_CMD_PARADA_EMERGENCIA"], valor=0, bit=4) for ug in self.ugs]

        except Exception as e:
            logger.exception(f"[CON] Houve um erro ao realizar acionar a emergência. Exception: \"{repr(e)}\"")
            logger.exception(f"[CON] Traceback: {traceback.print_stack}")
            return False

    def resetar_emergencia(self) -> None:
        logger.info("[USN] Acionando reset de emergência.")
        logger.debug("[USN] Bay resetado.") if self.bay.resetar_emergencia() else logger.info("[USN] Reset de emergência do Bay falhou.")
        logger.debug("[USN] Subestação resetada.") if self.se.resetar_emergencia() else logger.info("[USN] Reset de emergência da subestação falhou.")
        logger.debug("[USN] Tomada da Água resetada.") if self.tda.resetar_emergencia else logger.info("[USN] Reset de emergência da Tomada da Água falhou.")
        logger.debug("[USN] Serviço Auxiliar resetado.") if self.sa.resetar_emergencia() else logger.info("[USN] Reset de emergência do serviço auxiliar falhou.")

    def reconhecer_emergencia(self) -> None:
        logger.info("[USN] Reconhecendo emergência.")
        logger.debug("[USN] XAV possui apenas reconhecimento interno de alarmes")

    def normalizar_usina(self) -> bool:
        logger.debug("[USN] Normalizando...")
        logger.debug(f"[USN] Última tentativa: {self.ultima_tentativa_norm}. Tensão na linha: RS->{self.tensao_rs:2.1f}kV / ST->{self.tensao_st:2.1f}kV / TR->{self.tensao_tr:2.1f}kV")

        if not self.verificar_tensao():
            return False

        elif ((self.get_time() - self.ultima_tentativa_norm).seconds >= 60 * self.tentativas_normalizar) or self.normalizar_forcado:
            self.ultima_tentativa_norm = self.get_time()
            self.tentativas_normalizar += 1
            self.bd_emergencia = False
            self.clp_emergencia = False
            self.resetar_emergencia()
            self.bd.update_remove_emergencia()
            return True

        else:
            logger.debug("[USN] A normalização foi executada menos de 1 minuto atrás.")

    def leitura_periodica(self):
        proxima_leitura = time() + 1800
        logger.debug("Iniciando o timer de leitura por hora.")
        while True:
            try:
                if self.leituras_por_hora() and self.acionar_voip:
                    self.acionar_voip()
                for ug in self.ugs:
                    ug.leituras_por_hora()
                sleep(max(0, proxima_leitura - time()))

            except Exception:
                logger.debug("Houve um problema ao executar a leitura por hora")

            proxima_leitura += (time() - proxima_leitura) // 1800 * 1800 + 1800

    def acionar_voip(self):
        V_VARS = voip.VARS
        try:
            if self.acionar_voip:
                for i, j in zip(voip, V_VARS):
                    if i == j and self.dct["VOIP"][i]:
                        V_VARS[j][0] = self.dct["VOIP"][i]
                voip.enviar_voz_auxiliar()

            elif self.dct["GLB"]["avisado_eletrica"]:
                voip.enviar_voz_emergencia()
                self.dct["GLB"]["avisado_eletrica"] = False

        except Exception:
            logger.warning("Houve um problema ao ligar por Voip")

    def atualizar_montante_recente(self) -> None:
        if not self.dct["GLB"]["tda_offline"]:
            self.nv_montante_recente = self.nv_montante
            self.erro_nv_anterior = self.erro_nv
            self.erro_nv = self.nv_montante_recente - self.cfg["nv_alvo"]

    def atualizar_parametros_db(self, parametros) -> None:
        try:
            self.bd_emergencia = True if int(parametros["emergencia_acionada"]) == 1 else False
            logger.debug("[USN] Emergência acionada.")

            self.modo_autonomo = True if int(parametros["modo_autonomo"]) == 1 else False
            logger.debug(f"[USN] Modo autonomo que o banco respondeu: {int(parametros['modo_autonomo'])}")

            if not self.modo_de_escolha_das_ugs == int(parametros["modo_de_escolha_das_ugs"]):
                self.modo_de_escolha_das_ugs = int(parametros["modo_de_escolha_das_ugs"])
                logger.info(f"[USN] O modo de prioridade das ugs foi alterado (#{self.modo_de_escolha_das_ugs}).")

        except Exception as e:
            logger.exception(f"[USN] Houve um erro ao ler e atualizar os parâmetros do Banco de Dados. Exception: \"{repr(e)}\"")
            logger.exception(f"[USN] Traceback: {traceback.print_stack}")

    def atualizar_cfg(self, parametros) -> None:
        try:
            self.cfg["kp"] = float(parametros["kp"])
            self.cfg["ki"] = float(parametros["ki"])
            self.cfg["kd"] = float(parametros["kd"])
            self.cfg["kie"] = float(parametros["kie"])

            self.cfg["pt_kp"] = float(parametros["pt_kp"])
            self.cfg["pt_ki"] = float(parametros["pt_ki"])
            self.cfg["pt_kie"] = float(parametros["pt_kie"])
            self.cfg["press_turbina_alvo"] = float(parametros["press_turbina_alvo"])

            self.cfg["nv_alvo"] = float(parametros["nv_alvo"])
            self.cfg["nv_minimo"] = float(parametros["nv_minimo"])

            self.cfg["pot_maxima_alvo"] = float(parametros["pot_nominal"])
            self.cfg["pot_maxima_ug"] = float(parametros["pot_nominal_ug"])
            self.cfg["pot_maxima_usina"] = float(parametros["pot_nominal_ug"]) * 2

        except Exception as e:
            logger.exception(f"[USN] Houve um erro ao atualizar o arquivo de configuração \"cfg.json\". Exception: \"{repr(e)}\"")
            logger.exception(f"[USN] Traceback: {traceback.print_stack}")

    def heartbeat(self) -> None:
        try:
            agora = self.get_time()
            ano = int(agora.year)
            mes = int(agora.month)
            dia = int(agora.day)
            hor = int(agora.hour)
            mnt = int(agora.minute)
            seg = int(agora.second)
            mil = int(agora.microsecond / 1000)
            self.clp_moa.write_multiple_registers(0, [ano, mes, dia, hor, mnt, seg, mil])
            self.clp_moa.write_single_coil(MB["MOA"]["MOA_OUT_STATUS"], [self.estado_moa])
            self.clp_moa.write_single_coil(MB["MOA"]["MOA_OUT_MODE"], [self.modo_autonomo])

            if self.modo_autonomo:
                self.clp_moa.write_single_coil(MB["MOA"]["OUT_EMERG"], [self.clp_emergencia])
                self.clp_moa.write_multiple_registers(MB["MOA"]["OUT_SETPOINT"], [int(sum(ug.setpoint)) for ug in self.ugs])
                self.clp_moa.write_multiple_registers(MB["MOA"]["OUT_TARGET_LEVEL"], [int((self.cfg["nv_alvo"] - 800) * 1000)])

                if self.dct["GLB"]["avisado_eletrica"] and not self.borda_emerg:
                    [self.clp_moa.write_single_coil(MB["MOA"][f"OUT_BLOCK_UG{ug.id}"], [1]) for ug in self.ugs]
                    self.borda_emerg = True

                elif not self.dct["GLB"]["avisado_eletrica"] and self.borda_emerg:
                    [self.clp_moa.write_single_coil(MB["MOA"][f"OUT_BLOCK_UG{ug.id}"], [0]) for ug in self.ugs]
                    self.borda_emerg = False

                if self.clp_moa.read_coils(MB["MOA"]["IN_HABILITA_AUTO"])[0] == 1:
                    self.clp_moa.write_single_coil(MB["MOA"]["IN_HABILITA_AUTO"], [1])
                    self.clp_moa.write_single_coil(MB["MOA"]["IN_DESABILITA_AUTO"], [0])
                    self.modo_autonomo = True

                elif self.clp_moa.read_coils(MB["MOA"]["IN_DESABILITA_AUTO"])[0] == 1:
                    self.clp_moa.write_single_coil(MB["MOA"]["IN_HABILITA_AUTO"], [0])
                    self.clp_moa.write_single_coil(MB["MOA"]["IN_DESABILITA_AUTO"], [1])
                    self.modo_autonomo = False

                for ug in self.ugs:
                    if self.clp_moa.read_coils(MB["MOA"][f"OUT_BLOCK_UG{ug.id}"])[0] == 1:
                        self.clp_moa.write_single_coil(MB["MOA"][f"OUT_BLOCK_UG{ug.id}"], [1])
                    elif self.clp_moa.read_coils(MB["MOA"][f"OUT_BLOCK_UG{ug.id}"])[0] == 0:
                        self.clp_moa.write_single_coil(MB["MOA"][f"OUT_BLOCK_UG{ug.id}"], [0])

            elif not self.modo_autonomo:
                self.clp_moa.write_single_coil(MB["MOA"]["OUT_EMERG"], [0])
                self.clp_moa.write_single_coil(MB["MOA"]["OUT_SETPOINT"], [0])
                self.clp_moa.write_single_coil(MB["MOA"]["OUT_TARGET_LEVEL"], [0])
                [self.clp_moa.write_single_coil(MB["MOA"][f"OUT_BLOCK_UG{ug.id}"], [0]) for ug in self.ugs]

        except Exception as e:
            logger.exception(f"[USN] Houve um erro ao tentar escrever valores modbus no CLP MOA. Exception: \"{repr(e)}\"")
            logger.exception(f"[USN] Traceback: {traceback.print_stack}")

    def ler_valores(self) -> None:
        self.cln.ping_clients()
        try:
            if self.clp_moa.read_coils(MB["MOA"]["IN_EMERG"])[0] == 1 and not self.dct["GLB"]["avisado_eletrica"]:
                self.dct["GLB"]["avisado_eletrica"] = True
                for ug in self.ugs:
                    ug.deve_ler_condicionadores = True

            elif self.clp_moa.read_coils(MB["MOA"]["IN_EMERG"])[0] == 0 and self.dct["GLB"]["avisado_eletrica"]:
                self.dct["GLB"]["avisado_eletrica"] = True

            if self.clp_moa.read_coils(MB["MOA"]["IN_EMERG_UG1"])[0] == 1:
                self.ug1.deve_ler_condicionadores = True

            if self.clp_moa.read_coils(MB["MOA"]["IN_EMERG_UG2"])[0] == 1:
                self.ug2.deve_ler_condicionadores = True

            if self.clp_moa.read_coils(MB["MOA"]["IN_HABILITA_AUTO"])[0] == 1:
                self.clp_moa.write_single_coil(MB["MOA"]["IN_HABILITA_AUTO"], [1])
                self.clp_moa.write_single_coil(MB["MOA"]["IN_DESABILITA_AUTO"], [0])

            if self.clp_moa.read_coils(MB["MOA"]["IN_DESABILITA_AUTO"])[0] == 1:
                self.clp_moa.write_single_coil(MB["MOA"]["IN_HABILITA_AUTO"], [0])
                self.clp_moa.write_single_coil(MB["MOA"]["IN_DESABILITA_AUTO"], [1])

        except Exception as e:
            logger.exception(f"[USN] Houve um erro ao tentar ler valores modbus no CLP MOA. Exception: \"{repr(e)}\"")
            logger.exception(f"[USN] Traceback: {traceback.print_stack}")

        self.heartbeat()
        self.atualizar_montante_recente()

        parametros = self.bd.get_parametros_usina()
        self.atualizar_cfg(parametros)
        self.atualizar_parametros_db(parametros)
        for ug in self.ugs: ug.atualizar_limites_condicionadores(parametros)

    def escrever_valores(self) -> None:
        try:
            self.bd.update_valores_usina(
                self.get_time().strftime("%Y-%m-%d %H:%M:%S"),  # timestamp
                1 if self.aguardando_reservatorio else 0,  # aguardando_reservatorio
                True,  # DEPRECATED clp_online
                self.nv_montante, # nv_montante
                1 if self.ug1.disponivel else 0,  # ug1_disp
                self.ug1.leitura_potencia,  # ug1_pot
                self.ug1.setpoint,  # ug1_setpot
                self.ug1.etapa_atual,  # ug1_sinc
                self.ug1.leitura_horimetro,  # ug1_tempo
                1 if self.ug2.disponivel else 0,  # ug2_disp
                self.ug2.leitura_potencia,  # ug2_pot
                self.ug2.setpoint,  # ug2_setpot
                self.ug2.etapa_atual,  # ug2_sinc
                self.ug2.leitura_horimetro,  # ug2_tempo
            )

        except Exception as e:
            logger.exception(f"[USN] Houve um erro ao inserir os valores no banco. Exception: \"{repr(e)}\"")
            logger.exception(f"[USN] Traceback: {traceback.print_stack}")

        try:
            self.bd.insert_debug(
                self.get_time().timestamp(),
                self.cfg["kp"],
                self.cfg["ki"],
                self.cfg["kd"],
                self.cfg["kie"],
                self.controle_p,
                self.controle_i,
                self.controle_d,
                self.controle_ie,
                self.ug1.setpoint,
                self.ug1.leitura_potencia,
                self.ug2.setpoint,
                self.ug2.leitura_potencia,
                self.nv_montante_recente,
                self.erro_nv,
                1 if self.modo_autonomo else 0,
                self.cfg["cx_kp"],
                self.cfg["cx_ki"],
                self.cfg["cx_kie"],
                0,
            )

        except Exception as e:
            logger.exception(f"[USN] Houve um erro ao inserir dados DEBUG do controle de potência normal no banco. Exception: \"{repr(e)}\"")
            logger.exception(f"[USN] Traceback: {traceback.print_stack}")

    def distribuir_potencia(self, pot_alvo):
        if self.potencia_alvo_anterior == -1:
            self.potencia_alvo_anterior = pot_alvo

        if pot_alvo < 0.1:
            for ug in self.ugs:
                ug.setpoint = 0
            return 0

        logger.debug("Pot alvo = {}".format(pot_alvo))

        pot_medidor = self.potencia_ativa_kW
        logger.debug("Pot no medidor = {}".format(pot_medidor))

        # implementação nova
        pot_aux = self.cfg["pot_maxima_alvo"] - (self.cfg["pot_maxima_usina"] - self.cfg["pot_maxima_alvo"])

        pot_medidor = max(pot_aux, min(pot_medidor, self.cfg["pot_maxima_usina"]))

        try:
            if pot_medidor > self.cfg["pot_maxima_alvo"]:
                pot_alvo = self.pot_alvo_anterior * (1 - ((pot_medidor - self.cfg["pot_maxima_alvo"]) / self.cfg["pot_maxima_alvo"]))

        except TypeError as e:
            logger.info("A comunicação com os MFs falharam.")

        self.pot_alvo_anterior = pot_alvo
        
        logger.debug("Pot alvo após ajuste medidor = {}".format(pot_alvo))

        ugs: list[UnidadeGeracao] = self.controle_ugs_disponiveis()
        self.pot_disp = 0

        logger.debug("lista_de_ugs_disponiveis:")
        for ug in ugs:
            logger.debug("UG{}".format(ug.id))
            self.pot_disp += ug.cfg["pot_maxima_ug{}".format(ugs[0].id)]
        if ugs is None:
            return False
        elif len(ugs) == 0:
            return False

        logger.debug("Distribuindo {}".format(pot_alvo))

        sp = pot_alvo / self.cfg["pot_maxima_usina"]

        self.__split1 = True if sp > (0) else self.__split1
        self.__split2 = (True if sp > (0.5 + self.cfg["margem_pot_critica"]) else self.__split2)

        self.__split2 = False if sp < (0.5) else self.__split2
        self.__split1 = False if sp < (self.cfg["pot_minima"] / self.cfg["pot_maxima_usina"]) else self.__split1

        logger.debug(f"Sp {sp}")
        if len(ugs) == 2:

            if self.__split2:
                logger.debug("Split 2")
                ugs[0].setpoint = sp * ugs[0].cfg[f"pot_maxima_ug{self.id}"]
                ugs[1].setpoint = sp * ugs[1].cfg[f"pot_maxima_ug{self.id}"]

            elif self.__split1:
                logger.debug("Split 1")
                sp = sp * 2 / 1
                ugs[0].setpoint = sp * ugs[0].cfg[f"pot_maxima_ug{self.id}"]
                ugs[1].setpoint = 0
            else:
                for ug in ugs:
                    ug.setpoint = 0

        elif len(ugs) == 1:
            if self.__split1 or self.__split2:
                logger.debug("Split 1B")
                sp = sp * 2 / 1
                ugs[0].setpoint = sp * ugs[0].cfg[f"pot_maxima_ug{self.id}"]

            else:
                for ug in ugs:
                    ug.setpoint = 0

        for ug in self.ugs:
            logger.debug("UG{} SP:{}".format(ug.id, ug.setpoint))

        return pot_alvo

    def controle_ugs_disponiveis(self) -> list:
        ls = [ug for ug in self.ugs if ug.disponivel and not ug.etapa_atual == UG_PARANDO]

        if self.modo_de_escolha_das_ugs == MODO_ESCOLHA_MANUAL:
            ls = sorted(ls, key=lambda y: (-1 * y.leitura_potencia.valor, -1 * y.setpoint, y.prioridade,))
            logger.debug("")
            logger.debug("[USN] UGs disponíveis em ordem (prioridade):")
        else:
            ls = sorted(ls, key=lambda y: (y.leitura_horimetro.valor, -1 * y.leitura_potencia.valor, -1 * y.setpoint,))
            logger.debug("")
            logger.debug("[USN] UGs disponíveis em ordem (horas-máquina):")

        return ls

    def controle_normal(self):
        logger.debug("-------------------------------------------------")
        # Calcula PID
        logger.debug("Alvo: {:0.3f}, Recente: {:0.3f}".format(self.cfg["nv_alvo"], self.nv_montante_recente))
        self.controle_p = self.cfg["kp"] * self.erro_nv
        self.controle_i = max(min((self.cfg["ki"] * self.erro_nv) + self.controle_i, 0.8), 0)
        self.controle_d = self.cfg["kd"] * (self.erro_nv - self.erro_nv_anterior)
        saida_pid = (self.controle_p + self.controle_i + min(max(-0.3, self.controle_d), 0.3))
        logger.debug("PID: {:0.3f} <-- P:{:0.3f} + I:{:0.3f} + D:{:0.3f}; ERRO={}".format(
                saida_pid,
                self.controle_p,
                self.controle_i,
                self.controle_d,
                self.erro_nv,))

        # Calcula o integrador de estabilidade e limita
        self.controle_ie = max(min(saida_pid + self.controle_ie * self.cfg["kie"], 1), 0)

        if self.nv_montante_recente >= (self.cfg["nv_maximo"] + 0.03):
            self.controle_ie = 1
            self.controle_i = 1 - self.controle_p

        if self.nv_montante_recente <= (self.cfg["nv_minimo"] + 0.03):
            self.controle_ie = min(self.controle_ie, 0.3)
            self.controle_i = 0

        logger.debug("IE: {:0.3f}".format(self.controle_ie))

        # Arredondamento e limitação
        pot_alvo = max(min(round(self.cfg["pot_maxima_usina"] * self.controle_ie, 5), self.cfg["pot_maxima_usina"],), self.cfg["pot_minima"],)

        logger.debug("Pot alvo: {:0.3f}".format(pot_alvo))
        logger.debug("Nv alvo: {:0.3f}".format(self.cfg["nv_alvo"]))

    def controle_reservatorio(self) -> int:
        # Reservatório acima do nível máximo
        if self.nv_montante >= self.cfg["nv_maximo"]:
            logger.info("[USN] Nível montante acima do máximo.")

            if self.nv_montante_recente >= NIVEL_MAXIMORUM:
                logger.critical(f"[USN] Nivel montante ({self.nv_montante_recente:3.2f}) atingiu o maximorum!")
                self.distribuir_potencia(0)
                for ug in self.ugs: ug.step()
                return NV_FLAG_EMERGENCIA

            else:
                self.controle_i = 0.5
                self.controle_ie = 0.5
                self.distribuir_potencia(self.cfg["pot_maxima_usina"])
                for ug in self.ugs: ug.step()

        # Reservatório abaixo do nível mínimo
        elif self.nv_montante <= self.cfg["nv_minimo"] and not self.aguardando_reservatorio:
            logger.info("[USN] Nível montante abaixo do mínimo.")
            self.aguardando_reservatorio = True
            self.distribuir_potencia(0)
            for ug in self.ugs: ug.step()

            if self.nv_montante_recente <= NIVEL_FUNDO_RESERVATORIO:
                logger.critical(f"[USN] Nivel montante ({self.nv_montante_recente:3.2f}) atingiu o fundo do reservatorio!")
                return NV_FLAG_EMERGENCIA

        # Aguardando nível do reservatório
        elif self.aguardando_reservatorio:
            if self.nv_montante >= self.cfg["nv_alvo"]:
                logger.debug("[USN] Nível montante dentro do limite de operação.")
                self.aguardando_reservatorio = False

        # Reservatório Normal
        else:
            self.controle_normal()
            for ug in self.ugs: ug.step()

        return NV_FLAG_NORMAL
