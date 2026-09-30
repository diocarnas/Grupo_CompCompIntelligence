# AC2 — Fechamento: Otimização de Sistemas Computacionais e Resiliência de Redes (AULA 08)

---

## LAB 01 — PSO para Balanceamento Dinâmico de Carga em Datacenters

### Premissas adotadas
- Fitness = temperatura média ponderada Σ wᵢ·Cᵢ, com Cᵢ = [42, 35, 58, 30, 50, 65] °C.
- O roteiro não define a temperatura individual de cada AZ sob carga, então adotei Tᵢ = Cᵢ + 60·wᵢ². Quanto mais tráfego a AZ recebe, mais ela esquenta. Sem isso a restrição de 75 °C não atuaria e a solução seria trivial (w₄ = 1).
- Penalidade externa: 100 × Σ max(0, Tᵢ − 75). Normalização a cada iteração: clip(≥ 0) e divisão pela soma, que projeta no simplex.
- PSO: w = 0,72, c₁ = c₂ = 1,49, 100 iterações, 20 execuções por tamanho de população (seeds 0 a 19).
- Referência analítica: a AZ mais fria aceita no máximo wᵢ = √((75 − Cᵢ)/60), e o ótimo enche as AZs da mais fria para a mais quente. Resulta em W* = [0, 0,134, 0, 0,866, 0, 0], com 30,6699 °C.

### Código (`lab01_aula08.py`)
```python
"""LAB 01 - PSO contínuo para balanceamento de carga em 6 AZs."""
import numpy as np

C = np.array([42.0, 35.0, 58.0, 30.0, 50.0, 65.0])   # coeficiente de aquecimento (°C)
T_LIMIT = 75.0                                        # limite crítico (°C)
K_LOAD = 60.0                                         # aquecimento extra por carga: T_i = C_i + K*w_i^2
PENALTY = 100.0                                       # penalidade externa por °C acima do limite

def az_temps(W):
    return C + K_LOAD * W**2

def normalize(x):
    """Projeta no simplex: wi >= 0 e sum(wi) = 1."""
    x = np.clip(x, 0.0, None)
    s = x.sum()
    return np.full_like(x, 1.0 / len(x)) if s <= 1e-12 else x / s

def fitness(W):
    """Temperatura média ponderada + penalidade externa."""
    avg_temp = float(np.dot(W, C))
    excess = np.maximum(0.0, az_temps(W) - T_LIMIT)
    return avg_temp + PENALTY * excess.sum()

class PSO:
    def __init__(self, n_particles, dim=6, iters=100, w=0.72, c1=1.49, c2=1.49, seed=0):
        self.n, self.dim, self.iters = n_particles, dim, iters
        self.w, self.c1, self.c2 = w, c1, c2
        self.rng = np.random.default_rng(seed)

    def run(self):
        rng = self.rng
        X = np.array([normalize(rng.random(self.dim)) for _ in range(self.n)])
        V = rng.uniform(-0.1, 0.1, (self.n, self.dim))
        pbest_X = X.copy()
        pbest_f = np.array([fitness(x) for x in X])
        g = np.argmin(pbest_f)
        gbest_X, gbest_f = pbest_X[g].copy(), pbest_f[g]
        history = [gbest_f]
        for _ in range(self.iters):
            for i in range(self.n):
                r1, r2 = rng.random(self.dim), rng.random(self.dim)
                V[i] = (self.w * V[i] + self.c1 * r1 * (pbest_X[i] - X[i])
                        + self.c2 * r2 * (gbest_X - X[i]))
                V[i] = np.clip(V[i], -0.3, 0.3)
                X[i] = normalize(X[i] + V[i])          # normalização a cada iteração
                f = fitness(X[i])
                if f < pbest_f[i]:
                    pbest_f[i], pbest_X[i] = f, X[i].copy()
                    if f < gbest_f:
                        gbest_f, gbest_X = f, X[i].copy()
            history.append(gbest_f)
        return gbest_X, gbest_f, np.array(history)

def analytic_optimum():
    """Referência: preenche as AZs mais frias até o teto w_i <= sqrt((75-C_i)/K)."""
    cap = np.sqrt((T_LIMIT - C) / K_LOAD)
    W, left = np.zeros(6), 1.0
    for i in np.argsort(C):
        W[i] = min(cap[i], left); left -= W[i]
    return W, float(np.dot(W, C))

if __name__ == "__main__":
    N_RUNS, SHOW = 20, [0, 5, 10, 25, 50, 100]
    Wopt, fopt = analytic_optimum()
    print(f"Referência analítica: W* = {np.round(Wopt, 4)} | temp. média = {fopt:.4f} °C\n")
    hist_mean, results = {}, {}
    for n in (10, 30, 50):
        runs = [PSO(n, seed=s).run() for s in range(N_RUNS)]
        finals = np.array([r[1] for r in runs])
        hist_mean[n] = np.mean([r[2] for r in runs], axis=0)
        best = runs[int(np.argmin(finals))]
        results[n] = (best, finals)

    print("Evolução do fitness (média de 20 execuções, menor = melhor)")
    print("| Iteração | " + " | ".join(f"{n} partículas" for n in (10, 30, 50)) + " |")
    print("|---|---|---|---|")
    for it in SHOW:
        print(f"| {it} | " + " | ".join(f"{hist_mean[n][it]:.4f}" for n in (10, 30, 50)) + " |")

    print("\nMelhor distribuição W por população (melhor das 20 execuções)")
    print("| Partículas | w1 | w2 | w3 | w4 | w5 | w6 | sum(wi) | Temp. média (°C) | T_AZ máx (°C) | Média±dp (20 exec.) |")
    print("|---|---|---|---|---|---|---|---|---|---|---|")
    for n in (10, 30, 50):
        (W, f, _), finals = results[n]
        ws = " | ".join(f"{x:.4f}" for x in W)
        print(f"| {n} | {ws} | {W.sum():.12f} | {np.dot(W, C):.4f} | {az_temps(W).max():.2f} | {finals.mean():.4f} ± {finals.std():.4f} |")
```

