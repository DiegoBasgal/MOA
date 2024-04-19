__version__ = "0.2"
__author__ = "Diego Basgal"
__credits__ = ["Lucas Lavratti" , ...]
__description__ = "Este módulo corresponde a implementação de Agendamentos da Interface WEB."

import pytz
import logging

import src.usina as usn
import src.conectores.banco_dados as bd

from time import sleep
from datetime import datetime, timedelta

from src.dicionarios.const import *


logger = logging.getLogger("logger")


class Agendamentos:

    segundos_passados = 0
    segundos_adiantados = 0


    @classmethod
    def verificar_agendamentos_pendentes(cls) -> "list":
        """
        Função para extrair lista de agendamentos não executados do Banco de Dados.
        """

        pendentes = []
        agendamentos = bd.BancoDados.get_agendamentos_pendentes()

        for agendamento in agendamentos:
            ag = list(agendamento)
            ag[1] = ag[1] - timedelta(0, 60 * 60 * 3)
            pendentes.append(ag)

        return pendentes


    @classmethod
    def verificar_agendamentos_iguais(cls, agendamentos) -> "None":
        """
        Função para verificar agendamentos iguais.

        Verifica se o mesmo agendamento foi criado em um período de tempo pré-definido
        e concatena (marca como executado) para não haver problemas de operação.
        """

        limite_entre_agendamentos_iguais = 300
        agendamentos = sorted(agendamentos, key=lambda x:(x[3], x[1]))
        i = 0
        j = len(agendamentos)
        while i < j - 1:
            if agendamentos[i][3] == agendamentos[i+1][3] and (agendamentos[i+1][1] - agendamentos[i][1]).seconds < limite_entre_agendamentos_iguais:
                ag_concatenado = agendamentos.pop(i)
                obs = "Este agendamento foi concatenado ao seguinte por motivos de temporização."
                bd.BancoDados.update_agendamento(ag_concatenado[0], True, obs)
                i -= 1

            i += 1
            j = len(agendamentos)


    @classmethod
    def verificar_agendamentos(cls) -> "bool":
        """
        Função principal de verificação de agendamentos.

        Chama a função de extração da lista de agendamentos do Banco, e verifica
        se a lista possui algum item. Caso haja algum agendamento, passa a verificar
        se o agendamento está adiantado ou atrasado. Logo após, verifica se o
        agendamento não possui efeito, para depois, caso seja válido, passa a
        verificar se o agendamento é das Unidades ou de outros setores da Usina.
        """

        agora = usn.Usina.get_time()
        agendamentos = bd.BancoDados.get_agendamentos_pendentes()

        if agendamentos is None:
            return False
        else:
            i = len(agendamentos)

        cls.verificar_agendamentos_iguais(agendamentos)

        for agendamento in agendamentos:
            if agora > agendamento[1]:
                cls.segundos_adiantados = 0
                cls.segundos_passados = (agora - agendamento[1]).seconds
            else:
                cls.segundos_adiantados = (agendamento[1] - agora).seconds
                cls.segundos_passados = 0

            logger.debug("")
            logger.debug(f"[AGN] Criado por:                         \"{agendamento[6]}\"")
            logger.debug(f"      Comando:                            \"{AGN_STR_DICT[agendamento[3]] if agendamento[3] in AGN_STR_DICT else 'Inexistente'}\"")
            logger.debug(f"      Executar em:                        {agendamento[1].strftime('%H:%M:%S %d-%m-%Y')}")
            logger.debug("")

            cls.verificar_agendamentos_atrasados(agendamento)

            if cls.segundos_adiantados <= 60 and not bool(agendamento[4]):
                logger.info(f"[AGN] Executando agendamento:             \"{AGN_STR_DICT[agendamento[3]]}\"")
                logger.info(f"      Criado por:                         \"{agendamento[6]}\"")
                logger.info(f"      Criado em:                          {agendamento[9].strftime('%H:%M:%S %d-%m-%Y')}")
                logger.debug("")

                cls.verificar_agendamentos_sem_efeito(agendamento)
                cls.verificar_agendamentos_usina(agendamento)
                cls.verificar_agendamentos_ugs(agendamento)

                bd.BancoDados.update_agendamento(agendamento[0], executado=1)
                logger.debug(f"[AGN] Agendamento executado:              \"{AGN_STR_DICT[agendamentos[i-1][3]] if agendamentos[i-1][3] in AGN_STR_DICT else 'Inexistente'}\"")


    @classmethod
    def verificar_agendamentos_atrasados(cls, agendamento) -> "None":
        """
        Função para verificar se os agendamentos esão atrasados.

        Verifica se o agendamento ultrapassou o limite de tempo pré-definido para
        poder determinar como proceder, dependendo da função do agendamento.
        """

        agn_atrasados = 0

        if cls.segundos_passados > 240:
            logger.warning(f"[AGN] Agendamento: {agendamento[0]} atrasado! ({agendamento[3]}).")
            agn_atrasados += 1

        if cls.segundos_passados > 300 or agn_atrasados > 3:
            logger.warning("[AGN] Os agendamentos estão muito atrasados!")
            if agendamento[3] == AGN_INDISPONIBILIZAR:
                logger.warning("[AGN] Acionando emergência!")
                usn.Usina.acionar_emergencia()
                bd.BancoDados.update_agendamento(int(agendamento[0]), 1, obs="AGENDAMENTO EXECUTADO POR TRATATIVA DE CÓDIGO!")
                agn_atrasados += 1

            if agendamento[3] in (
                AGN_ALTERAR_NV_ALVO, \
                AGN_ALTERAR_POT_LIMITE_TODAS_AS_UGS, \
                AGN_AGUARDAR_RESERVATORIO, \
                AGN_NORMALIZAR_ESPERA_RESERVATORIO
            ):
                logger.warning("[AGN] Não foi possível executar o agendamento! Favor re-agendar")
                bd.BancoDados.update_agendamento(int(agendamento[0]), 1, obs="AGENDAMENTO NÃO EXECUTADO POR CONTA DE ATRASO!")
                agn_atrasados += 1

            for ug in usn.Usina.ugs:
                if agendamento[3] in AGN_LST_BLOQUEIO_UG:
                    logger.info(f"[AGN] Indisponibilizando UG{ug.id}")
                    ug.forcar_estado_indisponivel()
                    bd.BancoDados.update_agendamento(int(agendamento[0]), 1, obs="AGENDAMENTO NÃO EXECUTADO POR CONTA DE ATRASO!")
                    agn_atrasados += 1


    @classmethod
    def verificar_agendamentos_sem_efeito(cls, agendamento) -> "None":
        """
        Função para verificar se o agendamento possui algum efeito no modo atual
        do MOA.

        Verifica se o agendamento pode ser executado em modo autônomo ou manual.
        """

        if usn.Usina.modo_autonomo and not bd.BancoDados.get_executabilidade(agendamento[3])["executavel_em_automatico"]:
            bd.BancoDados.update_agendamento(agendamento[0], True, obs="Este agendamento não tem efeito com o módulo em modo autônomo. Executado sem realizar nenhuma ação")

        if not usn.Usina.modo_autonomo and not bd.BancoDados.get_executabilidade(agendamento[3])["executavel_em_manual"]:
            bd.BancoDados.update_agendamento(agendamento[0], True, obs="Este agendamento não tem efeito com o módulo em modo manual. Executado sem realizar nenhuma ação")


    @classmethod
    def verificar_agendamentos_usina(cls, agendamento) -> None:
        """
        Função para verificar o tipo de comando dos agendamentos da Usina (Serviço
        Auxiliar, Tomada da Água ou Subestação)
        """

        if agendamento[3] == AGN_INDISPONIBILIZAR:
            logger.info("[AGN] Indisponibilizando a usina via agendamento.")
            for ug in usn.Usina.ugs:
                ug.forcar_estado_indisponivel()
                ug.step()

            while (not usn.Usina.ug1.etapa == UG_PARADA and not usn.Usina.ug2.etapa == UG_PARADA):
                usn.Usina.ler_valores()
                logger.debug("[AGN] Aguardando parada total das Unidades...")
                sleep(5)

            usn.Usina.acionar_emergencia()
            logger.debug("[AGN] Emergência pressionada após indisponibilização agendada mudando para modo manual para evitar normalização automática.")
            usn.Usina.modo_autonomo = False

        if agendamento[3] == AGN_ALTERAR_NV_ALVO:
            try:
                novo = float(agendamento[5].replace(",", "."))
                bd.BancoDados.update_nv_alvo([novo])
                usn.Usina.cfg["nv_alvo"] = novo

            except Exception:
                logger.error(f"[AGN] Valor inválido no agendamento: {agendamento[0]} ({agendamento[3]} é inválido).")

        if agendamento[3] == AGN_ALTERAR_POT_LIMITE_TODAS_AS_UGS:
            try:
                novo = float(agendamento[5].replace(",", "."))

                usn.Usina.cfg["pot_maxima_alvo"] = novo

                for ug in usn.Usina.ugs:
                    usn.Usina.cfg[f"pot_maxima_ug{ug.id}"] = novo / 2

            except Exception:
                logger.error(f"[AGN] Valor inválido no agendamento: {agendamento[0]} ({agendamento[3]} é inválido)")


    @classmethod
    def verificar_agendamentos_ugs(cls, agendamento) -> None:
        """
        Função para verificar agendamentos das Unidades de Geração.
        """

        if agendamento[3] == AGN_UG1_ALTERAR_POT_LIMITE:
            try:
                novo = float(agendamento[5].replace(",", "."))
                usn.Usina.cfg[f"pot_maxima_ug1"] = novo

            except Exception:
                logger.error(f"[AGN] Valor inválido no agendamento: {agendamento[0]} ({agendamento[3]} é inválido)")

        if agendamento[3] == AGN_UG1_FORCAR_ESTADO_MANUAL:
            usn.Usina.ug1.forcar_estado_manual()

        if agendamento[3] == AGN_UG1_FORCAR_ESTADO_DISPONIVEL:
            usn.Usina.ug1.forcar_estado_disponivel()

        if agendamento[3] == AGN_UG1_FORCAR_ESTADO_INDISPONIVEL:
            usn.Usina.ug1.forcar_estado_indisponivel()

        if agendamento[3] == AGN_UG1_FORCAR_ESTADO_RESTRITO:
            usn.Usina.ug1.forcar_estado_restrito()

        if agendamento[3] == AGN_UG1_TEMPO_ESPERA_RESTRITO:
            try:
                usn.Usina.ug1.normalizacao_agendada = True
                novo = agendamento[5].split(":")
                tempo = (int(novo[0]) * 3600) + (int(novo[1]) * 60)
                usn.Usina.ug1.tempo_normalizar = tempo

            except Exception:
                logger.error(f"[AGN] Valor inválido no agendamento: {agendamento[0]} ({agendamento[3]} é inválido)")

        if agendamento[3] == AGN_UG2_ALTERAR_POT_LIMITE:
            try:
                novo = float(agendamento[5].replace(",", "."))
                usn.Usina.cfg[f"pot_maxima_ug2"] = novo

            except Exception:
                logger.error(f"[AGN] Valor inválido no agendamento: {agendamento[0]} ({agendamento[3]} é inválido)")

        if agendamento[3] == AGN_UG2_FORCAR_ESTADO_MANUAL:
            usn.Usina.ug2.forcar_estado_manual()

        if agendamento[3] == AGN_UG2_FORCAR_ESTADO_DISPONIVEL:
            usn.Usina.ug2.forcar_estado_disponivel()

        if agendamento[3] == AGN_UG2_FORCAR_ESTADO_INDISPONIVEL:
            usn.Usina.ug2.forcar_estado_indisponivel()

        if agendamento[3] == AGN_UG2_FORCAR_ESTADO_RESTRITO:
            usn.Usina.ug2.forcar_estado_restrito()

        if agendamento[3] == AGN_UG2_TEMPO_ESPERA_RESTRITO:
            try:
                usn.Usina.ug2.normalizacao_agendada = True
                novo = agendamento[5].split(":")
                tempo = (int(novo[0]) * 3600) + (int(novo[1]) * 60)
                usn.Usina.ug2.tempo_normalizar = tempo

            except Exception:
                logger.error(f"[AGN] Valor inválido no agendamento: {agendamento[0]} ({agendamento[3]} é inválido)")
