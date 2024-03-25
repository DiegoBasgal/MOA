import pytz
import logging
import traceback

import src.subestacao as se
import src.tomada_agua as tda
import src.unidade_geracao as u
import src.dicionarios.dict as d
import src.mensageiro.dict as vd
import src.mensageiro.voip as vp
import src.servico_auxiliar as sa
import src.funcoes.condicionador as c
import src.funcoes.agendamentos as agn
import src.conectores.servidores as srv
import src.conectores.banco_dados as bd

from time import sleep, time
from datetime import  datetime

from src.dicionarios.reg import *
from src.dicionarios.const import *

logger = logging.getLogger("logger")
debug_log = logging.getLogger("debug")


class Usina:
    def __init__(self, cfg: "dict"=None):

        # VERIFICAÇÃO DE ARGUMENTOS
        if None in (cfg):
            raise ValueError("[USN] Não foi possível carregar os arquivos de configuração (\"cfg.json\").")
        else:
            self.cfg = cfg

        # INCIALIZAÇÃO DE OBJETOS DA USINA
        self.clp = srv.Servidores.clp
        self.bd = bd.BancoDados("MOA-SEB")
        self.agn = agn.Agendamentos(self.cfg, self.bd, self)

        self.ug1 = u.UnidadeGeracao(1, self.cfg, self.bd)
        self.ug2 = u.UnidadeGeracao(2, self.cfg, self.bd)
        self.ug3 = u.UnidadeGeracao(3, self.cfg, self.bd)
        self.ugs: "list[u.UnidadeGeracao]" = [self.ug1, self.ug2, self.ug3]
        c.CondicionadorBase.ugs = self.ugs

        # PROTEGIDAS
        self._pid_inicial: "int" = -1
        self._pot_alvo_anterior: "int" = -1
        self._tentativas_normalizar: "int" = 0

        self._modo_autonomo: "bool" = False

        # PÚBLICAS
        self.estado_moa: "int" = 0

        self.ug_operando: "int" = 0
        self.ver_pot_ant: "int" = 0
        self.modo_escolha_ugs: "int" = -1

        self.controle_p: "float" = 0
        self.controle_i: "float" = 0
        self.controle_d: "float" = 0
        self.pid_inicial: "float" = -1

        self.borda_emerg: "bool" = False
        self.bd_emergencia: "bool" = False
        self.clp_emergencia: "bool" = False
        self.normalizar_forcado: "bool" = False
        self.aguardando_reservatorio: "bool" = False

        self.ultima_tentativa_norm: "datetime" = self.get_time()

        # FINALIZAÇÃO DO __INIT__
        logger.debug("")
        for ug in self.ugs:
            ug.lista_ugs = self.ugs
            ug.iniciar_ultimo_estado()

        self.ler_valores()
        self.ajustar_inicializacao()
        self.normalizar_usina()
        self.escrever_valores()


    @property
    def modo_autonomo(self) -> bool:
        # PROPRIEDADE -> Retrona o modo do MOA.
        return self._modo_autonomo

    @modo_autonomo.setter
    def modo_autonomo(self, var: bool) -> None:
        # SETTER -> Atribui o novo valor de modo do MOA e atualiza o Banco.
        self._modo_autonomo = var
        self.bd.update_modo_moa(self._modo_autonomo)

    @property
    def tentativas_normalizar(self) -> int:
        # PROPRIEDADE -> Retrona o número de tentativas de normalização da Usina.

        return self._tentativas_normalizar

    @tentativas_normalizar.setter
    def tentativas_normalizar(self, var: int) -> None:
        # SETTER -> Atribui o novo valor de tentativas de normalização da Usina.

        self._tentativas_normalizar = var

    @property
    def _pot_alvo_anterior(self) -> float:
        # PROPRIEDADE -> Retrona o valor de potência alvo anterior da Usina.

        return self._potencia_alvo_anterior

    @_pot_alvo_anterior.setter
    def _pot_alvo_anterior(self, var):
        # SETTER -> Atribui o novo valor de de potência alvo anterior da Usina.

        self._potencia_alvo_anterior = var


    # FUNÇÕES
    @staticmethod
    def get_time() -> "datetime":
        """
        Função para obter data e hora atual.
        """

        return datetime.now(pytz.timezone("Brazil/East")).replace(tzinfo=None)


    ### FUNÇÕES DE CONTROLE DE RESET E NORMALIZAÇÃO

    def acionar_emergencia(self) -> "None":
        """
        Função para acionamento de emergência geral da Usina. Envia o comando de
        emergência via supervisório para todos os CLPs.
        """

        logger.warning("[USN] Acionando Emergência.")

        try:
            for ug in self.ugs:
                self.clp[f"UG{ug.id}"].write_single_coil(REG_UG[f"UG{ug.id}"]["CMD_EMERG_SUPER"], [1])

        except Exception:
            logger.error(f"[USN] Houve um erro ao acionar a Emergência.")
            logger.debug(traceback.format_exc())


    def resetar_emergencia(self) -> "None":
        """
        Função para reset geral da Usina. Envia o comando de reset para todos os
        CLPs.
        """

        try:
            logger.debug("[USN] Reset geral")

            self.clp["SA"].write_single_coil(REG_SA["CMD_RESET_GERAL"], [1])
            self.clp["SA"].write_single_coil(REG_SA["CMD_CALA_SIRENE"], [1])
            self.clp["TDA"].write_single_coil(REG_TDA["CMD_RESET_GERAL"], [1]) if not d.glb["TDA_Offline"] else logger.debug("[USN] CLP TDA Offline, não há como realizar o reset geral")
            for ug in self.ugs:
                self.clp[f"UG{ug.id}"].write_single_coil(REG_UG[f"UG{ug.id}"]["CMD_RESET_GERAL"], [0])
                self.clp[f"UG{ug.id}"].write_single_coil(REG_UG[f"UG{ug.id}"]["CMD_CALA_SIRENE"], [0])
                self.clp[f"UG{ug.id}"].write_single_coil(REG_UG[f"UG{ug.id}"]["CMD_EMERG_SUPER"], [0])
            se.Subestacao.fechar_dj_linha()

        except Exception:
            logger.error(f"[USN] Houve um erro ao realizar o Reset Geral.")
            logger.debug(traceback.format_exc())


    def normalizar_usina(self) -> "int":
        """
        Função para normalização de ocorrências da Usina.

        Verifica primeiramente a tensão da linha.
        Caso a tenão esteja dentro dos limites, passa a verificar se a
        normalização foi executada à pouco tempo, se foi, avisa o operador,
        senão, passa a chamar as funções de reset geral.
        """

        logger.debug(f"[USN] Última tentativa de normalização:   {self.ultima_tentativa_norm.strftime('%d-%m-%Y %H:%M:%S')}")
        logger.debug(f"[USN] Tensão na linha:                    RS -> \"{se.Subestacao.l_tensao_rs.valor:2.1f} kV\" | ST -> \"{se.Subestacao.l_tensao_st.valor:2.1f} kV\" | TR -> \"{se.Subestacao.l_tensao_tr.valor:2.1f} kV\"")

        if not se.Subestacao.verificar_tensao():
            return NORM_USN_FALTA_TENSAO

        elif (self.tentativas_normalizar < 3 and (self.get_time() - self.ultima_tentativa_norm).seconds >= 60 * self.tentativas_normalizar) or self.normalizar_forcado:
            self.ultima_tentativa_norm = self.get_time()
            self.tentativas_normalizar += 1
            logger.info(f"[USN] Normalizando Usina... (Tentativa {self.tentativas_normalizar}/3)")
            self.clp_emergencia = self.bd_emergencia = False
            self.resetar_emergencia()
            sleep(2)
            se.Subestacao.fechar_dj_linha()
            self.bd.update_remove_emergencia()
            return NORM_USN_EXECUTADA

        else:
            logger.debug("[USN] A normalização foi executada menos de 1 minuto atrás")
            return NORM_USN_JA_EXECUTADA


    ### FUNÇÕES DE CONTROLE DE OPERAÇÃO:

    def leitura_periodica(self):
        """
        Função de temporizador com leituras para alertas de manutenção.

        Chama os métodos de leitura de objetos da Usina e Unidades de Geração.
        Caso haja alguma leitura fora do esperado, é enviado o alerta via
        WhatsApp ou Voip.
        """

        try:
            logger.debug("[USN] Iniciando o timer de leitura periódica...")
            while True:
                sa.ServicoAuxiliar.leitura_temporizada()
                for ug in self.ugs:
                    ug.leitura_temporizada()

                if True in (vd.voip_dict[r][0] for r in vd.voip_dict):
                    vp.Voip.acionar_chamada()
                    pass

                sleep(max(0, (time() + 1800) - time()))

        except Exception:
            logger.debug(f"[USN] Houve um erro com a função de Leituras Periódicas.")
            logger.debug(traceback.format_exc())


    def ajustar_inicializacao(self) -> None:
        """
        Função para ajustes na inicialização do MOA. Essa função é executada apenas
        uma vez.
        """

        for ug in self.ugs:
            if ug.etapa_atual == UG_SINCRONIZADA:
                self.ug_operando += 1

        self.__split1 = True if self.ug_operando == 1 else False
        self.__split2 = True if self.ug_operando == 2 else False
        self.__split3 = True if self.ug_operando == 3 else False

        self.controle_ie = sum(ug.potencia for ug in self.ugs) / self.cfg["pot_alvo_usina"]

        self.clp["MOA"].write_single_coil(REG_MOA["MOA_OUT_BLOCK_UG1"], 0)
        self.clp["MOA"].write_single_coil(REG_MOA["MOA_OUT_BLOCK_UG2"], 0)
        self.clp["MOA"].write_single_coil(REG_MOA["MOA_OUT_BLOCK_UG3"], 0)


    def controlar_reservatorio(self) -> int:
        """
        Função para controle de níveis do reservatório.

        Primeiramente aciona a função de reset da Tomada da Água (para desabilitar
        mecanismos como controle de nível e religamento do Dj 52L). Logo em seguida,
        realiza a leitura de nível montante e determina qual condição entrar. Se
        o nível estiver acima do máximo, verifica se atingiu o Maximorum. Nesse
        caso é acionada a emergência da Usina, porém se for apenas vertimento,
        distribui a potência máxima para as Unidades.
        Caso a leitura retornar que o nível está abaixo do mínimo, verifica antes
        se atingiu o fundo do reservatório, nesse caso é acionada a emergência.
        Se o valor ainda estiver acima do nível de fundo, será distribuída a
        potência 0 para todas as Unidades e aciona a espera pelo nível.
        Caso a leitura esteja dentro dos limites normais, é chamada a função para
        calcular e distribuir a potência para as Unidades.
        """

        tda.TomadaAgua.resetar_tda()

        if tda.TomadaAgua.nv_montante_recente >= self.cfg["nv_maximo"]:
            logger.debug("[USN] Nível montante acima do Máximo.")
            logger.debug(f"[USN]          Leitura:                   {tda.TomadaAgua.l_nivel_montante.valor:0.3f}")
            logger.debug(f"[USN]          Filtro EMA:                {tda.TomadaAgua.nv_montante_recente:0.3f}")
            logger.debug("")

            if tda.TomadaAgua.nv_montante_recente >= NIVEL_MAXIMORUM:
                logger.critical(f"[USN] Nível montante ({tda.TomadaAgua.nv_montante_recente:3.2f}) atingiu o maximorum!")
                return NV_FLAG_EMERGENCIA
            else:
                self.controle_i = 0.8
                self.controle_ie = 0.5
                self.ajustar_potencia(self.cfg["pot_alvo_usina"])

                for ug in self.ugs:
                    ug.step()

        elif tda.TomadaAgua.nv_montante_recente <= self.cfg["nv_minimo"] and not self.aguardando_reservatorio:
            logger.debug("[USN] Nível montante abaixo do Mínimo.")
            logger.debug(f"[USN]          Leitura:                   {tda.TomadaAgua.l_nivel_montante.valor:0.3f}")
            logger.debug(f"[USN]          Filtro EMA:                {tda.TomadaAgua.nv_montante_recente:0.3f}")

            if tda.TomadaAgua.nv_montante_recente <= NIVEL_FUNDO_RESERVATORIO:
                if tda.TomadaAgua.l_nivel_montante.valor <= 400 or not self.clp["TDA"].open():
                    d.glb["TDA_Offline"] = True
                    return NV_FLAG_NORMAL
                else:
                    logger.critical(f"[USN] Nível montante ({tda.TomadaAgua.nv_montante_recente:3.2f}) atingiu o fundo do reservatorio!")
                    return NV_FLAG_EMERGENCIA

            if tda.TomadaAgua.nv_montante_recente < self.cfg["nv_minimo"]:
                self.aguardando_reservatorio = True
                self.distribuir_potencia(0)

                for ug in self.ugs:
                    ug.step()

        elif self.aguardando_reservatorio:
            if tda.TomadaAgua.l_nivel_montante.valor >= self.cfg["nv_alvo"]:
                logger.debug(f"[USN]          Leitura:                   {tda.TomadaAgua.l_nivel_montante.valor:0.3f}")
                logger.debug("[USN] Nível montante dentro do limite de operação")
                self.aguardando_reservatorio = False

        else:
            self.nv_montante_anterior = self.nv_montante_anterior
            self.controlar_potencia()

            for ug in self.ugs:
                ug.step()

        return NV_FLAG_NORMAL


    def controlar_potencia(self) -> None:
        logger.debug(f"[USN] NÍVEL -> Alvo:                      {self.cfg['nv_alvo']:0.3f}")
        logger.debug(f"[USN]          Leitura:                   {tda.TomadaAgua.l_nivel_montante.valor:0.3f}")
        logger.debug(f"[USN]          Filtro EMA:                {tda.TomadaAgua.nv_montante_recente:0.3f}")

        self.controle_p = self.cfg["kp"] * tda.TomadaAgua.erro_nv

        if self._pid_inicial == -1:
            self.controle_i = max(min(self.controle_ie - self.controle_p, 0.8), 0)
            self._pid_inicial = 0
        else:
            self.controle_i = max(min((self.cfg["ki"] * tda.TomadaAgua.erro_nv) + self.controle_i, 0.8), 0)
            self.controle_d = self.cfg["kd"] * (tda.TomadaAgua.erro_nv - tda.TomadaAgua.erro_nv_anterior)

        saida_pid = (self.controle_p + self.controle_i + min(max(-0.3, self.controle_d), 0.3))

        logger.debug("")
        logger.debug(f"[USN] PID   -> P + I + D:                 {saida_pid:0.3f}")
        logger.debug(f"[USN] P:                                  {self.controle_p:0.3f}")
        logger.debug(f"[USN] I:                                  {self.controle_i:0.3f}")
        logger.debug(f"[USN] D:                                  {self.controle_d:0.3f}")

        self.controle_ie = max(min(saida_pid + self.controle_ie * self.cfg["kie"], 1), 0)

        logger.debug(f"[USN] IE:                                 {self.controle_ie:0.3f}")
        logger.debug(f"[USN] ERRO:                               {tda.TomadaAgua.erro_nv}")
        logger.debug("")

        if tda.TomadaAgua.nv_montante_recente >= (self.cfg["nv_maximo"] + 0.03):
            self.controle_ie = 1
            self.controle_i = 1 - self.controle_p

        if tda.TomadaAgua.nv_montante_recente <= (self.cfg["nv_minimo"] + 0.03):
            self.controle_ie = min(self.controle_ie, 0.3)
            self.controle_i = 0

        pot_alvo = max(min(round(self.cfg["pot_maxima_usina"] * self.controle_ie, 5), self.cfg["pot_maxima_usina"],), self.cfg["pot_minima_ugs"],)

        pot_alvo = self.ajustar_potencia(pot_alvo)


    def controlar_unidades_disponiveis(self) -> list:
        ls = [ug for ug in self.ugs if ug.disponivel and not ug.etapa_atual == UG_PARANDO]

        if self.modo_escolha_ugs in (UG_PRIORIDADE_1, UG_PRIORIDADE_2, UG_PRIORIDADE_3):
            ls = sorted(ls, key=lambda y: (-1 * y.etapa_atual, -1 * y.potencia, -1 * y.setpoint, y.prioridade))
        else:
            ls = sorted(ls, key=lambda y: (-1 * y.etapa_atual, y.leitura_horimetro, -1 * y.potencia, -1 * y.setpoint))

        return ls


    def ajustar_potencia(self, pot_alvo) -> None:
        if self._pot_alvo_anterior == -1:
            self.ver_pot_ant = pot_alvo
            self._pot_alvo_anterior = pot_alvo

        if pot_alvo < 0.1:
            for ug in self.ugs:
                ug.setpoint = 0
            return 0

        pot_medidor = se.Subestacao.l_potencia_medidor.valor

        logger.debug(f"[USN] Potência no medidor:                {se.Subestacao.l_potencia_medidor.valor:0.3f}")

        pot_aux = self.cfg["pot_alvo_usina"] - (self.cfg["pot_maxima_usina"] - self.cfg["pot_alvo_usina"])
        pot_medidor = max(pot_aux, min(pot_medidor, self.cfg["pot_maxima_usina"]))

        if pot_medidor > self.cfg["pot_alvo_usina"] * 0.97 and pot_alvo >= self.cfg["pot_alvo_usina"]:
            pot_alvo = self._pot_alvo_anterior * (1 - 0.25 * ((pot_medidor - self.cfg["pot_alvo_usina"]) / self.cfg["pot_alvo_usina"]))
            pot_alvo = min(pot_alvo, self.cfg["pot_maxima_usina"])

        self._pot_alvo_anterior = pot_alvo

        logger.debug(f"[USN] Setpoint alvo após ajuste:          {(pot_alvo / self.cfg['pot_maxima_usina']) * 100:0.2f} %")

        self.distribuir_potencia(pot_alvo)


    def ajustar_ie_padrao(self) -> int:
        """
        Função para ajustar o valor do IE.
        """

        return sum(ug.potencia for ug in self.ugs) / self.cfg["pot_alvo_usina"]


    def distribuir_potencia(self, pot_alvo) -> None:
        ugs: "list[u.UnidadeGeracao]" = self.controlar_unidades_disponiveis()

        if ugs is None or not len(ugs):
            return

        logger.debug("")
        logger.debug(f"[USN] Ordem das UGs (Prioridade):         {[ug.id for ug in ugs]}")
        logger.debug("")

        ajuste_manual = 0
        ug_sincronizando = 0

        for ug in self.ugs:
            if ug.manual:
                ajuste_manual += ug.potencia

        for ug in ugs:
            if ug.etapa_atual == UG_SINCRONIZANDO:
                ug_sincronizando += 1

        if (pot_alvo - ajuste_manual) < 0:
            return

        logger.debug(f"[USN] Distribuindo:                       {((pot_alvo - ajuste_manual) / self.cfg['pot_maxima_usina']) * 100:0.2f} %")

        sp = (pot_alvo - ajuste_manual) / self.cfg["pot_maxima_usina"]

        self.__split1 = True if sp > (0) else self.__split1
        self.__split2 = True if sp > ((self.cfg["pot_maxima_ugs"] / self.cfg["pot_maxima_usina"]) + self.cfg["margem_pot_critica"]) else self.__split2
        self.__split3 = True if sp > (2 * (self.cfg["pot_maxima_ugs"] / self.cfg["pot_maxima_usina"]) + self.cfg["margem_pot_critica"]) else self.__split3

        self.__split3 = False if sp < (2 * (self.cfg["pot_maxima_ugs"] / self.cfg["pot_maxima_usina"]) - self.cfg["margem_pot_critica"]) else self.__split3
        self.__split2 = False if sp < ((self.cfg["pot_maxima_ugs"] / self.cfg["pot_maxima_usina"]) - self.cfg["margem_pot_critica"]) else self.__split2
        self.__split1 = False if sp < (self.cfg["pot_minima_ugs"] / self.cfg["pot_maxima_usina"]) else self.__split1

        logger.debug(f"[USN] SP Geral:                           {sp}")

        for ug in self.ugs: ug.manter_unidade = False

        if len(ugs) == 3:
            if self.__split3:
                logger.debug("[USN] Split:                              3")
                logger.debug("")

                if ug_sincronizando != 0:
                    for ug in ugs:
                        if ug.etapa_atual == UG_SINCRONIZANDO:
                            ug.setpoint = self.cfg["pot_minima_ugs"]
                        else:
                            ug.setpoint = self.cfg["pot_maxima_ugs"]

                else:
                    ugs[0].setpoint = sp * ugs[0].setpoint_maximo
                    ugs[1].setpoint = sp * ugs[1].setpoint_maximo
                    ugs[2].setpoint = sp * ugs[2].setpoint_maximo

                logger.debug(f"[UG{ugs[0].id}] SP    <-                            {int(ugs[0].setpoint)}")
                logger.debug(f"[UG{ugs[1].id}] SP    <-                            {int(ugs[1].setpoint)}")
                logger.debug(f"[UG{ugs[2].id}] SP    <-                            {int(ugs[2].setpoint)}")

            elif self.__split2:
                logger.debug("[USN] Split:                              3 -> \"2B\"")
                logger.debug("")

                if ug_sincronizando != 0:
                    for ug in ugs:
                        if ug.etapa_atual == UG_SINCRONIZANDO:
                            ug.setpoint = self.cfg["pot_minima_ugs"]
                        else:
                            ug.setpoint = self.cfg["pot_maxima_ugs"]

                else:
                    sp = sp * 3 / 2
                    ugs[0].setpoint = sp * ugs[0].setpoint_maximo
                    ugs[1].setpoint = sp * ugs[1].setpoint_maximo

                ugs[2].setpoint = 0

                logger.debug(f"[UG{ugs[0].id}] SP    <-                            {int(ugs[0].setpoint)}")
                logger.debug(f"[UG{ugs[1].id}] SP    <-                            {int(ugs[1].setpoint)}")
                logger.debug(f"[UG{ugs[2].id}] SP    <-                            {int(ugs[2].setpoint)}")

            elif self.__split1:
                logger.debug("[USN] Split:                              3 -> \"1B\"")
                logger.debug("")

                ugs[0].manter_unidade = True

                sp = sp * 3
                ugs[0].setpoint = sp * ugs[0].setpoint_maximo
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
            if self.__split2 or self.__split3:
                logger.debug("[USN] Split:                              2")
                logger.debug("")

                if ug_sincronizando != 0:
                    for ug in ugs:
                        if ug.etapa_atual == UG_SINCRONIZANDO:
                            ug.setpoint = self.cfg["pot_minima_ugs"]
                        else:
                            ug.setpoint = self.cfg["pot_maxima_ugs"]

                else:
                    sp = sp * 3 / 2
                    ugs[0].setpoint = sp * ugs[0].setpoint_maximo
                    ugs[1].setpoint = sp * ugs[1].setpoint_maximo

                logger.debug(f"[UG{ugs[0].id}] SP    <-                            {int(ugs[0].setpoint)}")
                logger.debug(f"[UG{ugs[1].id}] SP    <-                            {int(ugs[1].setpoint)}")

            elif self.__split1:
                logger.debug("[USN] Split:                              2 -> \"1B\"")
                logger.debug("")

                ugs[0].manter_unidade = True

                sp = sp * 3
                ugs[0].setpoint = sp * ugs[0].setpoint_maximo
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
            logger.debug("[USN] Split:                              1")
            logger.debug("")

            ugs[0].manter_unidade = True

            ugs[0].setpoint = 3 * sp * ugs[0].setpoint_maximo

            logger.debug(f"[UG{ugs[0].id}] SP    <-                            {int(ugs[0].setpoint)}")


    # FUNÇÕES DE CONTROLE DE DADOS:
    def ler_valores(self) -> None:
        """
        Função para leitura e atualização de parâmetros de operação através de
        Banco de Dados da Interface WEB.
        """

        srv.Servidores.ping_clients()
        tda.TomadaAgua.atualizar_valores_montante()

        parametros = self.bd.get_parametros_usina()
        self.atualizar_valores_cfg(parametros)
        self.atualizar_valores_banco(parametros)

        for ug in self.ugs:
            ug.atualizar_limites_condicionadores(parametros)

        self.heartbeat()


    def atualizar_valores_banco(self, parametros) -> None:
        """
        Função para atualização de valores de Banco de Dados.
        """

        try:
            if int(parametros["emergencia_acionada"]) == 1 and not self.bd_emergencia:
                logger.info(f"[USN] Emergência:                         \"{'Ativada'}\"!")
                self.bd_emergencia = True
            elif int(parametros["emergencia_acionada"]) == 0 and self.bd_emergencia:
                logger.info(f"[USN] Emergência:                         \"{'Desativada'}\"!")
                self.bd_emergencia = False

            if int(parametros["modo_autonomo"]) == 1 and not self.modo_autonomo:
                self.modo_autonomo = True
                logger.info(f"[USN] Modo autônomo:                      \"{'Ativado'}\"")
            elif int(parametros["modo_autonomo"]) == 0 and self.modo_autonomo:
                self.modo_autonomo = False
                logger.info(f"[USN] Modo autônomo:                      \"{'Desativado'}\"")

            if self.modo_escolha_ugs != int(parametros["modo_de_escolha_das_ugs"]):
                self.modo_escolha_ugs = int(parametros["modo_de_escolha_das_ugs"])
                logger.info(f"[USN] Modo de prioridade das UGs:         \"{UG_STR_DCT_PRIORIDADE[self.modo_escolha_ugs]}\"")

        except Exception:
            logger.error(f"[USN] Houve um erro ao ler e atualizar os parâmetros do Banco de Dados.")
            logger.debug(traceback.format_exc())


    def atualizar_valores_cfg(self, parametros) -> None:
        """
        Função para atualização de valores de operação do arquivo cfg.json.
        """

        self.cfg["nv_alvo"] = float(parametros["nv_alvo"])
        self.cfg["nv_minimo"] = float(parametros["nv_minimo"])
        self.cfg["nv_maximo"] = float(parametros["nv_maximo"])

        self.cfg["pot_minima_ugs"] = float(parametros["pot_minima_ugs"])
        self.cfg["pot_maxima_ugs"] = float(parametros["pot_maxima_ugs"])
        self.cfg["pot_maxima_usina"] = float(parametros["pot_maxima_usina"])
        self.cfg["margem_pot_critica"] = float(parametros["margem_pot_critica"])

        self.cfg["kp"] = float(parametros["kp"])
        self.cfg["ki"] = float(parametros["ki"])
        self.cfg["kd"] = float(parametros["kd"])
        self.cfg["kie"] = float(parametros["kie"])
        self.cfg["cx_kp"] = float(parametros["cx_kp"])
        self.cfg["cx_ki"] = float(parametros["cx_ki"])
        self.cfg["cx_kie"] = float(parametros["cx_kie"])
        self.cfg["pressao_alvo_ug1"] = float(parametros["ug1_pressao_alvo"])
        self.cfg["pressao_alvo_ug2"] = float(parametros["ug2_pressao_alvo"])
        self.cfg["pressao_alvo_ug3"] = float(parametros["ug3_pressao_alvo"])


    def escrever_valores(self) -> None:
        """
        Função para escrita de valores de operação nos Bancos do módulo do Django
        e Debug.
        """

        try:
            v_params = [
                self.get_time().strftime("%Y-%m-%d %H:%M:%S"),
                1 if self.aguardando_reservatorio else 0,
                tda.TomadaAgua.l_nivel_montante.valor if not d.glb["TDA_Offline"] else 0,
                self.ug1.potencia,
                self.ug1.setpoint,
                self.ug1.estado,
                self.ug2.potencia,
                self.ug2.setpoint,
                self.ug2.estado,
                self.ug3.potencia,
                self.ug3.setpoint,
                self.ug3.estado,
            ]
            self.bd.update_valores_usina(v_params)

        except Exception:
            logger.error(f"[USN] Houve um erro ao gravar os parâmetros da Usina no Banco.")
            logger.debug(traceback.format_exc())

        try:
            v_debug = [
                time(),
                1 if self.modo_autonomo else 0,
                tda.TomadaAgua.nv_montante_recente,
                tda.TomadaAgua.erro_nv,
                self.ug1.setpoint,
                self.ug1.potencia,
                self.ug1.estado,
                self.ug2.setpoint,
                self.ug2.potencia,
                self.ug2.estado,
                self.ug3.setpoint,
                self.ug3.potencia,
                self.ug3.estado,
                self.controle_p,
                self.controle_i,
                self.controle_d,
                self.controle_ie,
                self.cfg["kp"],
                self.cfg["ki"],
                self.cfg["kd"],
                self.cfg["kie"]
            ]
            self.bd.update_debug(v_debug)

        except Exception:
            logger.error(f"[USN] Houve um erro ao gravar os parâmetros debug no Banco.")
            logger.debug(traceback.format_exc())


    def heartbeat(self) -> None:
        """
        Função para controle do CLP - MOA.

        Esta função tem como objetivo enviar comandos de controle/bloqueio para
        os CLPs da Usina e também, ativação/desativação do MOA através de chaves
        seletoras no painel do Sistema Auxiliar.
        """

        try:
            self.clp["MOA"].write_single_coil(REG_MOA["PAINEL_LIDO"], 1)
            self.clp["MOA"].write_single_coil(REG_MOA["MOA_OUT_MODE"], 1 if self.modo_autonomo else 0)
            self.clp["MOA"].write_single_register(REG_MOA["MOA_OUT_STATUS"], self.estado_moa)

            for ug in self.ugs:
                ug.atualizar_modbus_moa()

            if self.modo_autonomo:
                self.clp["MOA"].write_single_coil(REG_MOA["MOA_OUT_EMERG"], 1 if self.clp_emergencia else 0)
                self.clp["MOA"].write_single_register(REG_MOA["MOA_OUT_TARGET_LEVEL"], int((self.cfg["nv_alvo"] - 400) * 1000))
                self.clp["MOA"].write_single_register(REG_MOA["MOA_OUT_SETPOINT"], int(sum(ug.setpoint for ug in self.ugs)))

                if self.clp["MOA"].read_coils(REG_MOA["MOA_IN_EMERG"])[0] == 1 and not self.borda_emerg:
                    self.borda_emerg = True
                    self.clp_emergencia = True
                    # for ug in self.ugs:
                    #     ug.verificar_condicionadores()

                elif self.clp["MOA"].read_coils(REG_MOA["MOA_IN_EMERG"])[0] == 0 and self.borda_emerg:
                    self.borda_emerg = False

                if self.clp["MOA"].read_coils(REG_MOA["MOA_IN_EMERG_UG1"])[0] == 1:
                    # self.ug1.verificar_condicionadores()
                    pass

                if self.clp["MOA"].read_coils(REG_MOA["MOA_IN_EMERG_UG2"])[0] == 1:
                    # self.ug2.verificar_condicionadores()
                    pass

                if self.clp["MOA"].read_coils(REG_MOA["MOA_IN_EMERG_UG3"])[0] == 1:
                    # self.ug3.verificar_condicionadores()
                    pass

                if self.clp["MOA"].read_coils(REG_MOA["MOA_IN_HABILITA_AUTO"])[0] == 1:
                    self.clp["MOA"].write_single_coil(REG_MOA["MOA_IN_HABILITA_AUTO"], 1)
                    self.clp["MOA"].write_single_coil(REG_MOA["MOA_IN_DESABILITA_AUTO"], 0)
                    self.modo_autonomo = True

                if self.clp["MOA"].read_coils(REG_MOA["MOA_IN_DESABILITA_AUTO"])[0] == 1:
                    self.clp["MOA"].write_single_coil(REG_MOA["MOA_IN_HABILITA_AUTO"], 0)
                    self.clp["MOA"].write_single_coil(REG_MOA["MOA_IN_DESABILITA_AUTO"], 1)
                    self.modo_autonomo = False

                if self.clp["MOA"].read_coils(REG_MOA["MOA_OUT_BLOCK_UG1"]) == 1:
                    self.clp["MOA"].write_single_coil(REG_MOA["MOA_OUT_BLOCK_UG1"], 1)

                elif self.clp["MOA"].read_coils(REG_MOA["MOA_OUT_BLOCK_UG1"]) == 0:
                    self.clp["MOA"].write_single_coil(REG_MOA["MOA_OUT_BLOCK_UG1"], 0)

                if self.clp["MOA"].read_coils(REG_MOA["MOA_OUT_BLOCK_UG2"]) == 1:
                    self.clp["MOA"].write_single_coil(REG_MOA["MOA_OUT_BLOCK_UG2"], 1)

                elif self.clp["MOA"].read_coils(REG_MOA["MOA_OUT_BLOCK_UG2"]) == 0:
                    self.clp["MOA"].write_single_coil(REG_MOA["MOA_OUT_BLOCK_UG2"], 0)

                if self.clp["MOA"].read_coils(REG_MOA["MOA_OUT_BLOCK_UG3"]) == 1:
                    self.clp["MOA"].write_single_coil(REG_MOA["MOA_OUT_BLOCK_UG3"], 1)

                elif self.clp["MOA"].read_coils(REG_MOA["MOA_OUT_BLOCK_UG3"]) == 0:
                    self.clp["MOA"].write_single_coil(REG_MOA["MOA_OUT_BLOCK_UG3"], 0)

            else:
                if self.clp["MOA"].read_coils(REG_MOA["MOA_IN_HABILITA_AUTO"])[0] == 1:
                    self.clp["MOA"].write_single_coil(REG_MOA["MOA_IN_HABILITA_AUTO"], 1)
                    self.clp["MOA"].write_single_coil(REG_MOA["MOA_IN_DESABILITA_AUTO"], 0)
                    self.modo_autonomo = True

                self.clp["MOA"].write_single_coil(REG_MOA["MOA_OUT_EMERG"], 0)
                self.clp["MOA"].write_single_coil(REG_MOA["MOA_OUT_BLOCK_UG1"], 0)
                self.clp["MOA"].write_single_coil(REG_MOA["MOA_OUT_BLOCK_UG2"], 0)
                self.clp["MOA"].write_single_coil(REG_MOA["MOA_OUT_BLOCK_UG3"], 0)
                self.clp["MOA"].write_single_register(REG_MOA["MOA_OUT_SETPOINT"], int(0))
                self.clp["MOA"].write_single_register(REG_MOA["MOA_OUT_TARGET_LEVEL"], int(0))

        except Exception:
            logger.debug(f"[USN] Houve um erro ao tentar escrever valores modbus no CLP MOA.")
            logger.debug(traceback.format_exc())