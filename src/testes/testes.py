from src.dicionarios.reg import TESTE

# teste para acionar chamada voip diretamente checando o dicionário sem necessidade de ter variável acionar voip
"""
dict = {
    "v1": [False, "v1t"],
    "v2": [False, "v1t"],
    "v3": [False, "v1t"],
    "v4": [False, "v1t"],
    "v5": [False, "v1t"],
    "v6": [False, "v1t"],
    "v7": [True, "v1t"],
    "v8": [False, "v1t"],
    "v9": [False, "v1t"],
}

if True in [val[0] for name, val in dict.items()]:
    print("Funciona!") # Deu certo!
"""
"""------------------------------------------------------------------------------------------------------------ """

# teste de if de um linha com dois prints ou dois metodos por condicao
"""
def chamar() -> None:
    print("2")

a = 1

print("1"), chamar() if a == 1 else ...
"""
"""------------------------------------------------------------------------------------------------------------ """

# teste de classe sem instância com property e setter
"""
class Teste:
    a = 1
    _teste = 2

    b = False
    _teste2 = True

    @property
    def teste(cls) -> int:
        return cls._teste
    
    @teste.setter
    def teste(cls, var: int) -> None:
        cls._teste = var

    @property
    def teste2(cls) -> bool:
        return cls._teste2
    
    @teste2.setter
    def teste2(cls, var: bool) -> None:
        cls._teste2 = var


teste = Teste()
print(teste.teste2)
"""
"""------------------------------------------------------------------------------------------------------------ """

# teste setter valor dict
"""
valores: dict[str, bool] = {}


for n, v in TESTE.items():
    valores[n] = v

print(valores)
"""