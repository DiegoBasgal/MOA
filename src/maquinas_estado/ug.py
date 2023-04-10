from src.UnidadeDeGeracao import *
from src.UG1 import UnidadeDeGeracao1
from src.UG2 import UnidadeDeGeracao2
from src.UG3 import UnidadeDeGeracao3

logger = logging.getLogger("__main__")

class State:
    """
    Classe implementa a base para estados. É "Abstrata" assim por se dizer...
    """

    def __init__(self, parent_ug: UnidadeDeGeracao | UnidadeDeGeracao1 | UnidadeDeGeracao2 | UnidadeDeGeracao3):
        self.parent_ug = parent_ug

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
        logger.info(f"[UG{self.parent_ug.id}] Entrando no estado: \"Manual\". Para retornar a operação autônoma, favor agendar na interface web")

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
        logger.info(f"[UG{self.parent_ug.id}] Entrando no estado: \"Indisponível\". Para retornar a operação autônoma, favor agendar na interface web")
        self.parent_ug.__next_state = self
        self.parent_ug.release_timer = True

    def step(self) -> State:
        self.parent_ug.codigo_state = MOA_UNIDADE_INDISPONIVEL
        # Se as unidades estiverem paradas, ou o selo estiver ativo
        logger.debug(f"[UG{self.parent_ug.id}] self.parent_ug.etapa_atual -> {self.parent_ug.etapa_atual}")

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
        self.parent_ug.codigo_state = MOA_UNIDADE_RESTRITA
        logger.info(f"[UG{self.parent_ug.id}] Entrando no estado: \"Restrito\"")

    def step(self) -> State:
        self.parent_ug.codigo_state = MOA_UNIDADE_RESTRITA
        # Ler condiconadores

        # Devemos estudar quais os condicionadores que serão lidos no modo restrito para poder re-colocar a leitura de condicionadores abaixo.
        
        deve_indisponibilizar = False
        deve_normalizar = False
        condicionadores_ativos = []

        if self.parent_ug.deve_ler_condicionadores:
            for condicionador_essencial in self.parent_ug.condicionadores_essenciais:
                if condicionador_essencial.ativo:
                    if condicionador_essencial >= DEVE_INDISPONIBILIZAR:
                        condicionadores_ativos.append(condicionador_essencial)
                        deve_indisponibilizar = True

            for condicionador in self.parent_ug.condicionadores:
                if condicionador.ativo: 
                    if condicionador.gravidade>=DEVE_INDISPONIBILIZAR:
                        condicionadores_ativos.append(condicionador)
                        deve_indisponibilizar = True

        # Se algum condicionador deve gerar uma indisponibilidade
        if deve_indisponibilizar:
            # Logar os condicionadores ativos
            logger.warning(f"[UG{self.parent_ug.id}] UG em modo Restrito detectou condicionadores ativos, indisponibilizando UG.\nCondicionadores ativos:\n{[d.descr for d in condicionadores_ativos]}")
            # Vai para o estado StateIndisponivel
            return StateIndisponivel(self.parent_ug)

        # Se a unidade estiver parada, travar a mesma por sinal de TRIP
        if self.parent_ug.etapa_atual == UNIDADE_PARADA:
            self.parent_ug.acionar_trip_logico()
            self.parent_ug.acionar_trip_eletrico()
        # Caso contrário, deve parar a unidade
        else:
            self.parent_ug.parar()
        return self


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
        logger.info(f"[UG{self.parent_ug.id}] Entrando no estado: \"Disponível\"")
        self.parent_ug.tentativas_de_normalizacao = 0

    def step(self) -> State:
        self.parent_ug.codigo_state = MOA_UNIDADE_DISPONIVEL
        self.parent_ug.controle_limites_operacao()

        deve_normalizar = False
        deve_indisponibilizar = False
        condicionadores_ativos = []

        for condic in self.parent_ug.condicionadores_essenciais:
            if condic.ativo:
                self.parent_ug.deve_ler_condicionadores = True
                break

        if self.parent_ug.deve_ler_condicionadores:
            for condic in self.parent_ug.condicionadores_essenciais:
                if condic.ativo and condic.gravidade == DEVE_NORMALIZAR:
                    condicionadores_ativos.append(condic)
                    deve_normalizar = True
                if condic.ativo and condic.gravidade == DEVE_INDISPONIBILIZAR:
                    condicionadores_ativos.append(condic)
                    deve_indisponibilizar = True

            for condic in self.parent_ug.condicionadores:
                if condic.ativo and condic.gravidade == DEVE_NORMALIZAR:
                    condicionadores_ativos.append(condic)
                    deve_normalizar = True
                if condic.ativo and condic.gravidade == DEVE_INDISPONIBILIZAR:
                    condicionadores_ativos.append(condic)
                    deve_indisponibilizar = True

        if deve_indisponibilizar or deve_normalizar:
            logger.info(f"[UG{self.parent_ug.id}] UG em modo disponível detectou condicionadores ativos:")
            for d in condicionadores_ativos:
                logger.info(f"[UG{self.parent_ug.id}] Registrador: {d.descr}, Gravidade: {CONDIC_STR_DCT[d.gravidade] if d.gravidade in CONDIC_STR_DCT else 'Desconhecida'}")

        # Se algum condicionador deve gerar uma indisponibilidade
        if deve_indisponibilizar:
            logger.warning(f"[UG{self.parent_ug.id}] Indisponibilizando UG por gravidade.")
            # Vai para o estado StateIndisponivel
            self.parent_ug.deve_ler_condicionadores = False
            return StateIndisponivel(self.parent_ug)

        # Se algum condicionador deve gerar uma tentativa de normalizacao
        if deve_normalizar:
            # Se estourou as tentativas de normalização, vai para o estado StateIndisponivel
            if (self.parent_ug.tentativas_de_normalizacao > self.parent_ug.limite_tentativas_de_normalizacao):
                # Logar o ocorrido
                logger.warning(f"[UG{self.parent_ug.id}] Indisponibilizando UG por tentativas de normalização.")
                # Vai para o estado StateIndisponivel
                self.parent_ug.deve_ler_condicionadores = False
                return StateIndisponivel(self.parent_ug)

            elif self.parent_ug.etapa_atual == UNIDADE_PARANDO or self.parent_ug.etapa_atual == UNIDADE_SINCRONIZANDO:
                logger.debug(f"[UG{self.parent_ug.id}] Esperando para normalizar")
                self.parent_ug.deve_ler_condicionadores = False
                return self

            # Se não estourou as tentativas de normalização, e já se passou tempo suficiente, deve tentar normalizar
            elif (self.parent_ug.ts_auxiliar - datetime.now(pytz.timezone("Brazil/East")).replace(tzinfo=None)).seconds > self.parent_ug.tempo_entre_tentativas:
                # Adciona o contador
                self.parent_ug.tentativas_de_normalizacao += 1
                # Atualiza o timestamp
                self.parent_ug.ts_auxiliar = datetime.now(pytz.timezone("Brazil/East")).replace(tzinfo=None)
                # Logar o ocorrido
                logger.info(f"[UG{self.parent_ug.id}] Normalizando UG (tentativa {self.parent_ug.tentativas_de_normalizacao}/{self.parent_ug.limite_tentativas_de_normalizacao}).")
                # Reconhece e reset
                self.parent_ug.reconhece_reset_alarmes()
                self.parent_ug.deve_ler_condicionadores = False
                return self

                # Caso contrário (se ainda não deu o tempo), não faz nada
            else:
                self.parent_ug.deve_ler_condicionadores = False
                return self

        # Se não detectou nenhum condicionador ativo:
        else:
            logger.debug(f"[UG{self.parent_ug.id}] Etapa atual: \"{UNIDADE_DICT_ETAPAS[self.parent_ug.etapa_atual]}\"")

            if self.release == True and self.aux == 1:
                self.release = False
                self.aux = 0

            # Calcula a atenuação devido aos condicionadores antes de prosseguir
            atenuacao = 0
            # Para cada condicionador
            for condicionador in self.parent_ug.condicionadores_atenuadores:
                atenuacao = max(atenuacao, condicionador.valor)
                logger.debug(f"[UG{self.parent_ug.id}] Atenuador \"{condicionador.descr}\" -> Atenuação: {atenuacao} / Leitura: {condicionador.leitura.valor}")

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

            logger.debug(f"[UG{self.parent_ug.id}] SP {aux} * GANHO {ganho} = {self.parent_ug.setpoint}")
            # O comportamento da UG conforme a etapa em que a mesma se encontra

            if self.parent_ug.etapa_atual == UNIDADE_PARANDO:
                # Unidade parando
                # Se o setpoit for acima do mínimo
                if self.parent_ug.setpoint >= self.parent_ug.setpoint_minimo:
                    # E em seguida mandar o setpoint novo (boa prática)
                    self.parent_ug.enviar_setpoint(self.parent_ug.setpoint)

            elif self.parent_ug.etapa_atual == UNIDADE_SINCRONIZANDO:
                # Unidade sincronizando
                if self.release == False and self.aux == 0:
                    Thread(target=lambda: self.verificar_partindo()).start()
                    self.aux = 1
                # Se potência = 0, impedir,
                if self.parent_ug.setpoint == 0:
                    logger.warning(f"[UG{self.parent_ug.id}] A UG estava sincronizando com SP zerado, parando a UG.")
                    self.parent_ug.parar()
                else:
                    self.parent_ug.enviar_setpoint(self.parent_ug.setpoint)
                # Se não fazer nada

            elif self.parent_ug.etapa_atual == UNIDADE_PARADA:
                # Unidade parada
                # Se o setpoit for acima do mínimo
                if self.parent_ug.setpoint >= self.parent_ug.setpoint_minimo:
                    # Deve partir a UG
                    self.parent_ug.partir()
                    # E em seguida mandar o setpoint novo (boa prática)
                    self.parent_ug.enviar_setpoint(self.parent_ug.setpoint)

            elif self.parent_ug.etapa_atual == UNIDADE_SINCRONIZADA:
                # Unidade sincronizada
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
            
            if self.parent_ug.etapa_atual not in UNIDADE_LISTA_DE_ETAPAS:
                self.parent_ug.inconsistente = True

            if not self.parent_ug.etapa_atual == UNIDADE_SINCRONIZADA:
                self.parent_ug.aux_tempo_sincronizada = None

            return self

    def verificar_partindo(self) -> bool:
        timer = time() + 600
        try:
            logger.debug("Iniciando o timer de verificação de partida")
            while time() < timer:
                if self.parent_ug.etapa_atual == UNIDADE_SINCRONIZADA:
                    logger.debug(f"[UG{self.parent_ug.id}] Unidade sincronizada. Saindo do timer de verificação de partida")
                    self.release = True
                    return True
                elif not self.parent_ug.release_timer:
                    logger.debug(f"[UG{self.parent_ug.id}] MOA em modo manual. Saindo do timer de verificação de partida")
                    self.release = True
                    return False
            logger.debug(f"[UG{self.parent_ug.id}] A Unidade estourou o timer de verificação de partida, adicionando condição para normalizar")
            self.parent_ug.clp_ug1.write_single_coil(REG_UG1_CD_EmergenciaViaSuper, [1 if self.parent_ug.id==1 else 0]) 
            self.parent_ug.clp_ug2.write_single_coil(REG_UG2_CD_EmergenciaViaSuper, [1 if self.parent_ug.id==2 else 0])
            self.parent_ug.clp_ug3.write_single_coil(REG_UG3_CD_EmergenciaViaSuper, [1 if self.parent_ug.id==3 else 0])
            self.release = True

        except Exception as e:
            raise e

        return False
