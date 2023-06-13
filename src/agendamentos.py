from usina import *
from src.banco_dados import Database

class Agendamentos(Usina):
    def __init__(self, cfg=None, db: BancoDados=None):
        super().__init__(cfg, db)

    def obter_agendamentos(self):
        agendamentos_pendentes = []
        agendamentos = self.db.get_agendamentos_pendentes()

        for agendamento in agendamentos:
            ag = list(agendamento)
            ag[1] = ag[1] - timedelta(0, 60 * 60 * 3)
            agendamentos_pendentes.append(ag)
        return agendamentos_pendentes

    def verificar_agendamentos(self):
        agora = self.get_time()
        agendamentos = self.obter_agendamentos()

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

        logger.debug(agendamentos)

        if len(agendamentos) == 0:
            return True

        self.agendamentos_atrasados = 0

        for agendamento in agendamentos:
            # ag -> [id, data, observacao, comando_id, executado, campo_auxiliar, criado_por, modificado_por, ts_criado, ts_modificado]
            if agora > agendamento[1]:
                segundos_adiantados = 0
                segundos_passados = (agora - agendamento[1]).seconds
                logger.debug(segundos_passados)
            else:
                segundos_adiantados = (agendamento[1] - agora).seconds
                segundos_passados = 0


            if segundos_passados > 240:
                logger.info(f"Agendamento #{agendamento[0]} Atrasado! ({agendamento[3]}).")
                self.agendamentos_atrasados += 1

            if segundos_passados > 300 or self.agendamentos_atrasados > 3:
                logger.warning("Os agendamentos estão muito atrasados! Acionando emergência.")
                self.con.acionar_emergencia()
                return False

            if segundos_adiantados <= 60 and not bool(agendamento[4]):

                logger.info(f"Executando agendamento: {agendamento[0]}\n \
                    Comando: {AGN_STR_DICT[agendamento[3]]}\n \
                    Data: {agendamento[1]}\n \
                    Observação: {agendamento[2]}\n \
                    {f'Valor: {agendamento[5]}' if agendamento[5] is not None else ...}"
                )

                if (self.modo_autonomo and not self.db.get_executabilidade(agendamento[3])["executavel_em_autmoatico"]):
                    obs = "Este agendamento não tem efeito com o módulo em modo autônomo. Executado sem realizar nenhuma ação"
                    logger.debug(obs)
                    self.db.update_agendamento(agendamento[0], True, obs)
                    return True

                if (not self.modo_autonomo and not self.db.get_executabilidade(agendamento[3])["executavel_em_manual"]):
                    obs = "Este agendamento não tem efeito com o módulo em modo manual. Executado sem realizar nenhuma ação"
                    logger.debug(obs)
                    self.db.update_agendamento(agendamento[0], True, obs)
                    return True

                if agendamento[3] == AGENDAMENTO_INDISPONIBILIZAR:
                    logger.info("Indisponibilizando a usina (comando via agendamento).")
                    for ug in self.ugs:
                        ug.forcar_estado_indisponivel()
                    while (not self.ugs[0].etapa_atual == UG_PARADA and not self.ugs[1].etapa_atual == UG_PARADA):
                        self.ler_valores()
                        logger.debug("Indisponibilizando Usina... \n(freezing for 10 seconds)")
                        sleep(10)
                    self.con.acionar_emergencia()
                    logger.debug("Emergência pressionada após indizponibilização agendada mudando para modo manual para evitar normalização automática.")
                    self.modo_autonomo = 0

                if agendamento[3] == AGENDAMENTO_ALTERAR_NV_ALVO:
                    try:
                        novo = float(agendamento[5].replace(",", "."))
                    except Exception as e:
                        logger.info(f"Valor inválido no comando #{agendamento[0]} ({agendamento[3]} é inválido).")

                    self.cfg["nv_alvo"] = novo

                if agendamento[3] == AGENDAMENTO_BAIXAR_POT_UGS_MINIMO:
                    try:
                        for ug in self.ugs:
                            self.cfg[f"pot_maxima_ug{ug.id}"] = self.cfg["pot_limpeza_grade"]

                            if ug.etapa_atual == UG_PARADA or ug.etapa_atual == UG_PARANDO:
                                logger.debug(f"A UG{ug.id} já está no estado parada/parando.")
                            else:
                                ug.limpeza_grade = True
                                logger.debug(f"Enviando o setpoint de limpeza de grade ({self.cfg['pot_limpeza_grade']}) para a UG{ug.id}")

                    except Exception as e:
                        logger.debug(f"Traceback: {repr(e)}")

                if agendamento[3] == AGENDAMENTO_NORMALIZAR_POT_UGS_MINIMO:
                    try:
                        for ug in self.ugs:
                            self.cfg[f"pot_maxima_ug{ug.id}"] = self.cfg["pot_maxima_ug"]

                            ug.limpeza_grade = False
                            ug.enviar_setpoint(self.cfg["pot_maxima_ug"])

                    except Exception as e:
                        logger.debug(f"Traceback: {repr(e)}")

                if agendamento[3] == AGENDAMENTO_UG1_ALTERAR_POT_LIMITE:
                    try:
                        novo = float(agendamento[5].replace(",", "."))
                        self.cfg["pot_maxima_ug1"] = novo
                        self.ug1.pot_disponivel = novo
                    except Exception as e:
                        logger.info(f"Valor inválido no comando #{agendamento[0]} ({agendamento[3]} é inválido).")

                if agendamento[3] == AGENDAMENTO_UG1_FORCAR_ESTADO_MANUAL:
                    self.ug1.forcar_estado_manual()

                if agendamento[3] == AGENDAMENTO_UG1_FORCAR_ESTADO_DISPONIVEL:
                    self.ug1.forcar_estado_disponivel()

                if agendamento[3] == AGENDAMENTO_UG1_FORCAR_ESTADO_INDISPONIVEL:
                    self.ug1.forcar_estado_indisponivel()

                if agendamento[3] == AGENDAMENTO_UG1_FORCAR_ESTADO_RESTRITO:
                    self.ug1.forcar_estado_restrito()
                
                if agendamento[3] == AGENDAMENTO_UG1_TEMPO_ESPERA_RESTRITO:
                    try:
                        ug.normalizacao_agendada = True
                        novo = agendamento[5].split(":")
                        tempo = (int(novo[0]) * 3600) + (int(novo[1]) * 60)
                        ug.tempo_normalizar = tempo

                    except Exception:
                        logger.exception(f"Valor inválido no agendamento: {agendamento[0]} ({agendamento[3]} é inválido)")

                if agendamento[3] == AGENDAMENTO_UG2_ALTERAR_POT_LIMITE:
                    try:
                        novo = float(agendamento[5].replace(",", "."))
                        self.cfg["pot_maxima_ug2"] = novo
                        self.ug2.pot_disponivel = novo
                    except Exception as e:
                        logger.info(f"Valor inválido no comando #{agendamento[0]} ({agendamento[3]} é inválido).")

                if agendamento[3] == AGENDAMENTO_UG2_FORCAR_ESTADO_MANUAL:
                    self.ug2.forcar_estado_manual()

                if agendamento[3] == AGENDAMENTO_UG2_FORCAR_ESTADO_DISPONIVEL:
                    self.ug2.forcar_estado_disponivel()

                if agendamento[3] == AGENDAMENTO_UG2_FORCAR_ESTADO_INDISPONIVEL:
                    self.ug2.forcar_estado_indisponivel()

                if agendamento[3] == AGENDAMENTO_UG2_FORCAR_ESTADO_RESTRITO:
                    self.ug2.forcar_estado_restrito()

                if agendamento[3] == AGENDAMENTO_UG3_ALTERAR_POT_LIMITE:
                    try:
                        novo = float(agendamento[5].replace(",", "."))
                        self.cfg["pot_maxima_ug3"] = novo
                        self.ug3.pot_disponivel = novo
                    except Exception as e:
                        logger.info(f"Valor inválido no comando #{agendamento[0]} ({agendamento[3]} é inválido).")

                if agendamento[3] == AGENDAMENTO_UG3_FORCAR_ESTADO_MANUAL:
                    self.ug3.forcar_estado_manual()

                if agendamento[3] == AGENDAMENTO_UG3_FORCAR_ESTADO_DISPONIVEL:
                    self.ug3.forcar_estado_disponivel()

                if agendamento[3] == AGENDAMENTO_UG3_FORCAR_ESTADO_INDISPONIVEL:
                    self.ug3.forcar_estado_indisponivel()

                if agendamento[3] == AGENDAMENTO_UG3_FORCAR_ESTADO_RESTRITO:
                    self.ug3.forcar_estado_restrito()

                if agendamento[3] == AGENDAMENTO_ALTERAR_POT_LIMITE_TODAS_AS_UGS:
                    try:
                        novo = float(agendamento[5].replace(",", "."))
                        self.cfg["pot_maxima_alvo"] = novo
                        self.db._open()
                        self.db.execute(f"UPDATE parametros_moa_parametrosusina SET pot_nominal = {novo}")
                        self.db._close()
                    except Exception as e:
                        logger.info(f"Valor inválido no comando #{agendamento[0]} ({agendamento[3]} é inválido).")

                self.db.update_agendamento(int(agendamento[0]), 1)
                logger.info(f"O comando #{agendamento[0]} - {agendamento[5]} foi executado.")
                self.con.somente_reconhecer_emergencia()
                self.escrever_valores()
