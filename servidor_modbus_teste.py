
from time import sleep
from datetime import datetime
from pyModbusTCP.server import ModbusServer, DataBank

servidor_teste = ModbusServer(
        host="localhost",
        port=502,
        no_block=True
)

n_regs = 30000

servidor_teste.start()

for reg in range(n_regs):
    print(f"Carregando registrador: {reg}")
    DataBank.set_words(reg, [0])

while True:
    try:
        print("\nSeridor On-line.")
        print(f"Horário: {datetime.now().strftime('%H:%M:%S')}")
        sleep(5)

    except KeyboardInterrupt:
        servidor_teste.stop()
        print("\n Comando de Teclado. Parando servidor de testes...\n")
        break