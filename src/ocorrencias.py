import logging
import traceback
import src.dicionarios.dict as d

from time import sleep, time

from leituras import *
from condicionadores import *
from dicionarios.reg import *
from dicionarios.const import *

from usina import Usina
from mensageiro.voip import Voip
from unidade_geracao import UnidadeDeGeracao

logger = logging.getLogger("__main__")

class Ocorrencias(Usina):
    def __init__(self, clp: ModbusClient = None) -> None:
        super().__init__(clp)

    # Property/Setter Protegidos
    @property
    def ugs(self) -> "list[UnidadeDeGeracao]":
        return self._ugs

    @ugs.setter
    def ugs(self, var: "list[UnidadeDeGeracao]") -> None:
        self._ugs = var

class OcorrenciasUsn(Ocorrencias):
    def __init__(self, ugs):
        super().__init__(ugs)

        self._condicionadores: "list[CondicionadorBase]"
        self._condicionadores_essenciais: "list[CondicionadorBase]"

        self.flag: int = CONDIC_IGNORAR

        self.carregar_leituras()

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
        if True in (condic.ativo for condic in self.condicionadores_essenciais):
            condicionadores_ativos = [condic for condics in [self.condicionadores_essenciais, self.condicionadores] for condic in condics if condic.ativo]

            self.flag = [CONDIC_NORMALIZAR for condic in condicionadores_ativos if condic.gravidade == CONDIC_NORMALIZAR]
            self.flag = [CONDIC_INDISPONIBILIZAR for condic in condicionadores_ativos if condic.gravidade == CONDIC_INDISPONIBILIZAR]

            logger.warning(f"[OCO-USN] Foram detectados condicionadores ativos na Usina:")
            [logger.warning(f"[OCO-USN] Descrição: \"{condic.descr}\", Gravidade: {CONDIC_STR_DCT[condic.gravidade] if condic.gravidade in CONDIC_STR_DCT else 'Desconhecida'}") for condic in condicionadores_ativos]

        return self.flag

    def leitura_temporizada(self) -> None:
        if self.leitura_ED_GMG_Trip.valor != 0:
            logger.warning("[OCO-USN] O sensor de TRIP do Grupo Motor Gerador foi acionado, favor verificar.")

        if self.leitura_QCADE_BombasDng_Auto.valor == 0 and not d.voip["BombasDngRemoto"]:
            logger.warning("[OCO-USN] O poço de drenagem da Usina saiu do modo remoto, favor verificar.")
            d.voip["BombasDngRemoto"] = True
        elif self.leitura_QCADE_BombasDng_Auto.valor == 1 and d.voip["BombasDngRemoto"]:
            d.voip["BombasDngRemoto"] = False

    def carregar_leituras(self) -> None:
        # Leituras para acionamento temporizado por chamada Voip
        self.leitura_ED_GMG_Trip = LeituraModbusCoil(SA["SA_ED_GMG_Trip"], self.clp["SA"])
        self.leitura_QCADE_BombasDng_Auto = LeituraModbusCoil(SA["SA_ED_QCADE_BombasDng_Auto"], self.clp["SA"])

        # Leituras de Condicionadores
        leitura_ED_QCAP_TensaoPresenteTSA = LeituraModbusCoil(SA["SA_ED_QCAP_TensaoPresenteTSA"], self.clp["SA"])
        self.condicionadores_essenciais.append(CondicionadorBase(leitura_ED_QCAP_TensaoPresenteTSA, CONDIC_NORMALIZAR))

        leitura_ED_SEL787_Trip = LeituraModbusCoil(SA["SA_ED_SEL787_Trip"], self.clp["SA"])
        self.condicionadores_essenciais.append(CondicionadorBase(leitura_ED_SEL787_Trip))

        leitura_ED_QcataDisj52ETrip = LeituraModbusCoil(TDA["TDA_ED_QcataDisj52ETrip"], self.clp["TDA"])
        self.condicionadores.append(CondicionadorBase(leitura_ED_QcataDisj52ETrip))

        leitura_ED_MRU3_Falha = LeituraModbusCoil(SA["SA_ED_MRU3_Falha"], self.clp["SA"])
        self.condicionadores.append(CondicionadorBase(leitura_ED_MRU3_Falha))

        leitura_ED_SEL787_FalhaInterna = LeituraModbusCoil(SA["SA_ED_SEL787_FalhaInterna"], self.clp["SA"])
        self.condicionadores.append(CondicionadorBase(leitura_ED_SEL787_FalhaInterna))


