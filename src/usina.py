import sys
import pytz
import logging
import threading
import traceback
import subprocess

import src.mensageiro.dict as vd

from time import sleep, time
from datetime import  datetime, timedelta
from pyModbusTCP.client import ModbusClient

from src.ocorrencias import *
from src.funcoes.leitura import  *
from src.dicionarios.reg import *
from src.dicionarios.const import *
from src.maquinas_estado.ug import *

from src.mensageiro.voip import Voip
from src.banco_dados import BancoDados
from src.conector import ClientesUsina
from src.agendamentos import Agendamentos
from src.unidade_geracao import UnidadeGeracao
from src.Condicionadores import CondicionadorBase

logger = logging.getLogger("__main__")

class Usina:
    def __init__(self, cfg: dict=None):

        # VERIFICAÇÃO DE ARGUMENTOS

        if None in (cfg):
            raise ValueError("[USN] Não foi possível carregar os arquivos de configuração (\"cfg.json\").")
        else:
            self.cfg = cfg


        # INCIALIZAÇÃO DE OBJETOS DA USINA

        self.db = BancoDados("MOA-SEB")
        self.clp = ClientesUsina.clp
        self.oco = OcorrenciasUsn(self.clp)
        self.agn = Agendamentos(self.cfg, self.db)

        self.ug1 = UnidadeGeracao(1, self.cfg, self.db)
        self.ug2 = UnidadeGeracao(2, self.cfg, self.db)
        self.ug3 = UnidadeGeracao(3, self.cfg, self.db)
        self.ugs: "list[UnidadeGeracao]" = [self.ug1, self.ug2, self.ug3]
        CondicionadorBase.ugs = self.ugs

        for ug in self.ugs:
            ug.lista_ugs = self.ugs
            ug.iniciar_ultimo_estado()

        CondicionadorBase.ugs = self.ugs

        self.agn = Agendamentos(self.cfg, self.db, self)


        # ATRIBUIÇÃO DE VARIÁVEIS PRIVADAS

        self.__potencia_ativa_kW: LeituraModbus = LeituraModbus(
            "SA_EA_Medidor_potencia_kw_mp",
            self.clp["SA"],
            REG["SA_EA_PM_810_Potencia_Ativa"],
            1,
            op=4,
        )
        self.__tensao_rs: LeituraModbus = LeituraModbus(
            "SA_EA_PM_810_Tensao_AB",
            self.clp["SA"],
            REG["SA_EA_PM_810_Tensao_ab"],
            100,
            op=4,
        )
        self.__tensao_st: LeituraModbus = LeituraModbus(
            "SA_EA_PM_810_Tensao_BC",
            self.clp["SA"],
            REG["SA_EA_PM_810_Tensao_bc"],
            100,
            op=4,
        )
        self.__tensao_tr: LeituraModbus = LeituraModbus(
            "SA_EA_PM_810_Tensao_CA",
            self.clp["SA"],
            REG["SA_EA_PM_810_Tensao_ca"],
            100,
            op=4,
        )


        # ATRIBUIÇÃO DE VARIÁVEIS PROTEGIDAS

        self._nv_montante: LeituraModbus = LeituraModbus(
            "TDA_EntradasAnalogicas_MRR_NivelMaisCasasAntes",
            self.clp["TDA"],
            REG["TDA_EA_NivelAntesGrade"],
            1 / 10000,
            400,
            op=4,
        )

        self._pid_inicial: "int" = -1
        self._pot_alvo_anterior: "int" = -1
        self._tentativas_normalizar: "bool" = 0

        self._modo_autonomo: bool = False


        # ATRIBUIÇÃO DE VARIÁVEIS PÚBLICAS

        self.estado_moa: "int" = 0
        self.status_tensao: "int" = 0

        self.pot_disp: "int" = 0
        self.ug_operando: "int" = 0
        self.modo_de_escolha_das_ugs: "int" = -1

        self.erro_nv: "int" = 0
        self.erro_nv_anterior: "int" = 0
        self.nv_montante_recente: "int" = 0

        self.controle_p: "float" = 0
        self.controle_i: "float" = 0
        self.controle_d: "float" = 0
        self.pid_inicial: "float" = -1

        self.tentar_normalizar: "bool" = True
        self.normalizar_forcado: "bool" = False

        self.borda_emerg: "bool" = False
        self.db_emergencia: "bool" = False
        self.clp_emergencia: "bool" = False

        self.TDA_Offline: "bool" = False
        self.aguardando_reservatorio: "bool" = False

        self.ultima_tentativa_norm: "datetime" = self.get_time()

        logger.debug("")
        self.ler_valores()
        self.controlar_inicializacao()
        self.normalizar_usina()
        self.escrever_valores()


    # Property -> VARIÁVEIS PRIVADAS

    @property
    def potencia_ativa(self) -> int:
        return self.__potencia_ativa_kW.valor

    @property
    def nv_montante(self) -> float:
        return self._nv_montante.valor


    # Property/Setter -> VARIÁVEIS PROTEGIDAS

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
    def _pot_alvo_anterior(self) -> float:
        return self._potencia_alvo_anterior

    @_pot_alvo_anterior.setter
    def _pot_alvo_anterior(self, var):
        self._potencia_alvo_anterior = var


    # FUNÇÕES

    @staticmethod
    def get_time() -> datetime:
        return datetime.now(pytz.timezone("Brazil/East")).replace(tzinfo=None)


    ### MÉTODOS DE CONTROLE DE RESET E NORMALIZAÇÃO

    def acionar_emergencia(self) -> None:
        logger.warning("[USN] Acionando Emergência.")
        self.clp_emergencia = True

        try:
            self.clp["UG1"].write_single_coil(REG["UG1_CD_EmergenciaViaSuper"], [1])
            self.clp["UG2"].write_single_coil(REG["UG2_CD_EmergenciaViaSuper"], [1])
            self.clp["UG3"].write_single_coil(REG["UG3_CD_EmergenciaViaSuper"], [1])
            sleep(5)
            self.clp["UG1"].write_single_coil(REG["UG1_CD_EmergenciaViaSuper"], [0])
            self.clp["UG2"].write_single_coil(REG["UG2_CD_EmergenciaViaSuper"], [0])
            self.clp["UG3"].write_single_coil(REG["UG3_CD_EmergenciaViaSuper"], [0])

        except Exception:
            logger.error(f"[USN] Houve um erro ao acionar a Emergência.")
            logger.debug(traceback.format_exc())

    def resetar_emergencia(self) -> None:
        try:
            logger.debug("[USN] Reset geral")

            self.clp["SA"].write_single_coil(REG["SA_CD_ResetGeral"], [1])
            self.clp["UG1"].write_single_coil(REG["UG1_CD_ResetGeral"], [1])
            self.clp["UG2"].write_single_coil(REG["UG2_CD_ResetGeral"], [1])
            self.clp["UG3"].write_single_coil(REG["UG3_CD_ResetGeral"], [1])
            self.clp["TDA"].write_single_coil(REG["TDA_CD_ResetGeral"], [1]) if not self.TDA_Offline else logger.debug("[USN] CLP TDA Offline, não há como realizar o reset geral")

            self.clp["SA"].write_single_coil(REG["SA_CD_Cala_Sirene"], [1])
            self.clp["UG1"].write_single_coil(REG["UG1_CD_Cala_Sirene"], [1])
            self.clp["UG2"].write_single_coil(REG["UG2_CD_Cala_Sirene"], [1])
            self.clp["UG3"].write_single_coil(REG["UG3_CD_Cala_Sirene"], [1])
            self.fechar_dj_linha()

        except Exception:
            logger.error(f"[USN] Houve um erro ao realizar o Reset Geral.")
            logger.debug(traceback.format_exc())

    def resetar_tda(self) -> None:
        if not d.glb["TDA_Offline"]:
            self.clp["TDA"].write_single_coil(REG["TDA_CD_ResetGeral"], [1])
            # self.clp["TDA"].write_single_coil(REG["TDA_CD_Hab_Nivel"], [0])
            self.clp["TDA"].write_single_coil(REG["TDA_CD_Desab_Nivel"], [1])
            # self.clp["TDA"].write_single_coil(REG["TDA_CD_Hab_Religamento52L"], [0])
            self.clp["TDA"].write_single_coil(REG["TDA_CD_Desab_Religamento52L"], [1])
        else:
            logger.debug("[USN] Não é possível resetar a TDA pois o CLP da TDA se encontra offline")

    def normalizar_usina(self) -> bool:
        logger.debug("[USN] Normalizando...")
        logger.debug(f"[USN] Última tentativa de normalização:   {self.ultima_tentativa_norm.strftime('%d-%m-%Y %H:%M:%S')}")
        logger.debug(f"[USN] Tensão na linha:                    RS -> \"{self.__tensao_rs.valor:2.1f} kV\" | ST -> \"{self.__tensao_st.valor:2.1f} kV\" | TR -> \"{self.__tensao_tr.valor:2.1f} kV\"")

        if not self.verificar_tensao():
            return False

        elif (self.tentar_normalizar and (self.get_time() - self.ultima_tentativa_norm).seconds >= 60 * self.tentativas_normalizar) or self.normalizar_forcado:
            self.ultima_tentativa_norm = self.get_time()
            self.tentativas_normalizar += 1
            self.db_emergencia = False
            self.clp_emergencia = False
            d.glb["TDA_Offline"] = True if d.glb["TDA_Offline"] else False
            self.resetar_emergencia()
            self.db.update_remove_emergencia()
            return True

        else:
            logger.debug("[USN] A normalização foi executada menos de 1 minuto atrás")

    def fechar_dj_linha(self) -> bool:
        try:
            if self.verificar_falha_dj_linha():
                return False
            else:
                response = self.clp["SA"].write_single_coil(REG["SA_CD_Liga_DJ1"], [1])
                return response

        except Exception:
            logger.error(f"[USN] Houver um erro ao fechar o Disjuntor de Linha.")
            logger.debug(traceback.format_exc())

    def verificar_falha_dj_linha(self):
        flag = 0

        if self.clp["SA"].read_discrete_inputs(REG["SA_ED_DisjDJ1_SuperBobAbert1"])[0] == 0:
            logger.debug("[USN] DisjDJ1_SuperBobAbert1")
            flag += 1

        if self.clp["SA"].read_discrete_inputs(REG["SA_ED_DisjDJ1_SuperBobAbert2"])[0] == 0:
            logger.debug("[USN] DisjDJ1_SuperBobAbert2")
            flag += 1

        if self.clp["SA"].read_discrete_inputs(REG["SA_ED_DisjDJ1_Super125VccCiMot"])[0] == 0:
            logger.debug("[USN] DisjDJ1_Super125VccCiMot")
            flag += 1

        if self.clp["SA"].read_discrete_inputs(REG["SA_ED_DisjDJ1_Super125VccCiCom"])[0] == 0:
            logger.debug("[USN] DisjDJ1_Super125VccCiCom")
            flag += 1

        if self.clp["SA"].read_discrete_inputs(REG["SA_ED_DisjDJ1_AlPressBaixa"])[0] == 1:
            logger.debug("[USN] DisjDJ1_AlPressBaixa")
            flag += 1

        if self.clp["SA"].read_discrete_inputs(REG["SA_RD_DJ1_FalhaInt"])[0] == 1:
            logger.debug("[USN] MXR_DJ1_FalhaInt")
            flag += 1

        if self.clp["SA"].read_discrete_inputs(REG["SA_ED_DisjDJ1_BloqPressBaixa"])[0] == 1:
            logger.debug("[USN] DisjDJ1_BloqPressBaixa")
            flag += 1

        if self.clp["SA"].read_discrete_inputs(REG["SA_ED_DisjDJ1_Sup125VccBoFeAb1"])[0] == 0:
            logger.debug("[USN] DisjDJ1_Sup125VccBoFeAb1")
            flag += 1

        if self.clp["SA"].read_discrete_inputs(REG["SA_ED_DisjDJ1_Sup125VccBoFeAb2"])[0] == 0:
            logger.debug("DisjDJ1_Sup125VccBoFeAb2")
            flag += 1

        if self.clp["SA"].read_discrete_inputs(REG["SA_ED_DisjDJ1_Local"])[0] == 1:
            logger.debug("[USN] DisjDJ1_Local")
            flag += 1

        if self.clp["SA"].read_discrete_inputs(REG["SA_ED_DisjDJ1_MolaDescarregada"])[0] == 1:
            logger.debug("[USN] DisjDJ1_MolaDescarregada")
            flag += 1

        if flag > 0:
            logger.warning(f"[USN] Foram detectados bloqueios ao fechar o Dj52L. Número de bloqueios: \"{flag}\".")
            return True
        else:
            return False

    def verificar_tensao(self) -> bool:
        try:
            if (TENSAO_LINHA_BAIXA < self.__tensao_rs.valor < TENSAO_LINHA_ALTA) \
                and (TENSAO_LINHA_BAIXA < self.__tensao_st.valor < TENSAO_LINHA_ALTA) \
                and (TENSAO_LINHA_BAIXA < self.__tensao_tr.valor < TENSAO_LINHA_ALTA):
                return True
            else:
                logger.warning("[USN] Tensão da linha fora do limite.")
                return False

        except Exception:
            logger.error(f"[USN] Houve um erro ao realizar a verificação da tensão na linha.")
            logger.debug(traceback.format_exc())
            return False

    def aguardar_tensao(self) -> bool:
        if self.status_tensao == TENSAO_VERIFICAR:
            self.status_tensao = TENSAO_AGUARDO
            logger.debug("[USN] Iniciando o timer para a normalização da tensão na linha.")
            threading.Thread(target=lambda: self.acionar_temporizador_tensao(600)).start()

        elif self.status_tensao == TENSAO_REESTABELECIDA:
            logger.info("[USN] Tensão na linha reestabelecida.")
            self.status_tensao = TENSAO_VERIFICAR
            return True

        elif self.status_tensao == TENSAO_FORA:
            logger.critical("[USN] Não foi possível reestabelecer a tensão na linha. Acionando emergência")
            self.status_tensao = TENSAO_VERIFICAR
            return False

        else:
            logger.debug("[USN] A tensão na linha ainda está fora.")

    def acionar_temporizador_tensao(self, delay) -> None:
        while time() <= time() + delay:
            if self.verificar_tensao():
                self.status_tensao = TENSAO_REESTABELECIDA
                return
            sleep(time() - (time() - 15))
        self.status_tensao = TENSAO_FORA


    ### MÉTODOS DE CONTROLE DE OPERAÇÃO:

    def leitura_periodica(self):
        try:
            logger.debug("[USN] Iniciando o timer de leitura periódica...")
            while True:
                for ug in self.ugs:
                    ug.oco.leitura_temporizada()
                self.oco.leitura_temporizada()

                if True in (vd.voip_dict[r][0] for r in vd.voip_dict):
                    Voip.acionar_chamada()
                    pass

                sleep(max(0, (time() + 1800) - time()))

        except Exception:
            logger.error(f"[USN] Houve um erro ao executar o timer de leituras periódicas.")
            logger.debug(traceback.format_exc())

    def controlar_inicializacao(self) -> None:
        for ug in self.ugs:
            if ug.etapa_atual == UG_SINCRONIZADA:
                self.ug_operando += 1

        self.__split1 = True if self.ug_operando == 1 else False
        self.__split2 = True if self.ug_operando == 2 else False
        self.__split3 = True if self.ug_operando == 3 else False

        self.controle_ie = sum(ug.leitura_potencia for ug in self.ugs) / self.cfg["pot_maxima_alvo"]

        self.clp["MOA"].write_single_coil(REG["MOA_OUT_BLOCK_UG1"], [0])
        self.clp["MOA"].write_single_coil(REG["MOA_OUT_BLOCK_UG2"], [0])
        self.clp["MOA"].write_single_coil(REG["MOA_OUT_BLOCK_UG3"], [0])

    def controlar_reservatorio(self) -> int:
        self.resetar_tda()
        if self.nv_montante >= self.cfg["nv_maximo"]:
            logger.info("[USN] Nível montante acima do máximo")

            if self.nv_montante_recente >= NIVEL_MAXIMORUM:
                logger.critical(f"[USN] Nível montante ({self.nv_montante_recente:3.2f}) atingiu o maximorum!")
                return NV_FLAG_EMERGENCIA
            else:
                self.controle_i = 0.5
                self.controle_ie = 0.5
                self.distribuir_potencia(self.cfg["pot_maxima_usina"])
                for ug in self.ugs:
                    ug.step()

        elif self.nv_montante <= self.cfg["nv_minimo"] and not self.aguardando_reservatorio:
            logger.info("[USN] Nível montante abaixo do mínimo")
            self.aguardando_reservatorio = True
            self.distribuir_potencia(0)

            for ug in self.ugs:
                ug.step()

            if self.nv_montante_recente <= NIVEL_FUNDO_RESERVATORIO:
                if not ClientesUsina.ping(d.ips["TDA_ip"]):
                    logger.warning("[USN] A comunicação com a TDA falhou. Entrando em modo manual")
                    self.modo_autonomo = False
                    return NV_FLAG_EMERGENCIA
                else:
                    logger.critical(f"[USN] Nível montante ({self.nv_montante_recente:3.2f}) atingiu o fundo do reservatorio!")
                    return NV_FLAG_EMERGENCIA

        elif self.aguardando_reservatorio:
            if self.nv_montante >= self.cfg["nv_alvo"]:
                logger.debug("[USN] Nível montante dentro do limite de operação")
                self.aguardando_reservatorio = False

        else:
            self.controlar_potencia()

            for ug in self.ugs:
                ug.step()

        return NV_FLAG_NORMAL

    def controlar_potencia(self) -> None:
        logger.debug(f"[USN] NÍVEL -> Alvo:                      {self.cfg['nv_alvo']:0.3f}")
        logger.debug(f"[USN]          Leitura:                   {self.nv_montante_recente:0.3f}")
        
        self.controle_p = self.cfg["kp"] * self.erro_nv

        if self._pid_inicial == -1:
            self.controle_i = max(min(self.controle_ie - self.controle_p, 0.8), 0)
            self._pid_inicial = 0
        else:
            self.controle_i = max(min((self.cfg["ki"] * self.erro_nv) + self.controle_i, 0.8), 0)
            self.controle_d = self.cfg["kd"] * (self.erro_nv - self.erro_nv_anterior)

        saida_pid = (self.controle_p + self.controle_i + min(max(-0.3, self.controle_d), 0.3))

        logger.debug("")
        logger.debug(f"[USN] PID   -> P + I + D:                 {saida_pid:0.3f}")
        logger.debug(f"[USN] P:                                  {self.controle_p:0.3f}")
        logger.debug(f"[USN] I:                                  {self.controle_i:0.3f}")
        logger.debug(f"[USN] D:                                  {self.controle_d:0.3f}")

        self.controle_ie = max(min(saida_pid + self.controle_ie * self.cfg["kie"], 1), 0)
        logger.debug(f"[USN] IE:                                 {self.controle_ie:0.3f}")
        logger.debug(f"[USN] ERRO:                               {self.erro_nv}")
        logger.debug("")

        if self.nv_montante_recente >= (self.cfg["nv_maximo"] + 0.03):
            self.controle_ie = 1
            self.controle_i = 1 - self.controle_p

        if self.nv_montante_recente <= (self.cfg["nv_minimo"] + 0.03):
            self.controle_ie = min(self.controle_ie, 0.3)
            self.controle_i = 0

        pot_alvo = max(min(round(self.cfg["pot_maxima_usina"] * self.controle_ie, 5), self.cfg["pot_maxima_usina"],), self.cfg["pot_minima"],)
        logger.debug(f"[USN] Potência alvo:                      {pot_alvo:0.3f}")

        pot_alvo = self.ajustar_potencia(pot_alvo)

    def controlar_unidades_disponiveis(self) -> list:
        ls = [ug for ug in self.ugs if ug.disponivel and not ug.etapa_atual == UG_PARANDO]

        if self.modo_de_escolha_das_ugs in (UG_PRIORIDADE_1, UG_PRIORIDADE_2, UG_PRIORIDADE_3):
            ls = sorted(ls, key=lambda y: (-1 * y.etapa_atual, -1 * y.leitura_potencia, -1 * y.setpoint, y.prioridade))

        else:
            ls = sorted(ls, key=lambda y: (-1 * y.etapa_atual, y.leitura_horimetro, -1 * y.leitura_potencia, -1 * y.setpoint))

        return ls

    def ajustar_potencia(self, pot_alvo) -> None:
        if self._pot_alvo_anterior == -1:
            self._pot_alvo_anterior = pot_alvo

        if pot_alvo < 0.1:
            for ug in self.ugs: 
                ug.setpoint = 0
            return 0

        logger.debug(f"[USN] Potência no medidor:                {self.potencia_ativa:0.3f}")
        pot_aux = self.cfg["pot_maxima_alvo"] - (self.cfg["pot_maxima_usina"] - self.cfg["pot_maxima_alvo"])
        pot_medidor = max(pot_aux, min(self.potencia_ativa, self.cfg["pot_maxima_usina"]))

        if pot_medidor > self.cfg["pot_maxima_alvo"] * 0.97 and pot_alvo >= self.cfg["pot_maxima_alvo"]:
            pot_alvo = self._pot_alvo_anterior * (1 - 0.5 * ((pot_medidor - self.cfg["pot_maxima_alvo"]) / self.cfg["pot_maxima_alvo"]))

        self._pot_alvo_anterior = pot_alvo

        logger.debug(f"[USN] Potência alvo pós ajuste:           {pot_alvo:0.3f}")
        self.distribuir_potencia(pot_alvo)

    def ajustar_ie_padrao(self) -> int:
        return sum(ug.leitura_potencia for ug in self.ugs) / self.cfg["pot_maxima_alvo"]

    def distribuir_potencia(self, pot_alvo) -> None:
        ugs: "list[UnidadeGeracao]" = self.controlar_unidades_disponiveis()
        logger.debug("")
        logger.debug(f"[USN] Ordem das UGs (Prioridade):         {[ug.id for ug in ugs]}")
        logger.debug("")

        ug_sinc = 0
        pot_disp = 0
        ajuste_manual = 0

        for ug in self.ugs:
            pot_disp += ug.cfg[f"pot_maxima_ug{ug.id}"]
            if ug.manual:
                ajuste_manual += ug.leitura_potencia

        for ug in ugs:
            if ug.etapa_atual == UG_SINCRONIZANDO:
                ug_sinc += 1

        if ugs is None or not len(ugs):
            return

        logger.debug(f"[USN] Distribuindo:                       {pot_alvo - ajuste_manual:0.3f}")

        sp = (pot_alvo - ajuste_manual) / self.cfg["pot_maxima_usina"]

        self.__split1 = True if sp > (0) else self.__split1
        self.__split2 = True if sp > ((self.cfg["pot_maxima_ug"] / self.cfg["pot_maxima_usina"]) + self.cfg["margem_pot_critica"]) else self.__split2
        self.__split3 = True if sp > (2 * (self.cfg["pot_maxima_ug"] / self.cfg["pot_maxima_usina"]) + self.cfg["margem_pot_critica"]) else self.__split3

        self.__split3 = False if sp < (2 * (self.cfg["pot_maxima_ug"] / self.cfg["pot_maxima_usina"]) - self.cfg["margem_pot_critica"]) else self.__split3
        self.__split2 = False if sp < ((self.cfg["pot_maxima_ug"] / self.cfg["pot_maxima_usina"]) - self.cfg["margem_pot_critica"]) else self.__split2
        self.__split1 = False if sp < (self.cfg["pot_minima"] / self.cfg["pot_maxima_usina"]) else self.__split1

        logger.debug(f"[USN] SP Geral:                           {sp}")

        if len(ugs) == 3:
            if self.__split3:
                logger.debug("[USN] Split:                              3")
                logger.debug("")
                sp * 3 / (3 - ug_sinc)
                for ug in ugs:
                    if ug.etapa_atual == UG_SINCRONIZANDO:
                        ug.setpoint = sp * ug.setpoint_maximo
                    else:
                        ug.setpoint = sp * ug.setpoint_maximo

                logger.debug(f"[UG{ugs[0].id}] SP    <-                            {int(ugs[0].setpoint)}")
                logger.debug(f"[UG{ugs[1].id}] SP    <-                            {int(ugs[1].setpoint)}")
                logger.debug(f"[UG{ugs[2].id}] SP    <-                            {int(ugs[2].setpoint)}")

            elif self.__split2:
                logger.debug("[USN] Split:                              2")
                logger.debug("")
                sp = sp * 3 / (2 - ug_sinc)
                for ug in ugs:
                    if ug.etapa_atual == UG_SINCRONIZANDO:
                        ug.setpoint = sp * ug.setpoint_minimo
                    else:
                        ug.setpoint = sp * ug.setpoint_maximo

                ugs[2].setpoint = 0
                logger.debug(f"[UG{ugs[0].id}] SP    <-                            {int(ugs[0].setpoint)}")
                logger.debug(f"[UG{ugs[1].id}] SP    <-                            {int(ugs[1].setpoint)}")
                logger.debug(f"[UG{ugs[2].id}] SP    <-                            {int(ugs[2].setpoint)}")

            elif self.__split1:
                logger.debug("[USN] Split:                              1")
                logger.debug("")
                sp = sp * 3 / (1 - ug_sinc)
                for ug in ugs:
                    if ug.etapa_atual == UG_SINCRONIZANDO:
                        ug.setpoint = ug.setpoint_minimo
                    else:
                        ug.setpoint = sp * ug.setpoint_maximo

                ugs[1].setpoint = 0
                ugs[2].setpoint = 0
                logger.debug(f"[UG{ugs[0].id}] SP    <-                            {int(ugs[0].setpoint)}")
                logger.debug(f"[UG{ugs[1].id}] SP    <-                            {int(ugs[1].setpoint)}")
                logger.debug(f"[UG{ugs[2].id}] SP    <-                            {int(ugs[2].setpoint)}")

            else:
                logger.debug("")
                for ug in self.ugs:
                    ug.setpoint = 0
                    logger.debug(f"[UG{ug.id}] SP    <-                            {int(ug.setpoint)}")

        if len(ugs) == 2:
            if self.__split2:
                logger.debug("[USN] Split:                              2B")
                logger.debug("")
                sp = sp * 3 / (2 - ug_sinc)
                for ug in ugs:
                    if ug.etapa_atual == UG_SINCRONIZANDO:
                        ug.setpoint = sp * ug.setpoint_minimo
                    else:
                        ug.setpoint = sp * ug.setpoint_maximo

                logger.debug(f"[UG{ugs[0].id}] SP    <-                            {int(ugs[0].setpoint)}")
                logger.debug(f"[UG{ugs[1].id}] SP    <-                            {int(ugs[1].setpoint)}")

            elif self.__split1:
                logger.debug("[USN] Split:                              1")
                logger.debug("")
                sp = sp * 3 / (1 - ug_sinc)
                for ug in ugs:
                    if ug.etapa_atual == UG_SINCRONIZANDO:
                        ug.setpoint = ug.setpoint_minimo
                    else:
                        ug.setpoint = sp * ug.setpoint_maximo

                ugs[1].setpoint = 0
                logger.debug(f"[UG{ugs[0].id}] SP    <-                            {int(ugs[0].setpoint)}")
                logger.debug(f"[UG{ugs[1].id}] SP    <-                            {int(ugs[1].setpoint)}")

            else:
                logger.debug("")
                ugs[0].setpoint = 0
                ugs[1].setpoint = 0
                logger.debug(f"[UG{ugs[0].id}] SP    <-                            {int(ugs[0].setpoint)}")
                logger.debug(f"[UG{ugs[1].id}] SP    <-                            {int(ugs[1].setpoint)}")

        elif len(ugs) == 1:
            if self.__split1 or self.__split2:
                logger.debug("[USN] Split:                              1B")
                logger.debug("")
                sp = sp * 3 / 1
                ugs[0].setpoint = sp * ugs[0].setpoint_maximo
                logger.debug(f"[UG{ugs[0].id}] SP    <-                            {int(ugs[0].setpoint)}")


    ### MÉTODOS DE CONTROLE DE DADOS:

    def ler_valores(self) -> None:
        ClientesUsina.ping_clients()
        self.atualizar_valores_montante()

        parametros = self.db.get_parametros_usina()
        self.atualizar_valores_cfg(parametros)
        self.atualizar_valores_banco(parametros)

        for ug in self.ugs:
            ug.oco.atualizar_limites_condicionadores(parametros)

        self.heartbeat()

    def atualizar_valores_montante(self) -> None:
        self.nv_montante_recente = self.nv_montante
        self.erro_nv_anterior = self.erro_nv
        self.erro_nv = self.nv_montante_recente - self.cfg["nv_alvo"]

    def atualizar_valores_banco(self, parametros) -> None:
        try:
            if int(parametros["emergencia_acionada"]) == 1:
                logger.debug("[USN] Emergência acionada!")
                self.db_emergencia = True
            else:
                self.db_emergencia = False

            if int(parametros["modo_autonomo"]) == 1 and not self.modo_autonomo:
                self.modo_autonomo = True
                logger.debug(f"[USN] Modo autônomo:                      \"{'Ativado'}\"")
            elif int(parametros["modo_autonomo"]) == 0 and self.modo_autonomo:
                self.modo_autonomo = False
                logger.debug(f"[USN] Modo autônomo:                      \"{'Desativado'}\"")

            if not self.modo_de_escolha_das_ugs == int(parametros["modo_de_escolha_das_ugs"]):
                self.modo_de_escolha_das_ugs = int(parametros["modo_de_escolha_das_ugs"])
                logger.info(f"[USN] Modo de prioridade das UGs:         \"{UG_STR_DCT_PRIORIDADE[self.modo_de_escolha_das_ugs]}\"")

            for ug in self.ugs:
                ug.atualizar_limites_operacao(parametros)

        except Exception:
            logger.error(f"[USN] Houve um erro ao ler e atualizar os parâmetros do Banco de Dados.")
            logger.debug(traceback.format_exc())

    def atualizar_valores_cfg(self, parametros) -> None:
        self.cfg["nv_alvo"] = float(parametros["nv_alvo"])
        self.cfg["nv_minimo"] = float(parametros["nv_minimo"])

        self.cfg["kp"] = float(parametros["kp"])
        self.cfg["ki"] = float(parametros["ki"])
        self.cfg["kd"] = float(parametros["kd"])
        self.cfg["kie"] = float(parametros["kie"])
        self.cfg["cx_kp"] = float(parametros["cx_kp"])
        self.cfg["cx_ki"] = float(parametros["cx_ki"])
        self.cfg["cx_kie"] = float(parametros["cx_kie"])
        self.cfg["press_cx_alvo"] = float(parametros["press_cx_alvo"])

        self.cfg["pot_maxima_alvo"] = float(parametros["pot_nominal"])
        self.cfg["pot_maxima_ug"] = float(parametros["pot_nominal_ug"])
        self.cfg["pot_maxima_usina"] = float(parametros["pot_nominal_ug"]) * 3
        self.cfg["margem_pot_critica"] = float(parametros["margem_pot_critica"])

    def escrever_valores(self) -> None:
        try:
            v_params = [
                self.get_time().strftime("%Y-%m-%d %H:%M:%S"),
                1 if self.aguardando_reservatorio else 0,
                self.nv_montante if not d.glb["TDA_Offline"] else 0,
                self.ug1.leitura_potencia,
                self.ug1.setpoint,
                self.ug1.codigo_state,
                self.ug2.leitura_potencia,
                self.ug2.setpoint,
                self.ug2.codigo_state,
                self.ug3.leitura_potencia,
                self.ug3.setpoint,
                self.ug3.codigo_state,
            ]
            self.db.update_valores_usina(v_params)

        except Exception:
            logger.error(f"[USN] Houve um erro ao gravar os parâmetros da Usina no Banco.")
            logger.debug(traceback.format_exc())

        try:
            v_params = [
                time(),
                self.ug1.codigo_state,
                self.ug2.codigo_state,
                self.ug3.codigo_state,
            ]
            self.db.update_controle_estados(v_params)

        except Exception:
            logger.error(f"[USN] Houve um erro ao gravar os estados das Unidades no Banco.")
            logger.debug(traceback.format_exc())

        try:
            v_debug = [
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
                self.ug3.setpoint,
                self.ug3.leitura_potencia,
                self.ug3.codigo_state,
                self.controle_p,
                self.controle_i,
                self.controle_d,
                self.controle_ie,
                self.cfg["kp"],
                self.cfg["ki"],
                self.cfg["kd"],
                self.cfg["kie"]
            ]
            self.db.update_debug(v_debug)

        except Exception:
            logger.error(f"[USN] Houve um erro ao gravar os parâmetros debug no Banco.")
            logger.debug(traceback.format_exc())

    def heartbeat(self) -> None:
        try:
            self.clp["MOA"].write_single_coil(REG["PAINEL_LIDO"], [1])
            self.clp["MOA"].write_single_coil(REG["MOA_OUT_MODE"], [1 if self._modo_autonomo else 0])
            self.clp["MOA"].write_single_register(REG["MOA_OUT_STATUS"], self.estado_moa)

            for ug in self.ugs:
                ug.atualizar_modbus_moa()

            if self.modo_autonomo:
                self.clp["MOA"].write_single_coil(REG["MOA_OUT_EMERG"], [1 if self.clp_emergencia else 0])
                self.clp["MOA"].write_single_register(REG["MOA_OUT_TARGET_LEVEL"], int((self.cfg["nv_alvo"] - 400) * 1000))
                self.clp["MOA"].write_single_register(REG["MOA_OUT_SETPOINT"], int(sum(ug.setpoint for ug in self.ugs)))

                if self.clp["MOA"].read_coils(REG["MOA_IN_EMERG"]) == 1 and not self.borda_emerg:
                    self.borda_emerg = True
                    for ug in self.ugs:
                        ug.oco.verificar_condicionadores(ug)

                elif self.clp["MOA"].read_coils(REG["MOA_IN_EMERG"]) == 0 and self.borda_emerg:
                    self.borda_emerg = False

                if self.clp["MOA"].read_coils(REG["MOA_IN_EMERG_UG1"]) == 1:
                    self.ug1.oco.verificar_condicionadores(self.ug1)

                if self.clp["MOA"].read_coils(REG["MOA_IN_EMERG_UG2"]) == 1:
                    self.ug2.oco.verificar_condicionadores(self.ug2)

                if self.clp["MOA"].read_coils(REG["MOA_IN_EMERG_UG3"]) == 1:
                    self.ug2.oco.verificar_condicionadores(self.ug3)

                if self.clp["MOA"].read_coils(REG["MOA_IN_HABILITA_AUTO"]) == 1:
                    self.clp["MOA"].write_single_coil(REG["MOA_IN_HABILITA_AUTO"], [1])
                    self.clp["MOA"].write_single_coil(REG["MOA_IN_DESABILITA_AUTO"], [0])
                    self.modo_autonomo = True

                if self.clp["MOA"].read_coils(REG["MOA_IN_DESABILITA_AUTO"]) == 1:
                    self.clp["MOA"].write_single_coil(REG["MOA_IN_HABILITA_AUTO"], [0])
                    self.clp["MOA"].write_single_coil(REG["MOA_IN_DESABILITA_AUTO"], [1])
                    self.modo_autonomo = False

                if self.clp["MOA"].read_coils(REG["MOA_OUT_BLOCK_UG1"]) == 1:
                    self.clp["MOA"].write_single_coil(REG["MOA_OUT_BLOCK_UG1"], [1])

                elif self.clp["MOA"].read_coils(REG["MOA_OUT_BLOCK_UG1"]) == 0:
                    self.clp["MOA"].write_single_coil(REG["MOA_OUT_BLOCK_UG1"], [0])

                if self.clp["MOA"].read_coils(REG["MOA_OUT_BLOCK_UG2"]) == 1:
                    self.clp["MOA"].write_single_coil(REG["MOA_OUT_BLOCK_UG2"], [1])

                elif self.clp["MOA"].read_coils(REG["MOA_OUT_BLOCK_UG2"]) == 0:
                    self.clp["MOA"].write_single_coil(REG["MOA_OUT_BLOCK_UG2"], [0])

                if self.clp["MOA"].read_coils(REG["MOA_OUT_BLOCK_UG3"]) == 1:
                    self.clp["MOA"].write_single_coil(REG["MOA_OUT_BLOCK_UG3"], [1])

                elif self.clp["MOA"].read_coils(REG["MOA_OUT_BLOCK_UG3"]) == 0:
                    self.clp["MOA"].write_single_coil(REG["MOA_OUT_BLOCK_UG3"], [0])

            elif not self.modo_autonomo:
                if self.clp["MOA"].read_coils(REG["MOA_IN_HABILITA_AUTO"]) == 1:
                    self.clp["MOA"].write_single_coil(REG["MOA_IN_HABILITA_AUTO"], [1])
                    self.clp["MOA"].write_single_coil(REG["MOA_IN_DESABILITA_AUTO"], [0])
                    self.modo_autonomo = True

                self.clp["MOA"].write_single_coil(REG["MOA_OUT_EMERG"], [0])
                self.clp["MOA"].write_single_coil(REG["MOA_OUT_BLOCK_UG1"], [0])
                self.clp["MOA"].write_single_coil(REG["MOA_OUT_BLOCK_UG2"], [0])
                self.clp["MOA"].write_single_coil(REG["MOA_OUT_BLOCK_UG3"], [0])
                self.clp["MOA"].write_single_register(REG["MOA_OUT_SETPOINT"], int(0))
                self.clp["MOA"].write_single_register(REG["MOA_OUT_TARGET_LEVEL"], int(0))

        except Exception:
            logger.error(f"[USN] Houve um erro ao tentar escrever valores modbus no CLP MOA.")
            logger.debug(traceback.format_exc())