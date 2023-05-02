__version__ = "0.2"
__authors__ = "Diego Basgal", "Henrique Pfeifer"
__credits__ = ["Lucas Lavratti", ...]
__description__ = "Este módulo corresponde a implementação dos setores da Usina."

from usina import *

logger = logging.getLogger("__main__")

class ServicoAuxiliar(Usina):
    def __init__(self, *args, **kwargs) -> ...:
        super().__init__(self, *args, **kwargs)

        self._condicionadores: list[CondicionadorBase]
        self._condicionadores_essenciais = []

    @property
    def condicionadores(self) -> list[CondicionadorBase]:
        return self._condicionadores

    @condicionadores.setter
    def condicionadores(self, var: list[CondicionadorBase]) -> None:
        self._condicionadores = var

    @property
    def condicionadores_essenciais(self) -> list[CondicionadorBase]:
        return self._condicionadores_essenciais

    @condicionadores_essenciais.setter
    def condicionadores_essenciais(self, var: list[CondicionadorBase]) -> None:
        self._condicionadores_essenciais = var

    def verificar_condicionadores(self) -> int:
        if [condic.ativo for condic in self.condicionadores_essenciais]:
            condics_ativos = [condic for condics in [self.condicionadores_essenciais, self.condicionadores] for condic in condics if condic.ativo]
            condic_flag = [CONDIC_NORMALIZAR for condic in condics_ativos if condic.gravidade == CONDIC_NORMALIZAR]
            condic_flag = [CONDIC_INDISPONIBILIZAR for condic in condics_ativos if condic.gravidade == CONDIC_INDISPONIBILIZAR]

            if condic_flag in (CONDIC_NORMALIZAR, CONDIC_INDISPONIBILIZAR):
                logger.info("[SA] Foram detectados condicionadores ativos!")
                [logger.info(f"[SA] Condicionador: \"{condic.descr}\", Gravidade: \"{condic.gravidade}\".") for condic in condics_ativos]
        return condic_flag

    def resetar_emergencia(self) -> bool:
        try:
            res = EscritaModBusBit.escrever_bit(self.clp["SA"], OPC_UA["SA"]["RESET_FALHAS_BARRA_CA"], valor=1, bit=0)
            res = EscritaModBusBit.escrever_bit(self.clp["SA"], OPC_UA["SA"]["RESET_FALHAS_SISTEMA_AGUA"], valor=1, bit=1)
            res = EscritaModBusBit.escrever_bit(self.clp["SA"], OPC_UA["SA"]["REARME_BLOQUEIO_GERAL_E_FALHAS_SA"], valor=1, bit=23)
            return res

        except Exception as e:
            logger.error(f"[SA] Houve um erro ao realizar o reset geral. Exception: \"{repr(e)}\"")
            logger.debug(f"[SA] Traceback: {traceback.format_exc()}")
            return False

    def leitura_periodica(self) -> None:
        if self.leitura_falha_bomba_drenagem_1:
            logger.warning("[SA] Houve uma falha na bomba 1 do poço de drenagem. Favor verificar.")
        
        if self.leitura_falha_bomba_drenagem_2:
            logger.warning("[SA] Houve uma falha na bomba 2 do poço de drenagem. Favor verificar.")

        if self.leitura_falha_bomba_drenagem_3:
            logger.warning("[SA] Houve uma falha na bomba 3 do poço de drenagem. Favor verificar.")

        if self.leitura_falha_ligar_bomba_sis_agua:
            logger.warning("[SA] Houve uma falha ao ligar a bomba do sistema de água. Favor verificar.")

        if self.leitura_djs_barra_seletora_remoto:
            logger.warning("[SA] Os disjuntores da barra seletora saíram do modo remoto. Favor verificar.")

        if not self.leitura_bomba_sis_agua_disp:
            logger.warning("[SA] Foi identificado que a bomba do sistema de água está indisponível. Favor verificar.")

        if self.leitura_discrepancia_boia_poco_drenagem:
            logger.warning("[SA] Foram identificados sinais inconsistentes nas boias do poço de drenagem. Favor verificar.")


        if self.leitura_falha_partir_gmg and not Dicionarios.voip["GMG_FALHA_PARTIR"][0]:
            logger.warning("[SA] Houve uma falha ao partir o Gerador Diesel. Favor verificar.")
            Dicionarios.voip["GMG_FALHA_PARTIR"][0] = True
        elif not self.leitura_falha_partir_gmg and Dicionarios.voip["GMG_FALHA_PARTIR"][0]:
            Dicionarios.voip["GMG_FALHA_PARTIR"][0] = False

        if self.leitura_falha_parar_gmg and not Dicionarios.voip["GMG_FALHA_PARAR"][0]:
            logger.warning("[SA] Houve uma falha ao parar o Gerador Diesel. Favor verificar.")
            Dicionarios.voip["GMG_FALHA_PARAR"][0] = True
        elif not self.leitura_falha_parar_gmg and Dicionarios.voip["GMG_FALHA_PARAR"][0]:
            Dicionarios.voip["GMG_FALHA_PARAR"][0] = False

        if self.leitura_operacao_manual_gmg and not Dicionarios.voip["GMG_OPERACAO_MANUAL"][0]:
            logger.warning("[SA] O Gerador Diesel saiu do modo remoto. Favor verificar.")
            Dicionarios.voip["GMG_OPERACAO_MANUAL"][0] = True
        elif not self.leitura_operacao_manual_gmg and Dicionarios.voip["GMG_OPERACAO_MANUAL"][0]:
            Dicionarios.voip["GMG_OPERACAO_MANUAL"][0] = False

        if not self.leitura_sem_falha_52sa1 and not Dicionarios.voip["52SA1_SEM_FALHA"][0]:
            logger.warning("[SA] Houve uma falha com o disjuntor 52SA1 do transformador do SA. Favor verificar.")
            Dicionarios.voip["52SA1_SEM_FALHA"][0] = True
        elif self.leitura_sem_falha_52sa1 and Dicionarios.voip["52SA1_SEM_FALHA"][0]:
            Dicionarios.voip["52SA1_SEM_FALHA"][0] = False

        if not self.leitura_sem_falha_52sa2 and not Dicionarios.voip["52SA2_SEM_FALHA"][0]:
            logger.warning("[SA] Houve uma falha com o disjuntor 52SA2 do Gerador Diesel. Favor verificar.")
            Dicionarios.voip["52SA2_SEM_FALHA"][0] = True
        elif self.leitura_sem_falha_52sa2 and Dicionarios.voip["52SA2_SEM_FALHA"][0]:
            Dicionarios.voip["52SA2_SEM_FALHA"][0] = False

        if not self.leitura_sem_falha_52sa3 and not Dicionarios.voip["52SA3_SEM_FALHA"][0]:
            logger.warning("[SA] Houve uma falha com o disjuntor 52SA3 do barramento de cargas não essenciais. Favor verificar.")
            Dicionarios.voip["52SA3_SEM_FALHA"][0] = True
        elif self.leitura_sem_falha_52sa3 and Dicionarios.voip["52SA3_SEM_FALHA"][0]:
            Dicionarios.voip["52SA3_SEM_FALHA"][0] = False

        if self.leitura_falha_bomba_filtragem and not Dicionarios.voip["FILTRAGEM_BOMBA_FALHA"][0]:
            logger.warning("[SA] Houve uma falha na bomba de filtragem. Favor verificar.")
            Dicionarios.voip["FILTRAGEM_BOMBA_FALHA"][0] = True
        elif not self.leitura_falha_bomba_filtragem and Dicionarios.voip["FILTRAGEM_BOMBA_FALHA"][0]:
            Dicionarios.voip["FILTRAGEM_BOMBA_FALHA"][0] = False

        if self.leitura_nivel_alto_poco_drenagem and not Dicionarios.voip["POCO_DRENAGEM_NIVEL_ALTO"][0]:
            logger.warning("[SA] Nível do poço de drenagem alto. Favor verificar.")
            Dicionarios.voip["POCO_DRENAGEM_NIVEL_ALTO"][0] = True
        elif not self.leitura_nivel_alto_poco_drenagem and Dicionarios.voip["POCO_DRENAGEM_NIVEL_ALTO"][0]:
            Dicionarios.voip["POCO_DRENAGEM_NIVEL_ALTO"][0] = False

        if self.leitura_falha_bomba_drenagem_uni and not Dicionarios.voip["DRENAGEM_UNIDADES_BOMBA_FALHA"][0]:
            logger.warning("[SA] Houve uma falha na bomba de drenagem. Favor verificar.")
            Dicionarios.voip["DRENAGEM_UNIDADES_BOMBA_FALHA"][0] = True
        elif not self.leitura_falha_bomba_drenagem_uni and Dicionarios.voip["DRENAGEM_UNIDADES_BOMBA_FALHA"][0]:
            Dicionarios.voip["DRENAGEM_UNIDADES_BOMBA_FALHA"][0] = False

        if self.leitura_nivel_muito_alto_poco_drenagem and not Dicionarios.voip["POCO_DRENAGEM_NIVEL_MUITO_ALTO"][0]:
            logger.warning("[SA] Nível do poço de drenagem está muito alto. Favor verificar.")
            Dicionarios.voip["POCO_DRENAGEM_NIVEL_MUITO_ALTO"][0] = True
        elif not self.leitura_nivel_muito_alto_poco_drenagem and Dicionarios.voip["POCO_DRENAGEM_NIVEL_MUITO_ALTO"][0]:
            Dicionarios.voip["POCO_DRENAGEM_NIVEL_MUITO_ALTO"][0] = False

        if self.leitura_alarme_sistema_incendio_atuado and not Dicionarios.voip["SISTEMA_INCENDIO_ALARME_ATUADO"][0]:
            logger.warning("[SA] O alarme do sistema de incêndio foi acionado. Favor verificar.")
            Dicionarios.voip["SISTEMA_INCENDIO_ALARME_ATUADO"][0] = True
        elif not self.leitura_alarme_sistema_incendio_atuado and Dicionarios.voip["SISTEMA_INCENDIO_ALARME_ATUADO"][0]:
            Dicionarios.voip["SISTEMA_INCENDIO_ALARME_ATUADO"][0] = False

        if self.leitura_alarme_sistema_seguraca_atuado and not Dicionarios.voip["SISTEMA_SEGURANCA_ALARME_ATUADO"][0]:
            logger.warning("[SA] O alarme do sistem de seguraça foi acionado. Favor verificar.")
            Dicionarios.voip["SISTEMA_SEGURANCA_ALARME_ATUADO"][0] = True
        elif not self.leitura_alarme_sistema_seguraca_atuado and Dicionarios.voip["SISTEMA_SEGURANCA_ALARME_ATUADO"][0]:
            Dicionarios.voip["SISTEMA_SEGURANCA_ALARME_ATUADO"][0] = False
            
        if self.leitura_falha_tubo_succao_bomba_recalque and not Dicionarios.voip["BOMBA_RECALQUE_TUBO_SUCCAO_FALHA"][0]:
            logger.warning("[SA] Houve uma falha na sucção da bomba de recalque. Favor verificar.")
            Dicionarios.voip["BOMBA_RECALQUE_TUBO_SUCCAO_FALHA"][0] = True
        elif not self.leitura_falha_tubo_succao_bomba_recalque and Dicionarios.voip["BOMBA_RECALQUE_TUBO_SUCCAO_FALHA"][0]:
            Dicionarios.voip["BOMBA_RECALQUE_TUBO_SUCCAO_FALHA"][0] = False

    # TODO adicionar descricao nas variaves de leituras de condicionadores
    def iniciar_leituras_condicionadores(self) -> None:
        # CONDICIONADORES ESSENCIAIS
        # MOA -> Indisponibilizar
        self.leitura_in_emergencia = self.clp["MOA"].read_coils(MB["MOA"]["IN_EMERG"])[0]
        self.condicionadores_essenciais.append(CondicionadorBase(self.leitura_in_emergencia, CONDIC_INDISPONIBILIZAR))

        # Normalizar
            # Bit Invertido
        self.leitura_sem_emergencia_sa = LeituraModbus(OPC_UA["SA"]["SEM_EMERGENCIA"], 13, True)
        self.condicionadores_essenciais.append(CondicionadorBase(self.leitura_sem_emergencia_sa, CONDIC_NORMALIZAR))

        # CONDICIONADORES
        # Normalizar
            # Bit Normal
        self.leitura_retificador_subtensao = LeituraModbus(OPC_UA["SA"]["RETIFICADOR_SUBTENSAO"], 31)
        self.condicionadores.append(CondicionadorBase(self.leitura_retificador_subtensao, CONDIC_NORMALIZAR))

        self.leitura_retificador_sobretensao = LeituraModbus(OPC_UA["SA"]["RETIFICADOR_SOBRETENSAO"], 30)
        self.condicionadores.append(CondicionadorBase(self.leitura_retificador_sobretensao, CONDIC_NORMALIZAR))

        self.leitura_retificador_sobrecorrente_saida = LeituraModbus(OPC_UA["SA"]["RETIFICADOR_SOBRECORRENTE_SAIDA"], 0)
        self.condicionadores.append(CondicionadorBase(self.leitura_retificador_sobrecorrente_saida, CONDIC_NORMALIZAR))

        self.leitura_retificador_sobrecorrente_baterias = LeituraModbus(OPC_UA["SA"]["RETIFICADOR_SOBRECORRENTE_BATERIAS"], 1)
        self.condicionadores.append(CondicionadorBase(self.leitura_retificador_sobrecorrente_baterias, CONDIC_NORMALIZAR))

        self.leitura_falha_sistema_agua_pressurizar_fa = LeituraModbus(OPC_UA["SA"]["SISTEMA_AGUA_FALHA_PRESSURIZAR_FILTRO_A"], 3)
        self.condicionadores.append(CondicionadorBase(self.leitura_falha_sistema_agua_pressurizar_fa, CONDIC_NORMALIZAR))

        self.leitura_falha_sistema_agua_pressostato_fa = LeituraModbus(OPC_UA["SA"]["SISTEMA_AGUA_FALHA_PRESSOSTATO_FILTRO_A"], 4)
        self.condicionadores.append(CondicionadorBase(self.leitura_falha_sistema_agua_pressostato_fa, CONDIC_NORMALIZAR))

        self.leitura_falha_sistema_agua_pressurizar_fb = LeituraModbus(OPC_UA["SA"]["SISTEMA_AGUA_FALHA_PRESSURIZAR_FILTRO_B"], 5)
        self.condicionadores.append(CondicionadorBase(self.leitura_falha_sistema_agua_pressurizar_fb, CONDIC_NORMALIZAR))

        self.leitura_falha_sistema_agua_pressostato_fb = LeituraModbus(OPC_UA["SA"]["SISTEMA_AGUA_FALHA_PRESSOSTATO_FILTRO_B"], 6)
        self.condicionadores.append(CondicionadorBase(self.leitura_falha_sistema_agua_pressostato_fb, CONDIC_NORMALIZAR))

        # Indisponibilizar
            # Bit Invertido
        self.leitura_52sa1_sem_falha = LeituraModbus(OPC_UA["SA"]["52SA1_SEM_FALHA"], 31, True)
        self.condicionadores.append(CondicionadorBase(self.leitura_52sa1_sem_falha, CONDIC_INDISPONIBILIZAR))

        self.leitura_sa_72sa1_fechado = LeituraModbus(OPC_UA["SA"]["SA_72SA1_FECHADO"], 10, True)
        self.condicionadores.append(CondicionadorBase(self.leitura_sa_72sa1_fechado, CONDIC_INDISPONIBILIZAR))

        self.leitura_disj_24vcc_fechados = LeituraModbus(OPC_UA["SA"]["DISJUNTORES_24VCC_FECHADOS"], 12, True)
        self.condicionadores.append(CondicionadorBase(self.leitura_disj_24vcc_fechados, CONDIC_INDISPONIBILIZAR))

        self.leitura_disj_125vcc_fechados = LeituraModbus(OPC_UA["SA"]["DISJUNTORES_125VCC_FECHADOS"], 11, True)
        self.condicionadores.append(CondicionadorBase(self.leitura_disj_125vcc_fechados, CONDIC_INDISPONIBILIZAR))
        
        self.leitura_comando_24vcc_com_tensao = LeituraModbus(OPC_UA["SA"]["COM_TENSAO_COMANDO_24VCC"], 15, True)
        self.condicionadores.append(CondicionadorBase(self.leitura_comando_24vcc_com_tensao, CONDIC_INDISPONIBILIZAR))
        
        self.leitura_comando_125vcc_com_tensao = LeituraModbus(OPC_UA["SA"]["COM_TENSAO_COMANDO_125VCC"], 14, True)
        self.condicionadores.append(CondicionadorBase(self.leitura_comando_125vcc_com_tensao, CONDIC_INDISPONIBILIZAR))
        
        self.leitura_alimentacao_125vcc_com_tensao = LeituraModbus(OPC_UA["SA"]["COM_TENSAO_ALIMENTACAO_125VCC"], 13, True)
        self.condicionadores.append(CondicionadorBase(self.leitura_alimentacao_125vcc_com_tensao, CONDIC_INDISPONIBILIZAR))

            # Bit normal
        self.leitura_falha_abrir_52sa1 = LeituraModbus(OPC_UA["SA"]["FALHA_ABRIR_52SA1"], 0)
        self.condicionadores.append(CondicionadorBase(self.leitura_falha_abrir_52sa1, CONDIC_INDISPONIBILIZAR))

        self.leitura_falha_fechar_52sa1 = LeituraModbus(OPC_UA["SA"]["FALHA_FECHAR_52SA1"], 1)
        self.condicionadores.append(CondicionadorBase(self.leitura_falha_fechar_52sa1, CONDIC_INDISPONIBILIZAR))

        self.leitura_falha_abrir_52sa2 = LeituraModbus(OPC_UA["SA"]["FALHA_ABRIR_52SA2"], 3)
        self.condicionadores.append(CondicionadorBase(self.leitura_falha_abrir_52sa2, CONDIC_INDISPONIBILIZAR))

        self.leitura_falha_fechar_52sa2 = LeituraModbus(OPC_UA["SA"]["FALHA_FECHAR_52SA2"], 4)
        self.condicionadores.append(CondicionadorBase(self.leitura_falha_fechar_52sa2, CONDIC_INDISPONIBILIZAR))

        self.leitura_falha_abrir_52sa3 = LeituraModbus(OPC_UA["SA"]["FALHA_ABRIR_52SA3"], 5)
        self.condicionadores.append(CondicionadorBase(self.leitura_falha_abrir_52sa3, CONDIC_INDISPONIBILIZAR))

        self.leitura_falha_fechar_52sa3 = LeituraModbus(OPC_UA["SA"]["FALHA_FECHAR_52SA3"], 6)
        self.condicionadores.append(CondicionadorBase(self.leitura_falha_fechar_52sa3, CONDIC_INDISPONIBILIZAR))

        self.leitura_fusivel_queimado_retificador = LeituraModbus(OPC_UA["SA"]["RETIFICADOR_FUSIVEL_QUEIMADO"], 2)
        self.condicionadores.append(CondicionadorBase(self.leitura_fusivel_queimado_retificador, CONDIC_INDISPONIBILIZAR))

        self.leitura_fuga_terra_positivo_retificador = LeituraModbus(OPC_UA["SA"]["RETIFICADOR_FUGA_TERRA_POSITIVO"], 5)
        self.condicionadores.append(CondicionadorBase(self.leitura_fuga_terra_positivo_retificador, CONDIC_INDISPONIBILIZAR))

        self.leitura_fuga_terra_negativo_retificador = LeituraModbus(OPC_UA["SA"]["RETIFICADOR_FUGA_TERRA_NEGATIVO"], 6)
        self.condicionadores.append(CondicionadorBase(self.leitura_fuga_terra_negativo_retificador, CONDIC_INDISPONIBILIZAR))

        # LEITURAS PARA LEITURA PERIODICA
        # Telegram
            # Bit Invertido
        self.leitura_bomba_sis_agua_disp = LeituraModbus(OPC_UA["SA"]["SISTEMA_AGUA_BOMBA_DISPONIVEL"], 0, True)

            # Bit Normal
        self.leitura_falha_bomba_drenagem_1 = LeituraModbus(OPC_UA["SA"]["DRENAGEM_BOMBA_1_FALHA"], 0)
        self.leitura_falha_bomba_drenagem_2 = LeituraModbus(OPC_UA["SA"]["DRENAGEM_BOMBA_2_FALHA"], 2)
        self.leitura_falha_bomba_drenagem_3 = LeituraModbus(OPC_UA["SA"]["DRENAGEM_BOMBA_3_FALHA"], 4)
        self.leitura_falha_ligar_bomba_sis_agua = LeituraModbus(OPC_UA["SA"]["SISTEMA_AGUA_FALHA_LIGA_BOMBA"], 1)
        self.leitura_djs_barra_seletora_remoto = LeituraModbus(OPC_UA["SA"]["DISJUNTORES_BARRA_SELETORA_REMOTO"], 9)
        self.leitura_discrepancia_boia_poco_drenagem = LeituraModbus(OPC_UA["SA"]["DRENAGEM_DISCREPANCIA_BOIAS_POCO"], 9)

        # Telegram + Voip
            # Bit Invertido
        self.leitura_sem_falha_52sa3 = LeituraModbus(OPC_UA["SA"]["52SA3_SEM_FALHA"], 3, True)
        self.leitura_sem_falha_52sa2 = LeituraModbus(OPC_UA["SA"]["52SA2_SEM_FALHA"], 1, True)
        self.leitura_sem_falha_52sa1 = LeituraModbus(OPC_UA["SA"]["52SA1_SEM_FALHA"], 31, True)

            # Bit Normal
        self.leitura_falha_parar_gmg = LeituraModbus(OPC_UA["SA"]["GMG_FALHA_PARAR"], 7)
        self.leitura_falha_partir_gmg = LeituraModbus(OPC_UA["SA"]["GMG_FALHA_PARTIR"], 6)
        self.leitura_operacao_manual_gmg = LeituraModbus(OPC_UA["SA"]["GMG_OPERACAO_MANUAL"], 10)
        self.leitura_falha_bomba_filtragem = LeituraModbus(OPC_UA["SA"]["FILTRAGEM_BOMBA_FALHA"], 6)
        self.leitura_nivel_alto_poco_drenagem = LeituraModbus(OPC_UA["SA"]["POCO_DRENAGEM_NIVEL_ALTO"], 26)
        self.leitura_falha_bomba_drenagem_uni = LeituraModbus(OPC_UA["SA"]["DRENAGEM_UNIDADES_BOMBA_FALHA"], 12)
        self.leitura_alarme_sistema_incendio_atuado = LeituraModbus(OPC_UA["SA"]["SISTEMA_INCENDIO_ALARME_ATUADO"], 6)
        self.leitura_alarme_sistema_seguraca_atuado = LeituraModbus(OPC_UA["SA"]["SISTEMA_SEGURANCA_ALARME_ATUADO"], 7)
        self.leitura_nivel_muito_alto_poco_drenagem = LeituraModbus(OPC_UA["SA"]["POCO_DRENAGEM_NIVEL_MUITO_ALTO"], 25)
        self.leitura_falha_tubo_succao_bomba_recalque = LeituraModbus(OPC_UA["SA"]["BOMBA_RECALQUE_TUBO_SUCCAO_FALHA"], 14)