### Output da execução
```
Referência analítica: W* = [0.    0.134 0.    0.866 0.    0.   ] | temp. média = 30.6699 °C

Evolução do fitness (média de 20 execuções, menor = melhor)
| Iteração | 10 partículas | 30 partículas | 50 partículas |
|---|---|---|---|
| 0 | 40.6548 | 39.9539 | 39.5284 |
| 5 | 31.9792 | 30.7983 | 30.7110 |
| 10 | 30.9875 | 30.7129 | 30.6716 |
| 25 | 30.8150 | 30.6701 | 30.6700 |
| 50 | 30.8106 | 30.6699 | 30.6699 |
| 100 | 30.8105 | 30.6699 | 30.6699 |

Melhor distribuição W por população (melhor das 20 execuções)
| Partículas | w1 | w2 | w3 | w4 | w5 | w6 | sum(wi) | Temp. média (°C) | T_AZ máx (°C) | Média±dp (20 exec.) |
|---|---|---|---|---|---|---|---|---|---|---|
| 10 | 0.0000 | 0.1340 | 0.0000 | 0.8660 | 0.0000 | 0.0000 | 1.000000000000 | 30.6699 | 75.00 | 30.8105 ± 0.3349 |
| 30 | 0.0000 | 0.1340 | 0.0000 | 0.8660 | 0.0000 | 0.0000 | 1.000000000000 | 30.6699 | 75.00 | 30.6699 ± 0.0000 |
| 50 | 0.0000 | 0.1340 | 0.0000 | 0.8660 | 0.0000 | 0.0000 | 1.000000000000 | 30.6699 | 75.00 | 30.6699 ± 0.0000 |
```

### Análise técnica
- **Validade:** nas três populações, sum(wᵢ) = 1,000000000000 e nenhuma AZ passou de 75 °C (máximo = 75,00 °C, no limite da restrição).
- **Qualidade:** as três populações acharam o ótimo analítico (30,6699 °C). O ótimo fica na fronteira da restrição: a AZ 4 (30 °C) satura em 0,866 porque, com carga total, chegaria a 90 °C. O excedente vai para a AZ 2 (35 °C), a segunda mais fria.
- **Efeito do tamanho do enxame:** com 10 partículas, a média das 20 execuções foi 30,8105 ± 0,3349, ou seja, algumas execuções ficaram presas em pontos subótimos. Com 30 e 50 partículas, as 20 execuções chegaram ao ótimo (desvio 0,0000). Com 10 partículas a exploração é menor e a convergência prematura é mais provável.
- **Velocidade:** 50 partículas chegam a 30,6716 na iteração 10. Com 30 são necessárias cerca de 25 iterações para o mesmo patamar. Mais partículas custam mais avaliações por iteração, e 30 já foi suficiente, então o ganho de 30 para 50 é marginal.
- **Ressalva:** o modelo térmico Tᵢ = Cᵢ + 60·wᵢ² é uma premissa minha, e os números dependem dele. A estrutura do PSO não depende.

