"""LAB 02 - AG binário: penalidade rígida (A) x proporcional (B) para microsserviços em Edge."""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
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

    # ---- Gráficos: fitness médio±desvio, diversidade e % viáveis ----
    g = np.arange(res["A"]["stats"].shape[0])
    fig, ax = plt.subplots(1, 3, figsize=(15, 4))
    for name, color in (("A", "tab:red"), ("B", "tab:blue")):
        s = res[name]["stats"]
        ax[0].plot(g, s[:, 0], color=color, label=f"Estratégia {name}")
        ax[0].fill_between(g, s[:, 0] - s[:, 1], s[:, 0] + s[:, 1], color=color, alpha=.15)
        ax[1].plot(g, s[:, 2], color=color, label=f"Estratégia {name}")
        ax[2].plot(g, 100 * s[:, 3], color=color, label=f"Estratégia {name}")
    ax[0].set_title("Fitness da população (média ± desvio)"); ax[0].set_ylabel("Fitness")
    ax[1].set_title("Diversidade genética (Hamming normalizado)")
    ax[2].set_title("% de indivíduos viáveis")
    for a in ax:
        a.set_xlabel("Geração"); a.grid(alpha=.3); a.legend()
    plt.tight_layout(); plt.savefig("lab02_estrategias.png", dpi=130)
