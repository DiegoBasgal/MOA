class c:
    def __init__(self, a, b, c, d):
      self.descr = a
      self.ativo = b
      self.valor = c
      self.gravidade = d

condicionadores_ativos = [
    c("descr1", "ativo1", "valor1", "gravidade1"),
    c("descr2", "ativo2", "valor2", "gravidade2"),
    c("descr3", "ativo3", "valor3", "gravidade3"),
]
x = "[UG{}] UG em modo disponível detectou condicionadores ativos.\nCondicionadores ativos:\n".format(100) + \
"\n".join(["Desc: {}; Ativo: {}; Valor: {}; Gravidade: {}".format(d.descr, d.ativo, d.valor, d.gravidade) for d in condicionadores_ativos])

print(x)
