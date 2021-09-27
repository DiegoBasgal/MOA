import unittest


class TestAgendamentos(unittest.TestCase):

    # No estado ValoresInternosAtualizados ele verifica a existencia de agendamentos
    # Caso não tenha, prox estado não e tratamento de agendamento
    # Caso tenha, troca de estado para tratamento
    def test_sm_verifica_agendamento(self):
        self.assertIs(True, not True)

    # Se houver ate 3 agendamentos para executar agora (< 5 min), ele executa o e marca no banco
    def test_executa_agendamento_simples(self):
        self.assertIs(True, not True)

    # Se houver pelo menos 1 agendamento muito atrasado (> 5 min), ele sinaliza e aciona a emergencia
    def test_executa_agendamentos_atraso_grande(self):
        self.assertIs(True, not True)

    # Se houver 3 ou mais agendamentos levemente atrasados (< 5 min), ele sinaliza o erro e aciona e emergencia
    def test_executa_agendamentos_atraso_multiplo(self):
        self.assertIs(True, not True)


if __name__ == '__main__':
    unittest.main()
