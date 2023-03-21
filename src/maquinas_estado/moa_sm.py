import logging

logger = logging.getLogger("__main__")

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
            logger.warning("Estado ({}) levantou uma exception: {}".format(self.state, repr(e)))
            logger.debug("Traceback: {}".format(traceback.format_exc()))
            self.em_falha_critica = True
            self.state = FalhaCritica()

class State:
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def run(self) -> object:
        return self


class FalhaCritica(State):
    """
    Lida com a falha na inicialização do MOA
    :return: None
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        logger.critical("Falha crítica MOA. Exiting...")
        sys.exit(1)


class Pronto(State):
    """
    MOA está pronto, agora ele deve atualizar a vars
    :return: State
    """

    def __init__(self, instancia_usina, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.n_tentativa = 0
        self.usina = instancia_usina
        self.usina.state_moa = 3

    def run(self):

        if self.n_tentativa >= 2:
            return FalhaCritica()
        else:

            try:
                self.usina.ler_valores()
                if self.usina.TDA_Offline:
                    return OperacaoTDAOffline(self.usina)
                else:
                    return ValoresInternosAtualizados(self.usina)

            except Exception as e:
                self.n_tentativa += 1
                logger.error(
                    "Erro durante a comunicação do MOA com a usina. Tentando novamente em {}s (tentativa{}/3)."
                    " Exception: {}.".format(
                        self.usina.cfg["timeout_padrao"] * self.n_tentativa,
                        self.n_tentativa,
                        repr(e),
                    )
                )
                logger.debug("Traceback: {}".format(traceback.format_exc()))
                sleep(self.usina.cfg["timeout_padrao"] * self.n_tentativa)
                return self


class ValoresInternosAtualizados(State):
    def __init__(self, instancia_usina, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.usina = instancia_usina
        DataBank.set_words(REG_MB["MOA"]["PAINEL_LIDO"], [1])
        self.usina.heartbeat()
        self.deve_ler_condicionadores=False
        self.habilitar_emerg_condic_e=False
        self.habilitar_emerg_condic_c=False

    def run(self):
        """Decidir para qual modo de operação o sistema deve ir"""

        """
        Aqui a ordem do checks importa, e muito.
        """

        # atualizar arquivo das configurações
        global aux
        global deve_normalizar
        self.usina.TDA_Offline = False

        with open(os.path.join(os.path.dirname(__file__), "config.json"), "w") as file:
            json.dump(self.usina.cfg, file, indent=4)

        for condicionador_essencial in self.usina.condicionadores_essenciais:
            if condicionador_essencial.ativo:
                self.deve_ler_condicionadores=True

        if self.usina.avisado_em_eletrica or self.deve_ler_condicionadores==True:
            for condicionador_essencial in self.usina.condicionadores_essenciais:
                if condicionador_essencial.ativo and condicionador_essencial.gravidade >= DEVE_INDISPONIBILIZAR:
                    self.habilitar_emerg_condic_e=True
                elif condicionador_essencial.ativo and condicionador_essencial.gravidade == DEVE_NORMALIZAR:
                    deve_normalizar=True
                    self.habilitar_emerg_condic_e=False
                else:
                    deve_normalizar=False
                    self.habilitar_emerg_condic_e=False
            
            for condicionador in self.usina.condicionadores:
                if condicionador.ativo and condicionador.gravidade >= DEVE_INDISPONIBILIZAR:
                    self.habilitar_emerg_condic_c=True
                elif condicionador.ativo and condicionador.gravidade == DEVE_NORMALIZAR:
                    self.habilitar_emerg_condic_c=False
                    deve_normalizar=True
                else:
                    deve_normalizar=False
                    self.habilitar_emerg_condic_c=False
            
            if self.habilitar_emerg_condic_e or self.habilitar_emerg_condic_c:
                logger.info("Condicionadores ativos com gravidade alta!")
                return Emergencia(self.usina)

        if deve_normalizar:
            if (not self.usina.normalizar_emergencia()) and self.usina.tensao_ok==False and aux==0:
                logger.warning("Tensão da linha fora do limite ")
                aux = 1
                threading.Thread(target=lambda: self.usina.aguardar_tensao(600)).start()

            elif self.usina.timer_tensao:
                aux = 0
                deve_normalizar = None
                self.usina.timer_tensao = None

            elif self.usina.timer_tensao==False:
                aux = 0
                deve_normalizar = None
                self.usina.timer_tensao = None
                logger.critical("O tempo de normalização da linha excedeu o limite! (10 min)")
                return Emergencia(self.usina)

        if self.usina.clp_emergencia_acionada:
            logger.info("Comando recebido: habilitando modo de emergencia.")
            sleep(2)
            return Emergencia(self.usina)

        if self.usina.db_emergencia_acionada:
            logger.info("Comando recebido: habilitando modo de emergencia.")
            sleep(2)
            return Emergencia(self.usina)

        # Verificamos se existem agendamentos
        if len(self.usina.get_agendamentos_pendentes()) > 0:
            return AgendamentosPendentes(self.usina)

        # Em seguida com o modo manual (não autonomo)
        if not self.usina.modo_autonomo:
            logger.debug("Comando recebido: desabilitar modo autonomo.")
            sleep(2)
            return ModoManualAtivado(self.usina)

        # Se não foi redirecionado ainda,
        # assume-se que o MOA deve executar de modo autônomo

        # Verifica-se então a situação do reservatório
        if self.usina.aguardando_reservatorio:
            if self.usina.nv_montante > self.usina.cfg["nv_alvo"]:
                logger.debug("Reservatorio dentro do nivel de trabalho")
                self.usina.aguardando_reservatorio = 0
                return ReservatorioNormal(self.usina)

        if self.usina.nv_montante < self.usina.cfg["nv_minimo"]:
            self.usina.aguardando_reservatorio = 1
            logger.info("Reservatorio abaixo do nivel de trabalho")
            return ReservatorioAbaixoDoMinimo(self.usina)

        if self.usina.nv_montante >= self.usina.cfg["nv_maximo"]:
            return ReservatorioAcimaDoMaximo(self.usina)

        # Se estiver tudo ok:
        return ReservatorioNormal(self.usina)


class Emergencia(State):
    def __init__(self, instancia_usina, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.em_sm_acionada = datetime.now(pytz.timezone("Brazil/East")).replace(tzinfo=None)
        logger.warning(
            "Usina entrado em estado de emergência (Timestamp: {})".format(
                self.em_sm_acionada
            )
        )
        self.usina = instancia_usina
        self.n_tentativa = 0
        self.usina.escrever_valores()
        self.usina.heartbeat()
        self.nao_ligou = True

    def run(self):
        self.usina.heartbeat()
        self.n_tentativa += 1
        if self.n_tentativa > 2:
            logger.warning("Numero de tentaivas de normalização excedidas, entrando em modo manual.")
            self.usina.entrar_em_modo_manual()
            self.usina.heartbeat()
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

            self.usina.ler_valores()
            # Ler condiconadores
            deve_indisponibilizar = False
            deve_normalizar = False
            condicionadores_ativos = []
            
            for condicionador_essencial in self.usina.condicionadores_essenciais:
                if condicionador_essencial.ativo and condicionador_essencial.gravidade == DEVE_INDISPONIBILIZAR:
                    condicionadores_ativos.append(condicionador_essencial)
                    deve_indisponibilizar = True
                elif condicionador_essencial.gravidade == DEVE_NORMALIZAR:
                    condicionadores_ativos.append(condicionador_essencial)
                    deve_normalizar = True

            for condicionador in self.usina.condicionadores:
                if condicionador.ativo and condicionador.gravidade == DEVE_INDISPONIBILIZAR:
                    condicionadores_ativos.append(condicionador)
                    deve_indisponibilizar=True
                elif condicionador.gravidade == DEVE_NORMALIZAR:
                    condicionadores_ativos.append(condicionador)
                    deve_indisponibilizar=False

            if (self.usina.clp_emergencia_acionada or deve_normalizar or deve_indisponibilizar):
                try:

                    # Se algum condicionador deve gerar uma indisponibilidade
                    if deve_indisponibilizar:
                        # Logar os condicionadores ativos
                        logger.critical(
                            "[USN] USN detectou condicionadores ativos, passando USINA para manual e ligando por VOIP.\nCondicionadores ativos:\n{}".format(
                                [d.descr for d in condicionadores_ativos]
                            )
                        )
                        # Vai para o estado StateIndisponivel
                        self.usina.entrar_em_modo_manual()
                        return ModoManualAtivado(self.usina)

                    elif deve_normalizar:
                        logger.debug("Aguardando antes de tentar normalizar novamente (5s)")
                        sleep(5)
                        logger.info("Normalizando usina. (tentativa{}/2) (limite entre tentaivas: {}s)".format(self.n_tentativa, self.usina.cfg["timeout_normalizacao"]))
                        self.usina.deve_normalizar_forcado=True
                        self.usina.normalizar_emergencia()
                        self.usina.ler_valores()
                        return self

                    else:
                        logger.debug("Nenhum condicionador relevante ativo...")
                        self.usina.ler_valores()
                        return ControleRealizado(self.usina)

                except Exception as e:
                    logger.error(
                        "Erro durante a comunicação do MOA com a usina. Exception: {}.".format(
                            repr(e)
                        )
                    )
                    logger.debug("Traceback: {}".format(traceback.format_exc()))
                return self
            else:
                self.usina.ler_valores()
                logger.info("Usina normalizada")
                return ControleRealizado(self.usina)


class ModoManualAtivado(State):
    def __init__(self, instancia_usina, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.usina = instancia_usina
        self.usina.modo_autonomo = False
        self.usina.escrever_valores()
        logger.info("Usina em modo manual, deve-se alterar via painel ou interface web.")

    def run(self):
        self.usina.ler_valores()
        DataBank.set_words(REG_MB["MOA"]["PAINEL_LIDO"], [1])
        self.usina.ug1.setpoint = self.usina.ug1.leitura_potencia.valor
        self.usina.ug2.setpoint = self.usina.ug2.leitura_potencia.valor

        self.usina.controle_ie = (self.usina.ug1.setpoint + self.usina.ug2.setpoint) / self.usina.cfg["pot_maxima_alvo"]

        self.usina.heartbeat()
        sleep(1 / ESCALA_DE_TEMPO)
        if self.usina.modo_autonomo:
            logger.debug("Comando recebido: habilitar modo autonomo.")
            sleep(2)
            logger.info("Usina voltou para o modo Autonomo")
            self.usina.db.update_habilitar_autonomo()
            self.usina.ler_valores()
            if (self.usina.clp_emergencia_acionada == 1 or self.usina.db_emergencia_acionada == 1):
                self.usina.normalizar_emergencia()
            self.usina.heartbeat()
            return ControleRealizado(self.usina)

        if len(self.usina.get_agendamentos_pendentes()) > 0:
            return AgendamentosPendentes(self.usina)

        return self


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
        self.usina.distribuir_potencia(0)
        if self.usina.nv_montante_recente <= self.usina.cfg["nv_fundo_reservatorio"]:
            if not usina.ping(self.usina.cfg["TDA_slave_ip"]):
                logger.warning("Sem comunicação com CLP TDA, entrando no modo de operação Offline")
                self.usina.TDA_Offline = True
                return OperacaoTDAOffline(self.usina)
            else:
                logger.critical("Nivel montante ({:3.2f}) atingiu o fundo do reservatorio!".format(self.usina.nv_montante_recente))
                return Emergencia(self.usina)
        for ug in self.usina.ugs:
            print("")
            ug.step()
        return ControleRealizado(self.usina)


class ReservatorioAcimaDoMaximo(State):
    def __init__(self, instancia_usina, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.usina = instancia_usina

    def run(self):
        if self.usina.nv_montante_recente >= self.usina.cfg["nv_maximorum"]:
            self.usina.distribuir_potencia(0)
            logger.critical("Nivel montante ({:3.2f}) atingiu o maximorum!".format(self.usina.nv_montante_recente))
            return Emergencia(self.usina)
        else:
            self.usina.distribuir_potencia(self.usina.cfg["pot_maxima_usina"])
            self.usina.controle_ie = 0.5
            self.usina.controle_i = 0.5
            for ug in self.usina.ugs:
                print("")
                ug.step()
            return ControleRealizado(self.usina)


class ReservatorioNormal(State):
    def __init__(self, instancia_usina, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.usina = instancia_usina

    def run(self):

        self.usina.controle_normal()
        for ug in self.usina.ugs:
            print("")
            ug.step()
        return ControleRealizado(self.usina)

class OperacaoTDAOffline(State):
    def __init__(self, instancia_usina, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.usina = instancia_usina
        self.deve_ler_condicionadores = False
        self.habilitar_emerg_condic_e = False
        self.habilitar_emerg_condic_c = False

    def run(self):
        global aux
        global deve_normalizar
        self.usina.TDA_Offline = True

        for condicionador_essencial in self.usina.condicionadores_essenciais:
            if condicionador_essencial.ativo:
                self.deve_ler_condicionadores=True

        if self.usina.avisado_em_eletrica or self.deve_ler_condicionadores==True:
            for condicionador_essencial in self.usina.condicionadores_essenciais:
                if condicionador_essencial.ativo and condicionador_essencial.gravidade >= DEVE_INDISPONIBILIZAR:
                        self.habilitar_emerg_condic_e=True
                elif condicionador_essencial.ativo and condicionador_essencial.gravidade == DEVE_NORMALIZAR:
                    deve_normalizar=True
                    self.habilitar_emerg_condic_e=False
                else:
                    deve_normalizar=False
                    self.habilitar_emerg_condic_e=False
            
            for condicionador in self.usina.condicionadores:
                if condicionador.ativo and condicionador.gravidade >= DEVE_INDISPONIBILIZAR:
                    self.habilitar_emerg_condic_c=True
                elif condicionador.ativo and condicionador.gravidade == DEVE_NORMALIZAR:
                    self.habilitar_emerg_condic_c=False
                    deve_normalizar=True
                else:
                    deve_normalizar=False
                    self.habilitar_emerg_condic_c=False
            
            if self.habilitar_emerg_condic_e or self.habilitar_emerg_condic_c:
                logger.info("Condicionadores ativos com gravidade alta!")
                return Emergencia(self.usina)

        if deve_normalizar:
            if (not self.usina.normalizar_emergencia()) and self.usina.tensao_ok==False and aux==0:
                logger.warning("Tensão da linha fora do limite ")
                aux = 1
                threading.Thread(target=lambda: self.usina.aguardar_tensao(20)).start()

            elif self.usina.timer_tensao:
                aux = 0
                deve_normalizar = None
                self.usina.timer_tensao = None

            elif self.usina.timer_tensao==False:
                aux = 0
                deve_normalizar = None
                self.usina.timer_tensao = None
                logger.warning("O tempo de normalização da linha excedeu o limite! (10 min)")
                return Emergencia(self.usina)
        
        if not self.usina.modo_autonomo:
            logger.info("Comando recebido: desabilitar modo autonomo.")
            sleep(2)
            return ModoManualAtivado(self.usina)

        if len(self.usina.get_agendamentos_pendentes()) > 0:
            return AgendamentosPendentes(self.usina)

        for ug in self.usina.ugs:
            print("")
            ug.controle_press_turbina()
            ug.step()

        return ControleRealizado(self.usina)

class ControleRealizado(State):
    def __init__(self, instancia_usina, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.usina = instancia_usina

    def run(self):
        logger.debug("HB")
        self.usina.heartbeat()
        logger.debug("Escrevendo valores")
        self.usina.escrever_valores()
        return Pronto(self.usina)