---
## LAB 02 — AG Binário com Reparação/Penalidade para Seleção de Microsserviços em Edge

### Premissas adotadas
- O roteiro não fornece os dados, então defini 15 serviços (valor, RAM, CPU) fixos no código. A soma é 60 GB de RAM e 29 cores, contra limites de 16 GB e 8 cores. As restrições são apertadas.
- Estratégia A: fitness = 0 se violar RAM ou CPU. Estratégia B: fitness = max(0, valor − 20·GB_excedido − 30·cores_excedidos).
- AG: população 50, 100 gerações, torneio k = 3, crossover de ponto único (pc = 0,9), mutação por bit (pm = 0,05), sem elitismo, 30 execuções por estratégia.
- Diversidade = distância de Hamming média normalizada entre todos os pares (0,5 = população aleatória, 0 = clones).
- Validação: força bruta sobre os 2¹⁵ subconjuntos. Ótimo global = 245 (S1, S2, S11, S14, S15; 16 GB, 8 cores).

### Código (`lab02_aula08.py`)
```python
"""LAB 02 - AG binário: penalidade rígida (A) x proporcional (B) para microsserviços em Edge."""
import numpy as np
from itertools import product

VALUE = np.array([60, 45, 80, 30, 55, 70, 25, 90, 40, 65, 35, 50, 75, 20, 85])
RAM   = np.array([ 4,  3,  6,  2,  4,  5,  2,  7,  3,  5,  2,  4,  6,  1,  6])
CPU   = np.array([ 2,  1,  3,  1,  2,  2,  1,  3,  1,  2,  1,  2,  3,  1,  3])
MAX_RAM, MAX_CPU = 16, 8
N = len(VALUE)
LAMBDA_RAM, LAMBDA_CPU = 20.0, 30.0    # penalidade por GB / core excedido (Estratégia B)

def excess(ind):
    return max(0, ind @ RAM - MAX_RAM), max(0, ind @ CPU - MAX_CPU)

def feasible(ind):
    return excess(ind) == (0, 0)

def fitness_A(ind):
    return float(ind @ VALUE) if feasible(ind) else 0.0

def fitness_B(ind):
    er, ec = excess(ind)
    return max(0.0, float(ind @ VALUE) - LAMBDA_RAM * er - LAMBDA_CPU * ec)

def tournament(pop, fit, rng, k=3):
    idx = rng.choice(len(pop), k, replace=False)
    return pop[idx[np.argmax(fit[idx])]].copy()

def crossover(p1, p2, rng, pc=0.9):
    if rng.random() < pc:
        pt = rng.integers(1, N)
        return (np.concatenate([p1[:pt], p2[pt:]]), np.concatenate([p2[:pt], p1[pt:]]))
    return p1.copy(), p2.copy()

def mutate(ind, rng, pm=0.05):
    flip = rng.random(N) < pm
    ind[flip] = 1 - ind[flip]
    return ind

def diversity(pop):
    """Distância de Hamming média normalizada entre pares (0 = clones, ~0.5 = aleatório)."""
    P = len(pop)
    d = (pop[:, None, :] != pop[None, :, :]).sum(axis=2)
    return d.sum() / (P * (P - 1)) / N

def run(fit_fn, seed, pop_size=50, gens=100):
    rng = np.random.default_rng(seed)
    pop = rng.integers(0, 2, (pop_size, N))
    stats = []
    best_ind, best_val = None, -1
    for _ in range(gens + 1):
        fit = np.array([fit_fn(i) for i in pop])
        feas = np.array([feasible(i) for i in pop])
        stats.append((fit.mean(), fit.std(), diversity(pop), feas.mean()))
        for i in np.where(feas)[0]:                      # melhor solução VIÁVEL já vista
            v = pop[i] @ VALUE
            if v > best_val:
                best_val, best_ind = v, pop[i].copy()
        new = []
        while len(new) < pop_size:
            c1, c2 = crossover(tournament(pop, fit, rng), tournament(pop, fit, rng), rng)
            new += [mutate(c1, rng), mutate(c2, rng)]
        pop = np.array(new[:pop_size])
    return np.array(stats), best_ind, best_val

def brute_force():
    best, arg = -1, None
    for bits in product([0, 1], repeat=N):
        b = np.array(bits)
        if feasible(b) and b @ VALUE > best:
            best, arg = b @ VALUE, b
    return best, arg

if __name__ == "__main__":
    N_RUNS, SHOW = 30, [0, 5, 10, 20, 40, 60, 80, 100]
    opt, opt_ind = brute_force()
    svc = lambda ind: ", ".join(f"S{i+1}" for i in np.where(ind)[0])
    print(f"Ótimo global (força bruta, 2^15): valor = {opt} | {svc(opt_ind)} | RAM = {opt_ind@RAM} GB | CPU = {opt_ind@CPU}\n")

    res = {}
    for name, fn in (("A", fitness_A), ("B", fitness_B)):
        runs = [run(fn, s) for s in range(N_RUNS)]
        res[name] = dict(stats=np.mean([r[0] for r in runs], axis=0),
                         vals=np.array([r[2] for r in runs]),
                         inds=[r[1] for r in runs])

    print("Fitness da população por geração (média das 30 execuções; média ± desvio-padrão dentro da população)")
    print("| Geração | A: média | A: desvio | B: média | B: desvio |")
    print("|---|---|---|---|---|")
    for g in SHOW:
        a, b = res["A"]["stats"][g], res["B"]["stats"][g]
        print(f"| {g} | {a[0]:.2f} | {a[1]:.2f} | {b[0]:.2f} | {b[1]:.2f} |")

    print("\nDiversidade genética (Hamming médio normalizado) e % de indivíduos viáveis")
    print("| Geração | A: diversidade | B: diversidade | A: % viáveis | B: % viáveis |")
    print("|---|---|---|---|---|")
    for g in SHOW:
        a, b = res["A"]["stats"][g], res["B"]["stats"][g]
        print(f"| {g} | {a[2]:.3f} | {b[2]:.3f} | {100*a[3]:.1f}% | {100*b[3]:.1f}% |")

    print("\nMelhor combinação final (30 execuções)")
    print("| Estratégia | Melhor valor | Média±dp dos melhores | Execuções que acharam o ótimo | Melhor combinação | RAM | CPU |")
    print("|---|---|---|---|---|---|---|")
    for name in ("A", "B"):
        v, inds = res[name]["vals"], res[name]["inds"]
        bi = inds[int(np.argmax(v))]
        print(f"| {name} | {v.max():.0f} | {v.mean():.1f} ± {v.std():.1f} | {(v == opt).sum()}/{N_RUNS} | {svc(bi)} | {bi@RAM} | {bi@CPU} |")
```

