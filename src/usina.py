import pytz
import logging
import traceback

import dicionarios.dict as d

from time import sleep, time
from threading import Thread
from datetime import  datetime, timedelta

from src.funcoes.leitura import *
from ocorrencias import *
from dicionarios.const import *
from dicionarios.reg import MOA

from clients import ClientesUsina
from banco_dados import BancoDados
from unidade_geracao import UnidadeDeGeracao

logger = logging.getLogger("__main__")

class Usina:
    def __init__(self, cfg: dict=None):

        # VERIFICAÇÃO DE ARGUMENTOS
        if None in (cfg):
            raise ValueError("[USN] Não foi possível carregar os arquivos de configuração (\"cfg.json\").")
        else:
            self.cfg = cfg

        # INCIALIZAÇÃO DE OBJETOS DA USINA
        self.db = BancoDados("MOA")
        self.clp = ClientesUsina.clp

        self.ug1 = UnidadeDeGeracao(1)
        self.ug2 = UnidadeDeGeracao(2)
        self.ug3 = UnidadeDeGeracao(3)
        self.ugs: "list[UnidadeDeGeracao]" = [self.ug1, self.ug2, self.ug3]

        for ug in self.ugs:
            ug.lista_ugs = self.ugs
            ug.iniciar_ultimo_estado()

        self.oco_ug = OcorrenciasUg()
        self.oco_usn = OcorrenciasUsn()
        CondicionadorBase.ugs = self.ugs

        # ATRIBUIÇÃO DE VARIÁVEIS PROTEGIDAS
        self._potencia_ativa_kW: LeituraModbus = LeituraModbus(
            SA["SA_RA_PM_810_Potencia_Ativa"],
            self.clp["SA"],
            1,
            op=4,
        )
        self._nv_montante: LeituraModbus = LeituraModbus(
            TDA["TDA_NivelMaisCasasAntes"],
            self.clp["TDA"],
            1 / 10000,
            819.2,
            op=4,
        )
        self._tensao_rs: LeituraModbus = LeituraModbus(
            SA["SA_RA_PM_810_Tensao_AB"],
            self.clp["SA"],
            1000,
            op=4,
        )
        self._tensao_st: LeituraModbus = LeituraModbus(
            SA["SA_RA_PM_810_Tensao_BC"],
            self.clp["SA"],
            1000,
            op=4,
        )
        self._tensao_tr: LeituraModbus = LeituraModbus(
            SA["SA_RA_PM_810_Tensao_CA"],
            self.clp["SA"],
            1000,
            op=4,
        )

        self._tentativas_normalizar: int = 0
        self._potencia_alvo_anterior: int = -1

        self._modo_autonomo: bool = False

        # ATRIBUIÇÃO DE VARIÁVEIS PÚBLICAS
        self.estado_moa: int = 0
        self.status_tensao: int = 0

        self.controle_p: float = 0
        self.controle_i: float = 0
        self.controle_d: float = 0

        self.pot_disp: int = 0
        self.ug_operando: int = 0
        self.modo_de_escolha_das_ugs: int = 0

        self.erro_nv: float = 0
        self.erro_nv_anterior: float = 0
        self.nv_montante_recente: float = 0

        self.timer_tensao: bool = False

        self.borda_emerg: bool = False
        self.db_emergencia: bool = False
        self.clp_emergencia: bool = False

        self.tentar_normalizar: bool = True
        self.normalizar_forcado: bool = False

        self.aguardando_reservatorio: bool = False

        self.ts_last_ping_tda: datetime = self.get_time()
        self.ultima_tentativa_norm: datetime = self.get_time()

        # EXECUÇÃO FINAL DA INICIALIZAÇÃO
        self.ler_valores()
        self.controlar_inicializacao()
        self.normalizar_usina()
        self.escrever_valores()


    ### PROPRIEDADES DA OPERAÇÃO

    @property
    def potencia_ativa_kW(self) -> int:
        return self._potencia_ativa_kW.valor

    @property
    def nv_montante(self) -> float:
        return self._nv_montante.valor

    @property
    def tensao_rs(self) -> float:
        return self._tensao_rs.valor

    @property
    def tensao_st(self) -> float:
        return self._tensao_st.valor

    @property
    def tensao_tr(self) -> float:
        return self._tensao_tr.valor

    @property
    def modo_autonomo(self) -> bool:
        return self._modo_autonomo

    @modo_autonomo.setter
    def modo_autonomo(self, var: bool) -> None:
        self._modo_autonomo = var
        self.db.update_modo_moa(self._modo_autonomo)

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
    def pot_alvo_anterior(self, var):
        self._potencia_alvo_anterior = var

    def get_time(self) -> datetime:
        return datetime.now(pytz.timezone("Brazil/East")).replace(tzinfo=None)


    ### MÉTODOS DE CONTROLE DE RESET E NORMALIZAÇÃO

    def acionar_emergencia(self) -> None:
        logger.warning("[CON] Acionando emergência.")
        self.clp_emergencia = True

        try:
            self.clp["UG1"].write_single_coil(UG["UG1_CD_EmergenciaViaSuper"], [1])
            self.clp["UG2"].write_single_coil(UG["UG2_CD_EmergenciaViaSuper"], [1])
            sleep(5)
            self.clp["UG1"].write_single_coil(UG["UG1_CD_EmergenciaViaSuper"], [0])
            self.clp["UG2"].write_single_coil(UG["UG2_CD_EmergenciaViaSuper"], [0])

        except Exception:
            logger.error(f"[CON] Houve um erro ao acionar a emergência.")
            logger.debug(f"[CON] Traceback: {traceback.format_exc()}")

    def resetar_emergencia(self) -> None:
        try:
            logger.debug("[CON] Reset geral.")
            self.clp["SA"].write_single_coil(SA["SA_CD_ResetGeral"], [1])
            self.clp["UG1"].write_single_coil(UG["UG1_CD_ResetGeral"], [1])
            self.clp["UG2"].write_single_coil(UG["UG2_CD_ResetGeral"], [1])
            self.clp["TDA"].write_single_coil(TDA["TDA_CD_ResetGeral"], [1])

        except Exception:
            logger.error(f"[CON] Houve um erro ao realizar o reset geral.")
            logger.debug(f"[CON] Traceback: {traceback.format_exc()}")

    def reconhecer_emergencia(self) -> None:
        try:
            logger.debug("[CON] Cala sirene.")
            self.clp["SA"].write_single_coil(SA["SA_CD_Cala_Sirene"], [1])
            self.clp["UG1"].write_single_coil(UG["UG1_CD_Cala_Sirene"], [1])
            self.clp["UG2"].write_single_coil(UG["UG2_CD_Cala_Sirene"], [1])

        except Exception:
            logger.error(f"[CON] Houve um erro ao reconhecer os alarmes.")
            logger.debug(f"[CON] Traceback: {traceback.format_exc()}")

    def resetar_tda(self) -> None:
        try:
            self.clp["TDA"].write_single_coil(TDA["TDA_CD_ResetGeral"], [1])
            self.clp["TDA"].write_single_coil(TDA["TDA_CD_Hab_Nivel"], [0])
            self.clp["TDA"].write_single_coil(TDA["TDA_CD_Desab_Nivel"], [1])
            self.clp["TDA"].write_single_coil(TDA["TDA_CD_Hab_Religamento52L"], [0])
            self.clp["TDA"].write_single_coil(TDA["TDA_CD_Desab_Religamento52L"], [1])

        except Exception:
            logger.error(f"[CON] Houve um erro ao modificar os controles locais.")
            logger.debug(f"[CON] Traceback: {traceback.format_exc()}")

    def normalizar_usina(self) -> bool:
        logger.debug("[USN] Normalizando...")
        logger.debug(f"[USN] Última tentativa: {self.ultima_tentativa_norm}. Tensão na linha: RS->{self.tensao_rs:2.1f}kV / ST->{self.tensao_st:2.1f}kV / TR->{self.tensao_tr:2.1f}kV")

        if not self.verificar_tensao():
            return False

        elif (self.tentar_normalizar and (self.get_time() - self.ultima_tentativa_norm).seconds >= 60 * self.tentativas_normalizar) or self.normalizar_forcado:
            self.ultima_tentativa_norm = self.get_time()
            self.tentativas_normalizar += 1
            self.db_emergencia = False
            self.clp_emergencia = False
            self.resetar_tda()
            self.resetar_emergencia()
            self.reconhecer_emergencia()
            self.db.update_remove_emergencia()
            return True

        else:
            logger.debug("[USN] A normalização foi executada menos de 1 minuto atrás.")


    ### MÉTODOS DE CONTROLE DE OPERAÇÃO:

    def fechaDj52L(self) -> bool:
        try:
            if self.verificar_falhas_52l():
                return False
            else:
                response = self.clp["SA"].write_single_register(SA["SA_CD_Liga_DJ1"], 1)
                return response

        except Exception:
            logger.error(f"[CON] Houver um erro ao fechar o Dj52L.")
            logger.debug(f"[CON] Traceback: {traceback.format_exc()}")
            return False

    def verificar_falhas_52l(self) -> bool:
        dict_flags: "dict[str, int]" = {
            SA["SA_RD_DJ1_FalhaInt"]: 1,
            SA["SA_ED_DisjDJ1_Local"]: 1,
            SA["SA_ED_DisjDJ1_AlPressBaixa"]: 1,
            SA["SA_ED_DisjDJ1_BloqPressBaixa"]: 1,
            SA["SA_ED_DisjDJ1_SuperBobAbert2"]: 0,
            SA["SA_ED_DisjDJ1_Sup125VccBoFeAb1"]: 0,
            SA["SA_ED_DisjDJ1_Super125VccCiMot"]: 0,
            SA["SA_ED_DisjDJ1_Super125VccCiCom"]: 0,
            SA["SA_ED_DisjDJ1_Sup125VccBoFeAb2"]: 0,
        }

        try:
            flags = 0
            for nome, valor in zip(dict_flags[0], dict_flags.values()):
                if self.clp["SA"].read_discrete_inputs(nome)[0] == valor:
                    logger.debug(f"[CON] Flag -> {nome.keys()}")
                    flags += 1

            logger.info(f"[CON] Foram detectadas Flags de bloqueio ao abrir o Dj52L. Número de bloqueios ativos: \"{flags}\"") if flags else ...
            return True if flags >= 1 else False

        except Exception:
            logger.error(f"[CON] Houve um erro ao ler as flags do Dj52L.")
            logger.debug(f"[CON] Traceback: {traceback.format_exc()}")
            return None

    def verificar_tensao(self) -> bool:
        try:
            if (TENSAO_LINHA_BAIXA < self.tensao_rs < TENSAO_LINHA_ALTA) \
                and (TENSAO_LINHA_BAIXA < self.tensao_st < TENSAO_LINHA_ALTA) \
                and (TENSAO_LINHA_BAIXA < self.tensao_tr < TENSAO_LINHA_ALTA):
                return True
            else:
                logger.warning("[USN] Tensão da linha fora do limite.")
                return False

        except Exception:
            logger.error(f"[USN] Houve um erro ao realizar a verificação da tensão na linha.")
            logger.debug(f"[USN] Traceback: {traceback.format_exc()}")

    def aguardar_tensao(self) -> bool:
        if self.status_tensao == 0:
            self.status_tensao = 1
            logger.debug("[USN] Iniciando o timer para a normalização da tensão na linha.")
            Thread(target=lambda: self.acionar_temporizador_tensao(600)).start()

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

    def acionar_temporizador_tensao(self, delay) -> None:
        while time() <= time() + delay:
            if self.verificar_tensao():
                self.status_tensao = 2
                return
            sleep(time() - (time() - 15))
        self.status_tensao = 3

    def ajustar_ie_padrao(self) -> int:
        return sum(ug.leitura_potencia for ug in self.ugs) / self.cfg["pot_maxima_alvo"]

    def ajustar_potencia(self, pot_alvo) -> float:
        if self.pot_alvo_anterior == -1:
            self.pot_alvo_anterior = pot_alvo

        if pot_alvo < 0.1:
            for ug in self.ugs: ug.setpoint = 0
            return 0

        logger.debug(f"[USN] Potência no medidor = {self.potencia_ativa_kW:0.3f}")
        pot_aux = self.cfg["pot_maxima_alvo"] - (self.cfg["pot_maxima_usina"] - self.cfg["pot_maxima_alvo"])
        pot_medidor = max(pot_aux, min(self.potencia_ativa_kW, self.cfg["pot_maxima_usina"]))

        try:
            if pot_medidor > self.cfg["pot_maxima_alvo"]:
                pot_alvo = self.pot_alvo_anterior * (1 - ((pot_medidor - self.cfg["pot_maxima_alvo"]) / self.cfg["pot_maxima_alvo"]))
        except TypeError as te:
            logger.error(f"[USN] A comunicação com os MFs falharam. Exception: \"{repr(te)}\"")
            logger.debug(f"[USN] Traceback: {traceback.format_exc()}")

        self.pot_alvo_anterior = pot_alvo

        logger.debug(f"[USN] Pot alvo pós ajuste: {pot_alvo:0.3f}")
        self.distribuir_potencia(pot_alvo)
        return pot_alvo

    def distribuir_potencia(self, pot_alvo) -> None:
        ugs: "list[UnidadeDeGeracao]" = self.controlar_unidades_disponiveis()
        logger.debug(f"[USN] UG{[ug.id for ug in self.ugs]}")

        self.pot_disp = [sum(ug.setpoint_maximo) for ug in self.ugs if not ug.manual]
        ajuste_manual = min(max(0, [sum(ug.leitura_potencia) for ug in self.ugs if ug.manual]))

        if ugs is None or not len(ugs):
            return

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
                ugs[0].setpoint = sp * ugs[0].setpoint_maximo
                ugs[1].setpoint = sp * ugs[1].setpoint_maximo

            elif self.__split1:
                logger.debug("[USN] Split 1")
                sp = sp * 2 / 1
                ugs[0].setpoint = sp * ugs[0].setpoint_maximo
                ugs[1].setpoint = 0

        elif len(ugs) == 1:
            if self.__split1 or self.__split2:
                logger.debug("[USN] Split 1B")
                sp = sp * 2 / 1
                ugs[0].setpoint = sp * ugs[0].setpoint_maximo

        else:
            for ug in ugs:
                ug.setpoint = 0

    def controlar_inicializacao(self) -> None:
        self.ug_operando += [1 for ug in self.ugs if ug.etapa_atual == UG_SINCRONIZADA]

        self.__split1 = True if self.ug_operando == 1 else False
        self.__split2 = True if self.ug_operando == 2 else False

        self.controle_ie = self.ajustar_ie_padrao() if self.cfg["saida_ie_inicial"] == "auto" else self.cfg["saida_ie_inicial"]

    def controlar_potencia(self) -> None:
        logger.debug("-------------------------------------------------------------------------")
        logger.debug(f"[USN] NÍVEL -> Leitura: {self.nv_montante_recente:0.3f}; Alvo: {self.cfg['nv_alvo']:0.3f}")

        self.controle_p = self.cfg["kp"] * self.erro_nv
        self.controle_i = max(min((self.cfg["ki"] * self.erro_nv) + self.controle_i, 0.8), 0)
        self.controle_d = self.cfg["kd"] * (self.erro_nv - self.erro_nv_anterior)
        saida_pid = (self.controle_p + self.controle_i + min(max(-0.3, self.controle_d), 0.3))
        logger.debug(f"[USN] PID -> {saida_pid:0.3f} P:{self.controle_p:0.3f} + I:{self.controle_i:0.3f} + D:{self.controle_d:0.3f}; ERRO={self.erro_nv}")

        self.controle_ie = max(min(saida_pid + self.controle_ie * self.cfg["kie"], 1), 0)
        logger.debug(f"[USN] IE: {self.controle_ie:0.3f}")
        logger.debug("")

        self.controle_i = 1 - self.controle_p if self.nv_montante_recente >= (self.cfg["nv_maximo"] + 0.03) else 0
        self.controle_ie = 1 if self.nv_montante_recente <= (self.cfg["nv_minimo"] + 0.03) else min(self.controle_ie, 0.3)

        pot_alvo = max(min(round(self.cfg["pot_maxima_usina"] * self.controle_ie, 5), self.cfg["pot_maxima_usina"],), self.cfg["pot_minima"],)
        logger.debug(f"[USN] Potência alvo: {pot_alvo:0.3f}")

        pot_alvo = self.ajustar_potencia(pot_alvo)
        self.escrever_valores()

    def controlar_unidades_disponiveis(self) -> list:
        ls = [ug for ug in self.ugs if ug.disponivel and not ug.etapa_atual == UG_PARANDO]

        if self.modo_de_escolha_das_ugs == MODO_ESCOLHA_MANUAL:
            ls = sorted(ls, key=lambda y: (-1 * y.leitura_potencia, -1 * y.setpoint, y.prioridade))
            logger.debug("")
            logger.debug("[USN] UGs disponíveis em ordem (prioridade):")
        else:
            ls = sorted(ls, key=lambda y: (y.leitura_horimetro, -1 * y.leitura_potencia, -1 * y.setpoint))
            logger.debug("")
            logger.debug("[USN] UGs disponíveis em ordem (horas-máquina):")

        return ls

    def controlar_reservatorio(self) -> int:
        if self.nv_montante >= self.cfg["nv_maximo"]:
            logger.info("[USN] Nível montante acima do máximo.")

            if self.nv_montante_recente >= NIVEL_MAXIMORUM:
                logger.critical(f"[USN] Nivel montante ({self.nv_montante_recente:3.2f}) atingiu o maximorum!")
                return NV_FLAG_EMERGENCIA
            else:
                self.controle_i = 0.5
                self.controle_ie = 0.5
                self.distribuir_potencia(self.cfg["pot_maxima_usina"])

        elif self.nv_montante <= self.cfg["nv_minimo"] and not self.aguardando_reservatorio:
            logger.info("[USN] Nível montante abaixo do mínimo.")
            self.aguardando_reservatorio = True
            self.distribuir_potencia(0)

            if self.nv_montante_recente <= NIVEL_FUNDO_RESERVATORIO:
                if not ClientesUsina.ping(d.ips["TDA_slave_ip"]):
                    logger.warning("[USN] A comunicação com a TDA falhou. Entrando em modo manual.")
                    self.modo_autonomo = False
                    return NV_FLAG_EMERGENCIA
                else:
                    logger.critical(f"[USN] Nivel montante ({self.nv_montante_recente:3.2f}) atingiu o fundo do reservatorio!")
                    return NV_FLAG_EMERGENCIA

        elif self.aguardando_reservatorio:
            if self.nv_montante >= self.cfg["nv_alvo"]:
                logger.debug("[USN] Nível montante dentro do limite de operação.")
                self.aguardando_reservatorio = False

        else:
            self.controlar_potencia()

        for ug in self.ugs: ug.step()

        return NV_FLAG_NORMAL


    ### MÉTODOS DE CONTROLE DE DADOS:

    def ler_valores(self) -> None:
        ClientesUsina.ping_clients()
        self.atualizar_valores_montante()

        parametros = self.db.get_parametros_usina()
        self.atualizar_valores_cfg(parametros)
        self.atualizar_valores_banco(parametros)
        for ug in self.ugs: self.oco_ug.atualizar_limites_condicionadores(parametros, ug)

        self.heartbeat()

    def atualizar_valores_montante(self) -> None:
        self.resetar_tda()
        self.nv_montante_recente = self.nv_montante
        self.erro_nv_anterior = self.erro_nv
        self.erro_nv = self.nv_montante_recente - self.cfg["nv_alvo"]

    def atualizar_valores_banco(self, parametros) -> None:
        try:
            self.db_emergencia = True if int(parametros["emergencia_acionada"]) == 1 else False
            logger.debug("[USN] Emergência acionada.")

            self.modo_autonomo = True if int(parametros["modo_autonomo"]) == 1 else False
            logger.debug(f"[USN] Modo autonomo que o banco respondeu: {int(parametros['modo_autonomo'])}")

            if not self.modo_de_escolha_das_ugs == int(parametros["modo_de_escolha_das_ugs"]):
                self.modo_de_escolha_das_ugs = int(parametros["modo_de_escolha_das_ugs"])
                logger.info(f"[USN] O modo de prioridade das ugs foi alterado (#{self.modo_de_escolha_das_ugs}).")

        except Exception:
            logger.error(f"[USN] Houve um erro ao ler e atualizar os parâmetros do Banco de Dados.")
            logger.debug(f"[USN] Traceback: {traceback.format_exc()}")

    def atualizar_valores_cfg(self, parametros) -> None:
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

        except Exception:
            logger.error(f"[USN] Houve um erro ao atualizar o arquivo de configuração \"cfg.json\".")
            logger.debug(f"[USN] Traceback: {traceback.format_exc()}")

    def escrever_valores(self) -> None:
        try:
            self.db.update_valores_usina(
                self.get_time().strftime("%Y-%m-%d %H:%M:%S"),
                1 if self.aguardando_reservatorio else 0,
                True,
                self.nv_montante,
                1 if self.ug1.disponivel else 0,
                self.ug1.leitura_potencia,
                self.ug1.setpoint,
                self.ug1.etapa_atual,
                self.ug1.leitura_horimetro,
                1 if self.ug2.disponivel else 0,
                self.ug2.leitura_potencia,
                self.ug2.setpoint,
                self.ug2.etapa_atual,
                self.ug2.leitura_horimetro,
            )

        except Exception:
            logger.error(f"[USN] Houve um erro ao inserir os valores no banco.")
            logger.debug(f"[USN] Traceback: {traceback.format_exc()}")

        try:
            self.db.update_debug(
                time(),
                1 if self.modo_autonomo else 0,
                self.nv_montante_recente,
                self.erro_nv,
                self.ug1.setpoint,
                self.ug1.leitura_potencia,
                self.ug1.codigo_state,
                self.ug2.setpoint,
                self.ug2.leitura_potencia,
                self.ug2.codigo_state,
                self.cfg["kp"],
                self.cfg["ki"],
                self.cfg["kd"],
                self.cfg["kie"],
                self.controle_p,
                self.controle_i,
                self.controle_d,
                self.controle_ie,
            )

        except Exception:
            logger.error(f"[USN] Houve um erro ao inserir dados DEBUG do controle de potência normal no banco.")
            logger.debug(f"[USN] Traceback: {traceback.format_exc()}")

    def heartbeat(self) -> None:
        try:
            self.clp["MOA"].write_single_coil(REG_MOA["PAINEL_LIDO"], [1])
            self.clp["MOA"].write_single_coil(REG_MOA["MOA_OUT_MODE"], [1 if self.modo_autonomo else 0])
            self.clp["MOA"].write_single_register(REG_MOA["MOA_OUT_STATUS"], self.estado_moa)

            for ug in self.ugs: ug.atualizar_modbus_moa()

            if self.modo_autonomo:
                self.clp["MOA"].write_single_coil(REG_MOA["MOA_OUT_EMERG"], [1 if self.clp_emergencia else 0])
                self.clp["MOA"].write_single_register(REG_MOA["MOA_OUT_TARGET_LEVEL"], int((self.cfg["nv_alvo"] - 819.2) * (1/1000)))
                self.clp["MOA"].write_single_register(REG_MOA["MOA_OUT_SETPOINT"], int(sum(ug.setpoint for ug in self.ugs)))

                if self.clp["MOA"].read_coils(REG_MOA["MOA_IN_EMERG"]) == 1 and not self.borda_emerg:
                    self.borda_emerg = True
                    for ug in self.ugs: self.oco_ug.verificar_condicionadores(ug)

                elif self.clp["MOA"].read_coils(REG_MOA["MOA_IN_EMERG"]) == 0 and self.borda_emerg:
                    self.borda_emerg = False

                if self.clp["MOA"].read_coils(REG_MOA["MOA_IN_EMERG_UG1"]) == 1:
                    self.oco_ug.verificar_condicionadores(self.ug1)

                if self.clp["MOA"].read_coils(REG_MOA["MOA_IN_EMERG_UG2"]) == 1:
                    self.oco_ug.verificar_condicionadores(self.ug2)

                if self.clp["MOA"].read_coils(REG_MOA["MOA_IN_HABILITA_AUTO"]) == 1:
                    self.clp["MOA"].write_single_coil(REG_MOA["MOA_IN_HABILITA_AUTO"], [1])
                    self.clp["MOA"].write_single_coil(REG_MOA["MOA_IN_DESABILITA_AUTO"], [0])
                    self.modo_autonomo = True

                if self.clp["MOA"].read_coils(REG_MOA["MOA_IN_DESABILITA_AUTO"]) == 1:
                    self.clp["MOA"].write_single_coil(REG_MOA["MOA_IN_HABILITA_AUTO"], [0])
                    self.clp["MOA"].write_single_coil(REG_MOA["MOA_IN_DESABILITA_AUTO"], [1])
                    self.modo_autonomo = False

                if self.clp["MOA"].read_coils(REG_MOA["MOA_OUT_BLOCK_UG1"]) == 1:
                    self.clp["MOA"].write_single_coil(REG_MOA["MOA_OUT_BLOCK_UG1"], [1])

                elif self.clp["MOA"].read_coils(REG_MOA["MOA_OUT_BLOCK_UG1"]) == 0:
                    self.clp["MOA"].write_single_coil(REG_MOA["MOA_OUT_BLOCK_UG1"], [0])

                if self.clp["MOA"].read_coils(REG_MOA["MOA_OUT_BLOCK_UG2"]) == 1:
                    self.clp["MOA"].write_single_coil(REG_MOA["MOA_OUT_BLOCK_UG2"], [1])

                elif self.clp["MOA"].read_coils(REG_MOA["MOA_OUT_BLOCK_UG2"]) == 0:
                    self.clp["MOA"].write_single_coil(REG_MOA["MOA_OUT_BLOCK_UG2"], [0])

            elif not self.modo_autonomo:
                if self.clp["MOA"].read_coils(REG_MOA["MOA_IN_HABILITA_AUTO"]) == 1:
                    self.clp["MOA"].write_single_coil(REG_MOA["MOA_IN_HABILITA_AUTO"], [1])
                    self.clp["MOA"].write_single_coil(REG_MOA["MOA_IN_DESABILITA_AUTO"], [0])
                    self.modo_autonomo = True

                self.clp["MOA"].write_single_coil(REG_MOA["MOA_OUT_EMERG"], [0])
                self.clp["MOA"].write_single_coil(REG_MOA["MOA_OUT_BLOCK_UG1"], [0])
                self.clp["MOA"].write_single_coil(REG_MOA["MOA_OUT_BLOCK_UG2"], [0])
                self.clp["MOA"].write_single_register(REG_MOA["MOA_OUT_SETPOINT"], int(0))
                self.clp["MOA"].write_single_register(REG_MOA["MOA_OUT_TARGET_LEVEL"], int(0))

        except Exception:
            logger.error(f"[USN] Houve um erro ao tentar escrever valores modbus no CLP MOA.")
            logger.debug(f"[USN] Traceback: {traceback.format_exc()}")