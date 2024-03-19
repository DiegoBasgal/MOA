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


logger = logging.getLogger("__main__")


class Agendamentos:
    def __init__(self, cfg: "dict"=None, db: "bd.BancoDados"=None, usina: "usn.Usina"=None) -> "None":

        # ATRIBUIÇÂO DE VARIÁVEIS PÚBLICAS

        self.db = db
        self.cfg = cfg
        self.usn = usina

        self.segundos_passados = 0
        self.segundos_adiantados = 0

    def verificar_agendamentos_pendentes(self) -> "list":
        """
        Função para extrair lista de agendamentos não executados do Banco de Dados.
        """
        pendentes = []
        agendamentos = self.db.get_agendamentos_pendentes()

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
                self.db.update_agendamento(ag_concatenado[0], True, obs)
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
        agendamentos = self.db.get_agendamentos_pendentes()

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
                self.verificar_agendamentos_adufas(agendamento)

                self.db.update_agendamento(agendamento[0], executado=1)
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
                self.db.update_agendamento(int(agendamento[0]), 1, obs="AGENDAMENTO EXECUTADO POR TRATATIVA DE CÓDIGO!")
                agn_atrasados += 1

            if agendamento[3] in (AGN_ALTERAR_NV_ALVO, AGN_ALTERAR_POT_LIMITE_TODAS_AS_UGS, AGN_BAIXAR_POT_UGS_MINIMO, AGN_NORMALIZAR_POT_UGS_MINIMO, AGN_AGUARDAR_RESERVATORIO, AGN_NORMALIZAR_ESPERA_RESERVATORIO):
                logger.warning("[AGN] Não foi possível executar o agendamento! Favor re-agendar")
                self.db.update_agendamento(int(agendamento[0]), 1, obs="AGENDAMENTO NÃO EXECUTADO POR CONTA DE ATRASO!")
                agn_atrasados += 1

            for ug in self.usn.ugs:
                if agendamento[3] in AGN_LST_BLOQUEIO_UG:
                    logger.info(f"[AGN] Indisponibilizando UG{ug.id}")
                    ug.forcar_estado_indisponivel()
                    self.db.update_agendamento(int(agendamento[0]), 1, obs="AGENDAMENTO NÃO EXECUTADO POR CONTA DE ATRASO!")
                    agn_atrasados += 1

    def verificar_agendamentos_sem_efeito(self, agendamento) -> "None":
        """
        Função para verificar se o agendamento possui algum efeito no modo atual
        do MOA.

        Verifica se o agendamento pode ser executado em modo autônomo ou manual.
        """

        if self.usn.modo_autonomo and not self.db.get_executabilidade(agendamento[3])["executavel_em_automatico"]:
            self.db.update_agendamento(agendamento[0], True, obs="Este agendamento não tem efeito com o módulo em modo autônomo. Executado sem realizar nenhuma ação")

        if not self.usn.modo_autonomo and not self.db.get_executabilidade(agendamento[3])["executavel_em_manual"]:
            self.db.update_agendamento(agendamento[0], True, obs="Este agendamento não tem efeito com o módulo em modo manual. Executado sem realizar nenhuma ação")

    def verificar_agendamentos_usina(self, agendamento) -> None:
        """
        Função para verificar o tipo de comando dos agendamentos da Usina (Serviço
        Auxiliar, Tomada da Água ou Subestação)
        """

        if agendamento[3] == AGN_INDISPONIBILIZAR:
            logger.info("[AGN] Indisponibilizando a usina via agendamento.")
            for ug in self.usn.ugs:
                ug.forcar_estado_indisponivel()
                ug.step()

            while (not self.usn.ug1.etapa_atual == UG_PARADA and not self.usn.ug2.etapa_atual == UG_PARADA and not self.usn.ug3.etapa_atual == UG_PARADA):
                self.usn.ler_valores()
                logger.debug("[AGN] Aguardando parada total das Unidades...")
                sleep(5)

            self.usn.acionar_emergencia()
            logger.debug("[AGN] Emergência pressionada após indisponibilização agendada mudando para modo manual para evitar normalização automática.")
            self.usn.modo_autonomo = False

        if agendamento[3] == AGN_ALTERAR_NV_ALVO:
            try:
                novo = float(agendamento[5].replace(",", "."))
                self.cfg["nv_alvo"] = novo

            except Exception:
                logger.error(f"[AGN] Valor inválido no agendamento: {agendamento[0]} ({agendamento[3]} é inválido).")

        if agendamento[3] == AGN_BAIXAR_POT_UGS_MINIMO:
            for ug in self.usn.ugs:
                self.cfg[f"pot_maxima_ug{ug.id}"] = self.cfg["pot_limpeza_grade"]

                if ug.etapa_atual == UG_PARADA or ug.etapa_atual == UG_PARANDO:
                    logger.debug(f"[AGN] UG{ug.id} está no estado parada/parando.")
                else:
                    ug.limpeza_grade = True

        if agendamento[3] == AGN_NORMALIZAR_POT_UGS_MINIMO:
            for ug in self.usn.ugs:
                self.cfg[f"pot_maxima_ug{ug.id}"] = self.cfg["pot_maxima_ug"]
                ug.limpeza_grade = False
                ug.enviar_setpoint(self.cfg["pot_maxima_ug"])

        if agendamento[3] == AGN_AGUARDAR_RESERVATORIO:
            logger.debug("[AGN] Ativando estado de espera de nível do reservatório")
            self.aguardando_reservatorio = 1

        if agendamento[3] == AGN_NORMALIZAR_ESPERA_RESERVATORIO:
            logger.debug("[AGN] Desativando estado de espera de nível do reservatório")
            self.aguardando_reservatorio = 0

        if agendamento[3] == AGN_ALTERAR_POT_LIMITE_TODAS_AS_UGS:
            try:
                novo = float(agendamento[5].replace(",", "."))

                self.cfg["pot_maxima_alvo"] = novo

                for ug in self.usn.ugs:
                    self.cfg[f"pot_maxima_ug{ug.id}"] = novo / 3

            except Exception:
                logger.error(f"[AGN] Valor inválido no agendamento: {agendamento[0]} ({agendamento[3]} é inválido)")

    def verificar_agendamentos_ugs(self, agendamento) -> None:
        """
        Função para verificar agendamentos das Unidades de Geração.
        """

        if agendamento[3] == AGN_UG1_ALTERAR_POT_LIMITE:
            try:
                novo = float(agendamento[5].replace(",", "."))
                self.cfg[f"pot_maxima_ug1"] = novo

            except Exception:
                logger.error(f"[AGN] Valor inválido no agendamento: {agendamento[0]} ({agendamento[3]} é inválido)")

        if agendamento[3] == AGN_UG1_FORCAR_ESTADO_MANUAL:
            self.usn.ug1.forcar_estado_manual()

        if agendamento[3] == AGN_UG1_FORCAR_ESTADO_DISPONIVEL:
            self.usn.ug1.forcar_estado_disponivel()

        if agendamento[3] == AGN_UG1_FORCAR_ESTADO_INDISPONIVEL:
            self.usn.ug1.forcar_estado_indisponivel()

        if agendamento[3] == AGN_UG1_FORCAR_ESTADO_RESTRITO:
            self.usn.ug1.forcar_estado_restrito()

        if agendamento[3] == AGN_UG1_TEMPO_ESPERA_RESTRITO:
            try:
                self.usn.ug1.normalizacao_agendada = True
                novo = agendamento[5].split(":")
                tempo = (int(novo[0]) * 3600) + (int(novo[1]) * 60)
                self.usn.ug1.tempo_normalizar = tempo

            except Exception:
                logger.error(f"[AGN] Valor inválido no agendamento: {agendamento[0]} ({agendamento[3]} é inválido)")

        if agendamento[3] == AGN_UG2_ALTERAR_POT_LIMITE:
            try:
                novo = float(agendamento[5].replace(",", "."))
                self.cfg[f"pot_maxima_ug2"] = novo

            except Exception:
                logger.error(f"[AGN] Valor inválido no agendamento: {agendamento[0]} ({agendamento[3]} é inválido)")

        if agendamento[3] == AGN_UG2_FORCAR_ESTADO_MANUAL:
            self.usn.ug2.forcar_estado_manual()

        if agendamento[3] == AGN_UG2_FORCAR_ESTADO_DISPONIVEL:
            self.usn.ug2.forcar_estado_disponivel()

        if agendamento[3] == AGN_UG2_FORCAR_ESTADO_INDISPONIVEL:
            self.usn.ug2.forcar_estado_indisponivel()

        if agendamento[3] == AGN_UG2_FORCAR_ESTADO_RESTRITO:
            self.usn.ug2.forcar_estado_restrito()

        if agendamento[3] == AGN_UG2_TEMPO_ESPERA_RESTRITO:
            try:
                self.usn.ug2.normalizacao_agendada = True
                novo = agendamento[5].split(":")
                tempo = (int(novo[0]) * 3600) + (int(novo[1]) * 60)
                self.usn.ug2.tempo_normalizar = tempo

            except Exception:
                logger.error(f"[AGN] Valor inválido no agendamento: {agendamento[0]} ({agendamento[3]} é inválido)")

        if agendamento[3] == AGN_UG3_ALTERAR_POT_LIMITE:
            try:
                novo = float(agendamento[5].replace(",", "."))
                self.cfg[f"pot_maxima_ug3"] = novo

            except Exception:
                logger.error(f"[AGN] Valor inválido no agendamento: {agendamento[0]} ({agendamento[3]} é inválido)")

        if agendamento[3] == AGN_UG3_FORCAR_ESTADO_MANUAL:
            self.usn.ug3.forcar_estado_manual()

        if agendamento[3] == AGN_UG3_FORCAR_ESTADO_DISPONIVEL:
            self.usn.ug3.forcar_estado_disponivel()

        if agendamento[3] == AGN_UG3_FORCAR_ESTADO_INDISPONIVEL:
            self.usn.ug3.forcar_estado_indisponivel()

        if agendamento[3] == AGN_UG3_FORCAR_ESTADO_RESTRITO:
            self.usn.ug3.forcar_estado_restrito()

        if agendamento[3] == AGN_UG3_TEMPO_ESPERA_RESTRITO:
            try:
                self.usn.ug3.normalizacao_agendada = True
                novo = agendamento[5].split(":")
                tempo = (int(novo[0]) * 3600) + (int(novo[1]) * 60)
                self.usn.ug3.tempo_normalizar = tempo

            except Exception:
                logger.error(f"[AGN] Valor inválido no agendamento: {agendamento[0]} ({agendamento[3]} é inválido)")

        if agendamento[3] == AGN_UG4_ALTERAR_POT_LIMITE:
            try:
                novo = float(agendamento[5].replace(",", "."))
                self.cfg[f"pot_maxima_ug4"] = novo

            except Exception:
                logger.error(f"[AGN] Valor inválido no agendamento: {agendamento[0]} ({agendamento[3]} é inválido)")

        if agendamento[3] == AGN_UG4_FORCAR_ESTADO_MANUAL:
            self.usn.ug4.forcar_estado_manual()

        if agendamento[3] == AGN_UG4_FORCAR_ESTADO_DISPONIVEL:
            self.usn.ug4.forcar_estado_disponivel()

        if agendamento[3] == AGN_UG4_FORCAR_ESTADO_INDISPONIVEL:
            self.usn.ug4.forcar_estado_indisponivel()

        if agendamento[3] == AGN_UG4_FORCAR_ESTADO_RESTRITO:
            self.usn.ug4.forcar_estado_restrito()

        if agendamento[3] == AGN_UG4_TEMPO_ESPERA_RESTRITO:
            try:
                self.usn.ug4.normalizacao_agendada = True
                novo = agendamento[5].split(":")
                tempo = (int(novo[0]) * 3600) + (int(novo[1]) * 60)
                self.usn.ug4.tempo_normalizar = tempo

            except Exception:
                logger.error(f"[AGN] Valor inválido no agendamento: {agendamento[0]} ({agendamento[3]} é inválido)")


    def verificar_agendamentos_adufas(self, agendamento) -> "None":
        if agendamento[3] == AGN_ADCP1_FORCAR_ESTADO_DISPONIVEL:
            self.usn.ad.cp1.estado = 0

        if agendamento[3] == AGN_ADCP1_FORCAR_ESTADO_INDISPONIVEL:
            self.usn.ad.cp1.estado = 2

        if agendamento[3] == AGN_ADCP2_FORCAR_ESTADO_DISPONIVEL:
            self.usn.ad.cp2.estado = 0

        if agendamento[3] == AGN_ADCP2_FORCAR_ESTADO_INDISPONIVEL:
            self.usn.ad.cp2.estado = 2