### Output da execução
```
Ótimo global (força bruta, 2^15): valor = 245 | S1, S2, S11, S14, S15 | RAM = 16 GB | CPU = 8

Fitness da população por geração (média das 30 execuções; média ± desvio-padrão dentro da população)
| Geração | A: média | A: desvio | B: média | B: desvio |
|---|---|---|---|---|
| 0 | 7.90 | 34.68 | 38.62 | 62.75 |
| 5 | 83.43 | 85.33 | 160.09 | 61.48 |
| 10 | 109.27 | 91.52 | 167.49 | 59.08 |
| 20 | 113.83 | 96.36 | 176.28 | 58.79 |
| 40 | 116.62 | 98.87 | 184.48 | 54.01 |
| 60 | 120.92 | 101.14 | 185.21 | 56.62 |
| 80 | 126.20 | 101.85 | 189.10 | 54.44 |
| 100 | 120.23 | 102.07 | 182.84 | 58.74 |

Diversidade genética (Hamming médio normalizado) e % de indivíduos viáveis
| Geração | A: diversidade | B: diversidade | A: % viáveis | B: % viáveis |
|---|---|---|---|---|
| 0 | 0.500 | 0.500 | 4.3% | 4.3% |
| 5 | 0.385 | 0.372 | 48.4% | 45.1% |
| 10 | 0.325 | 0.326 | 61.3% | 43.3% |
| 20 | 0.303 | 0.283 | 60.7% | 42.6% |
| 40 | 0.257 | 0.228 | 59.7% | 46.3% |
| 60 | 0.249 | 0.213 | 60.3% | 44.7% |
| 80 | 0.228 | 0.199 | 61.7% | 50.7% |
| 100 | 0.220 | 0.204 | 59.8% | 45.3% |

Melhor combinação final (30 execuções)
| Estratégia | Melhor valor | Média±dp dos melhores | Execuções que acharam o ótimo | Melhor combinação | RAM | CPU |
|---|---|---|---|---|---|---|
| A | 245 | 243.7 ± 2.2 | 22/30 | S1, S2, S4, S5, S11, S14 | 16 | 8 |
| B | 245 | 244.5 ± 1.5 | 27/30 | S1, S2, S4, S5, S11, S14 | 16 | 8 |
```

