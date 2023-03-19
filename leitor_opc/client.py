import os
import json
import OpenOPC
import logging
import pywintypes

from time import sleep
from datetime import datetime

from reg import *

pywintypes.datetime = pywintypes.TimeType

logger = logging.getLogger("__main__")

class ComOpcDnp:
   def __init__(self) -> None:

      self.arquivo = os.path.join(os.path.dirname(__file__), "data.json")
      with open(self.arquivo, "r") as file:
         self.dados = json.load(file)

      self.antigos: list[str, float] = []

      self.opc = OpenOPC.client()
      self.opc.connect('Elipse.OPCSvr.1')
   
   def exec(self) -> None:
      while True:
         self.registrar_leitura()
         self.registar_mudanca()
         sleep(3)

   def registrar_leitura(self) -> None:
      for nome, reg, val in zip(REG_BAY[nome, reg], self.antigos[nome, val]):
         leitura = self.opc.read(REG_BAY[reg], group=0)
         if self.antigos[nome] == REG_BAY[nome] and leitura != self.antigos[val]:
            self.antigos[reg] = leitura

   def registar_mudanca(self) -> None:
      for reg, val in zip(self.antigos[reg, val], self.dados[reg, val]):
         if self.dados[reg] == self.antigos[reg] and self.antigos[val] != self.dados[val]:
            with open(self.dados, "w") as file:
               json.dump(self.antigos[val], file, indent=4)
            logger.info(f"Dado: {reg}, alterado. Valor: {self.dados[val]}")