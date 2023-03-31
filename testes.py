# teste para acionar chamada voip diretamente checando o dicionário sem necessidade de ter variável acionar voip
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

"""------------------------------------------------------------------------------------------------------------ """

