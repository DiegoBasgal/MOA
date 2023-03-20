import logging
import traceback

from time import sleep, time

from leituras import *
from mensageiro import voip
from condicionadores import *
from dicionarios.reg import *
from dicionarios.const import *

from clients import ClpClients
from unidade_geracao import UnidadeDeGeracao

logger = logging.getLogger("__main__")

class Ocorrencias:
    def __init__(self, sd: dict=None, clp: ClpClients=None, ugs: list[UnidadeDeGeracao]=None):
        if not sd:
            logger.warning("[OCO] Houve um erro ao carregar arquivos de configuração (\"shared_dict\").")
            raise ValueError
        else:
            self.dict = sd

        if not clp:
            logger.warning("[OCO-USN] Não foi possível carregar classes de conexão com clps | campo | banco de dados.")
            raise ConnectionError
        else:
            self.clp_usn = clp.clp_dict[1]
            self.clp_tda = clp.clp_dict[2]
            self.clp_ug = {
                "ug1": clp.clp_dict[3],
                "ug2": clp.clp_dict[4]
            }

        if not ugs:
            logger.error("[OCO] A lista de ugs é necessária para realizar a leitura de ocorrências.")
            raise ValueError
        else:
            self._ugs = ugs
            self._ug1 = ugs[0]
            self._ug2 = ugs[1]

        # Variáveis Públicas
        self.voip_ug: bool = None
        self.voip_usn: bool = None

        self.voip_dict: dict = voip.vars_dict

    # Property/Setter Protegidos
    @property
    def ugs(self) -> list[UnidadeDeGeracao]:
        return self._ugs

    @ugs.setter
    def ugs(self, var: list[UnidadeDeGeracao]) -> None:
        self._ugs = var

    def leitura_periodica(self, delay: int) -> None:
        logger.debug("[OCO] Iniciando o timer de leitura por hora.")
        try:
            proxima_leitura = time() + delay
            while True:
                if OcorrenciasUsn.leitura_temporizada() or (OcorrenciasUg.leitura_temporizada(ug) for ug in self.ugs):
                    self.acionar_voip()
                sleep(max(0, proxima_leitura - time()))
                proxima_leitura += (time() - proxima_leitura) // delay * delay + delay

        except Exception as e:
            logger.exception(f"[OCO] Houve um problema ao executar a leitura por hora. Exception: \"{repr(e)}\"")
            logger.exception(f"[OCO] Traceback: {traceback.print_stack}")

    def acionar_voip(self) -> None:
        try:
            if self.voip_usn or self.voip_ug:
                for i, j in zip(self.dict["VOIP"], self.voip_dict):
                    if i == j and self.dict["VOIP"][i]:
                        self.voip_dict[j][0] = self.dict["VOIP"][i]
                voip.enviar_voz_auxiliar()
                self.voip_ug = False
                self.voip_usn = False

            if self.dict["GLB"]["avisado_em_eletrica"]:
                voip.enviar_voz_emergencia()
                self.dict["GLB"]["avisado_em_eletrica"] = False

        except Exception as e:
            logger.exception(f"[OCO] Houve um problema ao ligar por Voip. Exception: \"{repr(e)}\"")
            logger.exception(f"[OCO] Traceback: {traceback.print_stack}")