class OcorrenciasUg(Ocorrencias):
    def __init__(self, ugs):
        super().__init__(ugs)

        self._temperatura_base: int = 100
        self._temperatura_limite: int = 200

        self._condicionadores: "list[CondicionadorBase]"
        self._condicionadores_essenciais: "list[CondicionadorBase]"

        self._leitura_dict: "dict[str, LeituraBase]"
        self._condic_dict: "dict[str, CondicionadorBase]"

        self.flag: int = CONDIC_IGNORAR

        for ug in self.ugs: 
            self.carregar_leituras(ug)

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
    def condic_dict(self) -> "dict[str, CondicionadorExponencial]":
        return self._condic_dict

    @condic_dict.setter
    def condic_dict(self, var: "dict[str, CondicionadorExponencial]") -> None:
        self._condic_dict = var
    
    @property
    def leitura_dict(self) -> "dict[str, LeituraBase]":
        return self._leitura_dict

    @leitura_dict.setter
    def leitura_dict(self, var: "dict[str, LeituraBase]") -> None:
        self._leitura_dict = var

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

    def verificar_condicionadores(self, ug: UnidadeDeGeracao) -> int:
        if True in (condic.ativo for condic in self.condicionadores_essenciais):
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

        except Exception:
            logger.error(f"[OCO-UG{ug.id}] Houve um erro ao atualizar os limites de temperaturas dos condicionadores.")
            logger.debug(f"[OCO-UG{ug.id}] Traceback: {traceback.format_exc()}")

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

    def leitura_temporizada(self, ug: UnidadeDeGeracao) -> None:
        if self.leitura_ED_FreioPastilhaGasta.valor != 0:
            logger.warning(f"[OCO-UG{ug.id}] O sensor de Freio da UG retornou que a Pastilha está gasta, favor considerar troca.")

        if self.leitura_ED_FreioCmdRemoto.valor == 0 and not d.voip[f"UG{ug.id}_FreioCmdRemoto"]:
            logger.warning(f"[OCO-UG{ug.id}] O freio da UG saiu do modo remoto, favor analisar a situação.")
            d.voip[f"UG{ug.id}_FreioCmdRemoto"] = True
        elif self.leitura_ED_FreioCmdRemoto.valor == 1 and d.voip[f"UG{ug.id}_FreioCmdRemoto"]:
            d.voip[f"UG{ug.id}_FreioCmdRemoto"] = False

    def carregar_leituras(self, ug: UnidadeDeGeracao) -> None:
        # Leituras para acionamento temporizado por chamada Voip
        self.leitura_ED_FreioCmdRemoto = LeituraModbusCoil(UG[f"UG{ug.id}_ED_FreioCmdRemoto"], self.clp[f"UG{ug.id}"])
        self.leitura_ED_FreioPastilhaGasta = LeituraModbusCoil(UG[f"UG{ug.id}_ED_FreioPastilhaGasta"], self.clp[f"UG{ug.id}"])


        # Leituras de condicionadores com limites de operção checados a cada ciclo
        # Fase R
        self.leitura_dict[f"tmp_fase_r_ug{ug.id}"] = LeituraModbus(
            UG[f"UG{ug.id}_RA_Temperatura_01"],
            self.clp[f"UG{ug.id}"],
            op=4
        )
        self.condic_dict[f"tmp_fase_r_ug{ug.id}"] = CondicionadorExponencial(
            self.leitura_dict[f"tmp_fase_r_ug{ug.id}"]
        )
        self.condicionadores_essenciais.append(self.condic_dict[f"tmp_fase_r_ug{ug.id}"])

        # Fase S
        self.leitura_dict[f"tmp_fase_s_ug{ug.id}"] = LeituraModbus(
            UG[f"UG{ug.id}_RA_Temperatura_02"],
            self.clp[f"UG{ug.id}"],
            op=4
        )
        self.condic_dict[f"tmp_fase_s_ug{ug.id}"] = CondicionadorExponencial(
            self.leitura_dict[f"tmp_fase_s_ug{ug.id}"]
        )
        self.condicionadores_essenciais.append(self.condic_dict[f"tmp_fase_s_ug{ug.id}"])

        # Fase T
        self.leitura_dict[f"tmp_fase_t_ug{ug.id}"] = LeituraModbus(
            UG[f"UG{ug.id}_RA_Temperatura_03"],
            self.clp[f"UG{ug.id}"],
            op=4
        )
        self.condic_dict[f"tmp_fase_t_ug{ug.id}"] = CondicionadorExponencial(
            self.leitura_dict[f"tmp_fase_t_ug{ug.id}"]
        )
        self.condicionadores_essenciais.append(self.condic_dict[f"tmp_fase_t_ug{ug.id}"])

        # Nucleo Gerador 1
        self.leitura_dict[f"tmp_nucleo_gerador_1_ug{ug.id}"] = LeituraModbus(
            UG[f"UG{ug.id}_RA_Temperatura_04"],
            self.clp[f"UG{ug.id}"],
            op=4
        )
        self.condic_dict[f"tmp_nucleo_gerador_1_ug{ug.id}"] = CondicionadorExponencial(
            self.leitura_dict[f"tmp_nucleo_gerador_1_ug{ug.id}"]
        )
        self.condicionadores_essenciais.append(self.condic_dict[f"tmp_nucleo_gerador_1_ug{ug.id}"])

        # Nucleo Gerador 2
        self.leitura_dict[f"tmp_nucleo_gerador_2_ug{ug.id}"] = LeituraModbus(
            UG[f"UG{ug.id}_RA_Temperatura_04"],
            self.clp[f"UG{ug.id}"],
            op=4
        )
        self.condic_dict[f"tmp_nucleo_gerador_2_ug{ug.id}"] = CondicionadorExponencial(
            self.leitura_dict[f"tmp_nucleo_gerador_2_ug{ug.id}"]
        )
        self.condicionadores_essenciais.append(self.condic_dict[f"tmp_nucleo_gerador_2_ug{ug.id}"])

        # Nucleo Gerador 3
        self.leitura_dict[f"tmp_nucleo_gerador_3_ug{ug.id}"] = LeituraModbus(
            UG[f"UG{ug.id}_RA_Temperatura_04"],
            self.clp[f"UG{ug.id}"],
            op=4
        )
        self.condic_dict[f"tmp_nucleo_gerador_3_ug{ug.id}"] = CondicionadorExponencial(
            self.leitura_dict[f"tmp_nucleo_gerador_3_ug{ug.id}"]
        )
        self.condicionadores_essenciais.append(self.condic_dict[f"tmp_nucleo_gerador_3_ug{ug.id}"])

        # Mancal Casquilho Radial
        self.leitura_dict[f"tmp_mancal_casq_rad_ug{ug.id}"] = LeituraModbus(
            UG[f"UG{ug.id}_RA_Temperatura_08"],
            self.clp[f"UG{ug.id}"],
            op=4
        )
        self.condic_dict[f"tmp_mancal_casq_rad_ug{ug.id}"] = CondicionadorExponencial(
            self.leitura_dict[f"tmp_mancal_casq_rad_ug{ug.id}"]
        )
        self.condicionadores_essenciais.append(self.condic_dict[f"tmp_mancal_casq_rad_ug{ug.id}"])

        # Mancal Casquilho Combinado
        self.leitura_dict[f"tmp_mancal_casq_comb_ug{ug.id}"] = LeituraModbus(
            UG[f"UG{ug.id}_RA_Temperatura_10"],
            self.clp[f"UG{ug.id}"],
            op=4
        )
        self.condic_dict[f"tmp_mancal_casq_comb_ug{ug.id}"] = CondicionadorExponencial(
            self.leitura_dict[f"tmp_mancal_casq_comb_ug{ug.id}"]
        )
        self.condicionadores_essenciais.append(self.condic_dict[f"tmp_mancal_casq_comb_ug{ug.id}"])

        # Mancal Escora Combinado
        self.leitura_dict[f"tmp_mancal_escora_comb_ug{ug.id}"] = LeituraModbus(
            UG[f"UG{ug.id}_RA_Temperatura_07"],
            self.clp[f"UG{ug.id}"],
            op=4
        )
        self.condic_dict[f"tmp_mancal_escora_comb_ug{ug.id}"] = CondicionadorExponencial(
            self.leitura_dict[f"tmp_mancal_escora_comb_ug{ug.id}"]
        )
        self.condicionadores_essenciais.append(self.condic_dict[f"tmp_mancal_escora_comb_ug{ug.id}"])


        # Leituras de condicionadores essenciais que serão lidos a cada ciclo das UGs
        leitura_CD_EmergenciaViaSuper = LeituraModbusCoil(UG[f"UG{ug.id}_CD_EmergenciaViaSuper"], self.clp[f"UG{ug.id}"], descr=f"UG{ug.id}_CD_EmergenciaViaSuper")
        self.condicionadores_essenciais.append(CondicionadorBase(leitura_CD_EmergenciaViaSuper, CONDIC_NORMALIZAR, [UG_SINCRONIZADA, UG_SINCRONIZANDO], ug.id))

        leitura_RD_TripEletrico = LeituraModbusCoil(UG[f"UG{ug.id}_RD_TripEletrico"], self.clp[f"UG{ug.id}"], descr=f"UG{ug.id}_RD_TripEletrico")
        self.condicionadores_essenciais.append(CondicionadorBase(leitura_RD_TripEletrico, CONDIC_NORMALIZAR, [UG_SINCRONIZADA, UG_SINCRONIZANDO], ug.id))

        leitura_ED_ReleBloqA86HAtuado = LeituraModbusCoil(UG[f"UG{ug.id}_ED_ReleBloqA86HAtuado"], self.clp[f"UG{ug.id}"], descr=f"UG{ug.id}_ED_ReleBloqA86HAtuado")
        self.condicionadores_essenciais.append(CondicionadorBase(leitura_ED_ReleBloqA86HAtuado, CONDIC_NORMALIZAR, [UG_SINCRONIZADA, UG_SINCRONIZANDO], ug.id))

        leitura_ED_FalhaDisjTPsSincrG1 = LeituraModbusCoil(SA["SA_ED_FalhaDisjTPsSincrG1"], self.clp["SA"], descr="SA_ED_FalhaDisjTPsSincrG1")
        self.condicionadores.append(CondicionadorBase(leitura_ED_FalhaDisjTPsSincrG1))

        # Leituras de condicionadores comuns que serão lidos caso haja algum disparo proveniente de um condicionador essencial
        leitura_ED_DisjDJ1_BloqPressBaixa = LeituraModbusCoil(SA["SA_ED_DisjDJ1_BloqPressBaixa"], self.clp["SA"], descr="SA_ED_DisjDJ1_BloqPressBaixa")
        self.condicionadores.append(CondicionadorBase(leitura_ED_DisjDJ1_BloqPressBaixa))

        leitura_ED_DisjDJ1_AlPressBaixa = LeituraModbusCoil(SA["SA_ED_DisjDJ1_AlPressBaixa"], self.clp["SA"], descr="SA_ED_DisjDJ1_AlPressBaixa")
        self.condicionadores.append(CondicionadorBase(leitura_ED_DisjDJ1_AlPressBaixa))
