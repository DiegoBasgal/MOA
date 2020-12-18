from time import sleep
import matplotlib.pyplot as plt

fp = open('debug.out', 'w')
fp.write("")
fp.close()
sleep(0.5)


limite_t = 24

fig, ax1 = plt.subplots()

ax1.set_xlabel('Tempo decorrido na simulação')
ax1.set_ylabel('Nível montante (m)', color='blue')
ax1.axis([0, limite_t, 642.95, 643.75])

ax3 = ax1.twinx()
ax3.set_ylabel('Vazão Afluente (m³/s)', color='Green')
ax3.axis([0, limite_t, 0, 30])
ax3.spines['right'].set_position(('outward', 60))
ax3.xaxis.set_ticks([])

ax2 = ax1.twinx()
ax2.set_ylabel('Potências (MW)', color='Red')
ax2.axis([0, limite_t, 0, 5])



ax1.axhline(y=643.50, color="black", linestyle="--")
ax1.axhline(y=643.25, color="gray", linestyle=":")
ax1.axhline(y=643.00, color="black", linestyle="--")
plt.title("MOA - Simulação do comportamento")
plt.xticks(range(0, limite_t+1, 5))

#fig.tight_layout()  # otherwise the right y-label is slightly clipped

# segundos_simulados, q_afluente, nv_montante, pot_ug1, pot_ug2

t_sim = [0]
nv_m = [0]
q_aflu = [0]
pot1 = [0]
pot2 = [0]
pott = [0]
setpoint = [0]

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
        q_aflu.append(aux[1])
        nv_m.append(aux[2])
        pot1.append(aux[3])
        pot2.append(aux[4])
        pott.append(aux[3]+aux[4])
        setpoint.append(aux[5])

    # if t_sim[-1] >= limite_t:
       # ax1.axis([t_sim[-1]-limite_t, t_sim[-1], 642.95, 643.75])
       # ax2.axis([t_sim[-1]-limite_t, t_sim[-1], 0, 5])
       # ax3.axis([t_sim[-1]-limite_t, t_sim[-1], 0, 30])

    linha1, = ax1.plot(t_sim, nv_m, label='Nível montante', color='blue')
    linha5, = ax3.plot(t_sim, q_aflu, label='Afluente', color='green')
    linha2, = ax2.plot(t_sim, pot1, label='Potência UG1', color='orange', linestyle="--")
    linha3, = ax2.plot(t_sim, pot2, label='Potência UG2', color='yellow', linestyle="--")
    linha4, = ax2.plot(t_sim, pott, label='Potência total', color='red', linestyle=":")
    linha6, = ax2.plot(t_sim, setpoint, label='SetPoint', color='purple', linestyle=":")
    if primeira_vez:
        plt.legend(handles=[linha1, linha5, linha2, linha3, linha4, linha6], loc='upper center', bbox_to_anchor=(0.5, -0.05), ncol=3)

    # print(t_sim)
    # print("running...")

    plt.pause(0.05)
    primeira_vez = False

plt.show()

