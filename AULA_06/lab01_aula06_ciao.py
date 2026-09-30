import numpy as np
import random
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

random.seed(42)
np.random.seed(42)

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
print("Matriz inicial de feromônio:")
print(feromonio)

def obter_vizinhos(no):
    vizinhos = []
    for proximo in range(len(CUSTOS)):
        if proximo != no and CUSTOS[no][proximo] != np.inf:
            vizinhos.append(proximo)
    return vizinhos

print("Vizinhos do nó 0:", obter_vizinhos(0))
print("Vizinhos do nó 2:", obter_vizinhos(2))

def escolher_proximo(no_atual, visitados):
    vizinhos = obter_vizinhos(no_atual)
    candidatos = [no for no in vizinhos if no not in visitados]
    if not candidatos:
        return None
    atratividades = []
    for proximo in candidatos:
        fer = feromonio[no_atual][proximo]
        custo = CUSTOS[no_atual][proximo]
        atratividades.append(fer ** ALPHA * (1 / custo) ** BETA)
    soma = sum(atratividades)
    probabilidades = [v / soma for v in atratividades]
    return random.choices(candidatos, weights=probabilidades, k=1)[0]

def construir_rota():
    rota = [ORIGEM]
    atual = ORIGEM
    while atual != DESTINO:
        proximo = escolher_proximo(atual, rota)
        if proximo is None:
            return None
        rota.append(proximo)
        atual = proximo
    return rota

print("\nRotas encontradas:")
for i in range(5):
    rota = construir_rota()
    print(f"Formiga {i + 1}: {rota}")

def calcular_custo(rota):
    total = 0
    for i in range(len(rota) - 1):
        total += CUSTOS[rota[i]][rota[i + 1]]
    return total

rota = construir_rota()
if rota is not None:
    print("\nRota:", rota)
    print("Custo:", calcular_custo(rota))

def depositar_feromonio(rota, custo):
    deposito = Q / custo
    for i in range(len(rota) - 1):
        feromonio[rota[i]][rota[i + 1]] += deposito

def evaporar_feromonio():
    global feromonio
    feromonio *= (1 - TAXA_EVAPORACAO)
    feromonio[CUSTOS == np.inf] = 0

melhor_rota = None
melhor_custo = float("inf")
historico = []

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
    historico.append(melhor_custo)

print("\n========== RESULTADO ==========")
print("Melhor rota encontrada:", melhor_rota)
print("Melhor custo:", melhor_custo)

plt.figure(figsize=(10, 5))
plt.plot(historico)
plt.xlabel("Iteração"); plt.ylabel("Melhor custo")
plt.title("Convergência do ACO"); plt.grid()
plt.savefig("lab01_convergencia.png"); plt.close()

plt.figure(figsize=(7, 6))
plt.imshow(feromonio, cmap="hot")
plt.colorbar(label="Quantidade de feromônio")
plt.xlabel("Nó de destino"); plt.ylabel("Nó de origem")
plt.title("Memória Coletiva da Colônia")
plt.savefig("lab01_feromonio.png"); plt.close()

np.set_printoptions(precision=2, suppress=True)
print("\nMatriz final de feromônio:")
print(feromonio)
print("Histórico (primeiras 5 iterações):", historico[:5])
