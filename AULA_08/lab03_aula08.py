"""LAB 03 - ACO para topologia em árvore geradora de 10 switches (baixa latência)."""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from collections import deque

N = 10
rng0 = np.random.default_rng(7)
COORD = rng0.uniform(0, 100, (N, 2))                      # posições físicas dos switches
D = np.round(np.linalg.norm(COORD[:, None] - COORD[None], axis=2) / 2.0, 1)  # latência física (µs)
# pares críticos: (origem, destino, peso de tráfego)
ALL = [(i, j) for i in range(N) for j in range(i + 1, N)]
sel = rng0.choice(len(ALL), 12, replace=False)
PAIRS = [(ALL[k][0], ALL[k][1], int(rng0.integers(1, 6))) for k in sel]

ALPHA, BETA, RHO = 1.0, 2.0, 0.2
N_ANTS, N_ITERS, TOP_K = 20, 100, 3
TAU_MIN, TAU_MAX = 0.05, 10.0

class UnionFind:
    def __init__(self, n): self.p = list(range(n))
    def find(self, x):
        while self.p[x] != x:
            self.p[x] = self.p[self.p[x]]; x = self.p[x]
        return x
    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb: return False          # fecharia um ciclo
        self.p[ra] = rb; return True

def is_valid_tree(edges):
    """N-1 arestas + sem ciclos + conectado."""
    if len(edges) != N - 1: return False
    uf = UnionFind(N)
    return all(uf.union(u, v) for u, v in edges)   # sem ciclo => com N-1 arestas é conexo

def tree_cost(edges):
    """Soma ponderada das latências fim-a-fim pelo caminho único da árvore entre pares críticos."""
    adj = {i: [] for i in range(N)}
    for u, v in edges:
        adj[u].append((v, D[u, v])); adj[v].append((u, D[u, v]))
    total = 0.0
    for s in {p[0] for p in PAIRS}:
        dist, q = {s: 0.0}, deque([s])
        while q:
            x = q.popleft()
            for y, w in adj[x]:
                if y not in dist: dist[y] = dist[x] + w; q.append(y)
        total += sum(w * dist[t] for a, t, w in PAIRS if a == s)
    return total

def prim_mst():
    in_t, edges = {0}, []
    while len(in_t) < N:
        u, v = min(((u, v) for u in in_t for v in range(N) if v not in in_t), key=lambda e: D[e])
        edges.append((u, v)); in_t.add(v)
    return edges

def random_tree(rng):
    """Árvore geradora aleatória (crescimento por aresta aleatória)."""
    in_t, edges = {int(rng.integers(N))}, []
    while len(in_t) < N:
        u = int(rng.choice(sorted(in_t)))
        v = int(rng.choice([x for x in range(N) if x not in in_t]))
        edges.append((min(u, v), max(u, v))); in_t.add(v)
    return edges

def build_tree(tau, rng):
    """Formiga constrói a árvore escolhendo arestas (nó na árvore -> nó fora); valida ciclos via Union-Find."""
    uf, in_t, edges = UnionFind(N), {int(rng.integers(N))}, []
    while len(in_t) < N:
        cand = [(u, v) for u in in_t for v in range(N) if v not in in_t and uf.find(u) != uf.find(v)]
        p = np.array([(tau[u, v] ** ALPHA) * ((1.0 / D[u, v]) ** BETA) for u, v in cand])
        u, v = cand[rng.choice(len(cand), p=p / p.sum())]
        uf.union(u, v); in_t.add(v); edges.append((min(u, v), max(u, v)))
    return edges

def aco(seed=0):
    rng = np.random.default_rng(seed)
    tau = np.ones((N, N))
    ref = tree_cost(prim_mst())
    best_edges, best_cost, hist = None, np.inf, []
    for _ in range(N_ITERS):
        ants = [build_tree(tau, rng) for _ in range(N_ANTS)]
        costs = [tree_cost(e) for e in ants]
        for e in ants: assert is_valid_tree(e)
        order = np.argsort(costs)[:TOP_K]
        if costs[order[0]] < best_cost:
            best_cost, best_edges = costs[order[0]], ants[order[0]]
        # evaporação (rho = 0.2) + depósito APENAS nas arestas das melhores topologias da iteração
        for k in order:
            for u, v in ants[k]:
                tau[u, v] = tau[v, u] = np.clip((1 - RHO) * tau[u, v] + ref / costs[k], TAU_MIN, TAU_MAX)
        hist.append(best_cost)
    return best_edges, best_cost, np.array(hist)

