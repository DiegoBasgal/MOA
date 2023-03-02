import os
import sys
import time
import json
import pytz
import threading
import traceback

from time import sleep
from datetime import datetime

import src.usina as usina
import src.conector as conector

from src.logger import *
from src.VAR_REG import *
from src.mensageiro import voip

class StateMachine:
    def __init__(self, initial_state):
        self.state = initial_state
        self.em_falha_critica = False

    def exec(self):
        try:
            if self.state is None:
                raise TypeError
            self.state = self.state.run()

        except Exception as e:
            logger.warning(f"Estado ({self.state}) levantou uma exception: {repr(e)}")
            logger.debug(f"Traceback: {traceback.format_exc()}")
            self.em_falha_critica = True
            self.state = FalhaCritica()

class State:
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def run(self) -> object:
        return self

class FalhaCritica(State):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        logger.critical("Falha crítica MOA. Exiting...")
        sys.exit(1)

class Pronto(State):
    def __init__(self, instancia_usina, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.usina = instancia_usina

        self.n_tentativa = 0
        self.usina.state_moa = 3

    def run(self):
        if self.n_tentativa >= 2:
            return FalhaCritica()
        else:
            try:
                self.usina.ler_valores()
                return ValoresInternosAtualizados(self.usina) if not self.usina.TDA_Offline else OperacaoTDAOffline(self.usina)

            except Exception as e:
                self.n_tentativa += 1
                logger.error(f"Erro durante a comunicação do MOA com a usina. Tentando novamente em {self.usina.cfg['timeout_padrao'] * self.n_tentativa}s (tentativa{self.n_tentativa}/3).\n Exception: {repr(e)}.")
                logger.debug(f"Traceback: {traceback.format_exc()}")
                sleep(self.usina.cfg["timeout_padrao"] * self.n_tentativa)
                return self

class ValoresInternosAtualizados(State):
    def __init__(self, instancia_usina, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.usina = instancia_usina
        self.usina.clp_moa.write_single_coil(self.usina.cfg["REG_PAINEL_LIDO"], [1])

    def run(self):
        global borda_tensao
        global deve_normalizar

        emergencia_condic=False
        ler_condicionadores=False
        self.usina.TDA_Offline = False

        self.usina.ler_valores()

        for condicionador_essencial in self.usina.condicionadores_essenciais:
            ler_condicionadores=True if condicionador_essencial.ativo else False
            break

        if self.usina.avisado_em_eletrica or ler_condicionadores:
            for condicionador_essencial in self.usina.condicionadores_essenciais:
                deve_normalizar=True if condicionador_essencial.ativo and condicionador_essencial.gravidade == DEVE_NORMALIZAR else False
                emergencia_condic=True if condicionador_essencial.ativo and condicionador_essencial.gravidade == DEVE_INDISPONIBILIZAR else False

            for condicionador in self.usina.condicionadores:
                deve_normalizar=True if condicionador.ativo and condicionador.gravidade == DEVE_NORMALIZAR else False
                emergencia_condic=True if condicionador.ativo and condicionador.gravidade == DEVE_INDISPONIBILIZAR else False

        if deve_normalizar:
            if not self.usina.normalizar_emergencia() and not self.usina.tensao_ok and not borda_tensao:
                logger.warning("Tensão da linha fora do limite ")
                borda_tensao = True
                threading.Thread(target=lambda: self.usina.aguardar_tensao(600)).start()

            elif self.usina.timer_tensao:
                borda_tensao = False
                deve_normalizar = None
                self.usina.timer_tensao = None

            elif not self.usina.timer_tensao:
                borda_tensao = False
                deve_normalizar = None
                self.usina.timer_tensao = None
                logger.critical("O tempo de normalização da linha excedeu o limite! (10 min)")
                return Emergencia(self.usina)

        if self.usina.clp_emergencia_acionada or self.usina.db_emergencia_acionada or emergencia_condic:
            logger.info("Atenção! Emergência acionada!")
            emergencia_condic=False
            return Emergencia(self.usina)

        if len(self.usina.get_agendamentos_pendentes()) > 0:
            return AgendamentosPendentes(self.usina)

        if not self.usina.modo_autonomo:
            logger.debug("Comando recebido: desabilitar modo autonomo.")
            return ModoManualAtivado(self.usina)

        if self.usina.aguardando_reservatorio == 1 and (self.usina.nv_montante > self.usina.cfg["nv_alvo"]):
            logger.debug("Reservatorio dentro do nivel de trabalho")
            self.usina.aguardando_reservatorio = 0
            return ReservatorioNormal(self.usina)

        if self.usina.nv_montante < self.usina.cfg["nv_minimo"]:
            self.usina.aguardando_reservatorio = 1
            logger.info("Reservatorio abaixo do nivel de trabalho")
            return ReservatorioAbaixoDoMinimo(self.usina)

        if self.usina.nv_montante >= self.usina.cfg["nv_maximo"]:
            return ReservatorioAcimaDoMaximo(self.usina)

        return ReservatorioNormal(self.usina)


class Emergencia(State):
    def __init__(self, instancia_usina, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.usina = instancia_usina
        self.n_tentativa = 0
        self.nao_ligou = True
        self.em_sm_acionada = datetime.now(pytz.timezone("Brazil/East")).replace(tzinfo=None)
        logger.warning(f"Usina entrado em estado de emergência (Timestamp: {self.em_sm_acionada})")

    def run(self):
        self.n_tentativa += 1

        deve_normalizar = False
        deve_indisponibilizar = False
        condicionadores_ativos = []

        self.usina.ler_valores()

        if self.n_tentativa > 2:
            logger.warning("Numero de tentaivas de normalização excedidas, entrando em modo manual.")
            for ug in self.usina.ugs:
                ug.forcar_estado_indisponivel()
                ug.step()
            return ModoManualAtivado(self.usina)

        else:
            if self.usina.db_emergencia_acionada:
                logger.warning("Emergencia acionada via Interface WEB/DB, aguardando Reset/Reconhecimento pela interface ou CLP")
                while self.usina.db_emergencia_acionada:
                    self.usina.ler_valores()
                    if not self.usina.clp.em_emergencia():
                        self.usina.db.update_emergencia(0)
                        self.usina.db_emergencia_acionada = 0

            for condic in self.usina.condicionadores_essenciais:
                if condic.gravidade == DEVE_NORMALIZAR:
                    condicionadores_ativos.append(condic)
                    deve_normalizar = True
                elif condic.ativo and condic.gravidade == DEVE_INDISPONIBILIZAR:
                    condicionadores_ativos.append(condic)
                    deve_indisponibilizar = True

            for condic in self.usina.condicionadores:
                if condic.gravidade == DEVE_NORMALIZAR:
                    condicionadores_ativos.append(condic)
                    deve_indisponibilizar=False
                elif condic.ativo and condic.gravidade == DEVE_INDISPONIBILIZAR:
                    condicionadores_ativos.append(condic)
                    deve_indisponibilizar=True

            if self.usina.clp_emergencia_acionada or deve_normalizar or deve_indisponibilizar:
                try:
                    if deve_indisponibilizar:
                        logger.critical(f"[USN] USN detectou condicionadores ativos, passando USINA para manual e ligando por VOIP.\nCondicionadores ativos:\n{[d.descr for d in condicionadores_ativos]}")
                        self.usina.entrar_em_modo_manual()
                        return ModoManualAtivado(self.usina)

                    elif deve_normalizar:
                        logger.debug("Aguardando antes de tentar normalizar novamente (5s)")
                        sleep(5)
                        logger.info(f"Normalizando usina. (tentativa{self.n_tentativa}/2) (limite entre tentaivas: {self.usina.cfg['timeout_normalizacao']}s)")
                        self.usina.deve_normalizar_forcado=True
                        self.usina.normalizar_emergencia()
                        return self

                    else:
                        logger.debug("Nenhum condicionador relevante ativo...")
                        return ControleRealizado(self.usina)

                except Exception as e:
                    logger.error(f"Erro durante a comunicação do MOA com a usina. Exception: {repr(e)}.")
                    logger.debug(f"Traceback: {traceback.format_exc()}")

                return self

            else:
                logger.info("Usina normalizada")
                return ControleRealizado(self.usina)

class ModoManualAtivado(State):
    def __init__(self, instancia_usina, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.usina = instancia_usina

        self.usina.modo_autonomo = False

        self.usina.entrar_em_modo_manual()
        self.usina.clp_moa.write_single_coil(usina.cfg["REG_PAINEL_LIDO"], [1])

        logger.info("Usina em modo manual, deve-se alterar via painel ou interface web.")

    def run(self):
        self.usina.ler_valores()
        self.usina.ug1.setpoint = self.usina.ug1.leitura_potencia.valor
        self.usina.ug2.setpoint = self.usina.ug2.leitura_potencia.valor
        self.usina.controle_ie = (self.usina.ug1.setpoint + self.usina.ug2.setpoint) / self.usina.cfg["pot_maxima_alvo"]

        sleep(1 / ESCALA_DE_TEMPO)
        if self.usina.modo_autonomo:
            self.usina.ler_valores()
            logger.debug("Comando recebido: habilitar modo autonomo.")
            sleep(2)
            logger.debug("Usina voltou para o modo Autonomo")
            self.usina.db.update_habilitar_autonomo()
            if self.usina.clp_emergencia_acionada == 1 or self.usina.db_emergencia_acionada == 1:
                self.usina.normalizar_emergencia()
            self.usina.heartbeat()
            return ControleRealizado(self.usina)

        return AgendamentosPendentes(self.usina) if len(self.usina.get_agendamentos_pendentes()) > 0 else self

class AgendamentosPendentes(State):
    def __init__(self, instancia_usina, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.usina = instancia_usina

    def run(self):
        logger.info("Tratando agendamentos")
        self.usina.verificar_agendamentos()
        return ControleRealizado(self.usina)

class ReservatorioAbaixoDoMinimo(State):
    def __init__(self, instancia_usina, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.usina = instancia_usina

    def run(self):
        self.usina.ler_valores()
        self.usina.distribuir_potencia(0)

        if self.usina.nv_montante_recente <= self.usina.cfg["nv_fundo_reservatorio"]:
            if not usina.ping(self.usina.cfg["TDA_slave_ip"]):
                logger.warning("Sem comunicação com CLP TDA, entrando no modo de operação Offline")
                return OperacaoTDAOffline(self.usina)
            else:
                logger.critical(f"Nivel montante ({self.usina.nv_montante_recente:3.2f}) atingiu o fundo do reservatorio!")
                return Emergencia(self.usina)

        for ug in self.usina.ugs:
            ug.step()
        return ControleRealizado(self.usina)

class ReservatorioAcimaDoMaximo(State):
    def __init__(self, instancia_usina, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.usina = instancia_usina

    def run(self):
        self.usina.ler_valores()
        if self.usina.nv_montante_recente >= self.usina.cfg["nv_maximorum"]:
            self.usina.distribuir_potencia(0)
            logger.critical(f"Nivel montante ({self.usina.nv_montante_recente:3.2f}) atingiu o maximorum!")
            return Emergencia(self.usina)
        else:
            self.usina.distribuir_potencia(self.usina.cfg["pot_maxima_usina"])
            self.usina.controle_ie = 0.5
            self.usina.controle_i = 0.5
            for ug in self.usina.ugs: ug.step()
            return ControleRealizado(self.usina)

class ReservatorioNormal(State):
    def __init__(self, instancia_usina, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.usina = instancia_usina

    def run(self):
        self.usina.ler_valores()
        self.usina.controle_normal()
        for ug in self.usina.ugs: ug.step()
        return ControleRealizado(self.usina)

class OperacaoTDAOffline(State):
    def __init__(self, instancia_usina, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.usina = instancia_usina

    def run(self):
        self.usina.ler_valores()

        global borda_tensao
        global deve_normalizar

        emergencia_condic = False
        ler_condicionadores = False
        self.usina.TDA_Offline = True

        for condicionador_essencial in self.usina.condicionadores_essenciais:
            ler_condicionadores=True if condicionador_essencial.ativo else False

        if self.usina.avisado_em_eletrica or ler_condicionadores:
            for condicionador_essencial in self.usina.condicionadores_essenciais:
                deve_normalizar=True if condicionador_essencial.ativo and condicionador_essencial.gravidade == DEVE_NORMALIZAR else False
                emergencia_condic=True if condicionador_essencial.ativo and condicionador_essencial.gravidade == DEVE_INDISPONIBILIZAR else False
            
            for condicionador in self.usina.condicionadores:
                deve_normalizar=True if condicionador.ativo and condicionador.gravidade == DEVE_NORMALIZAR else False
                emergencia_condic=True if condicionador.ativo and condicionador.gravidade == DEVE_INDISPONIBILIZAR else False

        if emergencia_condic:
            logger.info("Condicionadores ativos com gravidade alta!")
            return Emergencia(self.usina)

        if deve_normalizar:
            if not self.usina.normalizar_emergencia() and not self.usina.tensao_ok and not borda_tensao:
                logger.warning("Tensão da linha fora do limite ")
                borda_tensao=True
                threading.Thread(target=lambda: self.usina.aguardar_tensao(20)).start()

            elif self.usina.timer_tensao:
                borda_tensao=False
                deve_normalizar = None
                self.usina.timer_tensao = None

            elif not self.usina.timer_tensao:
                borda_tensao=False
                deve_normalizar = None
                self.usina.timer_tensao = None
                logger.warning("O tempo de normalização da linha excedeu o limite! (10 min)")
                return Emergencia(self.usina)
        
        if not self.usina.modo_autonomo:
            logger.info("Comando recebido: desabilitar modo autonomo")
            return ModoManualAtivado(self.usina)

        for ug in self.usina.ugs:
            ug.controle_cx_espiral()
            ug.step()

        return AgendamentosPendentes(self.usina) if len(self.usina.get_agendamentos_pendentes()) > 0 else ControleRealizado(self.usina)

class ControleRealizado(State):
    def __init__(self, instancia_usina, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.usina = instancia_usina

    def run(self):
        self.usina.ler_valores()
        logger.debug("Escrevendo valores")
        self.usina.escrever_valores()
        return Pronto(self.usina)

def leitura_temporizada(delay):
    proxima_leitura = time.time() + delay
    logger.debug("Iniciando o timer de leitura por hora.")
    while True:
        logger.debug("Inciando nova leitura...")
        try:
            if usina.leituras_por_hora() and usina.acionar_voip:
                acionar_voip()
            for ug in usina.ugs:
                if ug.leituras_por_hora() and ug.acionar_voip:
                    acionar_voip()
            time.sleep(max(0, proxima_leitura - time.time()))

        except Exception:
            logger.debug("Houve um problema ao executar a leitura por hora")

        proxima_leitura += (time.time() - proxima_leitura) // delay * delay + delay

def acionar_voip():
    V_VARS = voip.VARS
    try:
        if usina.acionar_voip:
            for i, j in zip(VOIP, V_VARS):
                if i == j and VOIP[i]:
                    V_VARS[j][0] = VOIP[i]
            voip.enviar_voz_auxiliar()
            usina.acionar_voip = False

        elif usina.avisado_em_eletrica:
            voip.enviar_voz_emergencia()
            usina.avisado_em_eletrica = False

    except Exception:
        logger.warning("Houve um problema ao ligar por Voip")

if __name__ == "__main__":
    ESCALA_DE_TEMPO = 5
    if len(sys.argv) > 1:
        ESCALA_DE_TEMPO = int(sys.argv[1])

    usina = None

    timeout = 10
    prox_estado = 0
    n_tentativa = 0

    borda_tensao = False
    deve_normalizar = None

    logger.debug("Debug is ON")
    logger.info("Iniciando MOA...")
    logger.debug(f"Iniciando o MOA_SM ESCALA_DE_TEMPO:{ESCALA_DE_TEMPO}")
    logger.debug("Inciando Threads de Leitura temporizada e acionamento por voip")

    while prox_estado == 0:
        n_tentativa += 1

        if n_tentativa > 2:
            prox_estado = FalhaCritica
        else:
            config_file = os.path.join(os.path.dirname(__file__), "config.json")
            with open(config_file, "r") as file:
                cfg = json.load(file)

            config_file = os.path.join(os.path.dirname(__file__), "config.json.bkp")
            with open(config_file, "w") as file:
                json.dump(cfg, file, indent=4)

            db = conector.DatabaseConnector()
            logger.debug("Iniciando classe Usina")
            try:
                usina = usina.Usina(cfg, db)
                usina.ler_valores()
                usina.normalizar_emergencia()
                usina.aguardando_reservatorio = 0

            except Exception as e:
                logger.error(f"Erro ao iniciar Classe Usina. Tentando novamente em {timeout}s (tentativa {n_tentativa}/2). Exception: {repr(e)}.")
                logger.debug(f"Traceback: {traceback.format_exc()}")
                sleep(timeout)
                continue

            try:
                prox_estado = Pronto

            except TypeError as e:
                logger.error(f"Erro ao iniciar abstração da usina. Tentando novamente em {timeout}s (tentativa {n_tentativa}/2). Exception: {repr(e)}.")
                logger.error(f"Traceback: {traceback.format_exc()}")
                sleep(timeout)

            except ConnectionError as e:
                logger.error(f"Erro ao iniciar Modbus MOA. Tentando novamente em {timeout}s (tentativa {n_tentativa}/2). Exception: {repr(e)}.")
                logger.error(f"Traceback: {traceback.format_exc()}")
                sleep(timeout)

            except PermissionError as e:
                logger.error(f"Não foi possível iniciar o Modbus MOA devido a permissão do usuário. Exception: {repr(e)}.")
                logger.error(f"Traceback: {traceback.format_exc()}")
                prox_estado = FalhaCritica

            except Exception as e:
                logger.error(f"Erro Inesperado. Tentando novamente em {timeout}s (tentativa{n_tentativa}/2). Exception: {repr(e)}.")
                logger.error(f"Traceback: {traceback.format_exc()}")
                sleep(timeout)

    logger.info("Inicialização completa, executando o MOA \U0001F916")

    threading.Thread(target=lambda: leitura_temporizada(1800)).start()

    sm = StateMachine(initial_state=prox_estado(usina))

    while True:
        logger.debug(f"Executando estado: {sm.state.__class__.__name__}")
        t_i = time.time()
        sm.exec()
        t_restante = max(30 - (time.time() - t_i), 0) / ESCALA_DE_TEMPO
        if t_restante == 0:
            print("ATENÇÃO!\nCiclo está demorando mais que o permitido\nATENÇÃO!")
        sleep(t_restante)
