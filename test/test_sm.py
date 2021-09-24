import logging
import unittest
from unittest.mock import MagicMock, patch

from src import operador_autonomo_sm


class TesteComportamentoSM(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        logging.disable(logging.CRITICAL)

    @classmethod
    def tearDownClass(cls):
        logging.disable(logging.NOTSET)

    def test_entra_no_estado(self):
        estado = MagicMock()
        parametros = MagicMock()
        operador_autonomo_sm.StateMachine(estado(parametros))
        estado.assert_called_once_with(parametros)

    def test_muda_de_estado(self):
        estado = MagicMock()
        parametros = MagicMock()
        estado2 = MagicMock()
        estado.run.returns(estado2(parametros))
        sm = operador_autonomo_sm.StateMachine(estado())
        sm.exec()
        estado2.assert_called_once_with(parametros)

    def test_raise_into_falha_critica(self):
        operador_autonomo_sm.FalhaCritica = MagicMock()
        estado = MagicMock()
        estado.run.side_effect = SystemError("test_raise_into_falha_critica")
        sm = operador_autonomo_sm.StateMachine(estado)
        sm.exec()
        operador_autonomo_sm.FalhaCritica.assert_called_once()


if __name__ == '__main__':
    unittest.main()
