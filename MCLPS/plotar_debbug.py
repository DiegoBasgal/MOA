import numpy as np
import matplotlib.pyplot as plt

fig, ax1 = plt.subplots()
ax1.set_xlabel('Amostra')
ax1.set_ylabel('Nv_montante', color='blue')
ax2 = ax1.twinx()
ax2.set_ylabel('Potências', color='black')
ax1.axis([0, 1000, 642.95, 643.75])
ax2.axis([0, 1000, 0, 5])
ax1.axhline(y=643.50, color="red", linestyle="--")
ax1.axhline(y=643.25, color="black", linestyle=":")
ax1.axhline(y=643.00, color="red", linestyle="--")

fig.tight_layout()  # otherwise the right y-label is slightly clipped

i = 0
nv = []
p1 = []
p2 = []
pt = []
while True:
    i += 1
    fp = open('debug.out', 'r')

    aux = fp.readline()
    if aux:
        nv.append(float(aux))
    else:
        nv.append(nv[-1])

    aux = fp.readline()
    if aux:
        p1.append(float(aux))
    else:
        p1.append(p1[-1])

    aux = fp.readline()
    if aux:
        p2.append(float(aux))
    else:
        p2.append(p2[-1])

    aux = fp.readline()
    if aux:
        pt.append(float(aux))
    else:
        pt.append(pt[-1])

    fp.close()
    print("running...")

    if i >= 1000:
        ax1.axis([i-1000, i, 642.95, 643.75])

    ax1.plot(nv, color='blue')
    ax2.plot(p1, color='orange', linestyle="--")
    ax2.plot(p2, color='yellow', linestyle="--")
    ax2.plot(pt, color='red', linestyle=":")

    plt.pause(0.1)

plt.show()

