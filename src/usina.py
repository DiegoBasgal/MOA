import os
import json
import pytz
import logging
import traceback

import src.subestacao as se
import src.tomada_agua as tda
import src.unidade_geracao as u
import src.mensageiro.voip as vp
import src.dicionarios.dict as d
import src.funcoes.escrita as esc
import src.servico_auxiliar as sa
import src.conectores.banco_dados as bd
import src.conectores.servidores as srv

from time import sleep, time
from datetime import  datetime

from src.dicionarios.reg import *
from src.dicionarios.const import *


logger = logging.getLogger("logger")


class Usina:

    cfg: "dict" = None

    ug1 = u.UnidadeDeGeracao(1, cfg)
    ug2 = u.UnidadeDeGeracao(2, cfg)
    ugs: "list[u.UnidadeDeGeracao]" = [ug1, ug2]

    pid_inicial: "int" = -1
    pot_alvo_anterior: "int" = -1

    estado_moa: "int" = 0

    pot_disp: "int" = 0
    atenuacao: "int" = 0
    ug_operando: "int" = 0
    tentativas_normalizar: "int" = 0
    modo_de_escolha_das_ugs: "int" = 0

    fator_pot: "float" = 0
    controle_p: "float" = 0
    controle_i: "float" = 0
    controle_d: "float" = 0

    modo_autonomo: "bool" = False

    borda_emerg: "bool" = False
    bd_emergencia: "bool" = False
    clp_emergencia: "bool" = False

    tentar_normalizar: "bool" = True
    normalizar_forcado: "bool" = False

    borda_erro_ler_nv: "bool" = False
    aguardando_reservatorio: "bool" = False

    ultima_tentativa_norm: "datetime" = datetime.now(pytz.timezone("Brazil/East")).replace(tzinfo=None)


    @staticmethod
    def get_time() -> "datetime":
        return datetime.now(pytz.timezone("Brazil/East")).replace(tzinfo=None)


    @staticmethod
    def resetar_emergencia() -> "None":
        """
        Função para reset geral da Usina. Envia o comando de reset para todos os
        CLPs.
        """

        logger.debug("")
        logger.info(f"[USN]  Enviando comando:                   \"RESET EMERGÊNCIA GERAL\"")
        logger.debug("")
        logger.debug("[USN] Tomada da Água resetada.") if tda.TomadaAgua.resetar_emergencia() else logger.info("[USN] Reset de emergência da Tomada da Água \"FALHOU\"!.")
        logger.debug("[USN] Serviço Auxiliar e Subestação resetados.") if sa.ServicoAuxiliar.resetar_emergencia() else logger.info("[USN] Reset de emergência do serviço auxiliar e subestação \"FALHOU\"!.")
        logger.debug("")


    @classmethod
    def acionar_emergencia(cls) -> "None":
        logger.warning("[USN] Enviando Comando:                  \"ACIONAR EMERGÊNCIA\".")

        try:
            cls.clp_emergencia = True
            for ug in cls.ugs:
                esc.EscritaModBusBit.escrever_bit(srv.Servidores.clp[f"UG{ug.id}"], REG_UG[f"UG{ug.id}"]["CMD_PARADA_EMERG"], valor=1)

        except Exception:
            logger.error(f"[USN] Houve um erro ao acionar a Emergência.")
            logger.debug(traceback.format_exc())


    @classmethod
    def normalizar_usina(cls) -> "bool":
        """
        Função para normalização de ocorrências da Usina.

        Verifica primeiramente a tensão da linha.
        Caso a tenão esteja dentro dos limites, passa a verificar se a
        normalização foi executada à pouco tempo, se foi, avisa o operador,
        senão, passa a chamar as funções de reset geral.
        """

        logger.debug(f"[USN] Última tentativa de normalização:   {cls.ultima_tentativa_norm.strftime('%d-%m-%Y %H:%M:%S')}")

        if (cls.tentativas_normalizar < 3 and (cls.get_time() - cls.ultima_tentativa_norm).seconds >= cls.tentativas_normalizar * 2) or cls.normalizar_forcado:
            cls.ultima_tentativa_norm = cls.get_time()
            cls.tentativas_normalizar += 1
            logger.info(f"[USN] Normalizando... (Tentativa {cls.tentativas_normalizar}/3)")
            cls.normalizar_forcado = cls.clp_emergencia = cls.bd_emergencia = False
            cls.resetar_emergencia()
            sleep(1)
            se.Subestacao.fechar_dj_linha()
            bd.BancoDados.update_remove_emergencia()
            return True

        else:
            logger.debug("[USN] A normalização foi executada menos de 1 minutos atrás.")
            sleep(1)
            return False


    @classmethod
    def verificar_se(cls) -> "int":
        """
        Função para verificação do Bay e Subestação.

        Apresenta a leitura de tensão VAB, VBC, VCA do Bay e Subestação.
        Caso haja uma falta de tensão na linha da subestação, aciona o temporizador
        para retomada em caso de queda de tensão. Caso a tensão esteja normal, tenta
        realizar o fechamento dos disjuntores do Bay e depois da Subestação. Caso
        haja um erro com o fechamento dos disjuntores, aciona a normalização da usina
        senão, sinaliza que está tudo correto para a máquina de estados do MOA.
        """

        if not se.Subestacao.verificar_tensao():
            logger.debug("")
            logger.debug(f"[SE]  Tensão Subestação:            RS -> \"{se.Subestacao.tensao_rs.valor:2.1f} V\" | ST -> \"{se.Subestacao.tensao_st.valor:2.1f} V\" | TR -> \"{se.Subestacao.tensao_tr.valor:2.1f} V\"")
            logger.debug("")
            return DJS_FALTA_TENSAO

        elif not se.Subestacao.fechar_dj_linha():
            cls.normalizar_forcado = True
            return DJS_FALHA

        else:
            return DJS_OK


    @classmethod
    def verificar_condicionadores(cls) -> "int":
        flag = CONDIC_IGNORAR

        lst_se = se.Subestacao.verificar_condicionadores()
        lst_sa = sa.ServicoAuxiliar.verificar_condicionadores()
        lst_tda = tda.TomadaAgua.verificar_condicionadores()

        condics = [condic for condics in [lst_sa, lst_se, lst_tda] for condic in condics]

        for condic in condics:
            if condic.gravidade == CONDIC_INDISPONIBILIZAR:
                flag = CONDIC_INDISPONIBILIZAR

            elif condic.gravidade == CONDIC_NORMALIZAR:
                flag = CONDIC_NORMALIZAR if flag != CONDIC_INDISPONIBILIZAR else flag

            bd.BancoDados.update_alarmes([cls.get_time(), condic.gravidade, condic.descricao])

        return flag


    @classmethod
    def verificar_leituras_periodicas(cls) -> "None":
        try:
            sleep(5)
            logger.debug("[USN] Iniciando o timer de leitura periódica...")

            while True:
                sa.ServicoAuxiliar.verificar_leituras()
                tda.TomadaAgua.verificar_leituras()
                for ug in cls.ugs: ug.verificar_leituras()

                if True in (d.voip[r][0] for r in d.voip):
                    vp.Voip.acionar_chamada()
                    pass

                sleep(max(0, (time() + 1800) - time()))

        except Exception:
            logger.debug(f"[USN] Houve um erro ao executar o timer de leituras periódicas.")
            logger.debug(traceback.format_exc())


    @classmethod
    def ajustar_inicializacao(cls) -> "None":
        for ug in cls.ugs:
            if ug.etapa == UG_SINCRONIZADA:
                cls.ug_operando += 1

        cls.__split1 = True if cls.ug_operando == 1 else False
        cls.__split2 = True if cls.ug_operando == 2 else False

        cls.controle_ie = sum(ug.potencia for ug in cls.ugs) / cls.cfg["pot_maxima_alvo"]


    @classmethod
    def controlar_potencia(cls) -> "None":
        logger.debug(f"[USN] NÍVEL -> Alvo:                      {cls.cfg['nv_alvo']:0.3f}")
        logger.debug(f"[USN]          Leitura:                   {tda.TomadaAgua.nv_montante_recente:0.3f}")

        cls.controle_p = cls.cfg["kp"] * tda.TomadaAgua.erro_nv

        if cls.pid_inicial == -1:
            cls.controle_i = max(min(cls.controle_ie - cls.controle_p, 0.9), 0)
            cls.pid_inicial = 0
        else:
            cls.controle_i = max(min((cls.cfg["ki"] * tda.TomadaAgua.erro_nv) + cls.controle_i, 0.9), 0)
            cls.controle_d = cls.cfg["kd"] * (tda.TomadaAgua.erro_nv - tda.TomadaAgua.erro_nv_anterior)

        saida_pid = (cls.controle_p + cls.controle_i + min(max(-0.3, cls.controle_d), 0.3))

        logger.debug("")
        logger.debug(f"[USN] PID   -> P + I + D:                 {saida_pid:0.3f}")
        logger.debug(f"[USN] P:                                  {cls.controle_p:0.3f}")
        logger.debug(f"[USN] I:                                  {cls.controle_i:0.3f}")
        logger.debug(f"[USN] D:                                  {cls.controle_d:0.3f}")

        cls.controle_ie = max(min(saida_pid + cls.controle_ie * cls.cfg["kie"], 1), 0)
        logger.debug(f"[USN] IE:                                 {cls.controle_ie:0.3f}")
        logger.debug(f"[USN] ERRO:                               {tda.TomadaAgua.erro_nv}")
        logger.debug("")

        if tda.TomadaAgua.nv_montante_recente >= (cls.cfg["nv_maximo"] + 0.03):
            cls.controle_ie = 1
            cls.controle_i = 1 - cls.controle_p

        if tda.TomadaAgua.nv_montante_recente <= (cls.cfg["nv_minimo"] + 0.03):
            cls.controle_ie = min(cls.controle_ie, 0.3)
            cls.controle_i = 0

        pot_alvo = max(min(round(cls.cfg["pot_maxima_usina"] * cls.controle_ie, 5), cls.cfg["pot_maxima_usina"],), cls.cfg["pot_minima"],)

        pot_alvo = cls.ajustar_potencia(pot_alvo)


    @classmethod
    def controlar_unidades_disponiveis(cls) -> "list":
        ls = [ug for ug in cls.ugs if ug.disponivel and not ug.etapa == UG_PARANDO]

        # if cls.modo_de_escolha_das_ugs in (UG_PRIORIDADE_1, UG_PRIORIDADE_2):
        ls = sorted(ls, key=lambda y: (-1 * y.potencia, -1 * y.setpoint, y.prioridade))

        # else:
        #     ls = sorted(ls, key=lambda y: (y.leitura_horimetro, -1 * y.potencia, -1 * y.setpoint))

        return ls


    @classmethod
    def ajustar_potencia(cls, pot_alvo) -> "None":
        if cls.pot_alvo_anterior == -1:
            cls.pot_alvo_anterior = pot_alvo

        if pot_alvo < 0.1:
            for ug in cls.ugs: ug.setpoint = 0
            return 0

        l_pot_rele = srv.Servidores.rele["SE"].read_holding_registers(REG_RELE["SE"]["P"], 2)[1]
        l_pot_medidor = 65535 - l_pot_rele

        logger.debug(f"[USN] Potência no medidor:                {l_pot_medidor}")

        pot_aux = cls.cfg["pot_maxima_alvo"] - (cls.cfg["pot_maxima_usina"] - cls.cfg["pot_maxima_alvo"])

        pot_medidor = max(pot_aux, min(l_pot_medidor, cls.cfg["pot_maxima_usina"]))

        if pot_medidor > cls.cfg["pot_maxima_alvo"]:
            pot_alvo = cls.pot_alvo_anterior * (1 - ((pot_medidor - cls.cfg["pot_maxima_alvo"]) / cls.cfg["pot_maxima_alvo"]))

        cls.pot_alvo_anterior = pot_alvo

        logger.debug(f"[USN] Potência alvo após ajuste:          {pot_alvo:0.3f}")

        cls.distribuir_potencia(pot_alvo)


    @classmethod
    def distribuir_potencia(cls, pot_alvo) -> "None":
        ugs: "list[u.UnidadeDeGeracao]" = cls.controlar_unidades_disponiveis()

        logger.debug("")
        logger.debug(f"[USN] Ordem das UGs (Prioridade):         {[ug.id for ug in ugs]}")
        logger.debug("")

        ajuste_manual = 0

        for ug in cls.ugs:
            if ug.manual:
                ajuste_manual += ug.potencia
            else:
                cls.pot_disp += ug.setpoint_maximo

        if ugs is None or not len(ugs):
            return

        pot_ajustada = pot_alvo - ajuste_manual
        pot_atenuada = cls.atenuar_carga(pot_ajustada)

        logger.debug("")
        logger.debug(f"[USN] Distribuindo:                       {pot_atenuada:0.3f}")

        sp = (pot_atenuada) / cls.cfg["pot_maxima_usina"]

        cls.__split1 = True if sp > (0) else cls.__split1
        cls.__split2 = (True if sp > (0.5 + cls.cfg["margem_pot_critica"]) else cls.__split2)

        cls.__split2 = False if sp < (0.5) else cls.__split2
        cls.__split1 = False if sp < (cls.cfg["pot_minima"] / cls.cfg["pot_maxima_usina"]) else cls.__split1

        logger.debug(f"[USN] SP Geral:                           {sp * 100:0.1f} %")

        if len(ugs) == 2:
            if cls.__split2:
                logger.debug("[USN] Split:                              2")

                for ug in ugs:
                    ug.manter_unidade = False
                    ug.setpoint = sp * ug.setpoint_maximo

            elif cls.__split1:
                logger.debug("[USN] Split:                              2 -> \"1B\"")

                ugs[0].manter_unidade = True if tda.TomadaAgua.nv_montante.valor > cls.cfg['nv_minimo'] else False
                ugs[0].setpoint = 2 * sp * ugs[0].setpoint_maximo
                ugs[1].setpoint = 0

            else:
                for ug in ugs:
                    ug.manter_unidade = False
                    ug.setpoint = 0

            logger.debug("")
            for ug in ugs: logger.debug(f"[UG{ug.id}] SP    <-                            {int(ug.setpoint)}")

        elif len(ugs) == 1:
            logger.debug("[USN] Split:                              1")

            ugs[0].manter_unidade = True if tda.TomadaAgua.nv_montante.valor > cls.cfg['nv_minimo'] else False
            ugs[0].setpoint = 2 * sp * ugs[0].setpoint_maximo

            logger.debug("")
            logger.debug(f"[UG{ugs[0].id}] SP    <-                            {int(ugs[0].setpoint)}")


    @classmethod
    def atenuar_carga(cls, setpoint: "int") -> "None":
        """
        Função para atenuação de carga através de leituras de condiconadores atenuadores.

        Calcula o ganho e verifica os limites máximo e mínimo para deteminar se
        deve atenuar ou não.
        """

        flags = 0
        atenuacao = 0
        logger.debug(f"[USN] Verificando Atenuadores Gerais...")

        for condic in tda.TomadaAgua.condicionadores_atenuadores:
            atenuacao = max(atenuacao, condic.valor)

            if atenuacao > 0:
                flags += 1
                logger.debug(f"[USN]    - \"{condic.descricao}\":")
                logger.debug(f"[USN]                                     Leitura: {condic.leitura:3.2f} | Atenuação: {atenuacao:0.4f}")

                if flags == 1:
                    cls.atenuacao = atenuacao
                elif atenuacao > cls.atenuacao:
                    cls.atenuacao = atenuacao
                atenuacao = 0

        if flags == 0:
            logger.debug(f"[USN] Não há necessidade de Atenuação.")
            return setpoint

        else:
            ganho = 1 - cls.atenuacao
            aux = setpoint
            cls.atenuacao = 0

            setpoint_atenuado = setpoint - 0.5 * (setpoint - (setpoint * ganho))
            logger.debug(f"[USN]                                     SP {aux} * GANHO {ganho:0.4f} = {setpoint_atenuado:0.3f} kW")

        return setpoint_atenuado


    @classmethod
    def ler_valores(cls) -> "None":

        srv.Servidores.ping_clients()
        tda.TomadaAgua.atualizar_valores_montante()

        parametros = bd.BancoDados.get_parametros_usina()
        cls.atualizar_valores_cfg(parametros)
        cls.atualizar_valores_banco(parametros)

        for ug in cls.ugs: ug.atualizar_limites_condicionadores(parametros)


    @classmethod
    def atualizar_valores_banco(cls, parametros) -> "None":
        try:
            if int(parametros["emergencia_acionada"]) == 1 and not cls.bd_emergencia:
                logger.info(f"[USN] Emergência:                      \"{'Acionada'}\"")
                cls.bd_emergencia = True
            elif int(parametros["emergencia_acionada"]) == 0 and cls.bd_emergencia:
                logger.info(f"[USN] Emergência:                      \"{'Desativada'}\"")
                cls.bd_emergencia = False

            if int(parametros["modo_autonomo"]) == 1 and not cls.modo_autonomo:
                cls.modo_autonomo = True
                logger.info(f"[USN] Modo autônomo:                      \"{'Ativado'}\"")
            elif int(parametros["modo_autonomo"]) == 0 and cls.modo_autonomo:
                cls.modo_autonomo = False
                logger.info(f"[USN] Modo autônomo:                      \"{'Desativado'}\"")

            if cls.modo_de_escolha_das_ugs != int(parametros["modo_de_escolha_das_ugs"]):
                cls.modo_de_escolha_das_ugs = int(parametros["modo_de_escolha_das_ugs"])
                logger.info(f"[USN] Modo de prioridade das UGs:         \"{UG_STR_DCT_PRIORIDADE[cls.modo_de_escolha_das_ugs]}\"")

        except Exception:
            logger.error(f"[USN] Houve um erro ao ler e atualizar os parâmetros do Banco de Dados.")
            logger.debug(traceback.format_exc())


    @classmethod
    def atualizar_valores_cfg(cls, parametros) -> "None":
        try:
            cls.cfg["kp"] = float(parametros["kp"])
            cls.cfg["ki"] = float(parametros["ki"])
            cls.cfg["kd"] = float(parametros["kd"])
            cls.cfg["kie"] = float(parametros["kie"])

            cls.cfg["nv_alvo"] = float(parametros["nv_alvo"])
            cls.cfg["nv_minimo"] = float(parametros["nv_minimo"])
            cls.cfg["nv_maximo"] = float(parametros["nv_maximo"])
            cls.cfg["nv_religamento"] = float(parametros["nv_religamento"])

            cls.cfg["pot_maxima_alvo"] = float(parametros["pot_nominal"])
            cls.cfg["pot_maxima_ug"] = float(parametros["pot_nominal_ug"])
            cls.cfg["pot_maxima_usina"] = float(parametros["pot_nominal_ug"]) * 2
            cls.cfg["margem_pot_critica"] = float(parametros["margem_pot_critica"])

            with open(os.path.join(os.path.dirname("/opt/operacao-autonoma/src/dicionarios/"), 'cfg.json'), 'w') as file:
                json.dump(cls.cfg, file)

        except Exception:
            logger.error(f"[USN] Houve um erro ao atualizar o arquivo de configuração \"cfg.json\".")
            logger.debug(traceback.format_exc())


    @classmethod
    def escrever_valores(cls) -> "None":

        try:
            bd.BancoDados.update_valores_usina([
                cls.get_time().strftime("%Y-%m-%d %H:%M:%S"),
                1 if cls.aguardando_reservatorio else 0,
                tda.TomadaAgua.nv_montante.valor,
                cls.ug1.potencia,
                cls.ug1.setpoint,
                cls.ug1.codigo_state,
                cls.ug2.potencia,
                cls.ug2.setpoint,
                cls.ug2.codigo_state,
            ])

        except Exception:
            logger.debug(f"[USN] Houve um erro ao inserir os valores no Banco.")
            logger.debug(traceback.format_exc())

        try:
            bd.BancoDados.update_debug([
                cls.get_time().timestamp(),
                1 if cls.modo_autonomo else 0,
                tda.TomadaAgua.nv_montante.valor,
                tda.TomadaAgua.erro_nv,
                cls.ug1.setpoint,
                cls.ug1.potencia,
                cls.ug1.codigo_state,
                cls.ug2.setpoint,
                cls.ug2.potencia,
                cls.ug2.codigo_state,
                cls.controle_p,
                cls.controle_i,
                cls.controle_d,
                cls.controle_ie,
                cls.cfg["kp"],
                cls.cfg["ki"],
                cls.cfg["kd"],
                cls.cfg["kie"],
            ])

        except Exception:
            logger.debug(f"[USN] Houve um erro ao inserir dados DEBUG no Banco.")
            logger.debug(traceback.format_exc())


    @classmethod
    def heartbeat(cls) -> None:
        try:
            srv.Servidores.clp["MOA"].write_single_coil(REG_MOA["PAINEL_LIDO"], [1])
            srv.Servidores.clp["MOA"].write_single_coil(REG_MOA["MOA_OUT_MODE"], [1 if cls.modo_autonomo else 0])
            srv.Servidores.clp["MOA"].write_single_register(REG_MOA["MOA_OUT_STATUS"], cls.estado_moa)

            for ug in cls.ugs: ug.atualizar_modbus_moa()

            if cls.modo_autonomo:
                srv.Servidores.clp["MOA"].write_single_coil(REG_MOA["MOA_OUT_EMERG"], [1 if cls.clp_emergencia else 0])
                srv.Servidores.clp["MOA"].write_single_register(REG_MOA["MOA_OUT_TARGET_LEVEL"], int((cls.cfg["nv_alvo"] - 819.2) * (1/1000)))
                srv.Servidores.clp["MOA"].write_single_register(REG_MOA["MOA_OUT_SETPOINT"], int(sum(ug.setpoint for ug in cls.ugs)))

                if srv.Servidores.clp["MOA"].read_coils(REG_MOA["MOA_IN_EMERG"])[0] and not cls.borda_emerg:
                    cls.borda_emerg = True
                    for ug in cls.ugs: ug.verificar_condicionadores(ug)

                elif not srv.Servidores.clp["MOA"].read_coils(REG_MOA["MOA_IN_EMERG"])[0] and cls.borda_emerg:
                    cls.borda_emerg = False

                if srv.Servidores.clp["MOA"].read_coils(REG_MOA["MOA_IN_EMERG_UG1"])[0]:
                    cls.ug1.verificar_condicionadores(cls.ug1)

                if srv.Servidores.clp["MOA"].read_coils(REG_MOA["MOA_IN_EMERG_UG2"])[0]:
                    cls.ug2.verificar_condicionadores(cls.ug2)

                if srv.Servidores.clp["MOA"].read_coils(REG_MOA["MOA_IN_HABILITA_AUTO"])[0]:
                    srv.Servidores.clp["MOA"].write_single_coil(REG_MOA["MOA_IN_HABILITA_AUTO"], 1)
                    srv.Servidores.clp["MOA"].write_single_coil(REG_MOA["MOA_IN_DESABILITA_AUTO"], 0)
                    cls.modo_autonomo = True

                if srv.Servidores.clp["MOA"].read_coils(REG_MOA["MOA_IN_DESABILITA_AUTO"])[0]:
                    srv.Servidores.clp["MOA"].write_single_coil(REG_MOA["MOA_IN_HABILITA_AUTO"], 0)
                    srv.Servidores.clp["MOA"].write_single_coil(REG_MOA["MOA_IN_DESABILITA_AUTO"], 1)
                    cls.modo_autonomo = False

                if srv.Servidores.clp["MOA"].read_coils(REG_MOA["MOA_OUT_BLOCK_UG1"])[0]:
                    srv.Servidores.clp["MOA"].write_single_coil(REG_MOA["MOA_OUT_BLOCK_UG1"], 1)

                elif not srv.Servidores.clp["MOA"].read_coils(REG_MOA["MOA_OUT_BLOCK_UG1"])[0]:
                    srv.Servidores.clp["MOA"].write_single_coil(REG_MOA["MOA_OUT_BLOCK_UG1"], 0)

                if srv.Servidores.clp["MOA"].read_coils(REG_MOA["MOA_OUT_BLOCK_UG2"])[0]:
                    srv.Servidores.clp["MOA"].write_single_coil(REG_MOA["MOA_OUT_BLOCK_UG2"], 1)

                elif not srv.Servidores.clp["MOA"].read_coils(REG_MOA["MOA_OUT_BLOCK_UG2"])[0]:
                    srv.Servidores.clp["MOA"].write_single_coil(REG_MOA["MOA_OUT_BLOCK_UG2"], 0)

            elif not cls.modo_autonomo:
                if srv.Servidores.clp["MOA"].read_coils(REG_MOA["MOA_IN_HABILITA_AUTO"])[0]:
                    srv.Servidores.clp["MOA"].write_single_coil(REG_MOA["MOA_IN_HABILITA_AUTO"], 1)
                    srv.Servidores.clp["MOA"].write_single_coil(REG_MOA["MOA_IN_DESABILITA_AUTO"], 0)
                    cls.modo_autonomo = True

                srv.Servidores.clp["MOA"].write_single_coil(REG_MOA["MOA_OUT_EMERG"], 0)
                srv.Servidores.clp["MOA"].write_single_coil(REG_MOA["MOA_OUT_BLOCK_UG1"], 0)
                srv.Servidores.clp["MOA"].write_single_coil(REG_MOA["MOA_OUT_BLOCK_UG2"], 0)
                srv.Servidores.clp["MOA"].write_single_register(REG_MOA["MOA_OUT_SETPOINT"], int(0))
                srv.Servidores.clp["MOA"].write_single_register(REG_MOA["MOA_OUT_TARGET_LEVEL"], int(0))

        except Exception:
            logger.error(f"[USN] Houve um erro ao tentar escrever valores modbus no CLP MOA.")
            logger.debug(traceback.format_exc())