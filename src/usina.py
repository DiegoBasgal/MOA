__version__ = "0.2"
__authors__ = "Lucas Lavratti", " Henrique Pfeifer"
__credits__ = ["Diego Basgal", ...]
__description__ = "Este módulo corresponde a implementação da operação da Usina."


import pytz
import logging
import traceback

import dicionarios.dict as Dicionarios

from time import sleep, time
from datetime import  datetime, timedelta

from condicionador import *
from dicionarios.reg import *
from dicionarios.const import *

from conector import ClientesUsina
from banco_dados import BancoDados
from unidade_geracao import UnidadeGeracao
from condicionador import CondicionadorBase

from mensageiro.voip import Voip
from leitura_escrita.leitura import *
from leitura_escrita.escrita import *
from conversor_protocolo.conversor import *

from bay import Bay
from comporta import Comporta
from subestacao import Subestacao
from tomada_agua import TomadaAgua
from servico_auxiliar import ServicoAuxiliar

logger = logging.getLogger("__main__")

class Usina:
    def __init__(self, cfg: dict = None):

        # VERIFICAÇÃO DE ARGUMENTOS

        if None in (cfg):
            raise ValueError("[USN] Não foi possível carregar os arquivos de configuração (\"cfg.json\").")
        else:
            self.cfg = cfg

        self.clp = ClientesUsina.clp
        self.rele = ClientesUsina.rele

        # INCIALIZAÇÃO DE OBJETOS DA USINA

        self.bay= Bay(self)
        self.se = Subestacao(self)
        self.tda = TomadaAgua(self)
        self.sa = ServicoAuxiliar(self)
        self.ug1 = UnidadeGeracao(self, 1)
        self.ug2 = UnidadeGeracao(self, 2)

        self.ugs: "list[UnidadeGeracao]" = [self.ug1, self.ug2]
        self.setores = [self.bay, self.se, self.tda, self.sa]

        self.ug1.lista_ugs = self.ugs
        self.ug2.lista_ugs = self.ugs

        self.cp: "dict[str, Comporta]" = {}
        self.cp["CP1"] = Comporta(1)
        self.cp["CP2"] = Comporta(2)

        # ATRIBUIÇÃO DE VARIÀVEIS
        # PRIVADAS
        self.__split1: bool = False
        self.__split2: bool = False

        self.__potencia_ativa_kW = LeituraModbus(self.clp["SA"], 999, escala=1, op=4)

        # PROTEGIDAS
        self._tentativas_normalizar: int = 0
        self._potencia_alvo_anterior: int = -1

        self._modo_autonomo: bool = False

        # PÚBLICAS
        self.estado_moa: int = 0

        self.pot_disp: int = 0
        self.ug_operando: int = 0

        self.bd_emergencia_acionada: int = 0
        self.modo_de_escolha_das_ugs: int = 0

        self.aguardando_reservatorio: int = 0

        self.controle_p: float = 0
        self.controle_i: float = 0
        self.controle_d: float = 0
        self.pot_alvo_anterior: float = -1

        self.clp_emerg: bool = False
        self.voip_emerg: bool = False
        self.borda_emerg: bool = False
        self.normalizar_forcado: bool = False

        self.glb_dict = Dicionarios.globais

        # FINALIZAÇÃO DO __INIT__
        self.ler_valores()
        self.ajustar_unidades_init()
        self.normalizar_usina()
        self.escrever_valores()

    # Getters de variáveis PRIVADAS
    @property
    def potencia_ativa_kW(self) -> float:
        return self.__potencia_ativa_kW.valor


    # Getters e Setters de variáveis PROTEGIDAS
    @property
    def modo_autonomo(self) -> bool:
        return self._modo_autonomo

    @modo_autonomo.setter
    def modo_autonomo(self, var: bool) -> None:
        self._modo_autonomo = var
        BancoDados.update_modo_moa(var)

    @property
    def tentativas_normalizar(self) -> int:
        return self._tentativas_normalizar

    @tentativas_normalizar.setter
    def tentativas_normalizar(self, var: int) -> None:
        self._tentativas_normalizar = var

    @property
    def pot_alvo_anterior(self) -> float:
        return self._potencia_alvo_anterior

    @pot_alvo_anterior.setter
    def pot_alvo_anterior(self, var: float):
        self._potencia_alvo_anterior = var

    @staticmethod
    def get_time() -> datetime:
        return datetime.now(pytz.timezone("Brazil/East")).replace(tzinfo=None)

    def ajustar_ie_padrao(self) -> int:
        return (sum(ug.leitura_potencia for ug in self.ugs) / self.cfg["pot_maxima_alvo"]) / self.ug_operando

    def ajustar_unidades_init(self) -> None:
        self.ug_operando += [1 for ug in self.ugs if ug.etapa_atual == UG_SINCRONIZADA]

        self.__split1 = True if self.ug_operando == 1 else False
        self.__split2 = True if self.ug_operando == 2 else False

        self.controle_ie = self.ajustar_ie_padrao()

    def verificar_condicionadores(self) -> int:
        flag_bay = self.bay.verificar_condicionadores()
        flag_se = self.se.verificar_condicionadores()
        flag_tda = self.tda.verificar_condicionadores()
        flag_sa = self.sa.verificar_condicionadores()
        if CONDIC_INDISPONIBILIZAR in (flag_bay, flag_se, flag_tda, flag_sa):
            return CONDIC_INDISPONIBILIZAR
        elif CONDIC_NORMALIZAR in (flag_bay, flag_se, flag_tda, flag_sa):
            return CONDIC_NORMALIZAR
        else:
            return CONDIC_IGNORAR

    def reconhecer_emergencia(self) -> None:
        logger.info("[USN] Reconhecendo emergência.")
        logger.debug("[USN] XAV possui apenas reconhecimento interno de alarmes")

    def resetar_emergencia(self) -> None:
        logger.info("[USN] Acionando reset de emergência.")
        logger.debug("[USN] Bay resetado.") if self.bay.resetar_emergencia() else logger.info("[USN] Reset de emergência do Bay falhou.")
        logger.debug("[USN] Subestação resetada.") if self.se.resetar_emergencia() else logger.info("[USN] Reset de emergência da subestação falhou.")
        logger.debug("[USN] Tomada da Água resetada.") if self.tda.resetar_emergencia else logger.info("[USN] Reset de emergência da Tomada da Água falhou.")
        logger.debug("[USN] Serviço Auxiliar resetado.") if self.sa.resetar_emergencia() else logger.info("[USN] Reset de emergência do serviço auxiliar falhou.")

    def acionar_emergencia(self):
        try:
            self.clp_emergencia = True
            [EscritaModBusBit.escrever_bit(self.clp[f"UG{ug.id}"], REG_CLP["UG"][f"UG{ug.id}_CMD_PARADA_EMERGENCIA"], bit=4, valor=1) for ug in self.ugs]
            sleep(5)
            [EscritaModBusBit.escrever_bit(self.clp[f"UG{ug.id}"], REG_CLP["UG"][f"UG{ug.id}_CMD_PARADA_EMERGENCIA"], bit=4, valor=0) for ug in self.ugs]

        except Exception as e:
            logger.exception(f"[USN] Houve um erro ao realizar acionar a emergência. Exception: \"{repr(e)}\"")
            logger.debug(f"[USN] Traceback: {traceback.format_exc()}")
            return False

    def normalizar_usina(self) -> bool:
        logger.debug("[USN] Normalizando...")
        logger.debug(f"[USN] Última tentativa: {self.ultima_tentativa_norm}. Tensão na linha: RS->{self.se.tensao_rs:2.1f}kV / ST->{self.se.tensao_st:2.1f}kV / TR->{self.se.tensao_tr:2.1f}kV")

        if not self.bay.verificar_status_DjBay():
            logger.warning("[USN] Enviando comando de fechamento de Disjuntor do Bay")
            if not self.bay.realizar_fechamento_DjBay():
                return None

        if not self.se.dj_se:
            logger.warning("[USN] Enviando comando de fechamento do Disjuntor 52L")
            if not self.se.fechar_Dj52L():
                logger.warning("[USN] Não foi possível realizar o fechameto do Disjuntor 52L")
                return None

        if not self.se.verificar_tensao():
            return False

        elif ((self.get_time() - self.ultima_tentativa_norm).seconds >= 60 * self.tentativas_normalizar) or self.normalizar_forcado:
            self.ultima_tentativa_norm = self.get_time()
            self.tentativas_normalizar += 1
            self.bd_emergencia = self.clp_emergencia = False
            for setor in self.setores: setor.resetar_emergencia()
            BancoDados.update_remove_emergencia()
            return True

        else:
            logger.debug("[USN] A normalização foi executada menos de 1 minuto atrás.")

    def leitura_temporizada(self):
        logger.debug("Iniciando o timer de leitura periódica. Tempo definido -> \"30 min\".")
        while True:
            for ug in self.ugs: ug.leitura_periodica()
            for setor in self.setores: setor.leitura_periodica()
            if True in (Dicionarios.voip[r][0] for r in Dicionarios.voip):
                Voip.acionar_chamada()
                pass
            sleep(max(0, (time() + 1800) - time()))

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
            logger.debug(f"[USN] Traceback: {traceback.format_exc()}")

    def atualizar_cfg(self, parametros) -> None:
        try:
            self.cfg["kp"] = float(parametros["kp"])
            self.cfg["ki"] = float(parametros["ki"])
            self.cfg["kd"] = float(parametros["kd"])
            self.cfg["kie"] = float(parametros["kie"])

            self.cfg["nv_alvo"] = float(parametros["nv_alvo"])
            self.cfg["nv_minimo"] = float(parametros["nv_minimo"])

            self.cfg["pot_maxima_alvo"] = float(parametros["pot_nominal"])
            self.cfg["pot_maxima_ug"] = float(parametros["pot_nominal_ug"])
            self.cfg["pot_maxima_usina"] = float(parametros["pot_nominal_ug"]) * 2

            with open(os.path.join(os.path.dirname(__file__), 'config.json'), 'w') as file:
                json.dump(self.cfg, file)

        except Exception as e:
            logger.exception(f"[USN] Houve um erro ao atualizar o arquivo de configuração \"cfg.json\". Exception: \"{repr(e)}\"")
            logger.debug(f"[USN] Traceback: {traceback.format_exc()}")

    def heartbeat(self) -> None:
        try:
            self.clp["MOA"].write_single_coil(REG_CLP["MOA"]["MOA_OUT_MODE"], [self.modo_autonomo])
            self.clp["MOA"].write_single_register(REG_CLP["MOA"]["MOA_OUT_STATUS"], [self.estado_moa])

            if self.modo_autonomo:
                self.clp["MOA"].write_single_coil(REG_CLP["MOA"]["OUT_EMERG"], [self.clp_emergencia])
                self.clp["MOA"].write_multiple_registers(REG_CLP["MOA"]["OUT_SETPOINT"], [int(sum(ug.setpoint)) for ug in self.ugs])
                self.clp["MOA"].write_multiple_registers(REG_CLP["MOA"]["OUT_TARGET_LEVEL"], [int((self.cfg["nv_alvo"] - 800) * 1000)])

                if self.clp["MOA"].read_coils(REG_CLP["MOA"]["IN_HABILITA_AUTO"])[0] == 1:
                    self.clp["MOA"].write_single_coil(REG_CLP["MOA"]["IN_HABILITA_AUTO"], [1])
                    self.clp["MOA"].write_single_coil(REG_CLP["MOA"]["IN_DESABILITA_AUTO"], [0])
                    self.modo_autonomo = True

                elif self.clp["MOA"].read_coils(REG_CLP["MOA"]["IN_DESABILITA_AUTO"])[0] == 1:
                    self.clp["MOA"].write_single_coil(REG_CLP["MOA"]["IN_HABILITA_AUTO"], [0])
                    self.clp["MOA"].write_single_coil(REG_CLP["MOA"]["IN_DESABILITA_AUTO"], [1])
                    self.modo_autonomo = False

                if self.clp["MOA"].read_coils(REG_CLP["MOA"]["IN_EMERG"])[0] == 1 and not self.glb_dict["avisado_eletrica"]:
                    self.glb_dict["avisado_eletrica"] = True
                    [ug.verificar_condicionadores() for ug in self.ugs]

                elif self.clp["MOA"].read_coils(REG_CLP["MOA"]["IN_EMERG"])[0] == 0 and self.glb_dict["avisado_eletrica"]:
                    self.glb_dict["avisado_eletrica"] = True

                if self.glb_dict["avisado_eletrica"] and not self.borda_emerg:
                    [self.clp["MOA"].write_single_coil(REG_CLP["MOA"][f"OUT_BLOCK_UG{ug.id}"], [1]) for ug in self.ugs]
                    self.borda_emerg = True

                elif not self.glb_dict["avisado_eletrica"] and self.borda_emerg:
                    [self.clp["MOA"].write_single_coil(REG_CLP["MOA"][f"OUT_BLOCK_UG{ug.id}"], [0]) for ug in self.ugs]
                    self.borda_emerg = False

                for ug in self.ugs:
                    if self.clp["MOA"].read_coils(REG_CLP["MOA"][f"IN_EMERG_UG{ug.id}"])[0] == 1:
                        ug.verificar_condicionadores()

                    if self.clp["MOA"].read_coils(REG_CLP["MOA"][f"OUT_BLOCK_UG{ug.id}"])[0] == 1:
                        self.clp["MOA"].write_single_coil(REG_CLP["MOA"][f"OUT_BLOCK_UG{ug.id}"], [1])
                    elif self.clp["MOA"].read_coils(REG_CLP["MOA"][f"OUT_BLOCK_UG{ug.id}"])[0] == 0:
                        self.clp["MOA"].write_single_coil(REG_CLP["MOA"][f"OUT_BLOCK_UG{ug.id}"], [0])

            elif not self.modo_autonomo:
                if self.clp["MOA"].read_coils(REG_CLP["MOA"]["IN_HABILITA_AUTO"])[0] == 1:
                    self.clp["MOA"].write_single_coil(REG_CLP["MOA"]["IN_HABILITA_AUTO"], [1])
                    self.clp["MOA"].write_single_coil(REG_CLP["MOA"]["IN_DESABILITA_AUTO"], [0])
                    self.modo_autonomo = True

                self.clp["MOA"].write_single_coil(REG_CLP["MOA"]["OUT_EMERG"], [0])
                self.clp["MOA"].write_single_register(REG_CLP["MOA"]["OUT_SETPOINT"], [0])
                self.clp["MOA"].write_single_register(REG_CLP["MOA"]["OUT_TARGET_LEVEL"], [0])
                [self.clp["MOA"].write_single_coil(REG_CLP["MOA"][f"OUT_BLOCK_UG{ug.id}"], [0]) for ug in self.ugs]

        except Exception as e:
            logger.exception(f"[USN] Houve um erro ao tentar escrever valores modbus no CLP MOA. Exception: \"{repr(e)}\"")
            logger.debug(f"[USN] Traceback: {traceback.format_exc()}")

    def ler_valores(self) -> None:
        ClientesUsina.ping_clients()
        self.heartbeat()
        self.tda.atualizar_montante_recente()

        parametros = BancoDados.get_parametros_usina()
        self.atualizar_cfg(parametros)
        self.atualizar_parametros_db(parametros)
        [ug.atualizar_limites_condicionadores(parametros) for ug in self.ugs]

    def escrever_valores(self) -> None:
        try:
            BancoDados.update_valores_usina(
                self.get_time().strftime("%Y-%m-%d %H:%M:%S"), # timestamp
                1 if self.aguardando_reservatorio else 0,  # aguardando_reservatorio
                True,  # DEPRECATED clp_online
                self.tda.nv_montante, # nv_montante
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
            logger.debug(f"[USN] Traceback: {traceback.format_exc()}")

        try:
            BancoDados.insert_debug(
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
                self.tda.nv_montante_recente,
                self.tda.erro_nv,
                1 if self.modo_autonomo else 0,
            )

        except Exception as e:
            logger.exception(f"[USN] Houve um erro ao inserir dados DEBUG do controle de potência normal no banco. Exception: \"{repr(e)}\"")
            logger.debug(f"[USN] Traceback: {traceback.format_exc()}")

    def ajuste_potencia(self, pot_alvo) -> float:
        self.pot_alvo_anterior = pot_alvo if self.pot_alvo_anterior == -1 else ...

        if pot_alvo < 0.1:
            for ug in self.ugs:
                ug.setpoint = 0
            return 0

        logger.debug(f"[USN] Potência no medidor = {self.potencia_ativa_kW:0.3f}")

        pot_aux = self.cfg["pot_maxima_alvo"] - (self.cfg["pot_maxima_usina"] - self.cfg["pot_maxima_alvo"])
        pot_medidor = max(pot_aux, min(self.potencia_ativa_kW, self.cfg["pot_maxima_usina"]))

        try:
            if pot_medidor > self.cfg["pot_maxima_alvo"]:
                pot_alvo = self.pot_alvo_anterior * (1 - ((pot_medidor - self.cfg["pot_maxima_alvo"]) / self.cfg["pot_maxima_alvo"]))
        except TypeError as te:
            logger.exception(f"[USN] A comunicação com os MFs falharam. Exception: \"{repr(te)}\"")
            logger.debug(f"[USN] Traceback: {traceback.format_exc()}")

        self.pot_alvo_anterior = pot_alvo

        logger.debug(f"[USN] Pot alvo pós ajuste: {pot_alvo:0.3f}")
        self.distribuir_potencia(pot_alvo)
        return pot_alvo

    def distribuir_potencia(self, pot_alvo) -> None:
        ugs = self.controle_ugs_disponiveis()
        if ugs is None:
            logger.warning("[USN] Sem UGs disponíveis para realizar a distribuição de potência.")
            return

        logger.debug(f"[USN] UG{[ug.id for ug in ugs]}")

        self.pot_disp = [sum(self.cfg[f"pot_maxima_ug{ug.id}"]) for ug in self.ugs if ug.disponivel]
        ajuste_manual = min(max(0, [sum(ug.leitura_potencia) for ug in self.ugs if ug.manual]))

        logger.debug(f"[USN] Distribuindo: {pot_alvo - ajuste_manual:0.3f}")
        sp = (pot_alvo - ajuste_manual) / self.cfg["pot_maxima_usina"]

        self.__split1 = True if sp > (0) else self.__split1
        self.__split2 = (True if sp > (0.5 + self.cfg["margem_pot_critica"]) else self.__split2)

        self.__split2 = False if sp < (0.5) else self.__split2
        self.__split1 = False if sp < (self.cfg["pot_minima"] / self.cfg["pot_maxima_usina"]) else self.__split1

        logger.debug(f"[USN] SP<-{sp}")
        if len(ugs) == 2:
            if self.__split2:
                logger.debug("[USN] Split 2")
                ugs[0].setpoint = sp * self.cfg[f"pot_maxima_ug{ugs[0].id}"]
                ugs[1].setpoint = sp * self.cfg[f"pot_maxima_ug{ugs[1].id}"]

            elif self.__split1:
                logger.debug("[USN] Split 1")
                ugs[0].setpoint = (sp * 2 / 1) * self.cfg[f"pot_maxima_ug{ugs[0].id}"]
                ugs[1].setpoint = 0

        elif len(ugs) == 1:
            logger.debug("[USN] Split 1B")
            ugs[0].setpoint = (sp * 2 / 1) * self.cfg[f"pot_maxima_ug{ugs[0].id}"] if self.__split1 or self.__split2 else ...

        else:
            for ug in ugs:
                ug.setpoint = 0

    def controle_inicial(self) -> None:
        self.ug_operando += [1 for ug in self.ugs if ug.etapa_atual == UG_SINCRONIZADA]

        self.__split1 = True if self.ug_operando == 1 else False
        self.__split2 = True if self.ug_operando == 2 else False

        self.controle_ie = self.ajustar_ie_padrao()

    def controle_ugs_disponiveis(self) -> "list[UnidadeGeracao]":
        ls = []
        [ls.append(ug) for ug in self.ugs if ug.disponivel and not ug.etapa_atual == UG_PARANDO]
        logger.debug("")

        if self.modo_de_escolha_das_ugs == MODO_ESCOLHA_MANUAL:
            logger.debug("[USN] UGs disponíveis em ordem (prioridade):")
            return sorted(ls, key=lambda y: (-1 * y.leitura_potencia, -1 * y.setpoint, y.prioridade))
        else:
            logger.debug("[USN] UGs disponíveis em ordem (horas-máquina):")
            return sorted(ls, key=lambda y: (y.leitura_horimetro, -1 * y.leitura_potencia, -1 * y.setpoint))

    def controle_potencia(self) -> None:
        logger.debug("-------------------------------------------------------------------------")
        logger.debug(f"[USN] NÍVEL -> Leitura: {self.tda.nv_montante_recente:0.3f}; Alvo: {self.cfg['nv_alvo']:0.3f}")

        self.controle_p = self.cfg["kp"] * self.tda.erro_nv
        self.controle_i = max(min((self.cfg["ki"] * self.tda.erro_nv) + self.controle_i, 0.8), 0)
        self.controle_d = self.cfg["kd"] * (self.tda.erro_nv - self.tda.erro_nv_anterior)
        saida_pid = (self.controle_p + self.controle_i + min(max(-0.3, self.controle_d), 0.3))
        logger.debug(f"[USN] PID -> {saida_pid:0.3f} P:{self.controle_p:0.3f} + I:{self.controle_i:0.3f} + D:{self.controle_d:0.3f}; ERRO={self.tda.erro_nv}")

        self.controle_ie = max(min(saida_pid + self.controle_ie * self.cfg["kie"], 1), 0)
        logger.debug(f"[USN] IE: {self.controle_ie:0.3f}")
        logger.debug("")

        self.controle_i = 1 - self.controle_p if self.tda.nv_montante_recente >= (self.cfg["nv_maximo"] + 0.03) else 0
        self.controle_ie = 1 if self.tda.nv_montante_recente <= (self.cfg["nv_minimo"] + 0.03) else min(self.controle_ie, 0.3)

        pot_alvo = max(min(round(self.cfg["pot_maxima_usina"] * self.controle_ie, 5), self.cfg["pot_maxima_usina"],), self.cfg["pot_minima"],)
        logger.debug(f"[USN] Potência alvo: {pot_alvo:0.3f}")

        self.ajuste_potencia(pot_alvo)
