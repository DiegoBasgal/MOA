__version__ = "0.2"
__authors__ = "Diego Basgal", "Henrique Pfeifer"
__credits__ = ["Lucas Lavratti", ...]
__description__ = "Este módulo corresponde a implementação dos setores da Usina."

from usina import *

logger = logging.getLogger("__main__")

class ServicoAuxiliar(Usina):
    def __init__(self, *args, **kwargs) -> ...:
        super().__init__(self, *args, **kwargs)

        self._condicionadores: "list[CondicionadorBase]"
        self._condicionadores_essenciais = []

    @property
    def condicionadores(self) -> "list[CondicionadorBase]":
        return self._condicionadores

    @condicionadores.setter
    def condicionadores(self, var: "list[CondicionadorBase]") -> None:
        self._condicionadores = var

    @property
    def condicionadores_essenciais(self) -> "list[CondicionadorBase]":
        return self._condicionadores_essenciais

    @condicionadores_essenciais.setter
    def condicionadores_essenciais(self, var: "list[CondicionadorBase]") -> None:
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
            res = EscritaModBusBit.escrever_bit(self.clp["SA"], REG_CLP["SA"]["RESET_FALHAS_BARRA_CA"], bit=0, valor=1)
            res = EscritaModBusBit.escrever_bit(self.clp["SA"], REG_CLP["SA"]["RESET_FALHAS_SISTEMA_AGUA"], bit=1, valor=1)
            res = EscritaModBusBit.escrever_bit(self.clp["SA"], REG_CLP["SA"]["REARME_BLOQUEIO_GERAL_E_FALHAS_SA"], bit=23, valor=1)
            return res

        except Exception as e:
            logger.error(f"[SA] Houve um erro ao realizar o reset geral. Exception: \"{repr(e)}\"")
            logger.debug(f"[SA] Traceback: {traceback.format_exc()}")
            return False

    def leitura_periodica(self) -> None:
        if self.leitura_falha_bomba_drenagem_1.valor:
            logger.warning("[SA] Houve uma falha na bomba 1 do poço de drenagem. Favor verificar.")
        
        if self.leitura_falha_bomba_drenagem_2.valor:
            logger.warning("[SA] Houve uma falha na bomba 2 do poço de drenagem. Favor verificar.")

        if self.leitura_falha_bomba_drenagem_3.valor:
            logger.warning("[SA] Houve uma falha na bomba 3 do poço de drenagem. Favor verificar.")

        if self.leitura_falha_ligar_bomba_sis_agua.valor:
            logger.warning("[SA] Houve uma falha ao ligar a bomba do sistema de água. Favor verificar.")

        if self.leitura_djs_barra_seletora_remoto.valor:
            logger.warning("[SA] Os disjuntores da barra seletora saíram do modo remoto. Favor verificar.")

        if not self.leitura_bomba_sis_agua_disp.valor:
            logger.warning("[SA] Foi identificado que a bomba do sistema de água está indisponível. Favor verificar.")

        if self.leitura_discrepancia_boia_poco_drenagem.valor:
            logger.warning("[SA] Foram identificados sinais inconsistentes nas boias do poço de drenagem. Favor verificar.")


        if self.leitura_falha_partir_gmg.valor and not Dicionarios.voip["GMG_FALHA_PARTIR"][0]:
            logger.warning("[SA] Houve uma falha ao partir o Gerador Diesel. Favor verificar.")
            Dicionarios.voip["GMG_FALHA_PARTIR"][0] = True
        elif not self.leitura_falha_partir_gmg.valor and Dicionarios.voip["GMG_FALHA_PARTIR"][0]:
            Dicionarios.voip["GMG_FALHA_PARTIR"][0] = False

        if self.leitura_falha_parar_gmg.valor and not Dicionarios.voip["GMG_FALHA_PARAR"][0]:
            logger.warning("[SA] Houve uma falha ao parar o Gerador Diesel. Favor verificar.")
            Dicionarios.voip["GMG_FALHA_PARAR"][0] = True
        elif not self.leitura_falha_parar_gmg.valor and Dicionarios.voip["GMG_FALHA_PARAR"][0]:
            Dicionarios.voip["GMG_FALHA_PARAR"][0] = False

        if self.leitura_operacao_manual_gmg.valor and not Dicionarios.voip["GMG_OPERACAO_MANUAL"][0]:
            logger.warning("[SA] O Gerador Diesel saiu do modo remoto. Favor verificar.")
            Dicionarios.voip["GMG_OPERACAO_MANUAL"][0] = True
        elif not self.leitura_operacao_manual_gmg.valor and Dicionarios.voip["GMG_OPERACAO_MANUAL"][0]:
            Dicionarios.voip["GMG_OPERACAO_MANUAL"][0] = False

        if not self.leitura_sem_falha_52sa1.valor and not Dicionarios.voip["52SA1_SEM_FALHA"][0]:
            logger.warning("[SA] Houve uma falha com o disjuntor 52SA1 do transformador do SA. Favor verificar.")
            Dicionarios.voip["52SA1_SEM_FALHA"][0] = True
        elif self.leitura_sem_falha_52sa1.valor and Dicionarios.voip["52SA1_SEM_FALHA"][0]:
            Dicionarios.voip["52SA1_SEM_FALHA"][0] = False

        if not self.leitura_sem_falha_52sa2.valor and not Dicionarios.voip["52SA2_SEM_FALHA"][0]:
            logger.warning("[SA] Houve uma falha com o disjuntor 52SA2 do Gerador Diesel. Favor verificar.")
            Dicionarios.voip["52SA2_SEM_FALHA"][0] = True
        elif self.leitura_sem_falha_52sa2.valor and Dicionarios.voip["52SA2_SEM_FALHA"][0]:
            Dicionarios.voip["52SA2_SEM_FALHA"][0] = False

        if not self.leitura_sem_falha_52sa3.valor and not Dicionarios.voip["52SA3_SEM_FALHA"][0]:
            logger.warning("[SA] Houve uma falha com o disjuntor 52SA3 do barramento de cargas não essenciais. Favor verificar.")
            Dicionarios.voip["52SA3_SEM_FALHA"][0] = True
        elif self.leitura_sem_falha_52sa3.valor and Dicionarios.voip["52SA3_SEM_FALHA"][0]:
            Dicionarios.voip["52SA3_SEM_FALHA"][0] = False

        if self.leitura_falha_bomba_filtragem.valor and not Dicionarios.voip["FILTRAGEM_BOMBA_FALHA"][0]:
            logger.warning("[SA] Houve uma falha na bomba de filtragem. Favor verificar.")
            Dicionarios.voip["FILTRAGEM_BOMBA_FALHA"][0] = True
        elif not self.leitura_falha_bomba_filtragem.valor and Dicionarios.voip["FILTRAGEM_BOMBA_FALHA"][0]:
            Dicionarios.voip["FILTRAGEM_BOMBA_FALHA"][0] = False

        if self.leitura_nivel_alto_poco_drenagem.valor and not Dicionarios.voip["POCO_DRENAGEM_NIVEL_ALTO"][0]:
            logger.warning("[SA] Nível do poço de drenagem alto. Favor verificar.")
            Dicionarios.voip["POCO_DRENAGEM_NIVEL_ALTO"][0] = True
        elif not self.leitura_nivel_alto_poco_drenagem.valor and Dicionarios.voip["POCO_DRENAGEM_NIVEL_ALTO"][0]:
            Dicionarios.voip["POCO_DRENAGEM_NIVEL_ALTO"][0] = False

        if self.leitura_falha_bomba_drenagem_uni.valor and not Dicionarios.voip["DRENAGEM_UNIDADES_BOMBA_FALHA"][0]:
            logger.warning("[SA] Houve uma falha na bomba de drenagem. Favor verificar.")
            Dicionarios.voip["DRENAGEM_UNIDADES_BOMBA_FALHA"][0] = True
        elif not self.leitura_falha_bomba_drenagem_uni.valor and Dicionarios.voip["DRENAGEM_UNIDADES_BOMBA_FALHA"][0]:
            Dicionarios.voip["DRENAGEM_UNIDADES_BOMBA_FALHA"][0] = False

        if self.leitura_nivel_muito_alto_poco_drenagem.valor and not Dicionarios.voip["POCO_DRENAGEM_NIVEL_MUITO_ALTO"][0]:
            logger.warning("[SA] Nível do poço de drenagem está muito alto. Favor verificar.")
            Dicionarios.voip["POCO_DRENAGEM_NIVEL_MUITO_ALTO"][0] = True
        elif not self.leitura_nivel_muito_alto_poco_drenagem.valor and Dicionarios.voip["POCO_DRENAGEM_NIVEL_MUITO_ALTO"][0]:
            Dicionarios.voip["POCO_DRENAGEM_NIVEL_MUITO_ALTO"][0] = False

        if self.leitura_alarme_sistema_incendio_atuado.valor and not Dicionarios.voip["SISTEMA_INCENDIO_ALARME_ATUADO"][0]:
            logger.warning("[SA] O alarme do sistema de incêndio foi acionado. Favor verificar.")
            Dicionarios.voip["SISTEMA_INCENDIO_ALARME_ATUADO"][0] = True
        elif not self.leitura_alarme_sistema_incendio_atuado.valor and Dicionarios.voip["SISTEMA_INCENDIO_ALARME_ATUADO"][0]:
            Dicionarios.voip["SISTEMA_INCENDIO_ALARME_ATUADO"][0] = False

        if self.leitura_alarme_sistema_seguraca_atuado.valor and not Dicionarios.voip["SISTEMA_SEGURANCA_ALARME_ATUADO"][0]:
            logger.warning("[SA] O alarme do sistem de seguraça foi acionado. Favor verificar.")
            Dicionarios.voip["SISTEMA_SEGURANCA_ALARME_ATUADO"][0] = True
        elif not self.leitura_alarme_sistema_seguraca_atuado.valor and Dicionarios.voip["SISTEMA_SEGURANCA_ALARME_ATUADO"][0]:
            Dicionarios.voip["SISTEMA_SEGURANCA_ALARME_ATUADO"][0] = False
            
        if self.leitura_falha_tubo_succao_bomba_recalque.valor and not Dicionarios.voip["BOMBA_RECALQUE_TUBO_SUCCAO_FALHA"][0]:
            logger.warning("[SA] Houve uma falha na sucção da bomba de recalque. Favor verificar.")
            Dicionarios.voip["BOMBA_RECALQUE_TUBO_SUCCAO_FALHA"][0] = True
        elif not self.leitura_falha_tubo_succao_bomba_recalque.valor and Dicionarios.voip["BOMBA_RECALQUE_TUBO_SUCCAO_FALHA"][0]:
            Dicionarios.voip["BOMBA_RECALQUE_TUBO_SUCCAO_FALHA"][0] = False

    # TODO adicionar descricao nas variaves de leituras de condicionadores
    def iniciar_leituras_condicionadores(self) -> None:
        # CONDICIONADORES ESSENCIAIS
        # Normalizar
            # Bit Invertido
        self.leitura_sem_emergencia_sa = LeituraModbusBit(self.clp["SA"], REG_CLP["SA"]["SEM_EMERGENCIA"], bit=13, invertido=True, descricao="SA_SEM_EMERGENCIA")
        self.condicionadores_essenciais.append(CondicionadorBase(self.leitura_sem_emergencia_sa, CONDIC_NORMALIZAR))

        # CONDICIONADORES
        # Normalizar
            # Bit Normal
        self.leitura_retificador_subtensao = LeituraModbusBit(self.clp["SA"], REG_CLP["SA"]["RETIFICADOR_SUBTENSAO"], bit=31, descricao="SA_RETIFICADOR_SUBTENSAO")
        self.condicionadores.append(CondicionadorBase(self.leitura_retificador_subtensao, CONDIC_NORMALIZAR))

        self.leitura_retificador_sobretensao = LeituraModbusBit(self.clp["SA"], REG_CLP["SA"]["RETIFICADOR_SOBRETENSAO"], bit=30, descricao="SA_RETIFICADOR_SOBRETENSAO")
        self.condicionadores.append(CondicionadorBase(self.leitura_retificador_sobretensao, CONDIC_NORMALIZAR))

        self.leitura_retificador_sobrecorrente_saida = LeituraModbusBit(self.clp["SA"], REG_CLP["SA"]["RETIFICADOR_SOBRECORRENTE_SAIDA"], bit=0, descricao="SA_RETIFICADOR_SOBRECORRENTE_SAIDA")
        self.condicionadores.append(CondicionadorBase(self.leitura_retificador_sobrecorrente_saida, CONDIC_NORMALIZAR))

        self.leitura_retificador_sobrecorrente_baterias = LeituraModbusBit(self.clp["SA"], REG_CLP["SA"]["RETIFICADOR_SOBRECORRENTE_BATERIAS"], bit=1, descricao="SA_RETIFICADOR_SOBRECORRENTE_BATERIAS")
        self.condicionadores.append(CondicionadorBase(self.leitura_retificador_sobrecorrente_baterias, CONDIC_NORMALIZAR))

        self.leitura_falha_sistema_agua_pressurizar_fa = LeituraModbusBit(self.clp["SA"], REG_CLP["SA"]["SISTEMA_AGUA_FALHA_PRESSURIZAR_FILTRO_A"], bit=3, descricao="SA_SISTEMA_AGUA_FALHA_PRESSURIZAR_FILTRO_A")
        self.condicionadores.append(CondicionadorBase(self.leitura_falha_sistema_agua_pressurizar_fa, CONDIC_NORMALIZAR))

        self.leitura_falha_sistema_agua_pressostato_fa = LeituraModbusBit(self.clp["SA"], REG_CLP["SA"]["SISTEMA_AGUA_FALHA_PRESSOSTATO_FILTRO_A"], bit=4, descricao="SA_SISTEMA_AGUA_FALHA_PRESSOSTATO_FILTRO_A")
        self.condicionadores.append(CondicionadorBase(self.leitura_falha_sistema_agua_pressostato_fa, CONDIC_NORMALIZAR))

        self.leitura_falha_sistema_agua_pressurizar_fb = LeituraModbusBit(self.clp["SA"], REG_CLP["SA"]["SISTEMA_AGUA_FALHA_PRESSURIZAR_FILTRO_B"], bit=5, descricao="SA_SISTEMA_AGUA_FALHA_PRESSURIZAR_FILTRO_B")
        self.condicionadores.append(CondicionadorBase(self.leitura_falha_sistema_agua_pressurizar_fb, CONDIC_NORMALIZAR))

        self.leitura_falha_sistema_agua_pressostato_fb = LeituraModbusBit(self.clp["SA"], REG_CLP["SA"]["SISTEMA_AGUA_FALHA_PRESSOSTATO_FILTRO_B"], bit=6, descricao="SA_SISTEMA_AGUA_FALHA_PRESSOSTATO_FILTRO_B")
        self.condicionadores.append(CondicionadorBase(self.leitura_falha_sistema_agua_pressostato_fb, CONDIC_NORMALIZAR))

        # Indisponibilizar
            # Bit Invertido
        self.leitura_52sa1_sem_falha = LeituraModbusBit(self.clp["SA"], REG_CLP["SA"]["52SA1_SEM_FALHA"], bit=31, invertido=True, descricao="SA_52SA1_SEM_FALHA")
        self.condicionadores.append(CondicionadorBase(self.leitura_52sa1_sem_falha, CONDIC_INDISPONIBILIZAR))

        self.leitura_sa_72sa1_fechado = LeituraModbusBit(self.clp["SA"], REG_CLP["SA"]["SA_72SA1_FECHADO"], bit=10, invertido=True, descricao="SA_SA_72SA1_FECHADO")
        self.condicionadores.append(CondicionadorBase(self.leitura_sa_72sa1_fechado, CONDIC_INDISPONIBILIZAR))

        self.leitura_disj_24vcc_fechados = LeituraModbusBit(self.clp["SA"], REG_CLP["SA"]["DISJUNTORES_24VCC_FECHADOS"], bit=12, invertido=True, descricao="SA_DISJUNTORES_24VCC_FECHADOS")
        self.condicionadores.append(CondicionadorBase(self.leitura_disj_24vcc_fechados, CONDIC_INDISPONIBILIZAR))

        self.leitura_disj_125vcc_fechados = LeituraModbusBit(self.clp["SA"], REG_CLP["SA"]["DISJUNTORES_125VCC_FECHADOS"], bit=11, invertido=True, descricao="SA_DISJUNTORES_125VCC_FECHADOS")
        self.condicionadores.append(CondicionadorBase(self.leitura_disj_125vcc_fechados, CONDIC_INDISPONIBILIZAR))
        
        self.leitura_comando_24vcc_com_tensao = LeituraModbusBit(self.clp["SA"], REG_CLP["SA"]["COM_TENSAO_COMANDO_24VCC"], bit=15, invertido=True, descricao="SA_COM_TENSAO_COMANDO_24VCC")
        self.condicionadores.append(CondicionadorBase(self.leitura_comando_24vcc_com_tensao, CONDIC_INDISPONIBILIZAR))
        
        self.leitura_comando_125vcc_com_tensao = LeituraModbusBit(self.clp["SA"], REG_CLP["SA"]["COM_TENSAO_COMANDO_125VCC"], bit=14, invertido=True, descricao="SA_COM_TENSAO_COMANDO_125VCC")
        self.condicionadores.append(CondicionadorBase(self.leitura_comando_125vcc_com_tensao, CONDIC_INDISPONIBILIZAR))
        
        self.leitura_alimentacao_125vcc_com_tensao = LeituraModbusBit(self.clp["SA"], REG_CLP["SA"]["COM_TENSAO_ALIMENTACAO_125VCC"], bit=13, invertido=True, descricao="SA_COM_TENSAO_ALIMENTACAO_125VCC")
        self.condicionadores.append(CondicionadorBase(self.leitura_alimentacao_125vcc_com_tensao, CONDIC_INDISPONIBILIZAR))

            # Bit normal
        self.leitura_falha_abrir_52sa1 = LeituraModbusBit(self.clp["SA"], REG_CLP["SA"]["FALHA_ABRIR_52SA1"], bit=0, descricao="SA_FALHA_ABRIR_52SA1")
        self.condicionadores.append(CondicionadorBase(self.leitura_falha_abrir_52sa1, CONDIC_INDISPONIBILIZAR))

        self.leitura_falha_fechar_52sa1 = LeituraModbusBit(self.clp["SA"], REG_CLP["SA"]["FALHA_FECHAR_52SA1"], bit=1, descricao="SA_FALHA_FECHAR_52SA1")
        self.condicionadores.append(CondicionadorBase(self.leitura_falha_fechar_52sa1, CONDIC_INDISPONIBILIZAR))

        self.leitura_falha_abrir_52sa2 = LeituraModbusBit(self.clp["SA"], REG_CLP["SA"]["FALHA_ABRIR_52SA2"], bit=3, descricao="SA_FALHA_ABRIR_52SA2")
        self.condicionadores.append(CondicionadorBase(self.leitura_falha_abrir_52sa2, CONDIC_INDISPONIBILIZAR))

        self.leitura_falha_fechar_52sa2 = LeituraModbusBit(self.clp["SA"], REG_CLP["SA"]["FALHA_FECHAR_52SA2"], bit=4, descricao="SA_FALHA_FECHAR_52SA2")
        self.condicionadores.append(CondicionadorBase(self.leitura_falha_fechar_52sa2, CONDIC_INDISPONIBILIZAR))

        self.leitura_falha_abrir_52sa3 = LeituraModbusBit(self.clp["SA"], REG_CLP["SA"]["FALHA_ABRIR_52SA3"], bit=5, descricao="SA_FALHA_ABRIR_52SA3")
        self.condicionadores.append(CondicionadorBase(self.leitura_falha_abrir_52sa3, CONDIC_INDISPONIBILIZAR))

        self.leitura_falha_fechar_52sa3 = LeituraModbusBit(self.clp["SA"], REG_CLP["SA"]["FALHA_FECHAR_52SA3"], bit=6, descricao="SA_FALHA_FECHAR_52SA3")
        self.condicionadores.append(CondicionadorBase(self.leitura_falha_fechar_52sa3, CONDIC_INDISPONIBILIZAR))

        self.leitura_fusivel_queimado_retificador = LeituraModbusBit(self.clp["SA"], REG_CLP["SA"]["RETIFICADOR_FUSIVEL_QUEIMADO"], bit=2, descricao="SA_RETIFICADOR_FUSIVEL_QUEIMADO")
        self.condicionadores.append(CondicionadorBase(self.leitura_fusivel_queimado_retificador, CONDIC_INDISPONIBILIZAR))

        self.leitura_fuga_terra_positivo_retificador = LeituraModbusBit(self.clp["SA"], REG_CLP["SA"]["RETIFICADOR_FUGA_TERRA_POSITIVO"], bit=5, descricao="SA_RETIFICADOR_FUGA_TERRA_POSITIVO")
        self.condicionadores.append(CondicionadorBase(self.leitura_fuga_terra_positivo_retificador, CONDIC_INDISPONIBILIZAR))

        self.leitura_fuga_terra_negativo_retificador = LeituraModbusBit(self.clp["SA"], REG_CLP["SA"]["RETIFICADOR_FUGA_TERRA_NEGATIVO"], bit=6, descricao="SA_RETIFICADOR_FUGA_TERRA_NEGATIVO")
        self.condicionadores.append(CondicionadorBase(self.leitura_fuga_terra_negativo_retificador, CONDIC_INDISPONIBILIZAR))

        # LEITURAS PARA LEITURA PERIODICA
        # Telegram
            # Bit Invertido
        self.leitura_bomba_sis_agua_disp = LeituraModbusBit(self.clp["SA"], REG_CLP["SA"]["SISTEMA_AGUA_BOMBA_DISPONIVEL"], bit=0, invertido=True, descricao="SA_SISTEMA_AGUA_BOMBA_DISPONIVEL")

            # Bit Normal
        self.leitura_falha_bomba_drenagem_1 = LeituraModbusBit(self.clp["SA"], REG_CLP["SA"]["DRENAGEM_BOMBA_1_FALHA"], bit=0, descricao="SA_DRENAGEM_BOMBA_1_FALHA")
        self.leitura_falha_bomba_drenagem_2 = LeituraModbusBit(self.clp["SA"], REG_CLP["SA"]["DRENAGEM_BOMBA_2_FALHA"], bit=2, descricao="SA_DRENAGEM_BOMBA_2_FALHA")
        self.leitura_falha_bomba_drenagem_3 = LeituraModbusBit(self.clp["SA"], REG_CLP["SA"]["DRENAGEM_BOMBA_3_FALHA"], bit=4, descricao="SA_DRENAGEM_BOMBA_3_FALHA")
        self.leitura_falha_ligar_bomba_sis_agua = LeituraModbusBit(self.clp["SA"], REG_CLP["SA"]["SISTEMA_AGUA_FALHA_LIGA_BOMBA"], bit=1, descricao="SA_SISTEMA_AGUA_FALHA_LIGA_BOMBA")
        self.leitura_djs_barra_seletora_remoto = LeituraModbusBit(self.clp["SA"], REG_CLP["SA"]["DISJUNTORES_BARRA_SELETORA_REMOTO"], bit=9, descricao="SA_DISJUNTORES_BARRA_SELETORA_REMOTO")
        self.leitura_discrepancia_boia_poco_drenagem = LeituraModbusBit(self.clp["SA"], REG_CLP["SA"]["DRENAGEM_DISCREPANCIA_BOIAS_POCO"], bit=9, descricao="SA_DRENAGEM_DISCREPANCIA_BOIAS_POCO")

        # Telegram + Voip
            # Bit Invertido
        self.leitura_sem_falha_52sa3 = LeituraModbusBit(self.clp["SA"], REG_CLP["SA"]["52SA3_SEM_FALHA"], bit=3, invertido=True, descricao="SA_52SA3_SEM_FALHA")
        self.leitura_sem_falha_52sa2 = LeituraModbusBit(self.clp["SA"], REG_CLP["SA"]["52SA2_SEM_FALHA"], bit=1, invertido=True, descricao="SA_52SA2_SEM_FALHA")
        self.leitura_sem_falha_52sa1 = LeituraModbusBit(self.clp["SA"], REG_CLP["SA"]["52SA1_SEM_FALHA"], bit=31, invertido=True, descricao="SA_52SA1_SEM_FALHA")

            # Bit Normal
        self.leitura_falha_parar_gmg = LeituraModbusBit(self.clp["SA"], REG_CLP["SA"]["GMG_FALHA_PARAR"], bit=7, descricao="SA_GMG_FALHA_PARAR")
        self.leitura_falha_partir_gmg = LeituraModbusBit(self.clp["SA"], REG_CLP["SA"]["GMG_FALHA_PARTIR"], bit=6, descricao="SA_GMG_FALHA_PARTIR")
        self.leitura_operacao_manual_gmg = LeituraModbusBit(self.clp["SA"], REG_CLP["SA"]["GMG_OPERACAO_MANUAL"], bit=10, descricao="SA_GMG_OPERACAO_MANUAL")
        self.leitura_falha_bomba_filtragem = LeituraModbusBit(self.clp["SA"], REG_CLP["SA"]["FILTRAGEM_BOMBA_FALHA"], bit=6, descricao="SA_FILTRAGEM_BOMBA_FALHA")
        self.leitura_nivel_alto_poco_drenagem = LeituraModbusBit(self.clp["SA"], REG_CLP["SA"]["POCO_DRENAGEM_NIVEL_ALTO"], bit=26, descricao="SA_POCO_DRENAGEM_NIVEL_ALTO")
        self.leitura_falha_bomba_drenagem_uni = LeituraModbusBit(self.clp["SA"], REG_CLP["SA"]["DRENAGEM_UNIDADES_BOMBA_FALHA"], bit=12, descricao="SA_DRENAGEM_UNIDADES_BOMBA_FALHA")
        self.leitura_alarme_sistema_incendio_atuado = LeituraModbusBit(self.clp["SA"], REG_CLP["SA"]["SISTEMA_INCENDIO_ALARME_ATUADO"], bit=6, descricao="SA_SISTEMA_INCENDIO_ALARME_ATUADO")
        self.leitura_alarme_sistema_seguraca_atuado = LeituraModbusBit(self.clp["SA"], REG_CLP["SA"]["SISTEMA_SEGURANCA_ALARME_ATUADO"], bit=7, descricao="SA_SISTEMA_SEGURANCA_ALARME_ATUADO")
        self.leitura_nivel_muito_alto_poco_drenagem = LeituraModbusBit(self.clp["SA"], REG_CLP["SA"]["POCO_DRENAGEM_NIVEL_MUITO_ALTO"], bit=25, descricao="SA_POCO_DRENAGEM_NIVEL_MUITO_ALTO")
        self.leitura_falha_tubo_succao_bomba_recalque = LeituraModbusBit(self.clp["SA"], REG_CLP["SA"]["BOMBA_RECALQUE_TUBO_SUCCAO_FALHA"], bit=14, descricao="SA_BOMBA_RECALQUE_TUBO_SUCCAO_FALHA")