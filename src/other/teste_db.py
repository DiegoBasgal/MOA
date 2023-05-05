import banco_dados

db = banco_dados.Database()
res = db.get_executabilidade(102)
print(res)

db.update_agendamento(235, True, "Teste manual")