class OcorrenciasUsn(Ocorrencias):
    def __init__(self, sd, ugs):
        super().__init__(sd, ugs)

        self._condicionadores: list[CondicionadorBase]
        self._condicionadores_essenciais: list[CondicionadorBase]

        self.flag: int = CONDIC_IGNORAR

        self.leitura_condicionadores()

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
            condicionadores_ativos = [condic for condics in [self.condicionadores_essenciais, self.condicionadores] for condic in condics if condic.ativo]

            self.flag = [CONDIC_NORMALIZAR for condic in condicionadores_ativos if condic.gravidade == CONDIC_NORMALIZAR]
            self.flag = [CONDIC_INDISPONIBILIZAR for condic in condicionadores_ativos if condic.gravidade == CONDIC_INDISPONIBILIZAR]

            logger.warning(f"[OCO-USN] Foram detectados condicionadores ativos na Usina:")
            [logger.warning(f"[OCO-USN] Descrição: \"{condic.descr}\", Gravidade: {CONDIC_STR_DCT[condic.gravidade] if condic.gravidade in CONDIC_STR_DCT else 'Desconhecida'}") for condic in condicionadores_ativos]

        return self.flag

    def leitura_temporizada(self) -> bool:
        try:
            if LeituraModbusCoil(SA["SA_ED_GMG_Trip"], self.clp_usn).valor != 0:
                logger.warning("[OCO-USN] O sensor de TRIP do Grupo Motor Gerador foi acionado, favor verificar.")

            leitura_QCADE_BombasDng_Auto = LeituraModbusCoil(SA["SA_ED_QCADE_BombasDng_Auto"], self.clp_usn)
            if leitura_QCADE_BombasDng_Auto.valor == 0 and not self.dict["VOIP"]["BombasDngRemoto"]:
                logger.warning("[OCO-USN] O poço de drenagem da Usina saiu do modo remoto, favor verificar.")
                self.dict["VOIP"]["BombasDngRemoto"] = True
                self.voip_usn = True
            elif leitura_QCADE_BombasDng_Auto.valor == 1 and self.dict["VOIP"]["BombasDngRemoto"]:
                self.dict["VOIP"]["BombasDngRemoto"] = False

            return True if self.voip_usn else False

        except Exception as e:
            logger.exception(f"[OCO-USN] Houve um erro ao realizar a leitura temporizada da Usina. Exception: \"{repr(e)}\"")
            logger.exception(f"[OCO-USN] Traceback: {traceback.print_stack}")
            return False

    def leitura_condicionadores(self) -> None:
        leitura_ED_QCAP_TensaoPresenteTSA = LeituraModbusCoil(SA["SA_ED_QCAP_TensaoPresenteTSA"], self.clp_usn)
        self.condicionadores_essenciais.append(CondicionadorBase(leitura_ED_QCAP_TensaoPresenteTSA, CONDIC_NORMALIZAR))

        leitura_ED_SEL787_Trip = LeituraModbusCoil(SA["SA_ED_SEL787_Trip"], self.clp_usn)
        self.condicionadores_essenciais.append(CondicionadorBase(leitura_ED_SEL787_Trip))

        if not self.dict["GLB"]["tda_offline"]:
            leitura_ED_QcataDisj52ETrip = LeituraModbusCoil(TDA["TDA_ED_QcataDisj52ETrip"], self.clp_tda)
            self.condicionadores.append(CondicionadorBase(leitura_ED_QcataDisj52ETrip))

        leitura_ED_MRU3_Falha = LeituraModbusCoil(SA["SA_ED_MRU3_Falha"], self.clp_usn)
        self.condicionadores.append(CondicionadorBase(leitura_ED_MRU3_Falha))

        leitura_ED_SEL787_FalhaInterna = LeituraModbusCoil(SA["SA_ED_SEL787_FalhaInterna"], self.clp_usn)
        self.condicionadores.append(CondicionadorBase(leitura_ED_SEL787_FalhaInterna))


