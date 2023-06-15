import pytz
import logging

from src.usina import *

from time import sleep
from datetime import datetime, timedelta

from src.dicionarios.const import *

from src.banco_dados import BancoDados


logger = logging.getLogger("__main__")

class Agendamentos:
    def __init__(self, cfg=None, db: BancoDados=None, usina=None):

        self.db = db
        self.cfg = cfg
        self.usn = usina

        self.segundos_passados = 0
        self.segundos_adiantados = 0

    def verificar_agendamentos_pendentes(self) -> list:
        pendentes = []
        try:
            agendamentos = self.db.get_agendamentos_pendentes()

        except Exception:
            logger.error(f"[AGN] Não foi possível extrair lista de agendamentos pendentes do banco.")
            return None

        else:
            for agendamento in agendamentos:
                ag = list(agendamento)
                ag[1] = ag[1] - timedelta(0, 60 * 60 * 3)
                pendentes.append(ag)

            return pendentes

    def verificar_agendamentos_iguais(self, agendamentos) -> None:
        limite_entre_agendamentos_iguais = 300
        agendamentos = sorted(agendamentos, key=lambda x:(x[3], x[1]))

        while (i := 0) < (j := len(agendamentos) - 1):
            if agendamentos[i][3] == agendamentos[i+1][3] and (agendamentos[i+1][1] - agendamentos[i][1]).seconds < limite_entre_agendamentos_iguais:
                ag_concatenado = agendamentos.pop(i)
                logger.info("[AGN] O agendamento foi ignorado, pois o mesmo foi agendado à menos de 5 minutos atrás.")
                self.db.update_agendamento(ag_concatenado[0], True, obs="Este agendamento foi concatenado ao seguinte por motivos de temporização.")
                i -= 1
            i += 1

    def verificar_agendamentos(self) -> bool:
        agora = datetime.now(pytz.timezone("Brazil/East")).replace(tzinfo=None)
        agendamentos = self.db.get_agendamentos_pendentes()

        if agendamentos is None:
            return False
        else:
            i = len(agendamentos)

        self.verificar_agendamentos_iguais(agendamentos)

        for agendamento in agendamentos:
            self.segundos_passados = (agora - agendamento[1]).seconds if agora > agendamento[1] else 0
            self.segundos_adiantados = (agendamento[1] - agora).seconds if agora < agendamento[1] else 0

            logger.debug(f"[AGN] Data: {agendamento[1].strftime('%Y-%m-%d %H:%M:%S')}")
            logger.debug(f"      Criado por: {agendamento[6]}")
            logger.debug(f"      Comando: {AGN_STR_DICT[agendamento[3]] if agendamento[3] in AGN_STR_DICT else 'Inexistente'}")

            if self.verificar_agendamentos_atrasados(agendamento):
                return False

            if self.segundos_adiantados <= 60 and not bool(agendamento[4]):
                logger.info(f"[AGN] Executando agendamento: {agendamento[0]} - Comando: {agendamento[3]} - Data: {agendamento[9]}.")

                self.verificar_agendamentos_sem_efeito(agendamento)

                if not self.verificar_agendamentos_usina(agendamento):
                    return False

                if not self.verificar_agendamentos_ugs(agendamento):
                    return False

                self.db.update_agendamento(agendamento[0], executado=1)
                logger.info(f"[AGN] O agendamento: {AGN_STR_DICT[agendamentos[i-1][3]] if agendamentos[i-1][3] in AGN_STR_DICT else 'Inexistente'} - {agendamento[5]} foi executado.")

    def verificar_agendamentos_atrasados(self, agendamento) -> bool:
        agn_atrasados = 0

        if self.segundos_passados > 240:
            logger.warning(f"[AGN] Agendamento: {agendamento[0]} atrasado! ({agendamento[3]}).")
            agn_atrasados += 1

        if self.segundos_passados > 300 or agn_atrasados > 3:
            logger.info("[AGN] Os agendamentos estão muito atrasados!")
            if agendamento[3] == AGN_INDISPONIBILIZAR:
                logger.warning("[AGN] Acionando emergência!")
                self.usn.acionar_emergencia()
                self.db.update_agendamento(int(agendamento[0]), 1, obs="AGENDAMENTO EXECUTADO POR TRATATIVA DE CÓDIGO!")
                agn_atrasados += 1

            if agendamento[3] in (AGN_ALTERAR_NV_ALVO, AGN_ALTERAR_POT_LIMITE_TODAS_AS_UGS, AGN_BAIXAR_POT_UGS_MINIMO, AGN_NORMALIZAR_POT_UGS_MINIMO, AGN_AGUARDAR_RESERVATORIO, AGN_NORMALIZAR_ESPERA_RESERVATORIO):
                logger.info("[AGN] Não foi possível executar o agendamento! Favor re-agendar")
                self.db.update_agendamento(int(agendamento[0]), 1, obs="AGENDAMENTO NÃO EXECUTADO POR CONTA DE ATRASO!")
                agn_atrasados += 1

            for ug in self.usn.ugs:
                if agendamento[3] in AGN_LST_BLOQUEIO_UG:
                    logger.info(f"[AGN] Indisponibilizando UG{ug.id}")
                    ug.forcar_estado_indisponivel()
                    self.db.update_agendamento(int(agendamento[0]), 1, obs="AGENDAMENTO NÃO EXECUTADO POR CONTA DE ATRASO!")
                    agn_atrasados += 1

        return True if agn_atrasados > 1 else False

    def verificar_agendamentos_sem_efeito(self, agendamento) -> None:
        if self.usn.modo_autonomo and not self.db.get_executabilidade(agendamento[3])["executavel_em_automatico"]:
            self.db.update_agendamento(agendamento[0], True, obs="Este agendamento não tem efeito com o módulo em modo autônomo. Executado sem realizar nenhuma ação")

        if not self.usn.modo_autonomo and not self.db.get_executabilidade(agendamento[3])["executavel_em_manual"]:
            self.db.update_agendamento(agendamento[0], True, obs="Este agendamento não tem efeito com o módulo em modo manual. Executado sem realizar nenhuma ação")

    def verificar_agendamentos_usina(self, agendamento) -> bool:
        if agendamento[3] == AGN_INDISPONIBILIZAR:
            logger.info("[AGN] Indisponibilizando a usina via agendamento.")
            for ug in self.usn.ugs:
                ug.forcar_estado_indisponivel()

            while (not self.usn.ug1.etapa_atual == UG_PARADA and not self.usn.ug2.etapa_atual == UG_PARADA):
                self.usn.ler_valores()
                logger.debug("[AGN] Indisponibilizando Usina...")
                sleep(10)

            self.usn.acionar_emergencia()
            logger.debug("[AGN] Emergência pressionada após indizponibilização agendada mudando para modo manual para evitar normalização automática.")
            self.usn.modo_autonomo = False
            return True

        if agendamento[3] == AGN_ALTERAR_NV_ALVO:
            try:
                novo = float(agendamento[5].replace(",", "."))
                self.cfg["nv_alvo"] = novo
                return True

            except Exception:
                logger.error(f"[AGN] Valor inválido no agendamento: {agendamento[0]} ({agendamento[3]} é inválido).")
                return False

        if agendamento[3] == AGN_BAIXAR_POT_UGS_MINIMO:
            for ug in self.usn.ugs:
                self.cfg[f"pot_maxima_ug{ug.id}"] = self.cfg["pot_minima"]
                if ug.etapa == UG_PARADA:
                    logger.debug(f"[AGN] A UG{ug.id} já está no estado parada/parando.")
                else:
                    logger.debug(f"[AGN] Enviando o setpoint mínimo ({self.cfg['pot_minima']}) para a UG{ug.id}")
                    ug.enviar_setpoint(self.cfg["pot_minima"])
            return True

        if agendamento[3] == AGN_NORMALIZAR_POT_UGS_MINIMO:
            for ug in self.usn.ugs:
                self.cfg[f"pot_maxima_ug{ug.id}"] = self.cfg["pot_maxima_ug"]
                ug.enviar_setpoint(self.cfg["pot_maxima_ug"])
            return True

        if agendamento[3] == AGN_AGUARDAR_RESERVATORIO:
            logger.debug("[AGN] Ativando estado de espera de nível do reservatório")
            self.aguardando_reservatorio = 1
            return True

        if agendamento[3] == AGN_NORMALIZAR_ESPERA_RESERVATORIO:
            logger.debug("[AGN] Desativando estado de espera de nível do reservatório")
            self.aguardando_reservatorio = 0
            return True

        if agendamento[3] == AGN_ALTERAR_POT_LIMITE_TODAS_AS_UGS:
            try:
                novo = float(agendamento[5].replace(",", "."))
                for ug in self.usn.ugs:
                    self.cfg[f"pot_maxima_ug{ug.id}"] = novo
                    return True

            except Exception:
                logger.error(f"[AGN] Valor inválido no agendamento: {agendamento[0]} ({agendamento[3]} é inválido)")
                return False

        return True

    def verificar_agendamentos_ugs(self, agendamento) -> bool:
        if agendamento[3] == AGN_UG1_ALTERAR_POT_LIMITE:
            try:
                novo = float(agendamento[5].replace(",", "."))
                self.cfg[f"pot_maxima_ug1"] = novo
                return True

            except Exception:
                logger.error(f"[AGN] Valor inválido no agendamento: {agendamento[0]} ({agendamento[3]} é inválido)")
                return False

        if agendamento[3] == AGN_UG1_FORCAR_ESTADO_MANUAL:
            self.usn.ug1.forcar_estado_manual()
            return True

        if agendamento[3] == AGN_UG1_FORCAR_ESTADO_DISPONIVEL:
            self.usn.ug1.forcar_estado_disponivel()
            return True

        if agendamento[3] == AGN_UG1_FORCAR_ESTADO_INDISPONIVEL:
            self.usn.ug1.forcar_estado_indisponivel()
            return True

        if agendamento[3] == AGN_UG1_FORCAR_ESTADO_RESTRITO:
            self.usn.ug1.forcar_estado_restrito()
            return True

        if agendamento[3] == AGN_UG1_TEMPO_ESPERA_RESTRITO:
            try:
                self.usn.ug1.normalizacao_agendada = True
                novo = agendamento[5].split(":")
                tempo = (int(novo[0]) * 3600) + (int(novo[1]) * 60)
                self.usn.ug1.tempo_normalizar = tempo
                return True

            except Exception:
                logger.error(f"[AGN] Valor inválido no agendamento: {agendamento[0]} ({agendamento[3]} é inválido)")
                return False

        if agendamento[3] == AGN_UG2_ALTERAR_POT_LIMITE:
            try:
                novo = float(agendamento[5].replace(",", "."))
                self.cfg[f"pot_maxima_ug2"] = novo
                return True

            except Exception:
                logger.error(f"[AGN] Valor inválido no agendamento: {agendamento[0]} ({agendamento[3]} é inválido)")
                return False

        if agendamento[3] == AGN_UG2_FORCAR_ESTADO_MANUAL:
            self.usn.ug2.forcar_estado_manual()
            return True

        if agendamento[3] == AGN_UG2_FORCAR_ESTADO_DISPONIVEL:
            self.usn.ug2.forcar_estado_disponivel()
            return True

        if agendamento[3] == AGN_UG2_FORCAR_ESTADO_INDISPONIVEL:
            self.usn.ug2.forcar_estado_indisponivel()
            return True

        if agendamento[3] == AGN_UG2_FORCAR_ESTADO_RESTRITO:
            self.usn.ug2.forcar_estado_restrito()
            return True

        if agendamento[3] == AGN_UG2_TEMPO_ESPERA_RESTRITO:
            try:
                self.usn.ug2.normalizacao_agendada = True
                novo = agendamento[5].split(":")
                tempo = (int(novo[0]) * 3600) + (int(novo[1]) * 60)
                self.usn.ug2.tempo_normalizar = tempo
                return True

            except Exception:
                logger.error(f"[AGN] Valor inválido no agendamento: {agendamento[0]} ({agendamento[3]} é inválido)")
                return False