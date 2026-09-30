import numpy as np
import random
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

random.seed(7)

# 1 - Rede como matriz de custos
CUSTOS = np.array([
    [0, 2, 4, np.inf, np.inf, np.inf],
    [2, 0, 1, 5, np.inf, np.inf],
    [4, 1, 0, 2, 3, np.inf],
    [np.inf, 5, 2, 0, 1, 4],
    [np.inf, np.inf, 3, 1, 0, 2],
    [np.inf, np.inf, np.inf, 4, 2, 0]
])
ORIGEM, DESTINO = 0, 5

NUM_FORMIGAS = 20
NUM_ITERACOES = 50
ALPHA = 1.0
BETA = 2.0
TAXA_EVAPORACAO = 0.5
Q = 100

# 2 - Matriz de feromônio
feromonio = np.ones_like(CUSTOS, dtype=float)
feromonio[CUSTOS == np.inf] = 0

def vizinhos(no):
    return [p for p in range(len(CUSTOS)) if p != no and CUSTOS[no][p] != np.inf]

# 3/4/5 - Formiga constrói rota sem revisitar nós
def construir_rota():
    rota = [ORIGEM]
    atual = ORIGEM
    while atual != DESTINO:
        cand = [n for n in vizinhos(atual) if n not in rota]
        if not cand:
            return None
        pesos = [feromonio[atual][n] ** ALPHA * (1 / CUSTOS[atual][n]) ** BETA for n in cand]
        atual = random.choices(cand, weights=pesos, k=1)[0]
        rota.append(atual)
    return rota

# 6 - Custo
def calcular_custo(rota):
    return sum(CUSTOS[rota[i]][rota[i + 1]] for i in range(len(rota) - 1))

# 7 - Depósito
def depositar(rota, custo):
    for i in range(len(rota) - 1):
        feromonio[rota[i]][rota[i + 1]] += Q / custo

# 8 - Evaporação
def evaporar():
    global feromonio
    feromonio *= (1 - TAXA_EVAPORACAO)
    feromonio[CUSTOS == np.inf] = 0

melhor_rota, melhor_custo, historico = None, float("inf"), []

# 9 - Iterações
for _ in range(NUM_ITERACOES):
    rotas = []
    for _ in range(NUM_FORMIGAS):
        r = construir_rota()
        if r is not None:
            c = calcular_custo(r)
            rotas.append((r, c))
            if c < melhor_custo:
                melhor_custo, melhor_rota = c, r.copy()
    evaporar()
    for r, c in rotas:
        depositar(r, c)
    historico.append(melhor_custo)

# 10/11 - Resultado
print("========== RESULTADO ==========")
print("\nMelhor rota encontrada:")
print(melhor_rota)
print("\nMelhor custo:")
print(melhor_custo)

# 12 - Gráfico
plt.figure(figsize=(10, 5))
plt.plot(historico, marker="o", markersize=3)
plt.xlabel("Iteração"); plt.ylabel("Melhor custo")
plt.title("Evolução do melhor custo — ACO"); plt.grid()
plt.savefig("lab04_evolucao.png"); plt.close()
print("\nGráfico salvo em lab04_evolucao.png")
