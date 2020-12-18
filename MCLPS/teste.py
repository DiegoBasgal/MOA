nv_montante = 0
volume = 206657
while nv_montante < 643.4:
    volume += 0.0001
    nv_montante = - 0.0000000002 * ((volume / 1000) ** 4) + 0.0000002 * ((volume / 1000) ** 3) - 0.0001 * (
        (volume / 1000) ** 2) + 0.0331 * ((volume / 1000)) + 639.43
    print(nv_montante, volume)