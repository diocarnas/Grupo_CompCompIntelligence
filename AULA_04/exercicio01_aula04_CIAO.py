"""
Exercicio 1: Analise do Elitismo na Estabilidade Algoritmica
Objetivo: Alterar a flag de controle do elitismo para observar o impacto da
preservacao do melhor individuo na curva de convergencia.

Este script roda o algoritmo genetico DUAS vezes (com e sem elitismo, usando a
mesma matriz de distancias) para permitir a comparacao pedida no roteiro.
"""

import numpy as np


def calcular_custo(rota, matriz):
    dist = 0
    for i in range(len(rota) - 1):
        dist += matriz[rota[i], rota[i + 1]]
    return dist + matriz[rota[-1], rota[0]]


NUM_NOS = 8
TAM_POP = 40
GERACOES = 80


def rodar_ga(usar_elitismo, matriz_teste, seed):
    rng = np.random.default_rng(seed)
    populacao = [rng.permutation(NUM_NOS) for _ in range(TAM_POP)]

    historico_melhor = []

    for g in range(GERACOES):
        custos = [calcular_custo(ind, matriz_teste) for ind in populacao]
        melhor_idx = np.argmin(custos)
        historico_melhor.append(custos[melhor_idx])

        novos = []
        if usar_elitismo:
            novos.append(populacao[melhor_idx].copy())

        while len(novos) < TAM_POP:
            i1, i2 = rng.choice(TAM_POP, 2, replace=False)
            pai = populacao[i1] if custos[i1] < custos[i2] else populacao[i2]

            filho = pai.copy()
            if rng.random() < 0.3:
                idx1, idx2 = rng.choice(NUM_NOS, 2, replace=False)
                filho[idx1], filho[idx2] = filho[idx2], filho[idx1]
            novos.append(filho)

        populacao = novos

    custos_finais = [calcular_custo(ind, matriz_teste) for ind in populacao]
    return historico_melhor, min(custos_finais)


if __name__ == "__main__":
    # Mesma matriz de distancias para ambas as execucoes, garantindo comparacao justa
    np.random.seed(42)
    matriz_teste = np.random.uniform(10, 100, (NUM_NOS, NUM_NOS))

    hist_com, custo_com = rodar_ga(True, matriz_teste, seed=1)
    hist_sem, custo_sem = rodar_ga(False, matriz_teste, seed=1)

    print(f"[Exercicio 1] Menor Custo Obtido (Elitismo=True): {custo_com:.2f}")
    print(f"[Exercicio 1] Menor Custo Obtido (Elitismo=False): {custo_sem:.2f}")

    print("\nGeracao | Melhor custo (COM elitismo) | Melhor custo (SEM elitismo)")
    for g in range(0, GERACOES, 10):
        print(f"{g:7d} | {hist_com[g]:27.2f} | {hist_sem[g]:26.2f}")

    print(
        "\nObservacao esperada: com elitismo a curva do melhor custo nunca piora "
        "de uma geracao para a outra (e monotonicamente nao-crescente), pois o "
        "melhor individuo e sempre preservado. Sem elitismo, a curva pode "
        "apresentar oscilacoes/pioras, ja que o melhor individuo pode se perder "
        "por efeito da selecao/cruzamento estocasticos."
    )
