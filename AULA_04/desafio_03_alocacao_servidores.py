"""
Exercicio 3: Balanceamento de Carga em Servidores (Desafio de Codigo)

Cenario: 20 tarefas com tempos de processamento (em segundos) distribuidas
entre 4 servidores disponiveis.

Objetivo: Minimizar o Makespan (tempo total gasto pelo servidor com a maior
carga acumulada).

Representacao do Individuo: Vetor de 20 posicoes contendo inteiros no
intervalo [0,3], em que o indice representa a tarefa e o valor representa o
servidor atribuido.

Algoritmo: Algoritmo Genetico com selecao por torneio, crossover uniforme,
mutacao por realocacao de tarefa e elitismo.
"""

import numpy as np

# ---------------------------------------------------------------------------
# Dados do problema
# ---------------------------------------------------------------------------
T = [12, 35, 40, 8, 15, 22, 19, 45, 60, 31, 14, 28, 50, 18, 25, 33, 42, 10, 5, 29]
NUM_TAREFAS = len(T)
NUM_SERVIDORES = 4

# ---------------------------------------------------------------------------
# Parametros do GA
# ---------------------------------------------------------------------------
TAM_POP = 60
GERACOES = 200
TAXA_MUTACAO = 0.15
TAM_TORNEIO = 3


def calcular_makespan(individuo, tempos, num_servidores):
    """Retorna a maior carga acumulada entre os servidores (o makespan)."""
    cargas = np.zeros(num_servidores)
    for tarefa_idx, servidor in enumerate(individuo):
        cargas[servidor] += tempos[tarefa_idx]
    return cargas.max(), cargas


def criar_individuo(rng):
    return rng.integers(0, NUM_SERVIDORES, size=NUM_TAREFAS)


def selecao_torneio(populacao, fitnesses, rng, k=TAM_TORNEIO):
    participantes = rng.choice(len(populacao), size=k, replace=False)
    melhor = min(participantes, key=lambda idx: fitnesses[idx])
    return populacao[melhor].copy()


def crossover_uniforme(pai1, pai2, rng):
    mascara = rng.random(NUM_TAREFAS) < 0.5
    filho = np.where(mascara, pai1, pai2)
    return filho


def mutacao(individuo, rng, taxa=TAXA_MUTACAO):
    for i in range(len(individuo)):
        if rng.random() < taxa:
            individuo[i] = rng.integers(0, NUM_SERVIDORES)
    return individuo


def algoritmo_genetico(seed=7):
    rng = np.random.default_rng(seed)
    populacao = [criar_individuo(rng) for _ in range(TAM_POP)]

    melhor_individuo = None
    melhor_makespan = float("inf")
    historico = []

    for geracao in range(GERACOES):
        fitnesses = [calcular_makespan(ind, T, NUM_SERVIDORES)[0] for ind in populacao]

        idx_melhor_geracao = int(np.argmin(fitnesses))
        if fitnesses[idx_melhor_geracao] < melhor_makespan:
            melhor_makespan = fitnesses[idx_melhor_geracao]
            melhor_individuo = populacao[idx_melhor_geracao].copy()

        historico.append(melhor_makespan)

        nova_populacao = [melhor_individuo.copy()]  # elitismo
        while len(nova_populacao) < TAM_POP:
            pai1 = selecao_torneio(populacao, fitnesses, rng)
            pai2 = selecao_torneio(populacao, fitnesses, rng)
            filho = crossover_uniforme(pai1, pai2, rng)
            filho = mutacao(filho, rng)
            nova_populacao.append(filho)

        populacao = nova_populacao

    return melhor_individuo, melhor_makespan, historico


if __name__ == "__main__":
    melhor_individuo, melhor_makespan, historico = algoritmo_genetico()

    _, cargas_finais = calcular_makespan(melhor_individuo, T, NUM_SERVIDORES)

    print("=" * 60)
    print("Desafio 03 - Balanceamento de Carga em Servidores")
    print("=" * 60)
    print(f"\nTarefas (tempos em s): {T}")
    print(f"Numero de servidores: {NUM_SERVIDORES}\n")

    print(f"Melhor Makespan encontrado: {melhor_makespan:.0f} s\n")

    print("Alocacao de tarefas por servidor:")
    for servidor in range(NUM_SERVIDORES):
        tarefas_do_servidor = [i for i, s in enumerate(melhor_individuo) if s == servidor]
        tempo_total = sum(T[i] for i in tarefas_do_servidor)
        print(f"  Servidor {servidor}: tarefas {tarefas_do_servidor} -> carga total = {tempo_total} s")

    print(f"\nCargas finais por servidor: {cargas_finais}")

    soma_total = sum(T)
    limite_teorico = soma_total / NUM_SERVIDORES
    print(f"\nSoma total de trabalho: {soma_total} s")
    print(f"Limite inferior teorico (balanceamento perfeito): {limite_teorico:.2f} s")
    print(f"Gap em relacao ao limite teorico: {melhor_makespan - limite_teorico:.2f} s")
