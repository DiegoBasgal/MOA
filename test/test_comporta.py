import unittest
from src.abstracao_usina import Comporta

class TesteComportamentoDaComporta(unittest.TestCase):

    def test_nivel_rampa_decr(self):
        comporta = Comporta()
        comporta.pos_0 = {'pos': 0, 'anterior': 0.0, 'proximo': 15.0}
        comporta.pos_1 = {'pos': 1, 'anterior': 10.0, 'proximo': 20.0}
        comporta.pos_2 = {'pos': 2, 'anterior': 15.0, 'proximo': 25.0}
        comporta.pos_3 = {'pos': 3, 'anterior': 20.0, 'proximo': 30.0}
        comporta.pos_4 = {'pos': 4, 'anterior': 25.0, 'proximo': 35.0}
        comporta.pos_5 = {'pos': 5, 'anterior': 30.0, 'proximo': 0.0}
        resposta_desejada = 0
        for pos in range(6):
            comporta.pos_comporta = pos
            comporta.atualizar_estado(1.0)
            self.assertEqual(comporta.pos_comporta, resposta_desejada)

    def test_nivel_rampa_cres(self):
        comporta = Comporta()
        comporta.pos_0 = {'pos': 0, 'anterior': 0.0, 'proximo': 15.0}
        comporta.pos_1 = {'pos': 1, 'anterior': 10.0, 'proximo': 20.0}
        comporta.pos_2 = {'pos': 2, 'anterior': 15.0, 'proximo': 25.0}
        comporta.pos_3 = {'pos': 3, 'anterior': 20.0, 'proximo': 30.0}
        comporta.pos_4 = {'pos': 4, 'anterior': 25.0, 'proximo': 35.0}
        comporta.pos_5 = {'pos': 5, 'anterior': 30.0, 'proximo': 0.0}
        comporta.pos_comporta = 0
        for pos in range(6):
            resposta_desejada = pos + 1 if pos < 5 else 5
            comporta.atualizar_estado(100.0)
            self.assertEqual(comporta.pos_comporta, resposta_desejada)

    def teste_nivel_degrau_acima(self):
        comporta = Comporta()
        comporta.pos_0 = {'pos': 0, 'anterior':  0.0, 'proximo': 15.0}
        comporta.pos_1 = {'pos': 1, 'anterior': 10.0, 'proximo': 20.0}
        comporta.pos_2 = {'pos': 2, 'anterior': 15.0, 'proximo': 25.0}
        comporta.pos_3 = {'pos': 3, 'anterior': 20.0, 'proximo': 30.0}
        comporta.pos_4 = {'pos': 4, 'anterior': 25.0, 'proximo': 35.0}
        comporta.pos_5 = {'pos': 5, 'anterior': 30.0, 'proximo':  0.0}
        comporta.posicoes = [comporta.pos_0, comporta.pos_1, comporta.pos_2, comporta.pos_3, comporta.pos_4, comporta.pos_5]

        for pos in range(6):
            nv_teste = comporta.posicoes[pos]['proximo'] + 1.0 if pos < 5 else 100
            resposta_desejada = pos + 1 if pos < 5 else 5
            comporta.pos_comporta = pos
            for _ in range(10):
                comporta.atualizar_estado(nv_teste)
            self.assertEqual(comporta.pos_comporta, resposta_desejada)


if __name__ == '__main__':
    unittest.main()
