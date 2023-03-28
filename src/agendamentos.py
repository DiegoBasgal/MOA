__version__ = "0.2"
__author__ = "Diego Basgal"
__credits__ = ["Lucas Lavratti" , ...]
__description__ = "Este módulo corresponde a implementação de Agendamentos da Interface WEB."


import logging

from time import sleep
from datetime import timedelta

from usina import *

logger = logging.getLogger("__main__")

class Agendamentos(Usina):
    def __init__(self):
        super().__init__(self)

    def verificar_agendamentos(self) -> bool:
        agora = self.get_time()
        agendamentos = self.agendamentos_pendentes()

        if agendamentos is None:
            return False
        else:
            i = len(agendamentos)

        logger.debug(f"[AGN] Data: {agendamentos[i-1][1].strftime('%Y-%m-%d %H:%M:%S')}")
        logger.debug(f"      Criado por: {agendamentos[i-1][6]}")
        logger.debug(f"      Comando: {AGN_STR_DICT[agendamentos[i-1][3]] if agendamentos[i-1][3] in AGN_STR_DICT else 'Inexistente'}")

        self.agendamentos_iguais(agendamentos)

        for agendamento in agendamentos:
            self.segundos_passados = (agora - agendamento[1]).seconds if agora > agendamento[1] else 0
            self.segundos_adiantados = (agendamento[1] - agora).seconds if agora < agendamento[1] else 0

            if self.agendamentos_atrasados(agendamento):
                return False

            if self.segundos_adiantados <= 60 and not bool(agendamento[4]):
                logger.info(f"[AGN] Executando agendamento: {agendamento[0]} - Comando: {agendamento[3]} - Data: {agendamento[9]}.")

                self.agendamentos_sem_efeito(agendamento)

                if not self.agendamentos_usina(agendamento):
                    return False

                for ug in self.ugs:
                    if not self.agendamentos_ugs(agendamento, ug):
                        return False

                self.bd.update_agendamento(int(agendamento[0]), 1)
                logger.info(f"[AGN] O agendamento: {AGN_STR_DICT[agendamentos[i-1][3]] if agendamentos[i-1][3] in AGN_STR_DICT else 'Inexistente'} - {agendamento[5]} foi executado.")

    def agendamentos_pendentes(self) -> list:
        try:
            pendentes = []
            agendamentos = self.bd.get_agendamentos_pendentes()

            for agendamento in agendamentos:
                ag = list(agendamento)
                ag[1] = ag[1] - timedelta(0, 60 * 60 * 3)
                pendentes.append(ag)

            return pendentes

        except Exception as e:
            logger.exception(f"[AGN] Não foi possível extrair lista de agendamentos pendentes do banco. Exception: \"{repr(e)}\"")
            logger.exception(f"[AGN] Traceback: {traceback.print_stack}")
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
                self.bd.update_agendamento(ag_concatenado[0], True, obs="Este agendamento foi concatenado ao seguinte por motivos de temporização.")
                i -= 1
            i += 1
            j = len(agendamentos)

    def agendamentos_atrasados(self, agendamento) -> bool:
        agn_atrasados = 0

        if self.segundos_passados > 240:
            logger.warning(f"[AGN] Agendamento: {agendamento[0]} atrasado! ({agendamento[3]}).")
            agn_atrasados += 1

        if self.segundos_passados > 300 or agn_atrasados > 3:
            logger.info("[AGN] Os agendamentos estão muito atrasados!")
            if agendamento[3] == AGN_INDISPONIBILIZAR:
                logger.warning("[AGN] Acionando emergência!")
                self.acionar_emergencia()
                self.bd.update_agendamento(int(agendamento[0]), 1, obs="AGENDAMENTO EXECUTADO POR TRATATIVA DE CÓDIGO!")
                agn_atrasados += 1

            if agendamento[3] == AGN_ALTERAR_NV_ALVO or AGN_ALTERAR_POT_LIMITE_TODAS_AS_UGS or AGN_BAIXAR_POT_UGS_MINIMO or AGN_NORMALIZAR_POT_UGS_MINIMO or AGN_AGUARDAR_RESERVATORIO or AGN_NORMALIZAR_ESPERA_RESERVATORIO:
                logger.info("[AGN] Não foi possível executar o agendamento! Favor re-agendar")
                self.bd.update_agendamento(int(agendamento[0]), 1, obs="AGENDAMENTO NÃO EXECUTADO POR CONTA DE ATRASO!")
                agn_atrasados += 1

            for ug in self.ugs:
                if agendamento[3] in AGN_LST_BLOQUEIO_UG:
                    logger.info(f"[AGN] Indisponibilizando UG{ug.id}")
                    ug.forcar_estado_indisponivel()
                    self.bd.update_agendamento(int(agendamento[0]), 1, obs="AGENDAMENTO NÃO EXECUTADO POR CONTA DE ATRASO!")
                    agn_atrasados += 1

        return True if agn_atrasados > 1 else False

    def agendamentos_sem_efeito(self, agendamento) -> None:
        if self.modo_autonomo and not self.bd.get_executabilidade(agendamento[3])["executavel_em_automatico"]:
            self.bd.update_agendamento(agendamento[0], True, obs="Este agendamento não tem efeito com o módulo em modo autônomo. Executado sem realizar nenhuma ação")

        if not self.modo_autonomo and not self.bd.get_executabilidade(agendamento[3])["executavel_em_manual"]:
            self.bd.update_agendamento(agendamento[0], True, obs="Este agendamento não tem efeito com o módulo em modo manual. Executado sem realizar nenhuma ação")

    def agendamentos_usina(self, agendamento) -> bool:
        if agendamento[3] == AGN_INDISPONIBILIZAR:
            try:
                logger.info("[AGN] Indisponibilizando a usina via agendamento.")
                for ug in self.ugs: 
                    ug.forcar_estado_indisponivel()

                while (not self.ug1.etapa_atual == UG_PARADA and not self.ug2.etapa_atual == UG_PARADA):
                    self.ler_valores()
                    logger.debug("[AGN] Indisponibilizando Usina...")
                    sleep(10)
                self.acionar_emergencia()
                logger.debug("[AGN] Emergência pressionada após indizponibilização agendada mudando para modo manual para evitar normalização automática.")
                self.modo_autonomo = False

            except Exception as e:
                logger.exception(f"[AGN] Houve um erro ao excutar o agendamento de indisponibilização da usina. Exception: \"{repr(e)}\"")
                logger.exception(f"[AGN] Traceback: {traceback.print_stack}")
                return False

        if agendamento[3] == AGN_ALTERAR_NV_ALVO:
            try:
                novo = float(agendamento[5].replace(",", "."))
                self.cfg["nv_alvo"] = novo

            except Exception:
                logger.exception(f"[AGN] Valor inválido no agendamento: {agendamento[0]} ({agendamento[3]} é inválido).")
                return False

        if agendamento[3] == AGN_BAIXAR_POT_UGS_MINIMO:
            try:
                for ug in self.ugs:
                    self.cfg[f"pot_maxima_ug{ug.id}"] = self.cfg["pot_minima"]
                    if ug.etapa_atual == UG_PARADA:
                        logger.debug(f"[AGN] A UG{ug.id} já está no estado parada/parando.")
                    else:
                        logger.debug(f"[AGN] Enviando o setpoint mínimo ({self.cfg['pot_minima']}) para a UG{ug.id}")
                        ug.enviar_setpoint(self.cfg["pot_minima"])

            except Exception as e:
                logger.exception(f"[AGN] Houve um erro ao atribuir a potência mínima das UGs. Exception: \"{repr(e)}\"")
                logger.exception(f"[AGN] Traceback: {traceback.print_stack}")
                return False

        if agendamento[3] == AGN_NORMALIZAR_POT_UGS_MINIMO:
            try:
                for ug in self.ugs:
                    self.cfg[f"pot_maxima_ug{ug.id}"] = self.cfg["pot_maxima_ug"]
                    ug.enviar_setpoint(self.cfg["pot_maxima_ug"])

            except Exception as e:
                logger.debug(f"[AGN] Houve um erro ao executar o agendamento de normalizar a potência das UGs. Exception: \"{repr(e)}\"")
                logger.exception(f"[AGN] Traceback: {traceback.print_stack}")
                return False

        if agendamento[3] == AGN_AGUARDAR_RESERVATORIO:
            try:
                logger.debug("[AGN] Ativando estado de espera de nível do reservatório")
                self.aguardando_reservatorio = 1

            except Exception as e:
                logger.exception(f"[AGN] Houve um erro ao executar o agendamento de aguardar o reservatório. Exception: \"{repr(e)}\"")
                logger.exception(f"[AGN] Traceback: {traceback.print_stack}")
                return False

        if agendamento[3] == AGN_NORMALIZAR_ESPERA_RESERVATORIO:
            try:
                logger.debug("[AGN] Desativando estado de espera de nível do reservatório")
                self.aguardando_reservatorio = 0

            except Exception as e:
                logger.exception(f"[AGN] Houve um erro ao executar o agendamento de normalizar espera do reservatório. Exception: \"{repr(e)}\"")
                logger.exception(f"[AGN] Traceback: {traceback.print_stack}")
                return False

        if agendamento[3] == AGN_ALTERAR_POT_LIMITE_TODAS_AS_UGS:
            try:
                novo = float(agendamento[5].replace(",", "."))
                for ug in self.ugs:
                    self.cfg[f"pot_maxima_ug{ug.id}"] = novo
            except Exception:
                logger.exception(f"[AGN] Valor inválido no agendamento: {agendamento[0]} ({agendamento[3]} é inválido)")
                return False

        return True

    def agendamentos_ugs(self, agendamento, ug: UnidadeGeracao) -> bool:
        if agendamento[3] == AGN_UG_ALTERAR_POT_LIMITE[ug.id]:
            try:
                novo = float(agendamento[5].replace(",", "."))
                self.cfg["pot_maxima_ug1"] = novo

            except Exception:
                logger.exception(f"[AGN] Valor inválido no agendamento: {agendamento[0]} ({agendamento[3]} é inválido)")
                return False

        try:
            if agendamento[3] == AGN_UG_FORCAR_ESTADO_MANUAL[ug.id]:
                ug.forcar_estado_manual()

            if agendamento[3] == AGN_UG_FORCAR_ESTADO_DISPONIVEL[ug.id]:
                ug.forcar_estado_disponivel()

            if agendamento[3] == AGN_UG_FORCAR_ESTADO_INDISPONIVEL[ug.id]:
                ug.forcar_estado_indisponivel()

            if agendamento[3] == AGN_UG_FORCAR_ESTADO_RESTRITO[ug.id]:
                ug.forcar_estado_restrito()

        except Exception as e:
            logger.exception(f"[AGN] Houve um erro ao executar o agendamento de forçar estado da UG. Exception: \"{repr(e)}\"")
            logger.exception(f"[AGN] Traceback: {traceback.print_stack}")
            return False

        if agendamento[3] == AGN_UG_TEMPO_ESPERA_RESTRITO[ug.id]:
            try:
                ug.norma_agendada = True
                novo = agendamento[5].split(":")
                tempo = (int(novo[0]) * 3600) + (int(novo[1]) * 60)
                ug.tempo_normalizar = tempo

            except Exception:
                logger.exception(f"[AGN] Valor inválido no agendamento: {agendamento[0]} ({agendamento[3]} é inválido)")
                return False