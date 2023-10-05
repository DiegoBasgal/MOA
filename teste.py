from time import sleep

from src.dicionarios.reg import *
from src.funcoes.leitura import *
from src.funcoes.condicionadores import *
from src.conectores.servidores import Servidores


# ---------------------------------------------------------------------------- #
# Classes

class Bay:
    def __init__(self, serv: "Servidores"=None) -> None:

        self.rele = serv.rele

        self.condicionadores: "list[CondicionadorBase]" = []
        self.condicionadores_ativos: "list[CondicionadorBase]" = []
        self.condicionadores_essenciais: "list[CondicionadorBase]" = []


    def verificar_condicionadores(self) -> "list[CondicionadorBase]":

        if True in (condic.ativo for condic in self.condicionadores_essenciais):
            condics_ativos = [condic for condics in [self.condicionadores_essenciais, self.condicionadores] for condic in condics if condic.ativo]

            print("")
            if self.condicionadores_ativos == []:
                print(f"[BAY] Foram detectados Condicionadores ativos no Bay!")

            else:
                print(f"[BAY] Ainda há Condicionadores ativos no Bay!")

            for condic in condics_ativos:
                if condic in self.condicionadores_ativos:
                    print(f"[BAY] Descrição: \"{condic.descricao}\", Gravidade: \"{condic.gravidade}\"")
                    continue
                else:
                    print(f"[BAY] Descrição: \"{condic.descricao}\", Gravidade: \"{condic.gravidade}\"")
                    self.condicionadores_ativos.append(condic)

            print("")
            return condics_ativos

        else:
            self.condicionadores_ativos = []
            return []


    def carregar_leituras(self) -> "None":
        self.bay_secc_fechada = LeituraModbusBit(
            self.rele['BAY'],
            REG_RELE['BAY']['SECC_FECHADA'],
            invertido=True,
        )

        self.secc_aberta = LeituraModbusBit(self.rele["BAY"], REG_RELE["BAY"]["SECC_FECHADA"], descricao="[BAY][RELE] Seccionadora Aberta")
        self.condicionadores_essenciais.append(CondicionadorBase(self.secc_aberta, 3))




class Usina:
    def __init__(self, serv: "Servidores"=None) -> None:

        self.bay = Bay(serv)

        serv.open_all()

        self.bay.carregar_leituras()



# ---------------------------------------------------------------------------- #
# Iniciar Classes

serv = Servidores()

usn = Usina(serv)


# ---------------------------------------------------------------------------- #
# Ciclo de Teste


while True:
    try:
        print("")
        print(f"Leitura Do Status da Seccionadora do Bay -> \"{usn.bay.bay_secc_fechada.valor}\"")
        print("")
        sleep(1)
        usn.bay.verificar_condicionadores()

    except Exception as e:
        print(f"Erro no Loop! Motivo: {e}")
        break

    except KeyboardInterrupt:
        break