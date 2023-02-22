import os
import json
import OpenOPC
import pywintypes

from time import sleep

pywintypes.datetime = pywintypes.TimeType

config_file = os.path.join(os.path.dirname(__file__), "data.json")
with open(config_file, "r") as file:
   data = json.load(file)

opc = OpenOPC.client()

opc.connect('Elipse.OPCSvr.1')

while True:

   print(opc.read('Driver1.Pasta1.Coil.Value', group='Group0'))
   sleep(4)
   
   ler_opc = opc.read('Driver1.Pasta1.Coil.Value', group='Group0')[0]
   
   if ler_opc != data["Driver1.Pasta1.Coil.Value"]:
      data["Driver1.Pasta1.Coil.Value"] = ler_opc
      dado_json_antigo = data["Driver1.Pasta1.Coil.Value"]
      with open(config_file, "w") as file:
         json.dump(data, file, indent=4)
   else:
      print("Os dados do server OPC e JSON continuam os mesmos")
   sleep(4)


   if data['Valor_coil_driver1'] != dado_json_antigo:
      print(opc.write(('Driver1.Pasta1.Coil2.Value', data['Valor_coil_driver1e'])))
   else:
      print("O dado não mudou")
   sleep(4)