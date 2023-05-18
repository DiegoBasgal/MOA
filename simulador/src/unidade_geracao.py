from simulador.main import *

logger = logging.getLogger("__main__")

class Ug:
    def __init__(self, id, shared_dict, time_handler: Temporizador) -> None:
        self.id = id
        self.dict = shared_dict

        self.escala_ruido = time_handler.escala_ruido
        self.segundos_por_passo = time_handler.segundos_por_passo

        self.potencia = 0
        self.setpoint = 0
        self.etapa_alvo = 0
        self.etapa_atual = 0
        self.horimetro_hora = 100
        self.tempo_na_transicao = 0

        self.avisou_trip = False

    def passo(self) -> None:
        self.setpoint = self.dict["UG"][f"setpoint_kw_ug{self.id}"]
        if self.dict["UG"][f"debug_partir_ug{self.id}"]:
            self.dict["UG"][f"debug_partir_ug{self.id}"] = False
            self.partir()

        if self.dict["UG"][f"debug_parar_ug{self.id}"]:
            self.dict["UG"][f"debug_parar_ug{self.id}"] = False
            self.parar()

        if self.dict["UG"][f"trip_ug{self.id}"]:
            self.tripar(1, "Trip Elétrico.")

        if self.dict["UG"][f"reconhece_reset_ug{self.id}"]:
            self.dict["UG"][f"trip_ug{self.id}"] = False
            self.dict["UG"][f"reconhece_reset_ug{self.id}"] = False
            self.reconhece_reset()

        self.controle_horimetro()
        self.controle_reservatorio()
        self.controle_etapas()
        self.controle_temperaturas()

        self.dict["UG"][f"potencia_kw_ug{self.id}"] = self.potencia
        self.dict["UG"][f"etapa_atual_ug{self.id}"] = self.etapa_atual

        self.dict["UG"][f"q_ug{self.id}"] = self.q_ug(self.potencia)

    def q_ug(self, potencia_kW) -> float:
        return 0.0106 * potencia_kW if potencia_kW > 200 else 0

    def partir(self) -> None:
        logger.info(f"[UG{self.id}] Comando de partida")
        self.dict["UG"][f"etapa_alvo_ug{self.id}"] = ETAPA_US

    def parar(self) -> None:
        logger.info(f"[UG{self.id}] Comando de parada")
        self.dict["UG"][f"etapa_alvo_ug{self.id}"] = ETAPA_UP

    def tripar(self, desc=None) -> None:
        self.potencia = 0
        self.etapa_atual = 1
        self.dict["UG"][f"etapa_alvo_ug{self.id}"] = ETAPA_UPGM
        if not self.avisou_trip:
            self.avisou_trip = True
            logger.warning(f"[UG{self.id}] Trip!")

    def reconhece_reset(self) -> None:
        logger.info(f"[UG{self.id}] Reconhece Reset.")
        self.avisou_trip = False

    def controle_horimetro(self) -> None:
        if self.etapa_atual > ETAPA_UP:
            self.horimetro_hora += self.segundos_por_passo / 3600

    def controle_reservatorio(self) -> None:
        if (self.etapa_atual > ETAPA_UP) and (self.dict["USN"]["nv_montante"] < USINA_NV_MINIMO_OPERACAO):
            self.potencia = 0
            self.etapa_atual = ETAPA_UPGM
            self.etapa_alvo = ETAPA_UPGM

    def controle_temperaturas(self) -> None:
        self.dict["UG"][f"temperatura_ug{self.id}_fase_r"] = np.random.normal(25, 1 * self.escala_ruido)
        self.dict["UG"][f"temperatura_ug{self.id}_fase_s"] = np.random.normal(25, 1 * self.escala_ruido)
        self.dict["UG"][f"temperatura_ug{self.id}_fase_t"] = np.random.normal(25, 1 * self.escala_ruido)
        self.dict["UG"][f"temperatura_ug{self.id}_nucleo_gerador_1"] = np.random.normal(25, 1 * self.escala_ruido)
        self.dict["UG"][f"temperatura_ug{self.id}_nucleo_gerador_2"] = np.random.normal(25, 1 * self.escala_ruido)
        self.dict["UG"][f"temperatura_ug{self.id}_nucleo_gerador_3"] = np.random.normal(25, 1 * self.escala_ruido)
        self.dict["UG"][f"temperatura_ug{self.id}_mancal_casq_rad"] = np.random.normal(25, 1 * self.escala_ruido)
        self.dict["UG"][f"temperatura_ug{self.id}_mancal_casq_comb"] = np.random.normal(25, 1 * self.escala_ruido)
        self.dict["UG"][f"temperatura_ug{self.id}_mancal_escora_comb"] = np.random.normal(25, 1 * self.escala_ruido)
        # self.dict["UG"]["pressao_caixa_espiral_ug{}"] = np.random.normal(20, 1 * self.escala_ruido)

    def controle_etapas(self) -> None:
        self.etapa_alvo = self.dict["UG"][f"etapa_alvo_ug{self.id}"]

        if self.etapa_atual == ETAPA_UP:
            self.potencia = 0
            if (self.etapa_alvo is None) or (self.etapa_alvo == self.etapa_atual):
                self.tempo_na_transicao = 0
                self.etapa_alvo = None
                self.dict["UG"][f"etapa_alvo_ug{self.id}"] = self.etapa_alvo
                self.dict["UG"][f"etapa_aux_ug{self.id}"] = UNIDADE_PARADA

            elif self.etapa_alvo > self.etapa_atual:
                self.tempo_na_transicao += self.segundos_por_passo
                self.dict["UG"][f"etapa_aux_ug{self.id}"] = UNIDADE_SINCRONIZANDO

                if self.tempo_na_transicao >= TEMPO_TRANS_US_UPS:
                    self.etapa_atual = ETAPA_UPGM
                    self.tempo_na_transicao = 0

        if self.etapa_atual == ETAPA_UPGM:
            self.potencia = 0
            if (self.etapa_alvo is None) or (self.etapa_alvo == self.etapa_atual):
                self.tempo_na_transicao = 0
                self.etapa_alvo = None
                self.dict["UG"][f"etapa_alvo_ug{self.id}"] = self.etapa_alvo

            elif self.etapa_alvo > self.etapa_atual:
                self.tempo_na_transicao += self.segundos_por_passo
                self.dict["UG"][f"etapa_aux_ug{self.id}"] = UNIDADE_SINCRONIZANDO

                if self.tempo_na_transicao >= TEMPO_TRANS_UPGM_UVD:
                    self.etapa_atual = ETAPA_UVD
                    self.tempo_na_transicao = 0

            elif self.etapa_alvo < self.etapa_atual:
                self.tempo_na_transicao -= self.segundos_por_passo
                self.dict["UG"][f"etapa_aux_ug{self.id}"] = UNIDADE_PARANDO

                if self.tempo_na_transicao <= -TEMPO_TRANS_UPGM_UP:
                    self.etapa_atual = ETAPA_UP
                    self.tempo_na_transicao = 0
                    self.dict["UG"][f"etapa_aux_ug{self.id}"] = UNIDADE_PARADA

        if self.etapa_atual == ETAPA_UVD:
            self.potencia = 0
            if (self.etapa_alvo is None) or (self.etapa_alvo == self.etapa_atual):
                self.tempo_na_transicao = 0
                self.etapa_alvo = None
                self.dict["UG"][f"etapa_alvo_ug{self.id}"] = self.etapa_alvo

            elif self.etapa_alvo > self.etapa_atual:
                self.tempo_na_transicao += self.segundos_por_passo
                self.dict["UG"][f"etapa_aux_ug{self.id}"] = UNIDADE_SINCRONIZANDO

                if self.tempo_na_transicao >= TEMPO_TRANS_UVD_UPS:
                    self.etapa_atual = ETAPA_UPS
                    self.tempo_na_transicao = 0

            elif self.etapa_alvo < self.etapa_atual:
                self.tempo_na_transicao -= self.segundos_por_passo
                self.dict["UG"][f"etapa_aux_ug{self.id}"] = UNIDADE_PARANDO

                if self.tempo_na_transicao <= -TEMPO_TRANS_UVD_UPGM:
                    self.etapa_atual = ETAPA_UPGM
                    self.tempo_na_transicao = 0

        if self.etapa_atual == ETAPA_UPS:
            self.potencia = 0
            if (self.etapa_alvo is None) or (self.etapa_alvo == self.etapa_atual):
                self.tempo_na_transicao = 0
                self.etapa_alvo = None
                self.dict["UG"][f"etapa_alvo_ug{self.id}"] = self.etapa_alvo

            elif self.etapa_alvo > self.etapa_atual:
                self.tempo_na_transicao += self.segundos_por_passo
                self.dict["UG"][f"etapa_aux_ug{self.id}"] = UNIDADE_SINCRONIZANDO

                if (self.tempo_na_transicao >= TEMPO_TRANS_UPS_US) and self.dict["DJ"]["dj52L_fechado"]:
                    self.etapa_atual = ETAPA_US
                    self.tempo_na_transicao = 0
                    self.dict["UG"][f"etapa_aux_ug{self.id}"] = UNIDADE_SINCRONIZADA

            elif self.etapa_alvo < self.etapa_atual:
                self.tempo_na_transicao -= self.segundos_por_passo
                self.dict["UG"][f"etapa_aux_ug{self.id}"] = UNIDADE_PARANDO

                if self.tempo_na_transicao <= -TEMPO_TRANS_UPS_UVD:
                    self.etapa_atual = ETAPA_UVD
                    self.tempo_na_transicao = 0

        if self.etapa_atual == ETAPA_US:
            if (self.etapa_alvo is None) or (self.etapa_alvo == self.etapa_atual):
                self.tempo_na_transicao = 0
                self.etapa_alvo = None
                self.dict["UG"][f"etapa_alvo_ug{self.id}"] = self.etapa_alvo

                if self.dict["DJ"]["dj52L_fechado"] and not self.dict["DJ"]["dj52L_trip"]:
                    self.potencia = min(self.potencia, POT_MAX)
                    self.potencia = max(self.potencia, POT_MIN)
                    self.dict["UG"][f"etapa_aux_ug{self.id}"] = UNIDADE_SINCRONIZADA

                    if self.setpoint > self.potencia:
                        self.potencia += 10.4167 * self.segundos_por_passo
                    else:
                        self.potencia -= 10.4167 * self.segundos_por_passo

                    self.potencia = np.random.normal(self.potencia, 1 * self.escala_ruido)

                if self.dict["DJ"]["dj52L_aberto"] or self.dict["DJ"]["dj52L_trip"]:
                    self.potencia = 0
                    self.etapa_atual = ETAPA_UVD
                    self.etapa_alvo = ETAPA_US
                    self.dict["UG"][f"etapa_alvo_ug{self.id}"] = self.etapa_alvo
                    self.tempo_na_transicao = 0

            elif self.etapa_alvo < self.etapa_atual:
                self.tempo_na_transicao -= self.segundos_por_passo
                self.potencia -= 10.4167 * self.segundos_por_passo
                self.dict["UG"][f"etapa_aux_ug{self.id}"] = UNIDADE_PARANDO

                if (self.tempo_na_transicao <= -TEMPO_TRANS_US_UPS) and self.potencia <= 0:
                    self.potencia = 0
                    self.tempo_na_transicao = 0
                    self.etapa_atual = ETAPA_UPS