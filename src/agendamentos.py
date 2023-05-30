import pytz
import logging

from time import sleep
from datetime import datetime, timedelta

from src.dicionarios.const import *
from src.banco_dados import BancoDados


logger = logging.getLogger("__main__")

class Agendamentos:

    segundos_passados = 0
    segundos_adiantados = 0

    db = BancoDados("Agendamentos")

    @classmethod
    def verificar_agendamentos_pendentes(cls) -> list:
        pendentes = []
        try:
            agendamentos = cls.db.get_agendamentos_pendentes()
            
        except Exception:
            logger.error(f"[AGN] Não foi possível extrair lista de agendamentos pendentes do banco.")
            return None

        else:
            for agendamento in agendamentos:
                ag = list(agendamento)
                ag[1] = ag[1] - timedelta(0, 60 * 60 * 3)
                pendentes.append(ag)

            return pendentes

    @classmethod
    def verificar_agendamentos_iguais(cls, agendamentos) -> None:
        limite_entre_agendamentos_iguais = 300
        agendamentos = sorted(agendamentos, key=lambda x:(x[3], x[1]))

        while (i := 0) < (j := len(agendamentos) - 1):
            if agendamentos[i][3] == agendamentos[i+1][3] and (agendamentos[i+1][1] - agendamentos[i][1]).seconds < limite_entre_agendamentos_iguais:
                ag_concatenado = agendamentos.pop(i)
                logger.info("[AGN] O agendamento foi ignorado, pois o mesmo foi agendado à menos de 5 minutos atrás.")
                cls.db.update_agendamento(ag_concatenado[0], True, obs="Este agendamento foi concatenado ao seguinte por motivos de temporização.")
                i -= 1
            i += 1

    @classmethod
    def verificar_agendamentos(cls) -> bool:
        agora = datetime.now(pytz.timezone("Brazil/East")).replace(tzinfo=None)
        agendamentos = cls.db.get_agendamentos_pendentes()

        if agendamentos is None:
            return False
        else:
            i = len(agendamentos)

        logger.debug(f"[AGN] Data: {agendamentos[i-1][1].strftime('%Y-%m-%d %H:%M:%S')}")
        logger.debug(f"      Criado por: {agendamentos[i-1][6]}")
        logger.debug(f"      Comando: {AGN_STR_DICT[agendamentos[i-1][3]] if agendamentos[i-1][3] in AGN_STR_DICT else 'Inexistente'}")

        cls.verificar_agendamentos_iguais(agendamentos)

        for agendamento in agendamentos:
            cls.segundos_passados = (agora - agendamento[1]).seconds if agora > agendamento[1] else 0
            cls.segundos_adiantados = (agendamento[1] - agora).seconds if agora < agendamento[1] else 0

            if cls.verificar_agendamentos_atrasados(agendamento):
                return False

            if cls.segundos_adiantados <= 60 and not bool(agendamento[4]):
                logger.info(f"[AGN] Executando agendamento: {agendamento[0]} - Comando: {agendamento[3]} - Data: {agendamento[9]}.")

                cls.verificar_agendamentos_sem_efeito(agendamento)

                if not cls.verificar_agendamentos_usina(agendamento):
                    return False

                for ug in cls.ugs:
                    if not cls.verificar_agendamentos_ugs(agendamento, ug):
                        return False

                cls.db.update_agendamento(int(agendamento[0]), 1)
                logger.info(f"[AGN] O agendamento: {AGN_STR_DICT[agendamentos[i-1][3]] if agendamentos[i-1][3] in AGN_STR_DICT else 'Inexistente'} - {agendamento[5]} foi executado.")

    @classmethod
    def verificar_agendamentos_atrasados(cls, agendamento) -> bool:
        agn_atrasados = 0

        if cls.segundos_passados > 240:
            logger.warning(f"[AGN] Agendamento: {agendamento[0]} atrasado! ({agendamento[3]}).")
            agn_atrasados += 1

        if cls.segundos_passados > 300 or agn_atrasados > 3:
            logger.info("[AGN] Os agendamentos estão muito atrasados!")
            if agendamento[3] == AGN_INDISPONIBILIZAR:
                logger.warning("[AGN] Acionando emergência!")
                cls.acionar_emergencia()
                cls.db.update_agendamento(int(agendamento[0]), 1, obs="AGENDAMENTO EXECUTADO POR TRATATIVA DE CÓDIGO!")
                agn_atrasados += 1

            if agendamento[3] in (AGN_ALTERAR_NV_ALVO, AGN_ALTERAR_POT_LIMITE_TODAS_AS_UGS, AGN_BAIXAR_POT_UGS_MINIMO, AGN_NORMALIZAR_POT_UGS_MINIMO, AGN_AGUARDAR_RESERVATORIO, AGN_NORMALIZAR_ESPERA_RESERVATORIO):
                logger.info("[AGN] Não foi possível executar o agendamento! Favor re-agendar")
                cls.db.update_agendamento(int(agendamento[0]), 1, obs="AGENDAMENTO NÃO EXECUTADO POR CONTA DE ATRASO!")
                agn_atrasados += 1

            for ug in cls.ugs:
                if agendamento[3] in AGN_LST_BLOQUEIO_UG:
                    logger.info(f"[AGN] Indisponibilizando UG{ug.id}")
                    ug.forcar_estado_indisponivel()
                    cls.db.update_agendamento(int(agendamento[0]), 1, obs="AGENDAMENTO NÃO EXECUTADO POR CONTA DE ATRASO!")
                    agn_atrasados += 1

        return True if agn_atrasados > 1 else False

    @classmethod
    def verificar_agendamentos_sem_efeito(cls, agendamento) -> None:
        if cls.modo_autonomo and not cls.db.get_executabilidade(agendamento[3])["executavel_em_automatico"]:
            cls.db.update_agendamento(agendamento[0], True, obs="Este agendamento não tem efeito com o módulo em modo autônomo. Executado sem realizar nenhuma ação")

        if not cls.modo_autonomo and not cls.db.get_executabilidade(agendamento[3])["executavel_em_manual"]:
            cls.db.update_agendamento(agendamento[0], True, obs="Este agendamento não tem efeito com o módulo em modo manual. Executado sem realizar nenhuma ação")

    @classmethod
    def verificar_agendamentos_usina(cls, agendamento) -> bool:
        if agendamento[3] == AGN_INDISPONIBILIZAR:
            logger.info("[AGN] Indisponibilizando a usina via agendamento.")
            for ug in cls.ugs:
                ug.forcar_estado_indisponivel()

            while (not cls.ug1.etapa_atual == UG_PARADA and not cls.ug2.etapa_atual == UG_PARADA):
                cls.ler_valores()
                logger.debug("[AGN] Indisponibilizando Usina...")
                sleep(10)

            cls.acionar_emergencia()
            logger.debug("[AGN] Emergência pressionada após indizponibilização agendada mudando para modo manual para evitar normalização automática.")
            cls.modo_autonomo = False

        if agendamento[3] == AGN_ALTERAR_NV_ALVO:
            try:
                novo = float(agendamento[5].replace(",", "."))
                cls.cfg["nv_alvo"] = novo

            except Exception:
                logger.error(f"[AGN] Valor inválido no agendamento: {agendamento[0]} ({agendamento[3]} é inválido).")
                return False

        if agendamento[3] == AGN_BAIXAR_POT_UGS_MINIMO:
            for ug in cls.ugs:
                cls.cfg[f"pot_maxima_ug{ug.id}"] = cls.cfg["pot_minima"]
                if ug.etapa_atual == UG_PARADA:
                    logger.debug(f"[AGN] A UG{ug.id} já está no estado parada/parando.")
                else:
                    logger.debug(f"[AGN] Enviando o setpoint mínimo ({cls.cfg['pot_minima']}) para a UG{ug.id}")
                    ug.enviar_setpoint(cls.cfg["pot_minima"])

        if agendamento[3] == AGN_NORMALIZAR_POT_UGS_MINIMO:
            for ug in cls.ugs:
                cls.cfg[f"pot_maxima_ug{ug.id}"] = cls.cfg["pot_maxima_ug"]
                ug.enviar_setpoint(cls.cfg["pot_maxima_ug"])

        if agendamento[3] == AGN_AGUARDAR_RESERVATORIO:
            logger.debug("[AGN] Ativando estado de espera de nível do reservatório")
            cls.aguardando_reservatorio = 1

        if agendamento[3] == AGN_NORMALIZAR_ESPERA_RESERVATORIO:
            logger.debug("[AGN] Desativando estado de espera de nível do reservatório")
            cls.aguardando_reservatorio = 0

        if agendamento[3] == AGN_ALTERAR_POT_LIMITE_TODAS_AS_UGS:
            try:
                novo = float(agendamento[5].replace(",", "."))
                for ug in cls.ugs:
                    cls.cfg[f"pot_maxima_ug{ug.id}"] = novo
            except Exception:
                logger.error(f"[AGN] Valor inválido no agendamento: {agendamento[0]} ({agendamento[3]} é inválido)")
                return False

        return True

    @classmethod
    def verificar_agendamentos_ugs(cls, agendamento, ug) -> bool:
        if agendamento[3] == AGN_UG_ALTERAR_POT_LIMITE[ug.id]:
            try:
                novo = float(agendamento[5].replace(",", "."))
                cls.cfg[f"pot_maxima_ug{ug.id}"] = novo

            except Exception:
                logger.error(f"[AGN] Valor inválido no agendamento: {agendamento[0]} ({agendamento[3]} é inválido)")
                return False

        if agendamento[3] == AGN_UG_FORCAR_ESTADO_MANUAL[ug.id]:
            ug.forcar_estado_manual()

        if agendamento[3] == AGN_UG_FORCAR_ESTADO_DISPONIVEL[ug.id]:
            ug.forcar_estado_disponivel()

        if agendamento[3] == AGN_UG_FORCAR_ESTADO_INDISPONIVEL[ug.id]:
            ug.forcar_estado_indisponivel()

        if agendamento[3] == AGN_UG_FORCAR_ESTADO_RESTRITO[ug.id]:
            ug.forcar_estado_restrito()

        if agendamento[3] == AGN_UG_TEMPO_ESPERA_RESTRITO[ug.id]:
            try:
                ug.normalizacao_agendada = True
                novo = agendamento[5].split(":")
                tempo = (int(novo[0]) * 3600) + (int(novo[1]) * 60)
                ug.tempo_normalizar = tempo

            except Exception:
                logger.error(f"[AGN] Valor inválido no agendamento: {agendamento[0]} ({agendamento[3]} é inválido)")
                return False