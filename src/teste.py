import pytz

from datetime import datetime

from src.conectores.banco_dados import BancoDados


bd = BancoDados("Teste")
ts = bd.get_horario_operar_lg()[0]

print(ts)
print(True if isinstance(ts, datetime) else False)
