import pytz
import logging

from datetime import datetime, timedelta

from src.usina import *
from src.conector import *

logger = logging.getLogger("__main__")

class Agendamentos:
    def __init__(self) -> None:
        self.agn_atrasados = 0
        self.segundos_passados = 0
        self.segundos_adiantados = 0

        self.db = DatabaseConnector()

        self.ugs = Usina.get_ugs
        self.ug1 = self.ugs[0]
        self.ug2 = self.ugs[1]

        config_file = os.path.join(os.path.dirname(__file__), "cfg.json")
        with open(config_file, "r") as file:
            self.cfg = json.load(file)

    def get_time(self) -> object:
        return datetime.now(pytz.timezone("Brazil/East")).replace(tzinfo=None)

    def verificar_agendamentos(self) -> bool:
        agora = self.get_time()
        agendamentos = self.agendamentos_pendentes()
        if agendamentos is None:
            return False
        else:
            i = len(agendamentos)

        logger.debug(f"[AGN] Data: {agendamentos[i-1][1].strftime('%Y-%m-%d %H:%M:%S')}\nCriado por: {agendamentos[i-1][6]}\nComando: {agendamentos[i-1][3]}")

        self.agendamentos_iguais(agendamentos)

        for agendamento in agendamentos:
            if agora > agendamento[1]:
                self.segundos_adiantados = 0
                self.segundos_passados = (agora - agendamento[1]).seconds
            else:
                self.segundos_adiantados = (agendamento[1] - agora).seconds
                self.segundos_passados = 0

            if self.agendamentos_atrasados(agendamento):
                return False

            if self.segundos_adiantados <= 60 and not bool(agendamento[4]):
                logger.info(f"[AGN] Executando gendamento: {agendamento[0]} - Comando: {agendamento[3]} - Data: {agendamento[9]}.")

                if self.agendamentos_sem_efeito(agendamento):
                    return False

                if not self.agendamentos_usina(agendamento):
                    return False

                if not self.agendamentos_ugs(agendamento):
                    return False

                self.db.update_agendamento(int(agendamento[0]), 1)
                logger.info(f"[AGN] O agendamento: {agendamento[0]} - {agendamento[5]} foi executado.")

    def agendamentos_pendentes(self) -> list:
        try:
            pendentes = []
            agendamentos = self.db.get_agendamentos_pendentes()

            for agendamento in agendamentos:
                ag = list(agendamento)
                ag[1] = ag[1] - timedelta(0, 60 * 60 * 3)
                pendentes.append(ag)

            return pendentes
        except Exception:
            logger.exception(f"[AGN] Não foi possível extrair lista de agendamentos pendentes do banco.\nTraceback: {traceback.print_stack}")
            return None

    def agendamentos_iguais(self, agendamentos) -> None:
        limite_entre_agendamentos_iguais = 300
        agendamentos = sorted(agendamentos, key=lambda x:(x[3], x[1]))
        i = 0
        j = len(agendamentos)
        while i < j - 1:
            if agendamentos[i][3] == agendamentos[i+1][3] and (agendamentos[i+1][1] - agendamentos[i][1]).seconds < limite_entre_agendamentos_iguais:
                ag_concatenado = agendamentos.pop(i)
                logger.info("[AGN] O agendamento foi ignorado, pois o mesmo foi agendado à menos de 5 minutos atrás.")
                self.db.update_agendamento(ag_concatenado[0], True, obs="Este agendamento foi concatenado ao seguinte por motivos de temporização.")
                i -= 1
            i += 1
            j = len(agendamentos)

    def agendamentos_atrasados(self, agendamento) -> bool:
        self.agn_atrasados = 0

        if self.segundos_passados > 240:
            logger.warning(f"[AGN] Agendamento: {agendamento[0]} atrasado! ({agendamento[3]}).")
            self.agn_atrasados += 1

        if self.segundos_passados > 300 or self.agn_atrasados > 3:
            logger.info("[AGN] Os agendamentos estão muito atrasados!")
            if agendamento[3] == AGENDAMENTO_INDISPONIBILIZAR:
                logger.warning("[AGN] Acionando emergência!")
                Usina.acionar_emergencia()
                self.db.update_agendamento(int(agendamento[0]), 1, obs="AGENDAMENTO EXECUTADO POR TRATATIVA DE CÓDIGO!")
                return True

            elif agendamento[3] == AGENDAMENTO_ALTERAR_NV_ALVO or AGENDAMENTO_ALTERAR_POT_LIMITE_TODAS_AS_UGS or AGENDAMENTO_BAIXAR_POT_UGS_MINIMO or AGENDAMENTO_NORMALIZAR_POT_UGS_MINIMO or AGENDAMENTO_AGUARDAR_RESERVATORIO or AGENDAMENTO_NORMALIZAR_ESPERA_RESERVATORIO:
                logger.info("[AGN] Não foi possível executar o agendamento! Favor re-agendar")
                self.db.update_agendamento(int(agendamento[0]), 1, obs="AGENDAMENTO NÃO EXECUTADO POR CONTA DE ATRASO!")
                return True

            elif agendamento[3] in AGENDAMENTO_LISTA_BLOQUEIO_UG1:
                logger.info("[AGN] Indisponibilizando UG1")
                self.ug1.forcar_estado_indisponivel()
                self.db.update_agendamento(int(agendamento[0]), 1, obs="AGENDAMENTO NÃO EXECUTADO POR CONTA DE ATRASO!")
                return True

            elif agendamento[3] in AGENDAMENTO_LISTA_BLOQUEIO_UG2:
                logger.info("[AGN] Indisponibilizando UG2")
                self.ug2.forcar_estado_indisponivel()
                self.db.update_agendamento(int(agendamento[0]), 1, obs="AGENDAMENTO NÃO EXECUTADO POR CONTA DE ATRASO!")
                return True

            else:
                logger.info("[AGN] Agendamento não encontrado! Retomando operação...")
                return True

        return False

    def agendamentos_sem_efeito(self, agendamento) -> bool:
        if Usina.get_modo_autonomo and not self.db.get_executabilidade(agendamento[3])["executavel_em_autmoatico"]:
            self.db.update_agendamento(agendamento[0], True, obs="Este agendamento não tem efeito com o módulo em modo autônomo. Executado sem realizar nenhuma ação")
            return True

        if not Usina.get_modo_autonomo and not self.db.get_executabilidade(agendamento[3])["executavel_em_manual"]:
            self.db.update_agendamento(agendamento[0], True, obs="Este agendamento não tem efeito com o módulo em modo manual. Executado sem realizar nenhuma ação")
            return True

        return False

    def agendamentos_usina(self, agendamento) -> bool:
        if agendamento[3] == AGENDAMENTO_INDISPONIBILIZAR:
            try:
                logger.info("[AGN] Indisponibilizando a usina via agendamento.")
                for ug in self.ugs:
                    ug.forcar_estado_indisponivel()

                while (not self.ug1.etapa_atual == UNIDADE_PARADA and not self.ug2.etapa_atual == UNIDADE_PARADA):
                    Usina.ler_valores()
                    logger.debug("[AGN] Indisponibilizando Usina...")
                    sleep(10)
                Usina.acionar_emergencia()
                logger.debug("[AGN] Emergência pressionada após indizponibilização agendada mudando para modo manual para evitar normalização automática.")
                Usina.entrar_em_modo_manual()
            except Exception:
                logger.exception(f"[AGN] Houve um erro ao excutar o agendamento de indisponibilização da usina.\nTraceback: {traceback.print_stack}")
                return False

        if agendamento[3] == AGENDAMENTO_ALTERAR_NV_ALVO:
            try:
                novo = float(agendamento[5].replace(",", "."))
                self.cfg["nv_alvo"] = novo
            except Exception:
                logger.exception(f"[AGN] Valor inválido no agendamento: {agendamento[0]} ({agendamento[3]} é inválido).")
                return False

        if agendamento[3] == AGENDAMENTO_BAIXAR_POT_UGS_MINIMO:
            try:
                for ug in self.ugs:
                    self.cfg[f"pot_maxima_ug{ug.id}"] = self.cfg["pot_minima"]
                    if ug.etapa_atual == UNIDADE_PARADA or ug.etapa_alvo == UNIDADE_PARADA:
                        logger.debug(f"[AGN] A UG{ug.id} já está no estado parada/parando.")
                    else:
                        logger.debug(f"[AGN] Enviando o setpoint mínimo ({self.cfg['pot_minima']}) para a UG{ug.id}")
                        ug.enviar_setpoint(self.cfg["pot_minima"])

            except Exception as e:
                logger.exception(f"[AGN] Houve um erro ao atribuir a potência mínima das UGs.\nTraceback: {traceback.print_stack}")
                return False

        if agendamento[3] == AGENDAMENTO_NORMALIZAR_POT_UGS_MINIMO:
            try:
                for ug in self.ugs:
                    self.cfg[f"pot_maxima_ug{ug.id}"] = self.cfg["pot_maxima_ug"]
                    ug.enviar_setpoint(self.cfg["pot_maxima_ug"])
            except Exception:
                logger.debug(f"[AGN] Houve um erro ao executar o agendamento de normalizar a potência das UGs.\nTraceback: {traceback.print_stack}")
                return False

        if agendamento[3] == AGENDAMENTO_AGUARDAR_RESERVATORIO:
            try:
                logger.debug("[AGN] Ativando estado de espera de nível do reservatório")
                self.aguardando_reservatorio = 1
            except Exception:
                logger.exception(f"[AGN] Houve um erro ao executar o agendamento de aguardar o resrvatório.\nTraceback: {traceback.print_stack}")
                return False

        if agendamento[3] == AGENDAMENTO_NORMALIZAR_ESPERA_RESERVATORIO:
            try:
                logger.debug("[AGN] Desativando estado de espera de nível do reservatório")
                self.aguardando_reservatorio = 0
            except Exception:
                logger.exception(f"[AGN] Houve um erro ao executar o agendamento de normalizar espera do reservatório.\nTraceback: {traceback.print_stack}")
                return False
        return True

    def agendamentos_ugs(self, agendamento) -> bool:
        if agendamento[3] == AGENDAMENTO_UG1_ALTERAR_POT_LIMITE:
            try:
                novo = float(agendamento[5].replace(",", "."))
                self.cfg["pot_maxima_ug1"] = novo
                self.ug1.pot_disponivel = novo
            except Exception:
                logger.exception(f"[AGN] Valor inválido no agendamento: {agendamento[0]} ({agendamento[3]} é inválido)")
                return False

        try:
            if agendamento[3] == AGENDAMENTO_UG1_FORCAR_ESTADO_MANUAL:
                self.ug1.forcar_estado_manual()

            if agendamento[3] == AGENDAMENTO_UG1_FORCAR_ESTADO_DISPONIVEL:
                self.ug1.forcar_estado_disponivel()

            if agendamento[3] == AGENDAMENTO_UG1_FORCAR_ESTADO_INDISPONIVEL:
                self.ug1.forcar_estado_indisponivel()

            if agendamento[3] == AGENDAMENTO_UG1_FORCAR_ESTADO_RESTRITO:
                self.ug1.forcar_estado_restrito()
        except Exception:
            logger.exception(f"[AGN] Houve um erro ao executar o agendamento de forçar estado da UG.\nTraceback: {traceback.print_stack}")
            return False

        if agendamento[3] == AGENDAMENTO_UG1_TEMPO_ESPERA_RESTRITO:
            try:
                self.ug1.norma_agendada = True
                novo = agendamento[5].split(":")
                tempo = (int(novo[0]) * 3600) + (int(novo[1]) * 60)
                self.ug1.tempo_normalizar = tempo
            except Exception:
                logger.exception(f"[AGN] Valor inválido no agendamento: {agendamento[0]} ({agendamento[3]} é inválido)")
                return False

        if agendamento[3] == AGENDAMENTO_UG2_ALTERAR_POT_LIMITE:
            try:
                novo = float(agendamento[5].replace(",", "."))
                self.cfg["pot_maxima_ug2"] = novo
                self.ug2.pot_disponivel = novo
            except Exception as e:
                logger.exception(f"[AGN] Valor inválido no agendamento: {agendamento[0]} ({agendamento[3]} é inválido)")
                return False

        try:
            if agendamento[3] == AGENDAMENTO_UG2_FORCAR_ESTADO_MANUAL:
                self.ug2.forcar_estado_manual()

            if agendamento[3] == AGENDAMENTO_UG2_FORCAR_ESTADO_DISPONIVEL:
                self.ug2.forcar_estado_disponivel()

            if agendamento[3] == AGENDAMENTO_UG2_FORCAR_ESTADO_INDISPONIVEL:
                self.ug2.forcar_estado_indisponivel()

            if agendamento[3] == AGENDAMENTO_UG2_FORCAR_ESTADO_RESTRITO:
                self.ug2.forcar_estado_restrito()
        except Exception:
            logger.exception(f"[AGN] Houve um erro ao executar o agendamento de tempo de espera para normalização do estado restrito da UG2.\nTraceback: {traceback.print_stack}")
            return False

        if agendamento[3] == AGENDAMENTO_UG2_TEMPO_ESPERA_RESTRITO:
            try:
                self.ug2.norma_agendada = True
                novo = agendamento[5].split(":")
                tempo = (int(novo[0]) * 3600) + (int(novo[1]) * 60)
                self.ug2.tempo_normalizar = tempo
            except Exception:
                logger.exception(f"[AGN] Valor inválido no agendamento: {agendamento[0]} ({agendamento[3]} é inválido)")
                return False

        if agendamento[3] == AGENDAMENTO_ALTERAR_POT_LIMITE_TODAS_AS_UGS:
            try:
                novo = float(agendamento[5].replace(",", "."))
                for ug in self.ugs:
                    self.cfg[f"pot_maxima_ug{ug.id}"] = novo
                    ug.pot_disponivel = novo
            except Exception:
                logger.exception(f"[AGN] Valor inválido no agendamento: {agendamento[0]} ({agendamento[3]} é inválido)")
                return False

        return True