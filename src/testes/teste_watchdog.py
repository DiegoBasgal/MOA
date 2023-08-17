import pytz

from time import sleep, time
from datetime import datetime
from pyModbusTCP.server import ModbusServer, DataBank

server = ModbusServer(host="0.0.0.0", port=5000, no_block=True)
server.start()

teste_erro = time() + 20

while True:
    agora = datetime.now(pytz.timezone("Brazil/East")).replace(tzinfo=None)

    ano = int(agora.year)
    mes = int(agora.month)
    dia = int(agora.day)
    hor = int(agora.hour)
    mnt = int(agora.minute)
    seg = int(agora.second)
    mil = int(agora.microsecond / 1000)

    DataBank.set_words(0, [ano, mes, dia, hor, mnt, seg, mil])
    print([ano, mes, dia, hor, mnt, seg, mil])

    if time() > teste_erro:
        DataBank.set_words(0, [ano, mes, dia + 1, hor, mnt, seg, mil])

    sleep(4)
