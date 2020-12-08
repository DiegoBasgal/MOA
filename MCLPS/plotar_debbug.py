from time import sleep

import numpy as np
import matplotlib.pyplot as plt

fig, ax1 = plt.subplots()
ax1.set_xlabel('T simulação (segundos)')
ax1.set_ylabel('Nv_montante', color='blue')
ax2 = ax1.twinx()
ax2.set_ylabel('Potências', color='Red')
ax1.axis([0, 10000, 642.95, 643.75])
ax2.axis([0, 10000, 0, 5])
ax1.axhline(y=643.50, color="red", linestyle="--")
ax1.axhline(y=643.25, color="black", linestyle=":")
ax1.axhline(y=643.00, color="red", linestyle="--")

fig.tight_layout()  # otherwise the right y-label is slightly clipped

# segundos_simulados, q_afluente, nv_montante, pot_ug1, pot_ug2

t_sim = []
nv_m = []
pot1 = []
pot2 = []
pott = []

fp = open('debug.out', 'w')
fp.write("")
fp.close()
sleep(1)

while True:
    fp = open('debug.out', 'r')
    aux = fp.readline()
    fp.close()
    if aux:
        aux = aux.split()[:]
        for a in range(len(aux)):
            aux[a] = float(aux[a])
        t_sim.append(aux[0])
        nv_m.append(aux[2])
        pot1.append(aux[3])
        pot2.append(aux[4])
        pott.append(aux[3]+aux[4])


    ax1.axis([t_sim[-1]-3600, t_sim[-1], 642.95, 643.75])

    ax1.plot(t_sim, nv_m, color='blue')
    ax2.plot(t_sim, pot1, color='orange', linestyle="--")
    ax2.plot(t_sim, pot2, color='yellow', linestyle="--")
    ax2.plot(t_sim, pott, color='red', linestyle=":")

    print(t_sim)
    print("running...")

    plt.pause(1)

plt.show()

