import numpy as np
import random
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

random.seed(42)

CUSTOS = np.array([
    [0, 2, 4, np.inf, np.inf, np.inf],
    [2, 0, 1, 5, np.inf, np.inf],
    [4, 1, 0, 2, 3, np.inf],
    [np.inf, 5, 2, 0, 1, 4],
    [np.inf, np.inf, 3, 1, 0, 2],
    [np.inf, np.inf, np.inf, 4, 2, 0]
])
ORIGEM = 0
DESTINO = 5
NUM_FORMIGAS = 20
NUM_ITERACOES = 50
ALPHA = 1.0
BETA = 2.0
TAXA_EVAPORACAO = 0.5
Q = 100

feromonio = np.ones_like(CUSTOS, dtype=float)
feromonio[CUSTOS == np.inf] = 0

def obter_vizinhos(no):
    vizinhos = []
    for proximo in range(len(CUSTOS)):
        if proximo != no and CUSTOS[no][proximo] != np.inf:
            vizinhos.append(proximo)
    return vizinhos

def calcular_atratividade(no_atual, proximo):
    fer = feromonio[no_atual][proximo]
    custo = CUSTOS[no_atual][proximo]
    atratividade = (fer ** ALPHA) * ((1 / custo) ** BETA)
    return atratividade

def evaporar_feromonio():
    global feromonio
    feromonio = feromonio * (1 - TAXA_EVAPORACAO)
    feromonio[CUSTOS == np.inf] = 0

def depositar_feromonio(rota, custo):
    deposito = Q / custo
    for i in range(len(rota) - 1):
        origem = rota[i]
        destino = rota[i + 1]
        feromonio[origem][destino] += deposito

def construir_rota():
    rota = [ORIGEM]
    atual = ORIGEM
    while atual != DESTINO:
        vizinhos = obter_vizinhos(atual)
        candidatos = [no for no in vizinhos if no not in rota]
        if not candidatos:
            return None
        atratividades = [calcular_atratividade(atual, no) for no in candidatos]
        soma = sum(atratividades)
        probabilidades = [a / soma for a in atratividades]
        proximo = random.choices(candidatos, weights=probabilidades, k=1)[0]
        rota.append(proximo)
        atual = proximo
    return rota

def calcular_custo(rota):
    return sum(CUSTOS[rota[i]][rota[i + 1]] for i in range(len(rota) - 1))

print("Teste calcular_atratividade(0,1):", calcular_atratividade(0, 1), "(esperado 0.25)")
print("Teste calcular_atratividade(0,2):", calcular_atratividade(0, 2), "(esperado 0.0625)")

melhor_rota = None
melhor_custo = float("inf")

for iteracao in range(NUM_ITERACOES):
    rotas = []
    for _ in range(NUM_FORMIGAS):
        rota = construir_rota()
        if rota is not None:
            custo = calcular_custo(rota)
            rotas.append((rota, custo))
            if custo < melhor_custo:
                melhor_custo = custo
                melhor_rota = rota.copy()
    evaporar_feromonio()
    for rota, custo in rotas:
        depositar_feromonio(rota, custo)

print("Melhor rota:", melhor_rota)
print("Melhor custo:", melhor_custo)
