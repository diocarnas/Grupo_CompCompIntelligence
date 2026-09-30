"""LAB 01 - PSO contínuo para balanceamento de carga em 6 AZs."""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

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

    # ---- Gráfico: evolução do fitness por tamanho de população ----
    plt.figure(figsize=(7, 4))
    for n in (10, 30, 50):
        plt.plot(hist_mean[n], label=f"{n} partículas")
    plt.axhline(fopt, color="k", ls="--", lw=1, label=f"ótimo analítico ({fopt:.2f} °C)")
    plt.ylim(fopt - 0.5, 42)
    plt.xlabel("Iteração"); plt.ylabel("Temperatura média ponderada (°C)")
    plt.title("LAB 01 - PSO: evolução do fitness (média de 20 execuções)")
    plt.grid(alpha=.3); plt.legend(); plt.tight_layout()
    plt.savefig("lab01_fitness.png", dpi=130)
