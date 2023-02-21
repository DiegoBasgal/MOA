import os
import json
import OpenOPC

from time import sleep

config_file = os.path.join(os.path.dirname(__file__), "data.json")
with open(config_file, "r") as file:
   cfg = json.load(file)

config_file = os.path.join(os.path.dirname(__file__), "data.json.bkp")
with open(config_file, "w") as file:
    json.dump(json.load(file), file, indent=4)


client = OpenOPC.client()

client.servers()

client.connect('localhost') # client.connect('Matrikon.OPC.Simulation') ## Exemplo sourceforge

while True:
   try:
      client.read('Alguma.Coisa1') # Exemplo: (19169, 'Good', '06/24/07 15:56:11')

      valor = client.read('Alguma.Coisa2')
      cfg["Algum_valor"] = valor

      client.write(('Triangle Waves.Real8', cfg["Valor_escrever"]))
      sleep(5)

   except Exception as e:
      raise e
   
   finally:
      client.close()