### Análise técnica
- **Fitness médio e desvio:** em todas as gerações a Estratégia B tem fitness médio maior (≈ 183 contra ≈ 120 na geração 100) e desvio-padrão menor (≈ 55 a 60 contra ≈ 100). Na A, a população inicial é 95,7 % inviável e quase todos os fitness são 0 (média 7,9), então a seleção é praticamente aleatória nas primeiras gerações. Na B, os inviáveis têm fitness parcial que guia a busca. Os números incluem indivíduos inviáveis, por isso a média da A é baixa: cerca de 40 % da população continua sendo 0.
- **Diversidade:** as duas estratégias perdem diversidade de forma parecida (0,50 → ≈ 0,21). A Estratégia A preservou um pouco mais (0,220 contra 0,204 na geração 100, e 0,249 contra 0,213 na 60). Esta vantagem é pequena; por isso não afirmo que a A seja claramente melhor nesse critério. A explicação plausível é que os indivíduos de fitness 0 não exercem pressão seletiva entre si, o que mantém mais variedade. Já a B empurra a população mais cedo para perto da fronteira viável (≈ 45 % viáveis contra ≈ 60 % da A, então ela mantém muitos indivíduos levemente inviáveis sob pressão).
- **Melhor combinação final:** ambas acharam o ótimo global (245). A B chegou nele em 27 das 30 execuções (média dos melhores 244,5 ± 1,5), e a A em 22 das 30 (243,7 ± 2,2). A melhor combinação registrada por ambas foi S1, S2, S4, S5, S11, S14 (valor 245, 16 GB, 8 cores), um ótimo alternativo com o mesmo valor do encontrado por força bruta. Logo há empate no melhor valor, e a B é mais confiável.
- **Conclusão:** a penalidade proporcional (B) encontrou o ótimo com mais consistência, porque dá gradiente à busca onde a rígida (A) tem um platô de zeros. A rígida preservou um pouco mais de diversidade genética, mas a diferença é pequena neste experimento. Os pesos de penalidade (20 e 30) foram escolhidos por mim e não foram ajustados; penalidades muito baixas fariam a B aceitar soluções inviáveis como melhores, por isso o código guarda apenas a melhor solução viável.

---
## LAB 03 — ACO para Projeto de Topologia de Rede de Baixa Latência

### Premissas adotadas
- O roteiro não fornece a matriz D nem os "pares mais críticos", então gerei D com seed fixa a partir de posições aleatórias dos 10 switches (latência física em µs, simétrica) e sorteei 12 pares críticos com pesos de tráfego de 1 a 5 (listados no output).
- Custo da topologia = Σ peso × latência fim-a-fim pelo caminho único da árvore entre cada par crítico. Assim a estrutura importa, e não apenas a soma das arestas (que seria o MST clássico).
- ACO: 20 formigas, 100 iterações, α = 1, β = 2 (η = 1/D), ρ = 0,2. Cada formiga parte de um nó e escolhe arestas (nó da árvore → nó fora dela). Um Union-Find descarta arestas que fechariam ciclo, e `is_valid_tree` confere N−1 arestas, sem ciclo e conectado em cada árvore construída.
- Feromônio: só as arestas das 3 melhores topologias da iteração são atualizadas: τ ← (1 − ρ)·τ + custo_MST/custo, com limites [0,05; 10]. As demais arestas não evaporam, conforme o roteiro, e os limites evitam estagnação.

### Código (`lab03_aula08.py`)
```python
"""LAB 03 - ACO para topologia em árvore geradora de 10 switches (baixa latência)."""
import numpy as np
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
```

