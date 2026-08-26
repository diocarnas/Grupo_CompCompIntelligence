"""
Exercicio 2: Insercao de Penalidades por Descumprimento de SLA
Objetivo: Implementar o calculo de penalidade estatica de +1000 ms para qualquer
enlace cuja latencia exceda o limite operacional de 50 ms.
"""

import numpy as np

np.random.seed(15)
matriz_latencia = np.random.uniform(5, 80, (6, 6))


def calcular_custo_com_sla(rota, matriz, limite_sla=50.0):
    custo_total = 0.0
    penalidade = 0.0

    for i in range(len(rota) - 1):
        latencia_enlace = matriz[rota[i], rota[i + 1]]
        custo_total += latencia_enlace

        # Incrementa a penalidade caso a latencia do enlace ultrapasse o SLA
        if latencia_enlace > limite_sla:
            penalidade += 1000.0

    return custo_total + penalidade


if __name__ == "__main__":
    rota_teste = np.array([0, 1, 2, 3, 4, 5])
    custo_final = calcular_custo_com_sla(rota_teste, matriz_latencia)

    print(f"[Exercicio 2] Custo Total (Com Penalizacoes de SLA): {custo_final:.2f} ms")

    # Detalhamento dos enlaces que violaram o SLA (util para o relatorio)
    print("\nDetalhamento dos enlaces da rota:")
    for i in range(len(rota_teste) - 1):
        a, b = rota_teste[i], rota_teste[i + 1]
        lat = matriz_latencia[a, b]
        status = "VIOLOU SLA (+1000 ms)" if lat > 50.0 else "dentro do SLA"
        print(f"  Enlace {a}->{b}: {lat:.2f} ms - {status}")
