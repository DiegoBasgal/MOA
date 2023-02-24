class State:
    """
    Classe implementa a base para estados. É "Abstrata" assim por se dizer...
    """

    def __init__(self, parent_ug: UnidadeDeGeracao):
        self.parent_ug = parent_ug
        self.logger = logging.getLogger("__main__")

    @abstractmethod
    def step(self) -> State:
        pass


class StateManual(State):
    """
    Implementação do estado StateManual

    Neste estado a máquina deve estar comletamente sobre controle do operador.
    O estado só será alterado utilizando as funções que forçam o estado.
    """

    def __init__(self, parent_ug: UnidadeDeGeracao):
        super().__init__(parent_ug)
        self.parent_ug.codigo_state = MOA_UNIDADE_MANUAL

        self.logger.info("[UG{}] Entrando no estado manual. Para retornar a operação autônoma da UG é necessário intervenção manual via interface web.".format(self.parent_ug.id))

    def step(self) -> State:
        self.parent_ug.setpoint = self.parent_ug.leitura_potencia.valor
        self.parent_ug.codigo_state = MOA_UNIDADE_MANUAL
        return self


class StateIndisponivel(State):
    """
    Implementação do estado StateIndisponivel

    Neste estado a máquina deve estar indisponibilizada, acionando os trips lógicos e elétricos da unidade de geração.
    O estado só será alterado utilizando as funções que forçam o estado.
    """

    def __init__(self, parent_ug: UnidadeDeGeracao):

        super().__init__(parent_ug)
        self.parent_ug.codigo_state = MOA_UNIDADE_INDISPONIVEL

        self.selo = False
        self.logger.warning("[UG{}] Entrando no estado indisponível. Para retornar a operação autônoma da UG é necessário intervenção manual via interface web.".format(self.parent_ug.id))
        self.parent_ug.__next_state = self

    def step(self) -> State:
        self.parent_ug.codigo_state = MOA_UNIDADE_INDISPONIVEL
        # Se as unidades estiverem paradas, ou o selo estiver ativo
        self.logger.debug(
            "[UG{}] self.parent_ug.etapa_atual -> {}".format(
                self.parent_ug.id, self.parent_ug.etapa_atual
            )
        )
        if self.parent_ug.etapa_atual == UNIDADE_PARADA or self.selo:
            # Ativar o selo interno do moa
            self.selo = True
            # Travar a unidade por sinal de TRIP
            self.parent_ug.acionar_trip_logico()
            self.parent_ug.acionar_trip_eletrico()
        else:
            # Caso contrário, deve parar a unidade
            self.parent_ug.parar()
        return self