### Output da execução
```
Matriz de latências físicas D (µs):
[[ 0.  34.4 16.3 31.2 23.1 34.9 29.2 18.2 19.2  4.6]
 [34.4  0.  40.2 48.7 12.2 23.8 28.3 21.3 30.4 39. ]
 [16.3 40.2  0.  15.  32.1 29.8 21.5 19.  35.  17.1]
 [31.2 48.7 15.   0.  43.4 31.  22.6 28.3 49.5 32. ]
 [23.1 12.2 32.1 43.4  0.  26.5 27.1 15.2 19.  27.5]
 [34.9 23.8 29.8 31.  26.5  0.   8.7 17.  43.1 38.9]
 [29.2 28.3 21.5 22.6 27.1  8.7  0.  13.6 40.9 32.8]
 [18.2 21.3 19.  28.3 15.2 17.  13.6  0.  27.3 22.6]
 [19.2 30.4 35.  49.5 19.  43.1 40.9 27.3  0.  21.1]
 [ 4.6 39.  17.1 32.  27.5 38.9 32.8 22.6 21.1  0. ]]

Pares críticos (origem, destino, peso): [(0, 2, 2), (1, 8, 5), (0, 6, 1), (0, 8, 1), (0, 7, 1), (4, 5, 5), (4, 7, 4), (0, 5, 5), (7, 8, 2), (2, 4, 4), (2, 9, 2), (8, 9, 3)]

Matriz de Adjacência final (10x10) do ACO:
[[0 0 1 0 0 0 0 1 1 1]
 [0 0 0 0 0 0 0 0 1 0]
 [1 0 0 1 0 0 0 0 0 0]
 [0 0 1 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0 1 0 0]
 [0 0 0 0 0 0 0 1 0 0]
 [0 0 0 0 0 0 0 1 0 0]
 [1 0 0 0 1 1 1 0 0 0]
 [1 1 0 0 0 0 0 0 0 0]
 [1 0 0 0 0 0 0 0 0 0]]

Arestas (u-v: latência): 0-2:16.3, 0-7:18.2, 0-8:19.2, 0-9:4.6, 1-8:30.4, 2-3:15.0, 4-7:15.2, 5-7:17.0, 6-7:13.6
Árvore válida: True | arestas = 9 | grau médio = 1.80

Custo = soma ponderada das latências fim-a-fim entre os pares críticos
| Topologia | Custo | Ganho do ACO |
|---|---|---|
| ACO (seed 0) | 1038.4 | — |
| Aleatória (1 topologia) | 2407.0 | 56.9% |
| Aleatória (média de 1000) | 2548.7 | 59.3% |
| Melhor de 2000 aleatórias (mesmo nº de avaliações) | 1299.8 | 20.1% |
| MST clássica (Prim, só cabeamento) | 1221.8 | 15.0% |

ACO em 20 sementes: média 1082.6 ± 39.8 | melhor 1038.4 | pior 1166.2
Convergência (melhor custo) nas iterações 1/10/25/50/100: [1307.3, 1204.4, 1091.9, 1091.9, 1038.4]
```

### Análise técnica
- **Topologia final:** árvore válida (9 arestas, sem ciclos, conexa). A matriz de adjacência está no output. O switch 7 funciona como hub (grau 4, ligado a 0, 4, 5 e 6), e o 0 também tem grau 4. A rede é mais "estrelada" que um MST, porque o custo depende de caminhos entre pares críticos.
- **Ganho de latência:** 56,9 % contra uma topologia aleatória específica (2407,0) e 59,3 % contra a média de 1000 topologias aleatórias (2548,7). O custo do ACO foi 1038,4.
- **Comparação justa:** contra a melhor de 2000 topologias aleatórias (mesmo número de avaliações do ACO), o ganho cai para 20,1 %. Contra o MST clássico (Prim), que só minimiza o cabeamento, é 15,0 %. Ou seja, parte do ganho contra a topologia aleatória é apenas "não ser aleatório", e o ganho contra as bases mais fortes é bem menor, mas continua positivo.
- **Robustez:** em 20 sementes, o ACO teve média 1082,6 ± 39,8 (melhor 1038,4, pior 1166,2). Todas ficaram abaixo do MST (1221,8). A convergência na seed 0 foi de 1307 (iteração 1) para 1204 (10), 1092 (25) e 1038 (100), com o último salto tardio, o que indica que mais iterações ainda poderiam ajudar.
- **Limitação:** não tenho o ótimo exato deste problema (árvore de custo mínimo de roteamento é NP-difícil), então não dá para dizer quão perto do ótimo o ACO ficou.

---