if __name__ == "__main__":
    np.set_printoptions(linewidth=200)
    print("Matriz de latências físicas D (µs):")
    print(D)
    print("\nPares críticos (origem, destino, peso):", PAIRS)

    edges, cost, hist = aco(seed=0)
    A = np.zeros((N, N), dtype=int)
    for u, v in edges: A[u, v] = A[v, u] = 1
    print("\nMatriz de Adjacência final (10x10) do ACO:")
    print(A)
    print("\nArestas (u-v: latência):", ", ".join(f"{u}-{v}:{D[u,v]}" for u, v in sorted(edges)))
    print(f"Árvore válida: {is_valid_tree(edges)} | arestas = {len(edges)} | grau médio = {A.sum()/N:.2f}")

    rr = np.random.default_rng(123)
    rand_costs = np.array([tree_cost(random_tree(rr)) for _ in range(1000)])
    single = tree_cost(random_tree(np.random.default_rng(5)))
    mst_cost = tree_cost(prim_mst())
    sample_best = min(tree_cost(random_tree(rr)) for _ in range(N_ANTS * N_ITERS))   # mesmo nº de avaliações do ACO

    runs = np.array([aco(seed=s)[1] for s in range(20)])
    print("\nCusto = soma ponderada das latências fim-a-fim entre os pares críticos")
    print("| Topologia | Custo | Ganho do ACO |")
    print("|---|---|---|")
    g = lambda ref: f"{100*(ref-cost)/ref:.1f}%"
    print(f"| ACO (seed 0) | {cost:.1f} | — |")
    print(f"| Aleatória (1 topologia) | {single:.1f} | {g(single)} |")
    print(f"| Aleatória (média de 1000) | {rand_costs.mean():.1f} | {g(rand_costs.mean())} |")
    print(f"| Melhor de {N_ANTS*N_ITERS} aleatórias (mesmo nº de avaliações) | {sample_best:.1f} | {g(sample_best)} |")
    print(f"| MST clássica (Prim, só cabeamento) | {mst_cost:.1f} | {g(mst_cost)} |")
    print(f"\nACO em 20 sementes: média {runs.mean():.1f} ± {runs.std():.1f} | melhor {runs.min():.1f} | pior {runs.max():.1f}")
    print("Convergência (melhor custo) nas iterações 1/10/25/50/100:", [round(float(hist[i-1]), 1) for i in (1, 10, 25, 50, 100)])

    # ---- Gráficos: topologia, convergência e comparação de custos ----
    fig, ax = plt.subplots(1, 3, figsize=(16, 4.6))
    for u, v in edges:
        ax[0].plot(*zip(COORD[u], COORD[v]), color="tab:blue", lw=2)
        mid = (COORD[u] + COORD[v]) / 2
        ax[0].text(*mid, f"{D[u, v]}", fontsize=7, color="gray")
    ax[0].scatter(COORD[:, 0], COORD[:, 1], s=260, color="white", edgecolor="k", zorder=3)
    for i, (x, y) in enumerate(COORD):
        ax[0].text(x, y, str(i), ha="center", va="center", zorder=4)
    ax[0].set_title("Topologia final do ACO (rótulo = latência µs)")
    ax[1].plot(np.arange(1, N_ITERS + 1), hist, color="tab:blue")
    ax[1].axhline(mst_cost, color="tab:green", ls="--", label="MST (Prim)")
    ax[1].axhline(rand_costs.mean(), color="tab:red", ls="--", label="Aleatória (média)")
    ax[1].set_title("Convergência do ACO (seed 0)"); ax[1].set_xlabel("Iteração"); ax[1].set_ylabel("Custo")
    ax[1].grid(alpha=.3); ax[1].legend()
    labels = ["ACO", "MST", "Melhor de\n2000 aleat.", "Aleat.\n(média)"]
    vals = [cost, mst_cost, sample_best, rand_costs.mean()]
    bars = ax[2].bar(labels, vals, color=["tab:blue", "tab:green", "tab:orange", "tab:red"])
    ax[2].bar_label(bars, fmt="%.0f"); ax[2].set_title("Custo por tipo de topologia")
    plt.tight_layout(); plt.savefig("lab03_topologia.png", dpi=130)
