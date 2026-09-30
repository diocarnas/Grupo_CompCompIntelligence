import numpy as np
import random

CUSTOS = np.array([
    [0, 2, 4, np.inf, np.inf, np.inf],
    [2, 0, 1, 5, np.inf, np.inf],
    [4, 1, 0, 2, 3, np.inf],
    [np.inf, 5, 2, 0, 1, 4],
    [np.inf, np.inf, 3, 1, 0, 2],
    [np.inf, np.inf, np.inf, 4, 2, 0]
])
ORIGEM, DESTINO = 0, 5

def vizinhos(no):
    return [p for p in range(len(CUSTOS)) if p != no and CUSTOS[no][p] != np.inf]

def executar(NUM_FORMIGAS=20, NUM_ITERACOES=50, ALPHA=1.0, BETA=2.0,
             TAXA_EVAPORACAO=0.5, Q=100, seed=42):
    random.seed(seed)
    fer = np.ones_like(CUSTOS, dtype=float)
    fer[CUSTOS == np.inf] = 0

    def construir():
        rota, atual = [ORIGEM], ORIGEM
        while atual != DESTINO:
            cand = [n for n in vizinhos(atual) if n not in rota]
            if not cand:
                return None
            at = [fer[atual][n] ** ALPHA * (1 / CUSTOS[atual][n]) ** BETA for n in cand]
            atual = random.choices(cand, weights=at, k=1)[0]
            rota.append(atual)
        return rota

    custo_de = lambda r: sum(CUSTOS[r[i]][r[i+1]] for i in range(len(r)-1))
    melhor_rota, melhor_custo, hist = None, float("inf"), []
    for _ in range(NUM_ITERACOES):
        rotas = []
        for _ in range(NUM_FORMIGAS):
            r = construir()
            if r is not None:
                c = custo_de(r)
                rotas.append((r, c))
                if c < melhor_custo:
                    melhor_custo, melhor_rota = c, r.copy()
        fer *= (1 - TAXA_EVAPORACAO)
        fer[CUSTOS == np.inf] = 0
        for r, c in rotas:
            for i in range(len(r)-1):
                fer[r[i]][r[i+1]] += Q / c
        hist.append(melhor_custo)
    primeira = next(i+1 for i, h in enumerate(hist) if h == melhor_custo)
    # fração de formigas na última iteração que usaram a melhor rota
    frac = sum(1 for r, c in rotas if r == melhor_rota) / max(len(rotas), 1)
    print("\n========== RESULTADO DO EXPERIMENTO ==========")
    print("Número de formigas:", NUM_FORMIGAS)
    print("Número de iterações:", NUM_ITERACOES)
    print("ALPHA:", ALPHA)
    print("BETA:", BETA)
    print("Taxa de evaporação:", TAXA_EVAPORACAO)
    print("Melhor rota:", melhor_rota)
    print("Melhor custo:", melhor_custo)
    print("Iteração em que o melhor custo foi achado:", primeira)
    print(f"% de formigas da última iteração na melhor rota: {frac*100:.0f}%")
    print("Feromônio máx. / total:", round(fer.max(), 2), "/", round(fer.sum(), 2))

print("#### EXPERIMENTO 1 — ALPHA ####")
for a in (1.0, 0.1, 5.0):
    executar(ALPHA=a)
print("\n#### EXPERIMENTO 2 — BETA ####")
for b in (2.0, 0.5, 5.0):
    executar(BETA=b)
print("\n#### EXPERIMENTO 3 — EVAPORAÇÃO ####")
for e in (0.5, 0.1, 0.9):
    executar(TAXA_EVAPORACAO=e)
print("\n#### EXPERIMENTO 4 — NÚMERO DE FORMIGAS ####")
for n in (20, 5, 50):
    executar(NUM_FORMIGAS=n)