class OcorrenciasUg(Ocorrencias):
    def __init__(self, sd, ugs):
        super().__init__(sd, ugs)

        self._temperatura_base: int = 100
        self._temperatura_limite: int = 200
        self._pressao_caixa_base: float = 16
        self._pressao_caixa_limite: float = 15.5

        self._condicionadores: list[CondicionadorBase]
        self._condicionadores_essenciais: list[CondicionadorBase]
        self._condicionadores_atenuadores: list[CondicionadorBase]

        self._leitura_dict: dict[str, LeituraBase]
        self._condic_dict: dict[str, CondicionadorExponencial | CondicionadorExponencialReverso]

        self.flag: int = CONDIC_IGNORAR

        for ug in self.ugs: 
            self.leitura_condicionadores(ug)

    @property
    def temperatura_base(self) -> int:
        return self._temperatura_base

    @temperatura_base.setter
    def temperatura_base(self, var: int) -> None:
        self._temperatura_base = var

    @property
    def temperatura_limite(self) -> int:
        return self._temperatura_limite

    @temperatura_limite.setter
    def temperatura_limite(self, var: int) -> None:
        self._temperatura_limite = var

    @property
    def pressao_caixa_base(self) -> float:
        return self._pressao_caixa_base

    @pressao_caixa_base.setter
    def pressao_caixa_base(self, var: float):
        self._pressao_caixa_base = var

    @property
    def pressao_caixa_limite(self) -> float:
        return self._pressao_caixa_limite

    @pressao_caixa_limite.setter
    def pressao_caixa_limite(self, var: float):
        self._pressao_caixa_limite = var

    @property
    def condic_dict(self) -> dict[str, CondicionadorExponencial]:
        return self._condic_dict

    @condic_dict.setter
    def condic_dict(self, var: dict[str, CondicionadorExponencial]) -> None:
        self._condic_dict = var
    
    @property
    def leitura_dict(self) -> dict[str, LeituraBase]:
        return self._leitura_dict

    @leitura_dict.setter
    def leitura_dict(self, var: dict[str, LeituraBase]) -> None:
        self._leitura_dict = var

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

    @property
    def condicionadores_atenuadores(self) -> list[CondicionadorBase]:
        return self._condicionadores_atenuadores

    @condicionadores_atenuadores.setter
    def condicionadores_atenuadores(self, var: list[CondicionadorBase]) -> None:
        self._condicionadores_atenuadores = var

    def verificar_condicionadores(self, ug: UnidadeDeGeracao) -> int:
        if [condic.ativo for condic in self.condicionadores_essenciais]:
            condicionadores_ativos = [x for y in [self.condicionadores_essenciais, self.condicionadores] for x in y if x.ativo]

            self.flag = [CONDIC_NORMALIZAR for condic in condicionadores_ativos if condic.gravidade == CONDIC_NORMALIZAR]
            self.flag = [CONDIC_AGUARDAR for condic in condicionadores_ativos if condic.gravidade == CONDIC_AGUARDAR]
            self.flag = [CONDIC_INDISPONIBILIZAR for condic in condicionadores_ativos if condic.gravidade == CONDIC_INDISPONIBILIZAR]

            logger.warning(f"[OCO-UG{ug.id}] Foram detectados condicionadores ativos na UG:")
            [logger.warning(f"[OCO-UG{ug.id}] Descrição: \"{condic.descr}\", Gravidade: {CONDIC_STR_DCT[condic.gravidade] if condic.gravidade in CONDIC_STR_DCT else 'Desconhecida'}") for condic in condicionadores_ativos]

        return self.flag

    def atualizar_limites_condicionadores(self, parametros, ug: UnidadeDeGeracao) -> None:
        try:
            ug.prioridade = int(parametros[f"ug{ug.id}_prioridade"])
            self.condic_dict[f"tmp_fase_r_ug{ug.id}"].valor_base = float(parametros[f"alerta_temperatura_fase_r_ug{ug.id}"])
            self.condic_dict[f"tmp_fase_r_ug{ug.id}"].valor_limite = float(parametros[f"limite_temperatura_fase_r_ug{ug.id}"])
            self.condic_dict[f"tmp_fase_s_ug{ug.id}"].valor_base = float(parametros[f"alerta_temperatura_fase_s_ug{ug.id}"])
            self.condic_dict[f"tmp_fase_s_ug{ug.id}"].valor_limite = float(parametros[f"limite_temperatura_fase_s_ug{ug.id}"])
            self.condic_dict[f"tmp_fase_t_ug{ug.id}"].valor_base = float(parametros[f"alerta_temperatura_fase_t_ug{ug.id}"])
            self.condic_dict[f"tmp_fase_t_ug{ug.id}"].valor_limite = float(parametros[f"limite_temperatura_fase_t_ug{ug.id}"])
            self.condic_dict[f"tmp_nucleo_gerador_1_ug{ug.id}"].valor_base = float(parametros[f"alerta_temperatura_nucleo_gerador_1_ug{ug.id}"])
            self.condic_dict[f"tmp_nucleo_gerador_1_ug{ug.id}"].valor_limite = float(parametros[f"limite_temperatura_nucleo_gerador_1_ug{ug.id}"])
            self.condic_dict[f"tmp_nucleo_gerador_2_ug{ug.id}"].valor_base = float(parametros[f"alerta_temperatura_nucleo_gerador_2_ug{ug.id}"])
            self.condic_dict[f"tmp_nucleo_gerador_2_ug{ug.id}"].valor_limite = float(parametros[f"limite_temperatura_nucleo_gerador_2_ug{ug.id}"])
            self.condic_dict[f"tmp_nucleo_gerador_3_ug{ug.id}"].valor_base = float(parametros[f"alerta_temperatura_nucleo_gerador_3_ug{ug.id}"])
            self.condic_dict[f"tmp_nucleo_gerador_3_ug{ug.id}"].valor_limite = float(parametros[f"limite_temperatura_nucleo_gerador_3_ug{ug.id}"])
            self.condic_dict[f"tmp_mancal_casq_rad_ug{ug.id}"].valor_base = float(parametros[f"alerta_temperatura_mancal_casq_rad_ug{ug.id}"])
            self.condic_dict[f"tmp_mancal_casq_rad_ug{ug.id}"].valor_limite = float(parametros[f"limite_temperatura_mancal_casq_rad_ug{ug.id}"])
            self.condic_dict[f"tmp_mancal_casq_comb_ug{ug.id}"].valor_base = float(parametros[f"alerta_temperatura_mancal_casq_comb_ug{ug.id}"])
            self.condic_dict[f"tmp_mancal_casq_comb_ug{ug.id}"].valor_limite = float(parametros[f"limite_temperatura_mancal_casq_comb_ug{ug.id}"])
            self.condic_dict[f"tmp_mancal_escora_comb_ug{ug.id}"].valor_base = float(parametros[f"alerta_temperatura_mancal_escora_comb_ug{ug.id}"])
            self.condic_dict[f"tmp_mancal_escora_comb_ug{ug.id}"].valor_limite = float(parametros[f"limite_temperatura_mancal_escora_comb_ug{ug.id}"])
            self.condic_dict[f"cx_espiral_ug{ug.id}"].valor_base = float(parametros[f"alerta_caixa_espiral_ug{ug.id}"])
            self.condic_dict[f"cx_espiral_ug{ug.id}"].valor_limite = float(parametros[f"limite_caixa_espiral_ug{ug.id}"])

        except Exception as e:
            logger.exception(f"[OCO-UG{ug.id}] Houve um erro ao atualizar os limites de temperaturas dos condicionadores. Exception: \"{repr(e)}\"")
            logger.exception(f"[OCO-UG{ug.id}] Traceback: {traceback.print_stack}")

    def controle_limites_operacao(self, ug: UnidadeDeGeracao) -> None:
        # TODO adicionar borda no caso de ter disparado a mensagem num tempo pre definido
        ld = self.leitura_dict
        cd = self.condic_dict

        if ld[f"tmp_fase_r_ug{ug.id}"].valor >= cd[f"tmp_fase_r_ug{ug.id}"].valor_base:
            logger.warning(f"[UG{ug.id}] A temperatura de Fase R da UG passou do valor base! ({cd[f'tmp_fase_r_ug{ug.id}'].valor_base}C) | Leitura: {ld[f'tmp_fase_r_ug{ug.id}'].valor}C")

        if ld[f"tmp_fase_r_ug{ug.id}"].valor >= 0.9*(cd[f"tmp_fase_r_ug{ug.id}"].valor_limite - cd[f"tmp_fase_r_ug{ug.id}"].valor_base) + cd[f"tmp_fase_r_ug{ug.id}"].valor_base:
            logger.critical(f"[UG{ug.id}] A temperatura de Fase R da UG está muito próxima do limite! ({cd[f'tmp_fase_r_ug{ug.id}'].valor_limite}C) | Leitura: {ld[f'tmp_fase_r_ug{ug.id}'].valor}C")

        if ld[f"tmp_fase_s_ug{ug.id}"].valor >= cd[f"tmp_fase_s_ug{ug.id}"].valor_base:
            logger.warning(f"[UG{ug.id}] A temperatura de Fase S da UG passou do valor base! ({cd[f'tmp_fase_s_ug{ug.id}'].valor_base}C) | Leitura: {ld[f'tmp_fase_s_ug{ug.id}'].valor}C")

        if ld[f"tmp_fase_s_ug{ug.id}"].valor >= 0.9*(cd[f"tmp_fase_s_ug{ug.id}"].valor_limite - cd[f"tmp_fase_s_ug{ug.id}"].valor_base) + cd[f"tmp_fase_s_ug{ug.id}"].valor_base:
            logger.critical(f"[UG{ug.id}] A temperatura de Fase S da UG está muito próxima do limite! ({cd[f'tmp_fase_s_ug{ug.id}'].valor_limite}C) | Leitura: {ld[f'tmp_fase_s_ug{ug.id}'].valor}C")

        if ld[f"tmp_fase_t_ug{ug.id}"].valor >= cd[f"tmp_fase_t_ug{ug.id}"].valor_base:
            logger.warning(f"[UG{ug.id}] A temperatura de Fase T da UG passou do valor base! ({cd[f'tmp_fase_t_ug{ug.id}'].valor_base}C) | Leitura: {ld[f'tmp_fase_t_ug{ug.id}'].valor}C")

        if ld[f"tmp_fase_t_ug{ug.id}"].valor >= 0.9*(cd[f"tmp_fase_t_ug{ug.id}"].valor_limite - cd[f"tmp_fase_t_ug{ug.id}"].valor_base) + cd[f"tmp_fase_t_ug{ug.id}"].valor_base:
            logger.critical(f"[UG{ug.id}] A temperatura de Fase T da UG está muito próxima do limite! ({cd[f'tmp_fase_t_ug{ug.id}'].valor_limite}C) | Leitura: {ld[f'tmp_fase_t_ug{ug.id}'].valor}C")

        if ld[f"tmp_nucleo_gerador_1_ug{ug.id}"].valor >= cd[f"tmp_nucleo_gerador_1_ug{ug.id}"].valor_base:
            logger.warning(f"[UG{ug.id}] A temperatura do Núcleo Gerador 1 da UG passou do valor base! ({cd[f'tmp_nucleo_gerador_1_ug{ug.id}'].valor_base}C) | Leitura: {cd[f'tmp_nucleo_gerador_1_ug{ug.id}'].valor}C")

        if ld[f"tmp_nucleo_gerador_1_ug{ug.id}"].valor >= 0.9*(cd[f"tmp_nucleo_gerador_1_ug{ug.id}"].valor_limite - cd[f"tmp_nucleo_gerador_1_ug{ug.id}"].valor_base) + cd[f"tmp_nucleo_gerador_1_ug{ug.id}"].valor_base:
            logger.critical(f"[UG{ug.id}] A temperatura do Núcleo Gerador 1 da UG está muito próxima do limite! ({cd[f'tmp_nucleo_gerador_1_ug{ug.id}'].valor_limite}C) | Leitura: {cd[f'tmp_nucleo_gerador_1_ug{ug.id}'].valor}C")

        if ld[f"tmp_nucleo_gerador_2_ug{ug.id}"].valor >= cd[f"tmp_nucleo_gerador_2_ug{ug.id}"].valor_base:
            logger.warning(f"[UG{ug.id}] A temperatura do Núcleo Gerador 2 da UG passou do valor base! ({cd[f'tmp_nucleo_gerador_2_ug{ug.id}'].valor_base}C) | Leitura: {cd[f'tmp_nucleo_gerador_2_ug{ug.id}'].valor}C")

        if ld[f"tmp_nucleo_gerador_2_ug{ug.id}"].valor >= 0.9*(cd[f"tmp_nucleo_gerador_2_ug{ug.id}"].valor_limite - cd[f"tmp_nucleo_gerador_2_ug{ug.id}"].valor_base) + cd[f"tmp_nucleo_gerador_2_ug{ug.id}"].valor_base:
            logger.critical(f"[UG{ug.id}] A temperatura do Núcleo Gerador 2 da UG está muito próxima do limite! ({cd[f'tmp_nucleo_gerador_2_ug{ug.id}'].valor_limite}C) | Leitura: {cd[f'tmp_nucleo_gerador_2_ug{ug.id}'].valor}C")

        if ld[f"tmp_nucleo_gerador_3_ug{ug.id}"].valor >= cd[f"tmp_nucleo_gerador_3_ug{ug.id}"].valor_base:
            logger.warning(f"[UG{ug.id}] A temperatura do Núcleo Gerador 3 da UG passou do valor base! ({cd[f'tmp_nucleo_gerador_3_ug{ug.id}'].valor_base}C) | Leitura: {cd[f'tmp_nucleo_gerador_3_ug{ug.id}'].valor}C")

        if ld[f"tmp_nucleo_gerador_3_ug{ug.id}"].valor >= 0.9*(cd[f"tmp_nucleo_gerador_3_ug{ug.id}"].valor_limite - cd[f"tmp_nucleo_gerador_3_ug{ug.id}"].valor_base) + cd[f"tmp_nucleo_gerador_3_ug{ug.id}"].valor_base:
            logger.critical(f"[UG{ug.id}] A temperatura do Núcleo Gerador 3 da UG está muito próxima do limite! ({cd[f'tmp_nucleo_gerador_3_ug{ug.id}'].valor_limite}C) | Leitura: {cd[f'tmp_nucleo_gerador_3_ug{ug.id}'].valor}C")

        if ld[f"tmp_mancal_casq_rad_ug{ug.id}"].valor >= cd[f"tmp_mancal_casq_rad_ug{ug.id}"].valor_base:
            logger.warning(f"[UG{ug.id}] A temperatura do Mancal Casquilho Radial da UG passou do valor base! ({cd[f'tmp_mancal_casq_rad_ug{ug.id}'].valor_base}C) | Leitura: {cd[f'tmp_mancal_casq_rad_ug{ug.id}'].valor}C")

        if ld[f"tmp_mancal_casq_rad_ug{ug.id}"].valor >= 0.9*(cd[f"tmp_mancal_casq_rad_ug{ug.id}"].valor_limite - cd[f"tmp_mancal_casq_rad_ug{ug.id}"].valor_base) + cd[f"tmp_mancal_casq_rad_ug{ug.id}"].valor_base:
            logger.critical(f"[UG{ug.id}] A temperatura do Mancal Casquilho Radial da UG está muito próxima do limite! ({cd[f'tmp_mancal_casq_rad_ug{ug.id}'].valor_limite}C) | Leitura: {cd[f'tmp_mancal_casq_rad_ug{ug.id}'].valor}C")

        if ld[f"tmp_mancal_casq_comb_ug{ug.id}"].valor >= cd[f"tmp_mancal_casq_comb_ug{ug.id}"].valor_base:
            logger.warning(f"[UG{ug.id}] A temperatura do Mancal Casquilho Combinado da UG passou do valor base! ({cd[f'tmp_mancal_casq_comb_ug{ug.id}'].valor_base}C) | Leitura: {cd[f'tmp_mancal_casq_comb_ug{ug.id}'].valor}C")

        if ld[f"tmp_mancal_casq_comb_ug{ug.id}"].valor >= 0.9*(cd[f"tmp_mancal_casq_comb_ug{ug.id}"].valor_limite - cd[f"tmp_mancal_casq_comb_ug{ug.id}"].valor_base) + cd[f"tmp_mancal_casq_comb_ug{ug.id}"].valor_base:
            logger.critical(f"[UG{ug.id}] A temperatura do Mancal Casquilho Combinado da UG está muito próxima do limite! ({cd[f'tmp_mancal_casq_comb_ug{ug.id}'].valor_limite}C) | Leitura: {cd[f'tmp_mancal_casq_comb_ug{ug.id}'].valor}C")

        if ld[f"tmp_mancal_escora_comb_ug{ug.id}"].valor >= cd[f"tmp_mancal_escora_comb_ug{ug.id}"].valor_base:
            logger.warning(f"[UG{ug.id}] A temperatura do Mancal Escora Combinado da UG passou do valor base! ({cd[f'tmp_mancal_escora_comb_ug{ug.id}'].valor_base}C) | Leitura: {cd[f'tmp_mancal_escora_comb_ug{ug.id}'].valor}C")

        if ld[f"tmp_mancal_escora_comb_ug{ug.id}"].valor >= 0.9*(cd[f"tmp_mancal_escora_comb_ug{ug.id}"].valor_limite - cd[f"tmp_mancal_escora_comb_ug{ug.id}"].valor_base) + cd[f"tmp_mancal_escora_comb_ug{ug.id}"].valor_base:
            logger.critical(f"[UG{ug.id}] A temperatura do Mancal Escora Combinado da UG está muito próxima do limite! ({cd[f'tmp_mancal_escora_comb_ug{ug.id}'].valor_limite}C) | Leitura: {cd[f'tmp_mancal_escora_comb_ug{ug.id}'].valor}C")

        if ld[f"cx_espiral_ug{ug.id}"].valor <= cd[f"cx_espiral_ug{ug.id}"].valor_base and ld[f"cx_espiral_ug{ug.id}"].valor != 0 and ug.etapa_atual == UG_SINCRONIZADA:
            logger.warning(f"[UG{ug.id}] A pressão Caixa Espiral da UG passou do valor base! ({cd[f'cx_espiral_ug{ug.id}'].valor_base:03.2f} KGf/m2) | Leitura: {ld[f'cx_espiral_ug{ug.id}'].valor:03.2f}")

        if ld[f"cx_espiral_ug{ug.id}"].valor <= cd[f"cx_espiral_ug{ug.id}"].valor_limite+0.9*(cd[f"cx_espiral_ug{ug.id}"].valor_base - cd[f"cx_espiral_ug{ug.id}"].valor_limite) and ld[f"cx_espiral_ug{ug.id}"].valor != 0 and ug.etapa_atual == UG_SINCRONIZADA:
            logger.critical(f"[UG{ug.id}] A pressão Caixa Espiral da UG está muito próxima do limite! ({cd[f'cx_espiral_ug{ug.id}'].valor_limite:03.2f} KGf/m2) | Leitura: {ld[f'cx_espiral_ug{ug.id}'].valor:03.2f} KGf/m2")


    def leitura_temporizada(self, ug: UnidadeDeGeracao) -> bool:
        try:
            if LeituraModbusCoil(UG[f"UG{ug.id}_ED_FreioPastilhaGasta"], self.clp_ug[f"ug{ug.id}"]).valor != 0:
                logger.warning(f"[OCO-UG{ug.id}] O sensor de Freio da UG retornou que a Pastilha está gasta, favor considerar troca.")

            leitura_ED_FreioCmdRemoto = LeituraModbusCoil(UG[f"UG{ug.id}_ED_FreioCmdRemoto"], self.clp_ug[f"ug{ug.id}"])
            if leitura_ED_FreioCmdRemoto.valor == 0 and not self.dict["VOIP"][f"UG{ug.id}_FreioCmdRemoto"]:
                logger.warning(f"[OCO-UG{ug.id}] O freio da UG saiu do modo remoto, favor analisar a situação.")
                self.dict["VOIP"][f"UG{ug.id}_FreioCmdRemoto"] = True
                self.voip_ug = True
            elif leitura_ED_FreioCmdRemoto.valor == 1 and self.dict["VOIP"][f"UG{ug.id}_FreioCmdRemoto"]:
                self.dict["VOIP"][f"UG{ug.id}_FreioCmdRemoto"] = False

            return True if self.voip_ug else False

        except Exception as e:
            logger.exception(f"[OCO-UG{ug.id}] Houve um erro ao executar a leitura temporizada da UG{ug.id}. Exception: \"{repr(e)}\"")
            logger.exception(f"[OCO-UG{ug.id}] Traceback: {traceback.print_stack}")
            return False

    def leitura_condicionadores(self, ug: UnidadeDeGeracao) -> None:
        # Leituras -> Condicionadores
        # Fase R
        self.leitura_dict[f"tmp_fase_r_ug{ug.id}"] = LeituraModbus(
            UG[f"UG{ug.id}_RA_Temperatura_01"],
            self.clp_ug,
            op=4
        )
        self.condic_dict[f"tmp_fase_r_ug{ug.id}"] = CondicionadorExponencial(
            self.leitura_dict[f"tmp_fase_r_ug{ug.id}"]
        )
        self.condicionadores_essenciais.append(self.condic_dict[f"tmp_fase_r_ug{ug.id}"])

        # Fase S
        self.leitura_dict[f"tmp_fase_s_ug{ug.id}"] = LeituraModbus(
            UG[f"UG{ug.id}_RA_Temperatura_02"],
            self.clp_ug,
            op=4
        )
        self.condic_dict[f"tmp_fase_s_ug{ug.id}"] = CondicionadorExponencial(
            self.leitura_dict[f"tmp_fase_s_ug{ug.id}"]
        )
        self.condicionadores_essenciais.append(self.condic_dict[f"tmp_fase_s_ug{ug.id}"])

        # Fase T
        self.leitura_dict[f"tmp_fase_t_ug{ug.id}"] = LeituraModbus(
            UG[f"UG{ug.id}_RA_Temperatura_03"],
            self.clp_ug,
            op=4
        )
        self.condic_dict[f"tmp_fase_t_ug{ug.id}"] = CondicionadorExponencial(
            self.leitura_dict[f"tmp_fase_t_ug{ug.id}"]
        )
        self.condicionadores_essenciais.append(self.condic_dict[f"tmp_fase_t_ug{ug.id}"])

        # Nucleo Gerador 1
        self.leitura_dict[f"tmp_nucleo_gerador_1_ug{ug.id}"] = LeituraModbus(
            UG[f"UG{ug.id}_RA_Temperatura_04"],
            self.clp_ug,
            op=4
        )
        self.condic_dict[f"tmp_nucleo_gerador_1_ug{ug.id}"] = CondicionadorExponencial(
            self.leitura_dict[f"tmp_nucleo_gerador_1_ug{ug.id}"]
        )
        self.condicionadores_essenciais.append(self.condic_dict[f"tmp_nucleo_gerador_1_ug{ug.id}"])

        # Nucleo Gerador 2
        self.leitura_dict[f"tmp_nucleo_gerador_2_ug{ug.id}"] = LeituraModbus(
            UG[f"UG{ug.id}_RA_Temperatura_04"],
            self.clp_ug,
            op=4
        )
        self.condic_dict[f"tmp_nucleo_gerador_2_ug{ug.id}"] = CondicionadorExponencial(
            self.leitura_dict[f"tmp_nucleo_gerador_2_ug{ug.id}"]
        )
        self.condicionadores_essenciais.append(self.condic_dict[f"tmp_nucleo_gerador_2_ug{ug.id}"])

        # Nucleo Gerador 3
        self.leitura_dict[f"tmp_nucleo_gerador_3_ug{ug.id}"] = LeituraModbus(
            UG[f"UG{ug.id}_RA_Temperatura_04"],
            self.clp_ug,
            op=4
        )
        self.condic_dict[f"tmp_nucleo_gerador_3_ug{ug.id}"] = CondicionadorExponencial(
            self.leitura_dict[f"tmp_nucleo_gerador_3_ug{ug.id}"]
        )
        self.condicionadores_essenciais.append(self.condic_dict[f"tmp_nucleo_gerador_3_ug{ug.id}"])

        # Mancal Casquilho Radial
        self.leitura_dict[f"tmp_mancal_casq_rad_ug{ug.id}"] = LeituraModbus(
            UG[f"UG{ug.id}_RA_Temperatura_08"],
            self.clp_ug,
            op=4
        )
        self.condic_dict[f"tmp_mancal_casq_rad_ug{ug.id}"] = CondicionadorExponencial(
            self.leitura_dict[f"tmp_mancal_casq_rad_ug{ug.id}"]
        )
        self.condicionadores_essenciais.append(self.condic_dict[f"tmp_mancal_casq_rad_ug{ug.id}"])

        # Mancal Casquilho Combinado
        self.leitura_dict[f"tmp_mancal_casq_comb_ug{ug.id}"] = LeituraModbus(
            UG[f"UG{ug.id}_RA_Temperatura_10"],
            self.clp_ug,
            op=4
        )
        self.condic_dict[f"tmp_mancal_casq_comb_ug{ug.id}"] = CondicionadorExponencial(
            self.leitura_dict[f"tmp_mancal_casq_comb_ug{ug.id}"]
        )
        self.condicionadores_essenciais.append(self.condic_dict[f"tmp_mancal_casq_comb_ug{ug.id}"])

        # Mancal Escora Combinado
        self.leitura_dict[f"tmp_mancal_escora_comb_ug{ug.id}"] = LeituraModbus(
            UG[f"UG{ug.id}_RA_Temperatura_07"],
            self.clp_ug,
            op=4
        )
        self.condic_dict[f"tmp_mancal_escora_comb_ug{ug.id}"] = CondicionadorExponencial(
            self.leitura_dict[f"tmp_mancal_escora_comb_ug{ug.id}"]
        )
        self.condicionadores_essenciais.append(self.condic_dict[f"tmp_mancal_escora_comb_ug{ug.id}"])

        # CX Espiral
        self.leitura_dict[f"cx_espiral_ug{ug.id}"] = LeituraModbus(
            UG[f"UG{ug.id}_EA_PressK1CaixaExpiral_MaisCasas"],
            self.clp_ug[f"ug{ug.id}"],
            escala=0.1,
            op=4
        )
        self.condic_dict[f"cx_espiral_ug{ug.id}"] = CondicionadorExponencialReverso(
            self.leitura_dict[f"cx_espiral_ug{ug.id}"]
        )
        self.condicionadores_essenciais.append(self.condic_dict[f"cx_espiral_ug{ug.id}"])
        self.condicionadores_atenuadores.append(self.condic_dict[f"cx_espiral_ug{ug.id}"])

        leitura_CD_EmergenciaViaSuper = LeituraModbusCoil(UG[f"UG{ug.id}_CD_EmergenciaViaSuper"], self.clp_ug[f"ug{ug.id}"])
        self.condicionadores_essenciais.append(CondicionadorBase(leitura_CD_EmergenciaViaSuper, CONDIC_NORMALIZAR, [UG_SINCRONIZADA, UG_SINCRONIZANDO], ug.id))

        leitura_RD_TripEletrico = LeituraModbusCoil(UG[f"UG{ug.id}_RD_TripEletrico"], self.clp_ug[f"ug{ug.id}"])
        self.condicionadores_essenciais.append(CondicionadorBase(leitura_RD_TripEletrico, CONDIC_NORMALIZAR, [UG_SINCRONIZADA, UG_SINCRONIZANDO], ug.id))

        leitura_ED_ReleBloqA86HAtuado = LeituraModbusCoil(UG[f"UG{ug.id}_ED_ReleBloqA86HAtuado"], self.clp_ug[f"ug{ug.id}"])
        self.condicionadores_essenciais.append(CondicionadorBase(leitura_ED_ReleBloqA86HAtuado, CONDIC_NORMALIZAR, [UG_SINCRONIZADA, UG_SINCRONIZANDO], ug.id))

        leitura_ED_FalhaDisjTPsSincrG1 = LeituraModbusCoil(SA["SA_ED_FalhaDisjTPsSincrG1"], self.clp_usn)
        self.condicionadores.append(CondicionadorBase(leitura_ED_FalhaDisjTPsSincrG1))

        leitura_ED_DisjDJ1_BloqPressBaixa = LeituraModbusCoil(SA["SA_ED_DisjDJ1_BloqPressBaixa"], self.clp_usn)
        self.condicionadores.append(CondicionadorBase(leitura_ED_DisjDJ1_BloqPressBaixa))

        leitura_ED_DisjDJ1_AlPressBaixa = LeituraModbusCoil(SA["SA_ED_DisjDJ1_AlPressBaixa"], self.clp_usn)
        self.condicionadores.append(CondicionadorBase(leitura_ED_DisjDJ1_AlPressBaixa))
