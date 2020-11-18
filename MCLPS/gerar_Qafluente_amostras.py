import MCLPS.connector_db as db
import usina

primeira_amostra = True
t = 0

amostras = db.get_amostras()

for a in amostras:
    tant = t
    t = a[0]
    nv_montante_anterior = nv_montante
    nv_montante = a[1]
    if primeira_amostra:
        primeira_amostra = False
    else:
        temp = (t - tant).total_seconds()
        pot_ug1 = a[2] / 1000
        pot_ug2 = a[4] / 1000
        flags_comporta = 0

        if a[7] != 0:
            flags_comporta += 0x1
        if a[8] != 0:
            flags_comporta += 0x2
        if a[9] != 0:
            flags_comporta += 0x4
        if a[10] != 0:
            flags_comporta += 0x8
        if a[11] != 0:
            flags_comporta += 0x16
        if a[12] != 0:
            flags_comporta += 0x32

        print(usina.q_afluente(temp, pot_ug1, pot_ug2, nv_montante, nv_montante_anterior, flags_comporta))