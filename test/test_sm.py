import logging
import unittest
from unittest.mock import MagicMock, patch

import MOA


class TestComportamentoSM(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        logging.disable(logging.CRITICAL)

    @classmethod
    def tearDownClass(cls):
        logging.disable(logging.NOTSET)

    def test_entra_no_estado(self):
        # Teste:            test_entra_no_estado
        # Objetivo:         Verificar funcionamento basico da sm
        # Resposta:         SM entra em um estado dado e executa-o, mesmo, devolvendo o proximo estado

        estado = MOA.State
        estado.run = MagicMock()
        estado.run.return_value = "next_state"
        parametros = MagicMock()
        sm = MOA.StateMachine(estado(parametros))
        sm.exec()
        estado.run.assert_called_once()
        self.assertEqual("next_state", sm.state)

    def test_simple_sm(self):
        # Teste:            test_entra_no_estado
        # Objetivo:         Verificar funcionamento basico da sm
        # Resposta:         SM alterna entre dois estados

        class EstadoA:
            def __init__(self, i):
                self.i = i

            def run(self):
                return EstadoB(self.i + 1)

        class EstadoB:
            def __init__(self, i):
                self.i = i

            def run(self):
                return EstadoA(self.i + 1)

        sm = MOA.StateMachine(EstadoA(0))
        for n in range(10):
            sm.exec()
            if n % 2:
                self.assertIsInstance(sm.state, EstadoA)
                self.assertNotIsInstance(sm.state, EstadoB)
            else:
                self.assertIsInstance(sm.state, EstadoB)
                self.assertNotIsInstance(sm.state, EstadoA)

    def test_raise_into_falha_critica(self):
        # Teste:            test_entra_no_estado
        # Objetivo:         Verificar se a SM chama a Falha critica
        # Resposta:         SM Falha e chama a Falha critica
        estado = MagicMock()
        estado.run.side_effect = TimeoutError
        sm = MOA.StateMachine(estado)
        sm.exec()
        self.assertTrue(sm.em_falha_critica)
        with self.assertRaises(SystemExit):
            sm.exec()

    def test_raise_into_falha_critica_2(self):
        class EstadoA:
            def run(self):
                return 1 / 0

        sm = MOA.StateMachine(EstadoA())
        sm.exec()

        self.assertTrue(sm.em_falha_critica)
        with self.assertRaises(SystemExit):
            sm.exec()


if __name__ == "__main__":
    unittest.main()
