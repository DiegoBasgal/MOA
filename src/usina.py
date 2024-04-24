import os
import json
import pytz
import logging
import traceback

import src.subestacao as se
import src.tomada_agua as tda
import src.unidade_geracao as u
import src.servico_auxiliar as sa

import src.mensageiro.voip as vp

import src.dicionarios.dict as d

import src.funcoes.escrita as esc
import src.funcoes.agendamentos as agn

import src.conectores.banco_dados as bd
import src.conectores.servidores as srv


from time import sleep, time
from datetime import  datetime

from src.dicionarios.const import *
from src.dicionarios.reg_elipse import *


logger = logging.getLogger("logger")


class Usina:
    def __init__(self, cfg: "dict"=None):

        # VERIFICAÇÃO DE ARGUMENTOS
        if None in (cfg):
            raise ValueError("[USN] Não foi possível carregar os arquivos de configuração (\"cfg.json\").")
        else:
            self.cfg = cfg
            tda.TomadaAgua.cfg = self.cfg
            agn.Agendamentos.cfg = self.cfg

        # INCIALIZAÇÃO DE OBJETOS DA USINA
        agn.Agendamentos.usn = self

        self.ug1 = u.UnidadeDeGeracao(1, self.cfg)
        self.ug2 = u.UnidadeDeGeracao(2, self.cfg)
        self.ugs: "list[u.UnidadeDeGeracao]" = [self.ug1, self.ug2]

        # ATRIBUIÇÃO DE VARIÁVEIS PRIVADAS
        self.__pid_inicial: "int" = -1

        # ATRIBUIÇÃO DE VARIÁVEIS PROTEGIDAS
        self._pot_alvo_anterior: "int" = -1
        self._tentativas_normalizar: "int" = 0

        self._modo_autonomo: "bool" = False

        # ATRIBUIÇÃO DE VARIÁVEIS PÚBLICAS
        self.estado_moa: "int" = 0

        self.pot_disp: "int" = 0
        self.atenuacao: "int" = 0
        self.ug_operando: "int" = 0
        self.modo_de_escolha_das_ugs: "int" = 0

        self.fator_pot: "float" = 0
        self.controle_p: "float" = 0
        self.controle_i: "float" = 0
        self.controle_d: "float" = 0

        self.borda_emerg: "bool" = False
        self.bd_emergencia: "bool" = False
        self.clp_emergencia: "bool" = False
        self.tentar_normalizar: "bool" = True
        self.borda_erro_ler_nv: "bool" = False
        self.normalizar_forcado: "bool" = False
        self.aguardando_reservatorio: "bool" = False

        self.ultima_tentativa_norm: "datetime" = self.get_time()

        # EXECUÇÃO FINAL DA INICIALIZAÇÃO
        logger.debug("")

        se.Subestacao.carregar_leituras()
        tda.TomadaAgua.carregar_leituras()
        sa.ServicoAuxiliar.carregar_leituras()

        self.ler_valores()
        self.ajustar_inicializacao()
        self.escrever_valores()

        self._tentativas_normalizar = 0


    ### PROPRIEDADES DA OPERAÇÃO
    @property
    def modo_autonomo(self) -> "bool":
        return self._modo_autonomo

    @modo_autonomo.setter
    def modo_autonomo(self, var: "bool") -> "None":
        self._modo_autonomo = var
        bd.BancoDados.update_modo_moa(self._modo_autonomo)

    @property
    def tentativas_normalizar(self) -> "int":
        return self._tentativas_normalizar

    @tentativas_normalizar.setter
    def tentativas_normalizar(self, var: "int") -> None:
        self._tentativas_normalizar = var

    @property
    def pot_alvo_anterior(self) -> "float":
        return self._pot_alvo_anterior

    @pot_alvo_anterior.setter
    def pot_alvo_anterior(self, var: "float") -> "None":
        self._pot_alvo_anterior = var

    @staticmethod
    def get_time() -> "datetime":
        return datetime.now(pytz.timezone("Brazil/East")).replace(tzinfo=None)


    ### MÉTODOS DE CONTROLE DE RESET E NORMALIZAÇÃO
    def resetar_emergencia(self) -> "None":
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


    def acionar_emergencia(self) -> "None":
        logger.warning("[USN] Enviando Comando:                  \"ACIONAR EMERGÊNCIA\".")

        try:
            self.clp_emergencia = True
            for ug in self.ugs:
                esc.EscritaModBusBit.escrever_bit(srv.Servidores.clp[f"UG{ug.id}"], REG_UG[f"UG{ug.id}"]["CMD_COMANDO_PARADA_DE_EMERGENCIA"], valor=1)

        except Exception:
            logger.error(f"[USN] Houve um erro ao acionar a Emergência.")
            logger.debug(traceback.format_exc())


    def normalizar_usina(self) -> "bool":
        """
        Função para normalização de ocorrências da Usina.

        Verifica primeiramente a tensão da linha.
        Caso a tenão esteja dentro dos limites, passa a verificar se a
        normalização foi executada à pouco tempo, se foi, avisa o operador,
        senão, passa a chamar as funções de reset geral.
        """

        logger.debug(f"[USN] Última tentativa de normalização:   {self.ultima_tentativa_norm.strftime('%d-%m-%Y %H:%M:%S')}")

        if (self.tentativas_normalizar < 3 and (self.get_time() - self.ultima_tentativa_norm).seconds >= self.tentativas_normalizar * 2) or self.normalizar_forcado:
            self.ultima_tentativa_norm = self.get_time()
            self.tentativas_normalizar += 1
            logger.info(f"[USN] Normalizando... (Tentativa {self.tentativas_normalizar}/3)")
            self.normalizar_forcado = self.clp_emergencia = self.bd_emergencia = False
            self.resetar_emergencia()
            sleep(1)
            se.Subestacao.fechar_dj_linha()
            bd.BancoDados.update_remove_emergencia()
            return True

        else:
            logger.debug("[USN] A normalização foi executada menos de 1 minutos atrás.")
            sleep(1)
            return False


    def verificar_condicionadores(self) -> "int":
        flag = CONDIC_IGNORAR

        lst_se = se.Subestacao.verificar_condicionadores()
        lst_tda = tda.TomadaAgua.verificar_condicionadores()
        lst_sa = sa.ServicoAuxiliar.verificar_condicionadores()

        condics = [condic for condics in [lst_sa, lst_se, lst_tda] for condic in condics]

        for condic in condics:
            if condic.gravidade == CONDIC_INDISPONIBILIZAR:
                return CONDIC_INDISPONIBILIZAR

            elif condic.gravidade == CONDIC_NORMALIZAR:
                flag = CONDIC_NORMALIZAR

        return flag


    def verificar_leituras_periodicas(self) -> "None":
        try:
            sleep(5)
            logger.debug("[USN] Iniciando o timer de leitura periódica...")

            while True:
                tda.TomadaAgua.verificar_leituras()
                sa.ServicoAuxiliar.verificar_leituras()
                for ug in self.ugs: ug.verificar_leituras()

                if True in (d.voip[r][0] for r in d.voip):
                    vp.Voip.acionar_chamada()
                    pass

                sleep(max(0, (time() + 1800) - time()))

        except Exception:
            logger.debug(f"[USN] Houve um erro ao executar o timer de leituras periódicas.")
            logger.debug(traceback.format_exc())


    ### MÉTODOS DE CONTROLE DE OPERAÇÃO:
    def ajustar_ie_padrao(self) -> "int":
        return sum(ug.potencia for ug in self.ugs) / self.cfg["pot_maxima_alvo"]


    def ajustar_inicializacao(self) -> "None":
        for ug in self.ugs:
            if ug.etapa == UG_SINCRONIZADA:
                self.ug_operando += 1

        self.__split1 = True if self.ug_operando == 1 else False
        self.__split2 = True if self.ug_operando == 2 else False

        self.controle_ie = self.ajustar_ie_padrao()


    def controlar_reservatorio(self) -> "int":
        """
        Função para controle de níveis do reservatório.

        Realiza a leitura de nível montante e determina qual condição entrar. Se
        o nível estiver acima do máximo, verifica se atingiu o Maximorum. Nesse
        caso é acionada a emergência da Usina, porém se for apenas vertimento,
        distribui a potência máxima para as Unidades.
        Caso a leitura retornar que o nível está abaixo do mínimo, verifica antes
        se atingiu o fundo do reservatório, nesse caso é acionada a emergência.
        Se o valor ainda estiver acima do nível de fundo, será distribuída a
        potência 0 para todas as Unidades e aciona a espera pelo nível.
        Caso a leitura esteja dentro dos limites normais, é chamada a função para
        calcular e distribuir a potência para as Unidades.
        """

        l_nivel = tda.TomadaAgua.nv_montante.valor

        if (l_nivel in (None, 0, 0.0) or l_nivel <= 800) and not self.borda_erro_ler_nv:
            logger.info(f"[TDA] Erro de Leitura de Nível Montante identificada! Acionando espera pelo Reservatório.")
            self.borda_erro_ler_nv = True
            tda.TomadaAgua.aguardando_reservatorio = True

        elif l_nivel >= self.cfg["nv_maximo"] and not tda.TomadaAgua.aguardando_reservatorio:
            logger.debug("[TDA] Nível Montante acima do Máximo.")
            logger.debug(f"[TDA]          Leitura:                   {l_nivel:0.3f}")
            logger.debug("")

            if tda.TomadaAgua.nv_montante_anterior >= NIVEL_MAXIMORUM:
                logger.critical(f"[TDA] Nivel Montante ({tda.TomadaAgua.nv_montante_anterior:3.2f}) atingiu o Maximorum!")
                logger.debug("")
                return NV_EMERGENCIA
            else:
                self.controle_i = 0.9
                self.controle_ie = self.ajustar_ie_padrao()
                self.ajustar_potencia(self.cfg["pot_maxima_usina"])

                for ug in self.ugs:
                    ug.step()

        elif l_nivel <= self.cfg["nv_minimo"] and not tda.TomadaAgua.aguardando_reservatorio:
            logger.debug("[TDA] Nível Montante abaixo do Mínimo.")
            logger.debug(f"[TDA]          Leitura:                   {l_nivel:0.3f}")
            logger.debug("")
            tda.TomadaAgua.aguardando_reservatorio = True
            self.distribuir_potencia(0)

            for ug in self.ugs:
                ug.step()

            if tda.TomadaAgua.nv_montante_anterior <= NIVEL_FUNDO_RESERVATORIO:
                logger.critical(f"[TDA] Nível Montante ({tda.TomadaAgua.nv_montante_anterior:3.2f}) atingiu o fundo do reservatorio!")
                logger.debug("")
                return NV_EMERGENCIA

        elif tda.TomadaAgua.aguardando_reservatorio:
            logger.debug("[TDA] Aguardando Nível Montante...")
            logger.debug(f"[TDA]          Leitura:                   {l_nivel:0.3f}")
            logger.debug(f"[TDA]          Nível de Religamento:      {self.cfg['nv_religamento']:0.3f}")
            logger.debug("")

            if l_nivel >= self.cfg["nv_religamento"]:
                logger.debug("[TDA] Nível Montante dentro do limite de operação.")
                logger.debug(f"[TDA]          Leitura:                   {l_nivel:0.3f}")
                logger.debug("")
                tda.TomadaAgua.aguardando_reservatorio = False

        else:
            self.controlar_potencia()

            for ug in self.ugs:
                ug.step()

        return NV_NORMAL


    def controlar_potencia(self) -> "None":
        logger.debug(f"[USN] NÍVEL -> Alvo:                      {self.cfg['nv_alvo']:0.3f}")
        logger.debug(f"[USN]          Leitura:                   {tda.TomadaAgua.nv_montante.valor:0.3f}")
        logger.debug(f"[USN]          Filtro EMA:                {tda.TomadaAgua.nv_montante_recente:0.3f}")

        self.controle_p = self.cfg["kp"] * tda.TomadaAgua.erro_nv

        if self.__pid_inicial == -1:
            self.controle_i = max(min(self.controle_ie - self.controle_p, 0.9), 0)
            self.__pid_inicial = 0
        else:
            self.controle_i = max(min((self.cfg["ki"] * tda.TomadaAgua.erro_nv) + self.controle_i, 0.9), 0)
            self.controle_d = self.cfg["kd"] * (tda.TomadaAgua.erro_nv - tda.TomadaAgua.erro_nv_anterior)

        saida_pid = (self.controle_p + self.controle_i + min(max(-0.3, self.controle_d), 0.3))

        logger.debug("")
        logger.debug(f"[USN] PID   -> P + I + D:                 {saida_pid:0.3f}")
        logger.debug(f"[USN] P:                                  {self.controle_p:0.3f}")
        logger.debug(f"[USN] I:                                  {self.controle_i:0.3f}")
        logger.debug(f"[USN] D:                                  {self.controle_d:0.3f}")

        self.controle_ie = max(min(saida_pid + self.controle_ie * self.cfg["kie"], 1), 0)
        logger.debug(f"[USN] IE:                                 {self.controle_ie:0.3f}")
        logger.debug(f"[USN] ERRO:                               {tda.TomadaAgua.erro_nv}")
        logger.debug("")

        if tda.TomadaAgua.nv_montante_recente >= (self.cfg["nv_maximo"] + 0.03):
            self.controle_ie = 1
            self.controle_i = 1 - self.controle_p

        if tda.TomadaAgua.nv_montante_recente <= (self.cfg["nv_minimo"] + 0.03):
            self.controle_ie = min(self.controle_ie, 0.3)
            self.controle_i = 0

        pot_alvo = max(min(round(self.cfg["pot_maxima_usina"] * self.controle_ie, 5), self.cfg["pot_maxima_usina"],), self.cfg["pot_minima"],)

        pot_alvo = self.ajustar_potencia(pot_alvo)


    def controlar_unidades_disponiveis(self) -> "list":
        ls = [ug for ug in self.ugs if ug.disponivel and not ug.etapa == UG_PARANDO]
        ls = sorted(ls, key=lambda y: (-1 * y.potencia, -1 * y.setpoint, y.prioridade))
        return ls


    def ajustar_potencia(self, pot_alvo) -> "None":
        if self.pot_alvo_anterior == -1:
            self.pot_alvo_anterior = pot_alvo

        if pot_alvo < 0.1:
            for ug in self.ugs: ug.setpoint = 0
            return 0

        try:
            l_pot_rele = srv.Servidores.rele["SE"].read_holding_registers(REG_RELE["SE"]["P"], 5)[1]
        except Exception:
            logger.debug(f"[USN] Erro de Leitura de Potência no Medidor da Usina.")
            l_pot_rele = 0

        l_pot_medidor = 65535 - l_pot_rele if 60000 <= l_pot_rele <= 65535 else l_pot_rele

        logger.debug(f"[USN] Potência no medidor:                {l_pot_medidor:0.3f}")

        pot_aux = self.cfg["pot_maxima_alvo"] - (self.cfg["pot_maxima_usina"] - self.cfg["pot_maxima_alvo"])
        pot_medidor = max(pot_aux, min(l_pot_medidor, self.cfg["pot_maxima_usina"]))

        if pot_medidor > self.cfg["pot_maxima_alvo"]:
            pot_alvo = self.pot_alvo_anterior * (1 - ((pot_medidor - self.cfg["pot_maxima_alvo"]) / self.cfg["pot_maxima_alvo"]))

        self.pot_alvo_anterior = pot_alvo

        logger.debug(f"[USN] Potência alvo após ajuste:          {pot_alvo:0.3f}")
        self.distribuir_potencia(pot_alvo)


    def distribuir_potencia(self, pot_alvo) -> "None":
        ugs: "list[u.UnidadeDeGeracao]" = self.controlar_unidades_disponiveis()
        logger.debug("")
        logger.debug(f"[USN] Ordem das UGs (Prioridade):         {[ug.id for ug in ugs]}")
        logger.debug("")

        ajuste_manual = 0

        for ug in self.ugs:
            if ug.manual:
                ajuste_manual += ug.potencia
            else:
                self.pot_disp += ug.setpoint_maximo

        if ugs is None or not len(ugs):
            return

        pot_ajustada = pot_alvo - ajuste_manual
        pot_atenuada = self.atenuar_carga(pot_ajustada)
        logger.debug("")
        logger.debug(f"[USN] Distribuindo:                       {pot_atenuada:0.3f}")

        sp = (pot_atenuada) / self.cfg["pot_maxima_usina"]

        self.__split1 = True if sp > (0) else self.__split1
        self.__split2 = (True if sp > (0.5 + self.cfg["margem_pot_critica"]) else self.__split2)

        self.__split2 = False if sp < (0.5) else self.__split2
        self.__split1 = False if sp < (self.cfg["pot_minima"] / self.cfg["pot_maxima_usina"]) else self.__split1

        logger.debug(f"[USN] SP Geral:                           {sp * 100:0.1f} %")

        if len(ugs) == 2:
            if self.__split2:
                logger.debug("[USN] Split:                              2")

                for ug in ugs:
                    ug.manter_unidade = False
                    ug.setpoint = sp * ug.setpoint_maximo

            elif self.__split1:
                logger.debug("[USN] Split:                              2 -> \"1B\"")

                ugs[0].manter_unidade = True if tda.TomadaAgua.nv_montante.valor > self.cfg['nv_minimo'] else False
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

            ugs[0].manter_unidade = True if tda.TomadaAgua.nv_montante.valor > self.cfg['nv_minimo'] else False
            ugs[0].setpoint = 2 * sp * ugs[0].setpoint_maximo

            logger.debug("")
            logger.debug(f"[UG{ugs[0].id}] SP    <-                            {int(ugs[0].setpoint)}")


    def atenuar_carga(self, setpoint) -> "None":
        """
        Função para atenuação de carga através de leituras de condiconadores atenuadores.

        Calcula o ganho e verifica os limites máximo e mínimo para deteminar se
        deve atenuar ou não.
        """

        try:
            flags = 0
            atenuacao = 0
            logger.debug(f"[USN] Verificando Atenuadores Gerais...")

            for condic in tda.TomadaAgua.condicionadores_atenuadores:
                atenuacao = max(atenuacao, condic.valor)

                if atenuacao > 0:
                    flags += 1
                    logger.debug(f"[USN]    - \"{condic.descricao}\":")
                    logger.debug(f"[USN]                                     Leitura: {condic.leitura:3.3f} | Atenuação: {atenuacao:0.4f}")

                    if flags == 1:
                        self.atenuacao = atenuacao
                    elif atenuacao > self.atenuacao:
                        self.atenuacao = atenuacao
                    atenuacao = 0

            if flags == 0:
                logger.debug(f"[USN] Não há necessidade de Atenuação.")
                return setpoint

            else:
                ganho = 1 - self.atenuacao
                self.atenuacao = 0
                aux = setpoint
                setpoint_atenuado = setpoint - 0.15 * (setpoint - (setpoint * ganho)) # 0.15 -> cenário de valor limite 0.47

                logger.debug(f"[USN]                                     SP {aux:0.1f} * GANHO {ganho:0.4f} = {setpoint_atenuado:0.3f} kW")

            return setpoint_atenuado

        except Exception:
            return setpoint


    ### MÉTODOS DE CONTROLE DE DADOS:
    def ler_valores(self) -> "None":

        srv.Servidores.ping_clients()
        tda.TomadaAgua.atualizar_valores_montante()

        parametros = bd.BancoDados.get_parametros_usina()
        self.atualizar_valores_cfg(parametros)
        self.atualizar_valores_banco(parametros)

        for ug in self.ugs: ug.atualizar_limites_condicionadores(parametros)


    def atualizar_valores_banco(self, parametros) -> "None":
        try:
            if int(parametros["emergencia_acionada"]) == 1 and not self.bd_emergencia:
                logger.info(f"[USN] Emergência:                      \"{'Acionada'}\"")
                self.bd_emergencia = True
            elif int(parametros["emergencia_acionada"]) == 0 and self.bd_emergencia:
                logger.info(f"[USN] Emergência:                      \"{'Desativada'}\"")
                self.bd_emergencia = False

            if int(parametros["modo_autonomo"]) == 1 and not self.modo_autonomo:
                self.modo_autonomo = True
                logger.info(f"[USN] Modo autônomo:                      \"{'Ativado'}\"")
            elif int(parametros["modo_autonomo"]) == 0 and self.modo_autonomo:
                self.modo_autonomo = False
                logger.info(f"[USN] Modo autônomo:                      \"{'Desativado'}\"")

            if self.modo_de_escolha_das_ugs != int(parametros["modo_de_escolha_das_ugs"]):
                self.modo_de_escolha_das_ugs = int(parametros["modo_de_escolha_das_ugs"])
                logger.info(f"[USN] Modo de prioridade das UGs:         \"{UG_STR_DCT_PRIORIDADE[self.modo_de_escolha_das_ugs]}\"")

        except Exception:
            logger.error(f"[USN] Houve um erro ao ler e atualizar os parâmetros do Banco de Dados.")
            logger.debug(traceback.format_exc())


    def atualizar_valores_cfg(self, parametros) -> None:
        try:
            self.cfg["kp"] = float(parametros["kp"])
            self.cfg["ki"] = float(parametros["ki"])
            self.cfg["kd"] = float(parametros["kd"])
            self.cfg["kie"] = float(parametros["kie"])

            self.cfg["nv_alvo"] = float(parametros["nv_alvo"])
            self.cfg["nv_minimo"] = float(parametros["nv_minimo"])
            self.cfg["nv_maximo"] = float(parametros["nv_maximo"])
            self.cfg["nv_religamento"] = float(parametros["nv_religamento"])

            self.cfg["pot_maxima_alvo"] = float(parametros["pot_nominal"])
            self.cfg["pot_maxima_ug"] = float(parametros["pot_nominal_ug"])
            self.cfg["pot_maxima_usina"] = float(parametros["pot_nominal_ug"]) * 2
            self.cfg["margem_pot_critica"] = float(parametros["margem_pot_critica"])

            with open(os.path.join(os.path.dirname("/opt/operacao-autonoma/src/dicionarios/"), 'cfg.json'), 'w') as file:
                json.dump(self.cfg, file)

        except Exception:
            logger.error(f"[USN] Houve um erro ao atualizar o arquivo de configuração \"cfg.json\".")
            logger.debug(traceback.format_exc())


    def escrever_valores(self) -> None:

        try:
            bd.BancoDados.update_valores_usina([
                self.get_time().strftime("%Y-%m-%d %H:%M:%S"),
                1 if self.aguardando_reservatorio else 0,
                tda.TomadaAgua.nv_montante.valor,
                self.ug1.potencia,
                self.ug1.setpoint,
                self.ug1.codigo_state,
                self.ug2.potencia,
                self.ug2.setpoint,
                self.ug2.codigo_state,
            ])

        except Exception:
            logger.debug(f"[USN] Houve um erro ao inserir os valores no Banco.")
            logger.debug(traceback.format_exc())

        try:
            bd.BancoDados.update_debug([
                self.get_time().timestamp(),
                1 if self.modo_autonomo else 0,
                tda.TomadaAgua.nv_montante.valor,
                tda.TomadaAgua.erro_nv,
                self.ug1.setpoint,
                self.ug1.potencia,
                self.ug1.codigo_state,
                self.ug2.setpoint,
                self.ug2.potencia,
                self.ug2.codigo_state,
                self.controle_p,
                self.controle_i,
                self.controle_d,
                self.controle_ie,
                self.cfg["kp"],
                self.cfg["ki"],
                self.cfg["kd"],
                self.cfg["kie"],
            ])

        except Exception:
            logger.debug(f"[USN] Houve um erro ao inserir dados DEBUG no Banco.")
            logger.debug(traceback.format_exc())


    def heartbeat(self) -> None:
        try:
            srv.Servidores.clp["MOA"].write_single_coil(REG_MOA["PAINEL_LIDO"], [1])
            srv.Servidores.clp["MOA"].write_single_coil(REG_MOA["MOA_OUT_MODE"], [1 if self.modo_autonomo else 0])
            srv.Servidores.clp["MOA"].write_single_register(REG_MOA["MOA_OUT_STATUS"], self.estado_moa)

            for ug in self.ugs: ug.atualizar_modbus_moa()

            if self.modo_autonomo:
                srv.Servidores.clp["MOA"].write_single_coil(REG_MOA["MOA_OUT_EMERG"], [1 if self.clp_emergencia else 0])
                srv.Servidores.clp["MOA"].write_single_register(REG_MOA["MOA_OUT_TARGET_LEVEL"], int((self.cfg["nv_alvo"] - 819.2) * (1/1000)))
                srv.Servidores.clp["MOA"].write_single_register(REG_MOA["MOA_OUT_SETPOINT"], int(sum(ug.setpoint for ug in self.ugs)))

                if srv.Servidores.clp["MOA"].read_coils(REG_MOA["MOA_IN_EMERG"])[0] and not self.borda_emerg:
                    self.borda_emerg = True
                    for ug in self.ugs: ug.verificar_condicionadores(ug)

                elif not srv.Servidores.clp["MOA"].read_coils(REG_MOA["MOA_IN_EMERG"])[0] and self.borda_emerg:
                    self.borda_emerg = False

                if srv.Servidores.clp["MOA"].read_coils(REG_MOA["MOA_IN_EMERG_UG1"])[0]:
                    self.ug1.verificar_condicionadores(self.ug1)

                if srv.Servidores.clp["MOA"].read_coils(REG_MOA["MOA_IN_EMERG_UG2"])[0]:
                    self.ug2.verificar_condicionadores(self.ug2)

                if srv.Servidores.clp["MOA"].read_coils(REG_MOA["MOA_IN_HABILITA_AUTO"])[0]:
                    srv.Servidores.clp["MOA"].write_single_coil(REG_MOA["MOA_IN_HABILITA_AUTO"], 1)
                    srv.Servidores.clp["MOA"].write_single_coil(REG_MOA["MOA_IN_DESABILITA_AUTO"], 0)
                    self.modo_autonomo = True

                if srv.Servidores.clp["MOA"].read_coils(REG_MOA["MOA_IN_DESABILITA_AUTO"])[0]:
                    srv.Servidores.clp["MOA"].write_single_coil(REG_MOA["MOA_IN_HABILITA_AUTO"], 0)
                    srv.Servidores.clp["MOA"].write_single_coil(REG_MOA["MOA_IN_DESABILITA_AUTO"], 1)
                    self.modo_autonomo = False

                if srv.Servidores.clp["MOA"].read_coils(REG_MOA["MOA_OUT_BLOCK_UG1"])[0]:
                    srv.Servidores.clp["MOA"].write_single_coil(REG_MOA["MOA_OUT_BLOCK_UG1"], 1)

                elif not srv.Servidores.clp["MOA"].read_coils(REG_MOA["MOA_OUT_BLOCK_UG1"])[0]:
                    srv.Servidores.clp["MOA"].write_single_coil(REG_MOA["MOA_OUT_BLOCK_UG1"], 0)

                if srv.Servidores.clp["MOA"].read_coils(REG_MOA["MOA_OUT_BLOCK_UG2"])[0]:
                    srv.Servidores.clp["MOA"].write_single_coil(REG_MOA["MOA_OUT_BLOCK_UG2"], 1)

                elif not srv.Servidores.clp["MOA"].read_coils(REG_MOA["MOA_OUT_BLOCK_UG2"])[0]:
                    srv.Servidores.clp["MOA"].write_single_coil(REG_MOA["MOA_OUT_BLOCK_UG2"], 0)

            elif not self.modo_autonomo:
                if srv.Servidores.clp["MOA"].read_coils(REG_MOA["MOA_IN_HABILITA_AUTO"])[0]:
                    srv.Servidores.clp["MOA"].write_single_coil(REG_MOA["MOA_IN_HABILITA_AUTO"], 1)
                    srv.Servidores.clp["MOA"].write_single_coil(REG_MOA["MOA_IN_DESABILITA_AUTO"], 0)
                    self.modo_autonomo = True

                srv.Servidores.clp["MOA"].write_single_coil(REG_MOA["MOA_OUT_EMERG"], 0)
                srv.Servidores.clp["MOA"].write_single_coil(REG_MOA["MOA_OUT_BLOCK_UG1"], 0)
                srv.Servidores.clp["MOA"].write_single_coil(REG_MOA["MOA_OUT_BLOCK_UG2"], 0)
                srv.Servidores.clp["MOA"].write_single_register(REG_MOA["MOA_OUT_SETPOINT"], int(0))
                srv.Servidores.clp["MOA"].write_single_register(REG_MOA["MOA_OUT_TARGET_LEVEL"], int(0))

        except Exception:
            logger.error(f"[USN] Houve um erro ao tentar escrever valores modbus no CLP MOA.")
            logger.debug(traceback.format_exc())