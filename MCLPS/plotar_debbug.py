from time import sleep
import matplotlib.pyplot as plt

fp = open('debug.out', 'w')
fp.write("")
fp.close()
sleep(0.5)


limite_t = 3

fig, ax1 = plt.subplots()
ax1.set_xlabel('Tempo decorrido na simulação (horas)')
ax1.set_ylabel('Nível montante (m)', color='blue')
ax2 = ax1.twinx()
ax2.set_ylabel('Potências (MW)', color='Red')
ax1.axis([0, limite_t, 642.95, 643.75])
ax2.axis([0, limite_t, 0, 5])
ax1.axhline(y=643.50, color="red", linestyle="--")
ax1.axhline(y=643.25, color="black", linestyle=":")
ax1.axhline(y=643.00, color="red", linestyle="--")
plt.title("MOA - Simulação do comportamento")


fig.tight_layout()  # otherwise the right y-label is slightly clipped

# segundos_simulados, q_afluente, nv_montante, pot_ug1, pot_ug2

t_sim = [0]
nv_m = [0]
pot1 = [0]
pot2 = [0]
pott = [0]


primeira_vez = True

while True:
    aux = False
    while not aux:
        fp = open('debug.out', 'r')
        aux = fp.readline()
        fp.close()
        sleep(0.1)
    if aux:


        aux = aux.split()[:]
        for a in range(len(aux)):
            aux[a] = float(aux[a])
        t_sim.append(aux[0]/3600)
        nv_m.append(aux[2])
        pot1.append(aux[3])
        pot2.append(aux[4])
        pott.append(aux[3]+aux[4])

    if int(t_sim[-1]) >= limite_t:
        ax1.axis([int(t_sim[-1])-limite_t, t_sim[-1], 642.95, 643.75])

    linha1, = ax1.plot(t_sim, nv_m, label='Nível montante', color='blue')
    linha2, = ax2.plot(t_sim, pot1, label='Potência UG1', color='orange', linestyle="--")
    linha3, = ax2.plot(t_sim, pot2, label='Potência UG2', color='yellow', linestyle="--")
    linha4, = ax2.plot(t_sim, pott, label='Potência total', color='red', linestyle=":")
    if primeira_vez:
        plt.legend(handles=[linha1, linha2, linha3, linha4], loc='upper center', bbox_to_anchor=(0.5, -0.05), ncol=4)

    print(t_sim)
    print("running...")

    plt.pause(1)
    primeira_vez = False

plt.show()

