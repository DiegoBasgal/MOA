valor = "00:02"

novo = str(valor.split(":"))

tempo = int(novo[0]) * 60 + int(novo[1])

print(novo[0])
print(novo[1])
print(tempo)