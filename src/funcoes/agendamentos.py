import pytz
import logging

import usina as u
import src.conectores.banco_dados as bd

from time import sleep
from datetime import datetime, timedelta

from src.dicionarios.const import *


logger = logging.getLogger("logger")


class Agendamentos:
    def __init__(self, cfg: "dict"=None, bd: "bd.BancoDados"=None, usina: "u.Usina"=None):

        self.bd = bd
        self.cfg = cfg
        self.usn = usina

        self.pot_anterior = {}

        self.segundos_passados = 0
        self.segundos_adiantados = 0


    def verificar_agendamentos_pendentes(self) -> "list":
        """
        Função para extrair lista de agendamentos não executados do Banco de Dados.
        """

        pendentes = []
        agendamentos = self.bd.get_agendamentos_pendentes()

        for agendamento in agendamentos:
            ag = list(agendamento)
            ag[1] = ag[1] - timedelta(0, 60 * 60 * 3)
            pendentes.append(ag)

        return pendentes


    def verificar_agendamentos_iguais(self, agendamentos) -> "None":
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
                self.bd.update_agendamento(ag_concatenado[0], True, obs)
                i -= 1

            i += 1
            j = len(agendamentos)


    def verificar_agendamentos(self) -> "bool":
        """
        Função principal de verificação de agendamentos.

        Chama a função de extração da lista de agendamentos do Banco, e verifica
        se a lista possui algum item. Caso haja algum agendamento, passa a verificar
        se o agendamento está adiantado ou atrasado. Logo após, verifica se o
        agendamento não possui efeito, para depois, caso seja válido, passa a
        verificar se o agendamento é das Unidades ou de outros setores da Usina.
        """

        agora = datetime.now(pytz.timezone("Brazil/East")).replace(tzinfo=None)
        agendamentos = self.bd.get_agendamentos_pendentes()

        if agendamentos is None:
            return False
        else:
            i = len(agendamentos)

        self.verificar_agendamentos_iguais(agendamentos)

        for agendamento in agendamentos:
            if agora > agendamento[1]:
                self.segundos_adiantados = 0
                self.segundos_passados = (agora - agendamento[1]).seconds
            else:
                self.segundos_adiantados = (agendamento[1] - agora).seconds
                self.segundos_passados = 0

            logger.debug("")
            logger.debug(f"[AGN] Executar em:                        {agendamento[1].strftime('%H:%M:%S %d-%m-%Y')}")
            logger.debug(f"      Criado por:                         \"{agendamento[6]}\"")
            logger.debug(f"      Comando:                            \"{AGN_STR_DICT[agendamento[3]] if agendamento[3] in AGN_STR_DICT else 'Inexistente'}\"")
            logger.debug("")

            self.verificar_agendamentos_atrasados(agendamento)

            if self.segundos_adiantados <= 60 and not bool(agendamento[4]):
                logger.info(f"[AGN] Executando agendamento:             {agendamento[0]}")
                logger.info(f"      Comando:                            \"{AGN_STR_DICT[agendamento[3]]}\"")
                logger.info(f"      Criado em:                          {agendamento[9].strftime('%H:%M:%S %d-%m-%Y')}")
                logger.debug("")

                self.verificar_agendamentos_sem_efeito(agendamento)
                self.verificar_agendamentos_usina(agendamento)
                self.verificar_agendamentos_ugs(agendamento)

                if agendamento[2] in ("", None):
                    self.bd.update_agendamento(agendamento[0], executado=1, obs=agendamento[5])
                else:
                    self.bd.update_agendamento(agendamento[0], executado=1)

                logger.debug(f"[AGN] Agendamento executado:              \"{AGN_STR_DICT[agendamentos[i-1][3]] if agendamentos[i-1][3] in AGN_STR_DICT else 'Inexistente'}\"")


    def verificar_agendamentos_atrasados(self, agendamento) -> "None":
        """
        Função para verificar se os agendamentos esão atrasados.

        Verifica se o agendamento ultrapassou o limite de tempo pré-definido para
        poder determinar como proceder, dependendo da função do agendamento.
        """

        agn_atrasados = 0

        if self.segundos_passados > 240:
            logger.warning(f"[AGN] Agendamento: {agendamento[0]} atrasado! ({agendamento[3]}).")
            agn_atrasados += 1

        if self.segundos_passados > 300 or agn_atrasados > 3:
            logger.warning("[AGN] Os agendamentos estão muito atrasados!")

            if agendamento[3] == AGN_INDISPONIBILIZAR:
                logger.warning("[AGN] Acionando emergência!")
                self.usn.acionar_emergencia()
                self.bd.update_agendamento(int(agendamento[0]), 1, obs="AGENDAMENTO EXECUTADO POR TRATATIVA DE CÓDIGO!")
                agn_atrasados += 1

            if agendamento[3] in (AGN_ALTERAR_NV_ALVO, AGN_ALTERAR_POT_LIMITE_TODAS_AS_UGS, AGN_BAIXAR_POT_UGS_MINIMO, AGN_NORMALIZAR_POT_UGS_MINIMO, AGN_AGUARDAR_RESERVATORIO, AGN_NORMALIZAR_ESPERA_RESERVATORIO):
                logger.warning("[AGN] Não foi possível executar o agendamento! Favor re-agendar")
                self.bd.update_agendamento(int(agendamento[0]), 1, obs="AGENDAMENTO NÃO EXECUTADO POR CONTA DE ATRASO!")
                agn_atrasados += 1

            for ug in self.usn.ugs:
                if agendamento[3] in AGN_LST_BLOQUEIO_UG:
                    logger.info(f"[AGN] Indisponibilizando UG{ug.id}")
                    ug.forcar_estado_indisponivel()
                    self.bd.update_agendamento(int(agendamento[0]), 1, obs="AGENDAMENTO NÃO EXECUTADO POR CONTA DE ATRASO!")
                    agn_atrasados += 1


    def verificar_agendamentos_sem_efeito(self, agendamento) -> "None":
        """
        Função para verificar se o agendamento possui algum efeito no modo atual
        do MOA.

        Verifica se o agendamento pode ser executado em modo autônomo ou manual.
        """

        if self.usn.modo_autonomo and not self.bd.get_executabilidade(agendamento[3])["executavel_em_automatico"]:
            self.bd.update_agendamento(agendamento[0], True, obs="Este agendamento não tem efeito com o módulo em modo autônomo. Executado sem realizar nenhuma ação")

        if not self.usn.modo_autonomo and not self.bd.get_executabilidade(agendamento[3])["executavel_em_manual"]:
            self.bd.update_agendamento(agendamento[0], True, obs="Este agendamento não tem efeito com o módulo em modo manual. Executado sem realizar nenhuma ação")


    def verificar_agendamentos_usina(self, agendamento) -> "None":
        """
        Função para verificar o tipo de comando dos agendamentos da Usina (Serviço
        Auxiliar, Tomada da Água ou Subestação)
        """

        if agendamento[3] == AGN_INDISPONIBILIZAR:
            logger.info("[AGN] Indisponibilizando a usina via agendamento.")
            for ug in self.usn.ugs:
                ug.forcar_estado_indisponivel()
                ug.step()
                sleep(1)

            while (not self.usn.ug1.etapa_atual == UG_PARADA and not self.usn.ug2.etapa_atual == UG_PARADA and not self.usn.ug3.etapa_atual == UG_PARADA):
                self.usn.ler_valores()
                logger.debug("[AGN] Aguardando parada total das Unidades...")
                sleep(5)

            logger.debug("[AGN] Emergência pressionada após indisponibilização agendada!")
            logger.debug("[AGN] Mudando para modo manual para evitar normalização automática.")
            self.usn.modo_autonomo = False

        if agendamento[3] == AGN_ALTERAR_NV_ALVO:
            try:
                self.cfg["nv_alvo"] = novo = float(agendamento[5].replace(",", "."))
                self.bd.update_nivel_alvo(novo)

            except Exception:
                logger.error(f"[AGN] Valor: {agendamento[5]}, inserido no agendamento {agendamento[0]} é inválido.")

        if agendamento[3] == AGN_BAIXAR_POT_UGS_MINIMO:

            for ug in self.usn.ugs:
                self.pot_anterior[f"UG{ug.id}"] = self.cfg[f"pot_maxima_ug{ug.id}"]
                self.cfg[f"pot_maxima_ug{ug.id}"] = self.cfg["pot_limpeza_grade"]

                if not ug.etapa_atual in (UG_PARADA, UG_PARANDO):
                    ug.limpeza_grade = True

        if agendamento[3] == AGN_NORMALIZAR_POT_UGS_MINIMO:

            for ug in self.usn.ugs:
                ug.limpeza_grade = False
                self.cfg[f"pot_maxima_ug{ug.id}"] = self.pot_anterior[f"UG{ug.id}"]
                ug.enviar_setpoint(self.cfg[f"pot_maxima_ug{ug.id}"])

        if agendamento[3] == AGN_AGUARDAR_RESERVATORIO:
            logger.debug("[AGN] Ativando estado de espera de nível do reservatório")
            self.aguardando_reservatorio = 1

        if agendamento[3] == AGN_NORMALIZAR_ESPERA_RESERVATORIO:
            logger.debug("[AGN] Desativando estado de espera de nível do reservatório")
            self.aguardando_reservatorio = 0

        if agendamento[3] == AGN_ALTERAR_POT_LIMITE_TODAS_AS_UGS:
            try:
                self.cfg["pot_alvo_usina"] = novo = float(agendamento[5].replace(",", "."))

            except Exception:
                logger.error(f"[AGN] Valor: {agendamento[5]}, inserido no agendamento {agendamento[0]} é inválido.")


    def verificar_agendamentos_ugs(self, agendamento) -> "None":
        """
        Função para verificar agendamentos das Unidades de Geração.
        """

        if agendamento[3] == AGN_UG1_FORCAR_ESTADO_MANUAL:
            self.usn.ug1.forcar_estado_manual()

        if agendamento[3] == AGN_UG1_FORCAR_ESTADO_DISPONIVEL:
            self.usn.ug1.forcar_estado_disponivel()

        if agendamento[3] == AGN_UG1_FORCAR_ESTADO_INDISPONIVEL:
            self.usn.ug1.forcar_estado_indisponivel()

        if agendamento[3] == AGN_UG1_FORCAR_ESTADO_RESTRITO:
            self.usn.ug1.forcar_estado_restrito()

        if agendamento[3] == AGN_UG1_ALTERAR_POT_LIMITE:
            try:
                self.cfg[f"pot_maxima_ug1"] = novo = float(agendamento[5].replace(",", "."))

            except Exception:
                logger.error(f"[AGN] Valor: {agendamento[5]}, inserido no agendamento {agendamento[0]} é inválido.")

        if agendamento[3] == AGN_UG1_TEMPO_ESPERA_RESTRITO:
            try:
                self.usn.ug1.normalizacao_agendada = True
                novo = agendamento[5].split(":")
                tempo = (int(novo[0]) * 3600) + (int(novo[1]) * 60)
                self.usn.ug1.tempo_normalizar = tempo

            except Exception:
                logger.error(f"[AGN] Valor: {agendamento[5]}, inserido no agendamento {agendamento[0]} é inválido.")


        if agendamento[3] == AGN_UG2_FORCAR_ESTADO_MANUAL:
            self.usn.ug2.forcar_estado_manual()

        if agendamento[3] == AGN_UG2_FORCAR_ESTADO_DISPONIVEL:
            self.usn.ug2.forcar_estado_disponivel()

        if agendamento[3] == AGN_UG2_FORCAR_ESTADO_INDISPONIVEL:
            self.usn.ug2.forcar_estado_indisponivel()

        if agendamento[3] == AGN_UG2_FORCAR_ESTADO_RESTRITO:
            self.usn.ug2.forcar_estado_restrito()

        if agendamento[3] == AGN_UG2_ALTERAR_POT_LIMITE:
            try:
                self.cfg[f"pot_maxima_ug2"] = novo = float(agendamento[5].replace(",", "."))

            except Exception:
                logger.error(f"[AGN] Valor: {agendamento[5]}, inserido no agendamento {agendamento[0]} é inválido.")

        if agendamento[3] == AGN_UG2_TEMPO_ESPERA_RESTRITO:
            try:
                self.usn.ug2.normalizacao_agendada = True
                novo = agendamento[5].split(":")
                tempo = (int(novo[0]) * 3600) + (int(novo[1]) * 60)
                self.usn.ug2.tempo_normalizar = tempo

            except Exception:
                logger.error(f"[AGN] Valor: {agendamento[5]}, inserido no agendamento {agendamento[0]} é inválido.")


        if agendamento[3] == AGN_UG3_FORCAR_ESTADO_MANUAL:
            self.usn.ug3.forcar_estado_manual()

        if agendamento[3] == AGN_UG3_FORCAR_ESTADO_DISPONIVEL:
            self.usn.ug3.forcar_estado_disponivel()

        if agendamento[3] == AGN_UG3_FORCAR_ESTADO_INDISPONIVEL:
            self.usn.ug3.forcar_estado_indisponivel()

        if agendamento[3] == AGN_UG3_FORCAR_ESTADO_RESTRITO:
            self.usn.ug3.forcar_estado_restrito()

        if agendamento[3] == AGN_UG3_ALTERAR_POT_LIMITE:
            try:
                self.cfg[f"pot_maxima_ug3"] = novo = float(agendamento[5].replace(",", "."))

            except Exception:
                logger.error(f"[AGN] Valor: {agendamento[5]}, inserido no agendamento {agendamento[0]} é inválido.")

        if agendamento[3] == AGN_UG3_TEMPO_ESPERA_RESTRITO:
            try:
                self.usn.ug3.normalizacao_agendada = True
                novo = agendamento[5].split(":")
                tempo = (int(novo[0]) * 3600) + (int(novo[1]) * 60)
                self.usn.ug3.tempo_normalizar = tempo

            except Exception:
                logger.error(f"[AGN] Valor: {agendamento[5]}, inserido no agendamento {agendamento[0]} é inválido.")