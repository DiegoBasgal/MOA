import random

for ganho in [0.9, 0.95, 0.99, 1, 1.1]:

    pot_medidor = 0
    pot_alvo = 5100
    pot_limite = 5000

    for aux in range(10):
        print(aux, ganho, pot_alvo, pot_medidor)

        if pot_medidor > pot_limite:
            pot_alvo = pot_alvo * (pot_limite / pot_medidor)

        pot_medidor = pot_alvo * ganho

    print()
