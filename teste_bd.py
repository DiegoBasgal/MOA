import src.conectores.banco_dados as bd
import src.mensageiro.voip as v


# banco = bd.BancoDados("teste")

# print(banco.get_contato_emergencia())

v.Voip.acionar_chamada()