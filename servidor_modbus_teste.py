from datetime import datetime
from pyModbusTCP.server import ModbusServer

servidor_teste = ModbusServer(
        host="localhost",
        port=502,
        no_block=True
)

servidor_teste.start()

while True:
    try:
        print("\nSeridor On-line.")
        print(f"Horário: {datetime.now().strftime('%H:%M:%S')}")
        for t in range(20000):
            pass

    except KeyboardInterrupt:
        servidor_teste.stop()
        print("\n Comando de Teclado. Parando servidor de testes...\n")
        break