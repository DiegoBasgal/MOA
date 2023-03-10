from time import sleep
from datetime import datetime
from pyModbusTCP.server import ModbusServer, DataBank

server = ModbusServer(port=502, no_block=True)
server.start()

while True:
    agora = datetime.now()
    ano = int(agora.year)
    mes = int(agora.month)
    dia = int(agora.day)
    hor = int(agora.hour)
    mnt = int(agora.minute)
    seg = int(agora.second)
    mil = int(agora.microsecond / 1000)
    DataBank.set_words(0, [ano, mes, dia, hor, mnt, seg, mil])
    print([ano, mes, dia, hor, mnt, seg, mil])
    sleep(4)