class StateRestrito(State):
    """
    Implementação do estado StateRestrito

    Neste estado a máquina deve estar restrita para operação.
    A ug estará com trips acionados para garantir que a máquina permanecerá parada
    O estado pode ser alterado atumoaticamente.
    O perador não tem controle sobre a UG.
    """
    def __init__(self, parent_ug: UnidadeDeGeracao):
        super().__init__(parent_ug)
        self.release = False
        self.parar_timer = False
        self.deve_normalizar = False
        self.deve_indisponibilizar = False

        self.parent_ug.codigo_state = MOA_UNIDADE_RESTRITA
        self.logger.info("[UG{}] Entrando no estado restrito.".format(self.parent_ug.id))

    def step(self) -> State:
        condicionadores_ativos = []

        for condic in self.parent_ug.condicionadores_essenciais:
            if condic.ativo and condic.gravidade == DEVE_INDISPONIBILIZAR:
                condicionadores_ativos.append(condic)
                self.deve_indisponibilizar = True
            elif condic.ativo and condic.gravidade == DEVE_AGUARDAR:
                condicionadores_ativos.append(condic)

        if condicionadores_ativos:
            if self.parent_ug.norma_agendada and not self.release:
                self.logger.info("[UG{}] Normalização por tempo ativada".format(self.parent_ug.id))
                self.logger.info("[UG{}] Aguardando normalização por tempo -> Tempo definido: {}".format(self.parent_ug.id, self.parent_ug.tempo_normalizar))
                self.release = True
                Thread(target=lambda: self.espera_normalizar(self.parent_ug.tempo_normalizar)).start()
            elif not self.release:
                self.logger.debug("[UG{}] Aguardando normalização sem tempo pré-definido".format(self.parent_ug.id))

        elif not condicionadores_ativos:
            self.logger.info("[UG{}] A UG não possui mais condicionadores ativos, normalizando e retornando para o estado disponível".format(self.parent_ug.id))
            self.parent_ug.tentativas_de_normalizacao += 1
            self.parent_ug.norma_agendada = False
            self.parar_timer = True
            self.release = False
            self.parent_ug.reconhece_reset_alarmes()
            return StateDisponivel(self.parent_ug)

        if self.deve_indisponibilizar:
            self.logger.warning("[UG{}] UG detectou condicionadores com gravidade alta, indisponibilizando UG.\nCondicionadores ativos:\n{}".format(self.parent_ug.id, [d.descr for d in condicionadores_ativos]))
            self.parent_ug.norma_agendada = False
            self.parar_timer = True
            self.release = False
            return StateIndisponivel(self.parent_ug)

        elif self.deve_normalizar:
            if (self.parent_ug.tentativas_de_normalizacao > self.parent_ug.limite_tentativas_de_normalizacao):
                self.logger.warning("[UG{}] A UG estourou as tentativas de normalização, indisponibilizando UG. \n Condicionadores ativos:\n{}".format(self.parent_ug.id,[d.descr for d in condicionadores_ativos],))
                self.parent_ug.norma_agendada = False
                return StateIndisponivel(self.parent_ug)

            elif (self.parent_ug.ts_auxiliar - datetime.now(pytz.timezone("Brazil/East")).replace(tzinfo=None)).seconds > self.parent_ug.tempo_entre_tentativas:
                self.parent_ug.tentativas_de_normalizacao += 1
                self.logger.info("[UG{}] Normalizando UG (tentativa {}/{}).".format(self.parent_ug.id,self.parent_ug.tentativas_de_normalizacao,self.parent_ug.limite_tentativas_de_normalizacao,))
                self.parent_ug.ts_auxiliar = datetime.now(pytz.timezone("Brazil/East")).replace(tzinfo=None)
                self.parent_ug.reconhece_reset_alarmes()
                return self
        
        if self.parent_ug.etapa_atual == UNIDADE_PARADA:
            self.parent_ug.acionar_trip_logico()
            self.parent_ug.acionar_trip_eletrico()
        else:
            self.parent_ug.parar()
        return self

    def espera_normalizar(self, delay):
        tempo = time() + delay
        logger.debug("[UG{}] Aguardando para normalizar UG".format(self.parent_ug.id))
        while not self.parar_timer:
            sleep(max(0, tempo - time()))
            break
        self.release = False
        self.deve_normalizar = True


