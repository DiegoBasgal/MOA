import pytz
import logging
import traceback

import src.dicionarios.dict as d

from time import sleep, time
from threading import Thread
from datetime import  datetime, timedelta

from src.ocorrencias import *
from src.funcoes.leitura import *
from src.dicionarios.const import *

from src.mensageiro.voip import Voip
from src.conectores.servidores import Servidores
from src.conectores.banco_dados import BancoDados
from src.unidade_geracao import UnidadeDeGeracao
from src.funcoes.agendamentos import Agendamentos
from src.funcoes.escrita import EscritaModBusBit as EMB

logger = logging.getLogger("logger")

class Usina:
    def __init__(self, cfg: "dict"=None):

        # VERIFICAÇÃO DE ARGUMENTOS

        if None in (cfg):
            raise ValueError("[USN] Não foi possível carregar os arquivos de configuração (\"cfg.json\").")
        else:
            self.cfg = cfg


        # INCIALIZAÇÃO DE OBJETOS DA USINA

        self.clp = Servidores.clp
        self.db = BancoDados("MOA-PPN")
        self.oco = OcorrenciasGerais(self.clp, self.db)
        self.agn = Agendamentos(self.cfg, self.db, self)

        self.ug1: "UnidadeDeGeracao" = UnidadeDeGeracao(1, self.cfg, self.db)
        self.ug2: "UnidadeDeGeracao" = UnidadeDeGeracao(2, self.cfg, self.db)
        self.ugs: "list[UnidadeDeGeracao]" = [self.ug1, self.ug2]


        # ATRIBUIÇÃO DE VARIÁVEIS PRIVADAS

        self.__pid_inicial: "int" = -1

        self.__leitura_dj_tsa: "LeituraModbusBit" = LeituraModbusBit(
            self.clp["SA"],
            REG["SA"]["SA_ED_PSA_DIJS_TSA_FECHADO"],
            descr="[USN] Status Disjuntor SA"
        )
        self.__leitura_dj_linha: "LeituraModbusBit" = LeituraModbusBit(
            self.clp["SA"],
            REG["SA"]["SA_ED_PSA_SE_DISJ_LINHA_FECHADO"],
            descr="[USN] Status Disjuntor Linha"
        )


        # ATRIBUIÇÃO DE VARIÁVEIS PROTEGIDAS

        self._pot_alvo_anterior: "int" = -1
        self._tentativas_normalizar: "int" = 0

        self._modo_autonomo: "bool" = False

        self._potencia_ativa: "LeituraModbus" = LeituraModbus(
            self.clp["SA"],
            REG_RELE["SE"]["RELE_SE_P"],
            op=3,
            descr="[USN] Potência Ativa"
        )
        self._tensao_rs: "LeituraModbus" = LeituraModbus(
            self.clp["SA"],
            REG_RELE["SE"]["RELE_SE_VAB"],
            op=4,
            descr="[USN] Tensão RS"
        )
        self._tensao_st: "LeituraModbus" = LeituraModbus(
            self.clp["SA"],
            REG_RELE["SE"]["RELE_SE_VBC"],
            op=4,
            descr="[USN] Tensão ST"
        )
        self._tensao_tr: "LeituraModbus" = LeituraModbus(
            self.clp["SA"],
            REG_RELE["SE"]["RELE_SE_VCA"],
            op=4,
            descr="[USN] Tensão TR"
        )
        self._nv_montante: "LeituraModbusFloat" = LeituraModbusFloat(
            self.clp["TDA"],
            REG_GERAL["GERAL_EA_NIVEL_MONTANTE_GRADE"],
            descr="[USN] Nível Montante"
        )


        # ATRIBUIÇÃO DE VARIÁVEIS PÚBLICAS

        self.estado_moa: "int" = 0
        self.status_tensao: "int" = 0

        self.controle_p: "float" = 0
        self.controle_i: "float" = 0
        self.controle_d: "float" = 0

        self.fator_pot: "float" = 0

        self.pot_disp: "int" = 0
        self.ug_operando: "int" = 0
        self.modo_de_escolha_das_ugs: "int" = 0

        self.erro_nv: "float" = 0
        self.erro_nv_anterior: "float" = 0
        self.nv_montante_recente: "float" = 0
        self.nv_montante_anterior: "float" = 0

        self.timer_tensao: "bool" = False


        self.borda_emerg: "bool" = False
        self.db_emergencia: "bool" = False
        self.clp_emergencia: "bool" = False

        self.tentar_normalizar: "bool" = True
        self.normalizar_forcado: "bool" = False

        self.aguardando_reservatorio: "bool" = False

        self.ultima_tentativa_norm: "datetime" = self.get_time()


        # EXECUÇÃO FINAL DA INICIALIZAÇÃO

        logger.debug("")
        for ug in self.ugs:
            ug.lista_ugs = self.ugs
            ug.iniciar_ultimo_estado()

        self.ler_valores()
        self.ajustar_inicializacao()
        self.djl_manual: "bool" = True
        self.normalizar_usina()
        self.escrever_valores()
        self.djl_manual = False

        self._tentativas_normalizar = 0


    ### PROPRIEDADES DA OPERAÇÃO

    @property
    def potencia_ativa(self) -> "int":
        return self._potencia_ativa.valor

    @property
    def nv_montante(self) -> "float":
        return self._nv_montante.valor

    @property
    def tensao_rs(self) -> "float":
        return self._tensao_rs.valor

    @property
    def tensao_st(self) -> "float":
        return self._tensao_st.valor

    @property
    def tensao_tr(self) -> "float":
        return self._tensao_tr.valor

    @property
    def modo_autonomo(self) -> "bool":
        return self._modo_autonomo

    @modo_autonomo.setter
    def modo_autonomo(self, var: "bool") -> "None":
        self._modo_autonomo = var
        self.db.update_modo_moa(self._modo_autonomo)

    @property
    def tentativas_normalizar(self) -> "int":
        return self._tentativas_normalizar

    @tentativas_normalizar.setter
    def tentativas_normalizar(self, var: "int") -> None:
        self._tentativas_normalizar = var

    @property
    def pot_alvo_anterior(self) -> "float":
        return self._pot_alvo_anterior

    @pot_alvo_anterior.setter
    def pot_alvo_anterior(self, var: "float") -> "None":
        self._pot_alvo_anterior = var

    def get_time(self) -> "datetime":
        return datetime.now(pytz.timezone("Brazil/East")).replace(tzinfo=None)


    ### MÉTODOS DE CONTROLE DE RESET E NORMALIZAÇÃO

    def acionar_emergencia(self) -> "None":
        logger.warning("[USN] Acionando Emergência.")
        self.clp_emergencia = True

        try:
            for ug in self.ugs:
                EMB.escrever_bit(self.clp[f"UG{ug.id}"], REG["UG"][f"UG{ug.id}_CD_CMD_PARADA_EMERGENCIA"], 1, descr=f"UG{ug.id}_CD_CMD_PARADA_EMERGENCIA")

        except Exception:
            logger.error(f"[USN] Houve um erro ao acionar a Emergência.")
            logger.debug(traceback.format_exc())

    def resetar_emergencia(self) -> "None":
        try:
            logger.info(f"[USN] Enviando comando:                   \"RESET GERAL\"")

            EMB.escrever_bit(self.clp["SA"], REG["SA"]["SA_CD_REARME_FALHAS"], valor=1, descr="SA_CD_REARME_FALHAS")
            EMB.escrever_bit(self.clp["SA"], REG["GERAL"]["GERAL_CD_RESET_GERAL"], valor=1, descr="GERAL_CD_RESET_GERAL")

            for ug in self.ugs:
                EMB.escrever_bit(self.clp[f"UG{ug.id}"], REG["UG"][f"UG{ug.id}_CD_CMD_REARME_FALHAS"], valor=1, descr=f"UG{ug.id}_CD_CMD_REARME_FALHAS")

        except Exception:
            logger.error(f"[USN] Houve um erro ao realizar o Reset Geral.")
            logger.debug(traceback.format_exc())

    def normalizar_usina(self) -> "int":
        logger.debug("")
        logger.debug(f"[USN] Última tentativa de normalização:   {self.ultima_tentativa_norm.strftime('%d-%m-%Y %H:%M:%S')}")
        logger.debug(f"[USN] Tensão na linha:                    RS -> \"{self.tensao_rs:2.1f} kV\" | ST -> \"{self.tensao_st:2.1f} kV\" | TR -> \"{self.tensao_tr:2.1f} kV\"")
        logger.debug("")

        if not self.verificar_tensao():
            return NORM_USN_FALTA_TENSAO

        elif (self.tentativas_normalizar < 3 and (self.get_time() - self.ultima_tentativa_norm).seconds >= 60 * self.tentativas_normalizar) or self.normalizar_forcado:
            self.ultima_tentativa_norm = self.get_time()
            self.tentativas_normalizar += 1
            logger.debug("")
            logger.info(f"[USN] Normalizando Usina... (Tentativa {self.tentativas_normalizar}/3)")
            self.db_emergencia = False
            self.clp_emergencia = False
            self.resetar_emergencia()
            sleep(2)
            if not self.djl_manual:
                self.fechar_dj_linha()

            self.db.update_remove_emergencia()
            return NORM_USN_EXECUTADA

        else:
            logger.debug("")
            logger.debug("[USN] A normalização foi executada menos de 5 minutos atrás...")
            return NORM_USN_JA_EXECUTADA


    def aguardar_normalizacao_djl(self) -> "bool":
        """
        Função com loop, para aguardar normalização manual do Disjuntor 52L
        por conta de problemas de aberturas.
        """

        self.djl_manual = self.db.get_status_djl()

        if self.djl_manual:
            logger.info("[USN] Aguardando fechamento manual do Disjuntor 52L...")

            while not self.__leitura_dj_linha.valor:
                logger.debug("[USN] Aguardando...")
                sleep(TEMPO_CICLO_TOTAL)
                self.escrever_valores()

            logger.info("[USN] Disjuntor Fechado! Retomando operação...")
            return True

        else:
            return False


    ### MÉTODOS DE CONTROLE DE OPERAÇÃO:

    def verificar_leituras_periodicas(self) -> "None":
        try:
            logger.debug("[USN] Iniciando o timer de leitura periódica...")
            while True:
                # for ug in self.ugs:
                #     ug.oco.verificar_leituras()
                # self.oco.verificar_leituras()

                if True in (d.voip[r][0] for r in d.voip):
                    Voip.acionar_chamada()
                    pass

                sleep(max(0, (time() + 1800) - time()))

        except Exception:
            logger.debug(f"[USN] Houve um erro ao executar o timer de leituras periódicas.")
            logger.debug(traceback.format_exc())

    def fechar_dj_linha(self) -> "bool":
        try:
            if self.__leitura_dj_linha.valor:
                logger.debug("[USN] O Disjuntor de Linha já está fechado!")

            elif not self.__leitura_dj_tsa.valor:
                logger.info("[USN] Não foi possível fechar o Disjuntor de Linha, pois o Disjuntor do SA está aberto")
                return False

            else:
                logger.info(f"[USN] Enviando comando:                   \"FECHAR DJ LINHA\"")
                res = EMB.escrever_bit(self.clp["SA"], REG["SA"]["SA_CD_DISJ_LINHA_FECHA"], valor=1)
                return res

        except Exception:
            logger.error(f"[USN] Houver um erro ao fechar o Disjuntor de Linha.")
            logger.debug(traceback.format_exc())
            return False

    def verificar_tensao(self) -> "bool":
        try:
            if (TENSAO_LINHA_BAIXA <= self.tensao_rs <= TENSAO_LINHA_ALTA) \
                and (TENSAO_LINHA_BAIXA <= self.tensao_st <= TENSAO_LINHA_ALTA) \
                and (TENSAO_LINHA_BAIXA <= self.tensao_tr <= TENSAO_LINHA_ALTA):
                return True

            else:
                logger.warning("[USN] Tensão da linha fora do limite")
                return False

        except Exception:
            logger.error(f"[USN] Houve um erro ao realizar a verificação da tensão na linha.")
            logger.debug(traceback.format_exc())

    def aguardar_tensao(self) -> "bool":
        if self.status_tensao == TENSAO_VERIFICAR:
            self.status_tensao = TENSAO_AGUARDO
            logger.debug("[USN] Iniciando o timer para a normalização da tensão na linha")
            Thread(target=lambda: self.temporizar_espera_tensao(600)).start()

        elif self.status_tensao == TENSAO_REESTABELECIDA:
            logger.info("[USN] Tensão na linha reestabelecida.")
            self.status_tensao = TENSAO_VERIFICAR
            return True

        elif self.status_tensao == TENSAO_FORA:
            logger.critical("[USN] Não foi possível reestabelecer a tensão na linha. Acionando emergência!")
            self.status_tensao = TENSAO_VERIFICAR
            return False

        else:
            logger.debug("[USN] A tensão na linha ainda está fora")

    def temporizar_espera_tensao(self, delay) -> "None":
        while time() <= time() + delay:
            if self.verificar_tensao():
                self.status_tensao = TENSAO_REESTABELECIDA
                return

            sleep(time() - (time() - 15))
        self.status_tensao = TENSAO_FORA

    def ajustar_inicializacao(self) -> "None":
        for ug in self.ugs:
            if ug.etapa == UG_SINCRONIZADA:
                self.ug_operando += 1

        self.__split1 = True if self.ug_operando == 1 else False
        self.__split2 = True if self.ug_operando == 2 else False

        self.controle_ie = self.ajustar_ie_padrao()

    def controlar_reservatorio(self) -> "int":

        if self.nv_montante_recente >= self.cfg["nv_maximo"]:
            logger.debug("[USN] Nível montante acima do limite Máximo!")
            logger.debug(f"[USN]          Leitura:                   {self.nv_montante_recente:0.3f}")
            logger.debug("")

            if self.nv_montante_recente >= NIVEL_MAXIMORUM:
                logger.critical(f"[USN] Nível montante ({self.nv_montante_recente:3.2f}) atingiu o maximorum!")
                return NV_FLAG_EMERGENCIA
            else:
                self.controle_i = 0.5
                self.controle_ie = 0.5
                self.ajustar_potencia(self.cfg["pot_maxima_usina"])
                for ug in self.ugs:
                    ug.step()

        elif self.nv_montante_recente <= self.cfg["nv_minimo"] and not self.aguardando_reservatorio:

            if self.nv_montante < self.cfg["nv_minimo"] and self.nv_montante_recente > self.cfg["nv_minimo"]:
                if self.erro_leitura_montante == 3:
                    logger.warning(f"[USN] Tentativas de Leitura de Nível Montante ultrapassadas!")
                    self.erro_leitura_montante = 0
                    self.distribuir_potencia(0)

                    for ug in self.ugs:
                        ug.step()

                    return NV_FLAG_EMERGENCIA

                self.erro_leitura_montante += 1
                logger.info("[USN] Foi identificada uma diferença nas Leituras de Nível Montante anterior e atual")
                logger.debug(f"[USN] Verificando erros de Leitura... (Tentativa {self.erro_leitura_montante}/3)")
            else:
                logger.debug("[USN] Nível Montante abaixo do limite Mínimo!")
                logger.debug(f"[USN]          Leitura:                   {self.nv_montante_recente:0.3f}")
                logger.debug("")

                self.erro_leitura_montante = 0
                self.aguardando_reservatorio = True
                self.distribuir_potencia(0)

                for ug in self.ugs:
                    ug.step()

                if self.nv_montante_recente <= NIVEL_FUNDO_RESERVATORIO:
                    logger.critical(f"[USN] Nível montante ({self.nv_montante_recente:3.2f}) atingiu o fundo do reservatorio!")
                    return NV_FLAG_EMERGENCIA

        elif self.aguardando_reservatorio:
            if self.nv_montante_recente >= self.cfg["nv_alvo"]:
                logger.debug("[USN] Nível montante dentro do limite de operação")
                self.aguardando_reservatorio = False

        else:
            self.controlar_potencia()

            for ug in self.ugs:
                ug.step()

        return NV_FLAG_NORMAL

    def controlar_potencia(self) -> "None":
        logger.debug(f"[USN] NÍVEL -> Alvo:                      {self.cfg['nv_alvo']:0.3f}")
        logger.debug(f"[USN]          Leitura:                   {self.nv_montante_recente:0.3f}")

        self.controle_p = self.cfg["kp"] * self.erro_nv

        if self.__pid_inicial == -1:
            self.controle_i = max(min(self.controle_ie - self.controle_p, 0.9), 0)
            self.__pid_inicial = 0
        else:
            self.controle_i = max(min((self.cfg["ki"] * self.erro_nv) + self.controle_i, 0.9), 0)
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

        pot_alvo = self.ajustar_potencia(pot_alvo)

    def controlar_unidades_disponiveis(self) -> "list":
        ls = [ug for ug in self.ugs if ug.disponivel and not ug.etapa == UG_PARANDO]

        # TODO verificar leituras de horímetro das Unidades
        # if self.modo_de_escolha_das_ugs in (UG_PRIORIDADE_1, UG_PRIORIDADE_2):
        ls = sorted(ls, key=lambda y: (-1 * y.leitura_potencia, -1 * y.setpoint, y.prioridade))

        # else:
        #     ls = sorted(ls, key=lambda y: (y.leitura_horimetro, -1 * y.leitura_potencia, -1 * y.setpoint))

        return ls

    def ajustar_potencia(self, pot_alvo) -> "None":
        if self.pot_alvo_anterior == -1:
            self.pot_alvo_anterior = pot_alvo

        if pot_alvo < 0.1:
            for ug in self.ugs: ug.setpoint = 0
            return 0

        logger.debug(f"[USN] Potência no medidor:                {self.potencia_ativa:0.3f}")
        pot_aux = self.cfg["pot_maxima_alvo"] - (self.cfg["pot_maxima_usina"] - self.cfg["pot_maxima_alvo"])
        pot_medidor = max(pot_aux, min(self.potencia_ativa, self.cfg["pot_maxima_usina"]))

        if pot_medidor > self.cfg["pot_maxima_alvo"]:
            pot_alvo = self.pot_alvo_anterior * (1 - ((pot_medidor - self.cfg["pot_maxima_alvo"]) / self.cfg["pot_maxima_alvo"]))

        self.pot_alvo_anterior = pot_alvo

        logger.debug(f"[USN] Potência alvo após ajuste:          {pot_alvo:0.3f}")
        self.distribuir_potencia(pot_alvo)

    def ajustar_ie_padrao(self) -> "int":
        return sum(ug.leitura_potencia for ug in self.ugs) / self.cfg["pot_maxima_alvo"]

    def distribuir_potencia(self, pot_alvo) -> "None":
        ugs: "list[UnidadeDeGeracao]" = self.controlar_unidades_disponiveis()
        logger.debug("")
        logger.debug(f"[USN] Ordem das UGs (Prioridade):         {[ug.id for ug in ugs]}")
        logger.debug("")

        ajuste_manual = 0

        for ug in self.ugs:
            if ug.manual:
                ajuste_manual += ug.leitura_potencia
            else:
                self.pot_disp += ug.setpoint_maximo

        if ugs is None or not len(ugs):
            return

        logger.debug(f"[USN] Distribuindo:                       {pot_alvo - ajuste_manual:0.3f}")
        sp = (pot_alvo - ajuste_manual) / self.cfg["pot_maxima_usina"]

        self.__split1 = True if sp > (0) else self.__split1
        self.__split2 = (True if sp > (0.5 + self.cfg["margem_pot_critica"]) else self.__split2)

        self.__split2 = False if sp < (0.5) else self.__split2
        self.__split1 = False if sp < (self.cfg["pot_minima"] / self.cfg["pot_maxima_usina"]) else self.__split1

        logger.debug(f"[USN] SP Geral:                           {sp}")

        if len(ugs) == 2:
            if self.__split2:
                logger.debug("[USN] Split:                              2")
                logger.debug("")
                ugs[0].setpoint = sp * ugs[0].setpoint_maximo
                ugs[1].setpoint = sp * ugs[1].setpoint_maximo
                logger.debug(f"[UG{ugs[0].id}] SP    <-                            {int(ugs[0].setpoint)}")
                logger.debug(f"[UG{ugs[1].id}] SP    <-                            {int(ugs[1].setpoint)}")

            elif self.__split1:
                logger.debug("[USN] Split:                              2 -> \"1B\"")
                logger.debug("")
                sp = sp * 2 / 1
                ugs[0].setpoint = sp * ugs[0].setpoint_maximo
                ugs[1].setpoint = 0
                logger.debug(f"[UG{ugs[0].id}] SP    <-                            {int(ugs[0].setpoint)}")
                logger.debug(f"[UG{ugs[1].id}] SP    <-                            {int(ugs[1].setpoint)}")

        elif len(ugs) == 1:
            if self.__split1 or self.__split2:
                logger.debug("[USN] Split:                              1")
                logger.debug("")
                sp = sp * 2 / 1
                ugs[0].setpoint = sp * ugs[0].setpoint_maximo
                logger.debug(f"[UG{ugs[0].id}] SP    <-                            {int(ugs[0].setpoint)}")

        else:
            for ug in ugs:
                ug.setpoint = 0


    ### MÉTODOS DE CONTROLE DE DADOS:

    def ler_valores(self) -> "None":
        Servidores.ping_clients()
        self.atualizar_valores_montante()

        parametros = self.db.get_parametros_usina()
        self.atualizar_valores_cfg(parametros)
        self.atualizar_valores_banco(parametros)

        # if self.clp["SA"].read_coils(REG["SA"]["RESERVA_X"])[0] == 1 and not self.modo_autonomo:
        #     self.modo_autonomo = True
        # elif self.clp["SA"].read_coils(REG["SA"]["RESERVA_X"])[0] == 0 and self.modo_autonomo:
        #     self.modo_autonomo == False

        for ug in self.ugs:
            ug.oco.atualizar_limites_condicionadores(parametros)

        # self.heartbeat()

    def atualizar_valores_montante(self) -> "None":
        self.nv_montante_recente = self.nv_montante if 820 < self.nv_montante < 825 else self.nv_montante_recente
        self.erro_nv_anterior = self.erro_nv
        self.erro_nv = self.nv_montante_recente - self.cfg["nv_alvo"]

    def atualizar_valores_banco(self, parametros) -> "None":
        try:
            if int(parametros["emergencia_acionada"]) == 1 and not self.db_emergencia:
                logger.info(f"[USN] Emergência:                      \"{'Acionada'}\"")
                self.db_emergencia = True
            elif int(parametros["emergencia_acionada"]) == 0 and self.db_emergencia:
                logger.info(f"[USN] Emergência:                      \"{'Desativada'}\"")
                self.db_emergencia = False

            if int(parametros["modo_autonomo"]) == 1 and not self.modo_autonomo:
                self.modo_autonomo = True
                logger.info(f"[USN] Modo autônomo:                      \"{'Ativado'}\"")
            elif int(parametros["modo_autonomo"]) == 0 and self.modo_autonomo:
                self.modo_autonomo = False
                logger.info(f"[USN] Modo autônomo:                      \"{'Desativado'}\"")

            if self.modo_de_escolha_das_ugs != int(parametros["modo_de_escolha_das_ugs"]):
                self.modo_de_escolha_das_ugs = int(parametros["modo_de_escolha_das_ugs"])
                logger.info(f"[USN] Modo de prioridade das UGs:         \"{UG_STR_DCT_PRIORIDADE[self.modo_de_escolha_das_ugs]}\"")

        except Exception:
            logger.error(f"[USN] Houve um erro ao ler e atualizar os parâmetros do Banco de Dados.")
            logger.debug(traceback.format_exc())

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
            logger.debug(traceback.format_exc())

    def escrever_valores(self) -> None:
        try:
            v1 = [
                self.get_time().strftime("%Y-%m-%d %H:%M:%S"),
                1 if self.aguardando_reservatorio else 0,
                self.nv_montante,
                self.ug1.leitura_potencia,
                self.ug1.setpoint,
                self.ug1.codigo_state,
                self.ug2.leitura_potencia,
                self.ug2.setpoint,
                self.ug2.codigo_state,
            ]

            v2 = [
                self.get_time().timestamp(),
                1 if self.modo_autonomo else 0,
                self.nv_montante,
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
            ]
            self.db.update_valores_usina(v1)

        except Exception:
            logger.debug(f"[USN] Houve um erro ao inserir os valores no Banco.")
            logger.debug(traceback.format_exc())

        try:
            self.db.update_debug(v2)

        except Exception:
            logger.debug(f"[USN] Houve um erro ao inserir dados DEBUG no Banco.")
            logger.debug(traceback.format_exc())


    # TODO -> Adicionar após a integração do CLP do MOA no painel do SA, que depende da intervenção da Automatic.
    """
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
                    for ug in self.ugs:
                        ug.oco.verificar_condicionadores(ug)

                elif self.clp["MOA"].read_coils(REG_MOA["MOA_IN_EMERG"]) == 0 and self.borda_emerg:
                    self.borda_emerg = False

                if self.clp["MOA"].read_coils(REG_MOA["MOA_IN_EMERG_UG1"]) == 1:
                    self.ug1.oco.verificar_condicionadores(self.ug1)

                if self.clp["MOA"].read_coils(REG_MOA["MOA_IN_EMERG_UG2"]) == 1:
                    self.ug2.oco.verificar_condicionadores(self.ug2)

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
            logger.debug(traceback.format_exc())
    """