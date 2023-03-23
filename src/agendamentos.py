import logging
import pytz

from time import sleep
from datetime import datetime, timedelta

from dicionarios.const import *

from usina import Usina
from banco_dados import BancoDados
from unidade_geracao import UnidadeGeracao

logger = logging.getLogger("__main__")

class Agendamentos:
    def __init__(
            self,
            config: dict | None = ...,
            usina: Usina | None = ...
        ) -> ...:

        if not config:
            logger.warning("[AGN] Não foi possível carregar os arquivos de configuração (\"cfg.json\") e(ou) dicionário compartilhado (\"shared_dict\").")
            raise ValueError
        else:
            self.cfg = config

        if not usina:
            logger.warning("[AGN] Não foi possível carregar a instância da Usina.")
            raise ImportError
        else:
            self.usn = usina

        self.db = usina.db
        ugs = self.usn.lista_ugs
        self.ug1 = ugs[0]
        self.ug1 = ugs[1]

    def 

    def get_agendamentos_pendentes(self):
            agendamentos_pendentes = []
            agendamentos = self.db.get_agendamentos_pendentes()

            for agendamento in agendamentos:
                ag = list(agendamento)
                ag[1] = ag[1] - timedelta(0, 60 * 60 * 3)
                agendamentos_pendentes.append(ag)
            return agendamentos_pendentes

    def verificar_agendamentos(self):
        agora = datetime.now(pytz.timezone("Brazil/East")).replace(tzinfo=None)
        agendamentos = self.get_agendamentos_pendentes()

        limite_entre_agendamentos_iguais = 300
        agendamentos = sorted(agendamentos, key=lambda x:(x[3], x[1]))
        i = 0
        j = len(agendamentos)
        while i < j - 1:

            if agendamentos[i][3] == agendamentos[i+1][3] and (agendamentos[i+1][1] - agendamentos[i][1]).seconds < limite_entre_agendamentos_iguais:
                ag_concatenado = agendamentos.pop(i)
                obs = "Este agendamento foi concatenado ao seguinte por motivos de temporização."
                logger.warning(obs)
                self.db.update_agendamento(ag_concatenado[0], True, obs)
                i -= 1

            i += 1
            j = len(agendamentos)

        i = len(agendamentos)
        logger.debug("Data: {}  Criado por: {}  Comando: {}".format(agendamentos[i-1][1].strftime("%Y-%m-%d %H:%M:%S"), agendamentos[i-1][6], agendamentos[i-1][3]))

        if len(agendamentos) == 0:
            return True

        self.agendamentos_atrasados = 0

        for agendamento in agendamentos:
            if agora > agendamento[1]:
                segundos_adiantados = 0
                segundos_passados = (agora - agendamento[1]).seconds
                logger.debug(segundos_passados)
            else:
                segundos_adiantados = (agendamento[1] - agora).seconds
                segundos_passados = 0


            if segundos_passados > 240:
                logger.warning("Agendamento #{} Atrasado! ({}).".format(agendamento[0], agendamento[3]))
                self.agendamentos_atrasados += 1

            if segundos_passados > 5 or self.agendamentos_atrasados > 3:
                logger.info("Os agendamentos estão muito atrasados!")
                if agendamento[3] == AGN_INDISPONIBILIZAR:
                    logger.warning("Acionando emergência!")
                    self.acionar_emergencia()
                    self.db.update_agendamento(int(agendamento[0]), 1, obs="AGENDAMENTO NÃO EXECUTADO POR CONTA DE ATRASO!")
                    return False
                elif agendamento[3] == AGN_ALTERAR_NV_ALVO or agendamento[3] == AGN_ALTERAR_POT_LIMITE_TODAS_AS_UGS or agendamento[3] == AGN_BAIXAR_POT_UGS_MINIMO or agendamento[3] == AGN_NORMALIZAR_POT_UGS_MINIMO:
                    logger.info("Não foi possível executar o agendamento! Favor re-agendar")
                    self.db.update_agendamento(int(agendamento[0]), 1, obs="AGENDAMENTO NÃO EXECUTADO POR CONTA DE ATRASO!")
                    return False
                elif agendamento[3] in AGN_LST_BLOQUEIO_UG1:
                    logger.info("Indisponibilizando UG1")
                    self.ug1.forcar_estado_indisponivel()
                    self.db.update_agendamento(int(agendamento[0]), 1, obs="AGENDAMENTO NÃO EXECUTADO POR CONTA DE ATRASO!")
                    return False
                elif agendamento[3] in AGN_LST_BLOQUEIO_UG2:
                    logger.info("Indisponibilizando UG2")
                    self.ug2.forcar_estado_indisponivel()
                    self.db.update_agendamento(int(agendamento[0]), 1, obs="AGENDAMENTO NÃO EXECUTADO POR CONTA DE ATRASO!")
                    return False
                else:
                    logger.info("Agendamento não encontrado! Retomando operação...")
                    self.db.update_agendamento(int(agendamento[0]), 1, obs="Agendamento inexistente.")
                    return False


            if segundos_adiantados <= 60 and not bool(agendamento[4]):
                logger.info("Executando gendamento: {} - Comando: {} - Data: .".format(agendamento[0], agendamento[3], agendamento[9]))

                if (self.modo_autonomo and not self.db.get_executabilidade(agendamento[3])["executavel_em_autmoatico"]):
                    obs = "Este agendamento não tem efeito com o módulo em modo autônomo. Executado sem realizar nenhuma ação"
                    logger.warning(obs)
                    self.db.update_agendamento(agendamento[0], True, obs)
                    return True

                if (not self.modo_autonomo and not self.db.get_executabilidade(agendamento[3])["executavel_em_manual"]):
                    obs = "Este agendamento não tem efeito com o módulo em modo manual. Executado sem realizar nenhuma ação"
                    logger.warning(obs)
                    self.db.update_agendamento(agendamento[0], True, obs)
                    return True

                if agendamento[3] == AGN_INDISPONIBILIZAR:
                    logger.info("Indisponibilizando a usina (comando via agendamento).")
                    for ug in self.ugs:
                        ug.forcar_estado_indisponivel()
                    while (not self.ugs[0].etapa_atual == UG_PARADA and not self.ugs[1].etapa_atual == UG_PARADA):
                        self.ler_valores()
                        logger.debug("Indisponibilizando Usina... \n(freezing for 10 seconds)")
                        sleep(10)
                    self.acionar_emergencia()
                    logger.debug("Emergência pressionada após indizponibilização agendada mudando para modo manual para evitar normalização automática.")
                    self.entrar_em_modo_manual()

                if agendamento[3] == AGN_ALTERAR_NV_ALVO:
                    try:
                        novo = float(agendamento[5].replace(",", "."))
                    except Exception as e:
                        logger.info("Valor inválido no comando #{} ({} é inválido).".format(agendamento[0], agendamento[3]))

                    self.cfg["nv_alvo"] = novo

                if agendamento[3] == AGN_BAIXAR_POT_UGS_MINIMO:
                    try:
                        self.cfg["pot_maxima_ug1"] = self.cfg["pot_minima"]
                        self.cfg["pot_maxima_ug2"] = self.cfg["pot_minima"]
                        for ug in self.ugs:
                            if ug.etapa_atual == UG_PARADA or ug.etapa_alvo == UG_PARADA:
                                logger.debug("A UG{} já está no estado parada/parando.".format(ug.id))
                            else:
                                logger.debug("Enviando o setpoint mínimo ({}) para a UG{}".format(self.cfg["pot_minima"], ug.id))
                                ug.enviar_setpoint(self.cfg["pot_minima"])

                    except Exception as e:
                        logger.info("Traceback: {}".format(repr(e)))

                if agendamento[3] == AGN_NORMALIZAR_POT_UGS_MINIMO:
                    try:
                        self.cfg["pot_maxima_ug1"] = self.cfg["pot_maxima_ug"]
                        self.cfg["pot_maxima_ug2"] = self.cfg["pot_maxima_ug"]
                        for ug in self.ugs:
                            ug.enviar_setpoint(self.cfg["pot_maxima_ug"])

                    except Exception as e:
                        logger.debug("Traceback: {}".format(repr(e)))

                if agendamento[3] == AGN_UG1_ALTERAR_POT_LIMITE:
                    try:
                        novo = float(agendamento[5].replace(",", "."))
                        self.cfg["pot_maxima_ug1"] = novo
                        self.ug1.pot_disponivel = novo
                    except Exception as e:
                        logger.info("Valor inválido no comando #{} ({} é inválido).".format(agendamento[0], agendamento[3]))

                if agendamento[3] == AGN_UG1_FORCAR_ESTADO_MANUAL:
                    self.ug1.forcar_estado_manual()

                if agendamento[3] == AGN_UG1_FORCAR_ESTADO_DISPONIVEL:
                    self.ug1.forcar_estado_disponivel()

                if agendamento[3] == AGN_UG1_FORCAR_ESTADO_INDISPONIVEL:
                    self.ug1.forcar_estado_indisponivel()

                if agendamento[3] == AGN_UG1_FORCAR_ESTADO_RESTRITO:
                    self.ug1.forcar_estado_restrito()

                if agendamento[3] == AGN_UG2_ALTERAR_POT_LIMITE:
                    try:
                        novo = float(agendamento[5].replace(",", "."))
                        self.cfg["pot_maxima_ug2"] = novo
                        self.ug2.pot_disponivel = novo
                    except Exception as e:
                        logger.info("Valor inválido no comando #{} ({} é inválido).".format(agendamento[0], agendamento[3]))

                if agendamento[3] == AGN_UG2_FORCAR_ESTADO_MANUAL:
                    self.ug2.forcar_estado_manual()

                if agendamento[3] == AGN_UG2_FORCAR_ESTADO_DISPONIVEL:
                    self.ug2.forcar_estado_disponivel()

                if agendamento[3] == AGN_UG2_FORCAR_ESTADO_INDISPONIVEL:
                    self.ug2.forcar_estado_indisponivel()

                if agendamento[3] == AGN_UG2_FORCAR_ESTADO_RESTRITO:
                    self.ug2.forcar_estado_restrito()

                if agendamento[3] == AGN_ALTERAR_POT_LIMITE_TODAS_AS_UGS:
                    try:
                        novo = float(agendamento[5].replace(",", "."))
                        self.cfg["pot_maxima_ug1"] = novo
                        self.ug1.pot_disponivel = novo
                        self.cfg["pot_maxima_ug2"] = novo
                        self.ug2.pot_disponivel = novo
                    except Exception as e:
                        logger.info("Valor inválido no comando #{} ({} é inválido).".format(agendamento[0], agendamento[3]))

                self.db.update_agendamento(int(agendamento[0]), 1)
                logger.info("O comando #{} - {} foi executado.".format(agendamento[0], agendamento[5]))
                self.con.reconhecer_emergencia()
                self.escrever_valores()