class StateDisponivel(State):
    """
    Implementação do estado StateDisponivel

    Neste estado a máquina deve estar disponivel para operação.
    O estado pode ser alterado atumoaticamente.
    O perador não tem controle sobre a UG.
    """

    def __init__(self, parent_ug: UnidadeDeGeracao):

        super().__init__(parent_ug)
        self.aux = 0
        self.release = False
        self.parent_ug.codigo_state = MOA_UNIDADE_DISPONIVEL
        self.logger.info("[UG{}] Entrando no estado disponível.".format(self.parent_ug.id))

    def step(self) -> State:
        self.parent_ug.codigo_state = MOA_UNIDADE_DISPONIVEL

        self.logger.debug("[UG{}] (tentativas_de_normalizacao atual: {})".format(self.parent_ug.id, self.parent_ug.tentativas_de_normalizacao))

        deve_aguardar = False
        deve_normalizar = False
        deve_indisponibilizar = False
        condicionadores_ativos = []
        
        self.parent_ug.controle_limites_operacao()

        for condicionador_essencial in self.parent_ug.condicionadores_essenciais:
            if condicionador_essencial.ativo:
                self.parent_ug.deve_ler_condicionadores = True

        if self.parent_ug.deve_ler_condicionadores:
            for condic in self.parent_ug.condicionadores_essenciais:
                if condic.ativo and condic.gravidade == DEVE_INDISPONIBILIZAR:
                    condicionadores_ativos.append(condic)
                    deve_indisponibilizar = True
                elif condic.ativo and condic.gravidade == DEVE_AGUARDAR:
                    condicionadores_ativos.append(condic)
                    deve_aguardar = True
                elif condic.ativo and condic.gravidade == DEVE_NORMALIZAR:
                    condicionadores_ativos.append(condic)
                    deve_normalizar = True

            self.parent_ug.deve_ler_condicionadores = False

        # Logar os condicionadores ativos
        if deve_indisponibilizar or deve_normalizar or deve_aguardar:
            self.logger.info("[UG{}] UG em modo disponível detectou condicionadores ativos.\nCondicionadores ativos:".format(self.parent_ug.id))
            for d in condicionadores_ativos:
                self.logger.warning("Desc: {}; Ativo: {}; Valor: {}; Gravidade: {}".format(d.descr, d.ativo, d.valor, d.gravidade))

        # Se algum condicionador deve gerar uma indisponibilidade
        if deve_indisponibilizar:
            self.logger.warning("[UG{}] Indisponibilizando UG.".format(self.parent_ug.id))
            # Vai para o estado StateIndisponivel
            return StateIndisponivel(self.parent_ug)

        if deve_aguardar:
            self.logger.warning("[UG{}] Entrando no estado Restrito até normalização da condição.".format(self.parent_ug.id))
            return StateRestrito(self.parent_ug)

        # Se algum condicionador deve gerar uma tentativa de normalizacao
        if deve_normalizar:
            # Se estourou as tentativas de normalização, vai para o estado StateIndisponivel
            if (self.parent_ug.tentativas_de_normalizacao > self.parent_ug.limite_tentativas_de_normalizacao):
                # Logar o ocorrido
                self.logger.warning("[UG{}] A UG estourou as tentativas de normalização, indisponibilizando UG. \n Condicionadores ativos:\n{}".format(self.parent_ug.id,[d.descr for d in condicionadores_ativos],))
                # Vai para o estado StateIndisponivel
                return StateIndisponivel(self.parent_ug)

            # Se não estourou as tentativas de normalização, e já se passou tempo suficiente, deve tentar normalizar
            elif (self.parent_ug.ts_auxiliar - datetime.now(pytz.timezone("Brazil/East")).replace(tzinfo=None)).seconds > self.parent_ug.tempo_entre_tentativas:
                # Adciona o contador
                self.parent_ug.tentativas_de_normalizacao += 1
                # Atualiza o timestamp
                self.parent_ug.ts_auxiliar = datetime.now(pytz.timezone("Brazil/East")).replace(tzinfo=None)
                # Logar o ocorrido
                self.logger.info("[UG{}] Normalizando UG (tentativa {}/{}).".format(self.parent_ug.id,self.parent_ug.tentativas_de_normalizacao,self.parent_ug.limite_tentativas_de_normalizacao,))
                # Reconhece e reset
                self.parent_ug.reconhece_reset_alarmes()
                return self

            # Caso contrário (se ainda não deu o tempo), não faz nada
            else:
                return self

        # Se não detectou nenhum condicionador ativo:
        else:

            self.logger.debug("[UG{}] Etapa atual: '{}', etapa_alvo: '{}'".format(self.parent_ug.id, self.parent_ug.etapa_atual, self.parent_ug.etapa_alvo))

            if self.release == True and self.aux == 1:
                self.release = False
                self.aux = 0

            # Calcula a atenuação devido aos condicionadores antes de prosseguir
            atenuacao = 0
            # Para cada condicionador
            self.logger.debug(f"[UG{self.parent_ug.id}] Lendo condicionadores_atenuadores")
            for condicionador in self.parent_ug.condicionadores_atenuadores:
                atenuacao = max(atenuacao, condicionador.valor)
                self.logger.debug(f"[UG{self.parent_ug.id}] Atenuador \"{condicionador.descr}\" -> leitura: {condicionador.leitura.valor}-> atenucao: {atenuacao}")

            # A atenuação já vem normalizada de 0 a 1, portanto
            # para ter o ganho é necessário apenas subtrair a atenuação
            ganho = 1 - atenuacao
            aux = self.parent_ug.setpoint
            if (self.parent_ug.setpoint > self.parent_ug.setpoint_minimo) and self.parent_ug.setpoint * ganho > self.parent_ug.setpoint_minimo:
                self.parent_ug.setpoint = self.parent_ug.setpoint * ganho

            elif self.parent_ug.limpeza_grade:
                self.parent_ug.setpoint_minimo = self.parent_ug.cfg["pot_limpeza_grade"]
                self.parent_ug.setpoint = self.parent_ug.setpoint_minimo

            elif (self.parent_ug.setpoint * ganho < self.parent_ug.setpoint_minimo) and (self.parent_ug.setpoint > self.parent_ug.setpoint_minimo):
                self.parent_ug.setpoint =  self.parent_ug.setpoint_minimo

            self.logger.debug(
                "[UG{}] SP {} * GAIN {} = {}".format(
                    self.parent_ug.id,
                    aux,
                    ganho,
                    self.parent_ug.setpoint,
                )
            )
            # O comportamento da UG conforme a etapa em que a mesma se encontra

            if self.parent_ug.etapa_alvo == UNIDADE_PARADA and not self.parent_ug.etapa_atual == UNIDADE_PARADA:
                # Unidade parando
                self.logger.debug("[UG{}] Unidade parando".format(self.parent_ug.id))
                # Se o setpoit for acima do mínimo
                if self.parent_ug.setpoint >= self.parent_ug.setpoint_minimo:
                    # E em seguida mandar o setpoint novo (boa prática)
                    self.parent_ug.enviar_setpoint(self.parent_ug.setpoint)

            elif self.parent_ug.etapa_alvo == UNIDADE_SINCRONIZADA and not self.parent_ug.etapa_atual == UNIDADE_SINCRONIZADA:
                # Unidade sincronizando
                self.logger.debug("[UG{}] Unidade sincronizando".format(self.parent_ug.id))
                if self.release == False and self.aux == 0:
                    Thread(target=lambda: self.verificar_partindo()).start()
                    self.aux = 1
                # Se potência = 0, impedir,
                if self.parent_ug.setpoint == 0:
                    self.logger.warning("[UG{}] A UG estava sincronizando com SP zerado, parando a UG.".format(self.parent_ug.id))
                    self.parent_ug.parar()
                else:
                    self.parent_ug.partir()
                # Se não fazer nada

            elif self.parent_ug.etapa_atual == UNIDADE_PARADA:
                # Unidade parada
                self.logger.debug("[UG{}] Unidade parada".format(self.parent_ug.id))
                # Se o setpoit for acima do mínimo
                if self.parent_ug.setpoint >= self.parent_ug.setpoint_minimo:
                    # Deve partir a UG
                    self.parent_ug.partir()
                    # E em seguida mandar o setpoint novo (boa prática)
                    self.parent_ug.enviar_setpoint(self.parent_ug.setpoint)

            elif self.parent_ug.etapa_atual == UNIDADE_SINCRONIZADA:
                # Unidade sincronizada
                self.logger.debug("[UG{}] Unidade sincronizada".format(self.parent_ug.id))

                # Unidade sincronizada significa que ela está normalizada, logo zera o contador de tentativas
                if not self.parent_ug.aux_tempo_sincronizada:
                    self.parent_ug.aux_tempo_sincronizada = datetime.now(pytz.timezone("Brazil/East")).replace(tzinfo=None)

                elif (datetime.now(pytz.timezone("Brazil/East")).replace(tzinfo=None) - self.parent_ug.aux_tempo_sincronizada).seconds >= 300:
                    self.parent_ug.tentativas_de_normalizacao = 0
                # Se o setpoit estiver abaixo do mínimo
                if self.parent_ug.setpoint == 0:
                    # Deve manter a UG
                    self.parent_ug.parar()
                else:
                    # Caso contrário, mandar o setpoint novo
                    self.parent_ug.enviar_setpoint(self.parent_ug.setpoint)

            elif self.parent_ug.etapa_atual not in UNIDADE_LISTA_DE_ETAPAS:
                # Etapa inconsistente
                # Logar o ocorrido
                self.logger.warning("[UG{}] UG em etapa inconsistente. (etapa_atual:{})".format(self.parent_ug.id,self.parent_ug.etapa_atual,))

                # Vai para o estado StateIndisponivel
                # return StateIndisponivel(self.parent_ug)

            if not self.parent_ug.etapa_atual == UNIDADE_SINCRONIZADA:
                self.parent_ug.aux_tempo_sincronizada = None

            return self
    
    def verificar_partindo(self) -> bool:
        timer = time() + 600
        try:
            self.logger.debug("Iniciando o timer de verificação de partida")
            while time() < timer:
                if self.parent_ug.etapa_atual == UNIDADE_SINCRONIZADA:
                    self.logger.debug("[UG{}] Unidade sincronizada. Saindo do timer de verificação de partida".format(self.parent_ug.id))
                    self.release = True
                    return True
            self.logger.debug("[UG{}] A Unidade estourou o timer de verificação de partida, adicionando condição para normalizar".format(self.parent_ug.id))
            self.parent_ug.clp.write_single_coil(REG_UG1_ComandosDigitais_MXW_EmergenciaViaSuper, [1 if self.parent_ug.id==1 else 0]) 
            self.parent_ug.clp.write_single_coil(REG_UG2_ComandosDigitais_MXW_EmergenciaViaSuper, [1 if self.parent_ug.id==2 else 0])
            self.release = True

        except Exception as e:
            raise e

        return False