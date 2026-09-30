# AC2 — Parte 2: Laboratório Prático de Meta-heurísticas (AULA 07)

---

## LAB 01 — ACO com Busca Local (Exploration vs. Exploitation)

**Código (`lab01_aula07.py`):**
```python
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
np.random.seed(42)

dist_matrix = np.array([
    [0, 10, 15, 20, 25],
    [10, 0, 35, 25, 30],
    [15, 35, 0, 30, 5],
    [20, 25, 30, 0, 15],
    [25, 30, 5, 15, 0]
])
num_nodes = len(dist_matrix)
num_ants = 10
num_iterations = 50
alpha, beta, rho = 1.0, 2.0, 0.1
pheromone = np.ones((num_nodes, num_nodes))
best_cost = float('inf')
best_path = None
convergence = []

def path_cost(p, m):
    return sum(m[p[i], p[i + 1]] for i in range(len(p) - 1))

def local_search_2opt(path, matrix):
    improved = True
    best_local_path = list(path)
    best_local_cost = path_cost(best_local_path, matrix)
    while improved:
        improved = False
        for i in range(1, len(best_local_path) - 2):
            for j in range(i + 1, len(best_local_path) - 1):
                new_path = best_local_path[:i] + best_local_path[i:j + 1][::-1] + best_local_path[j + 1:]
                new_cost = path_cost(new_path, matrix)
                if new_cost < best_local_cost:
                    best_local_cost, best_local_path, improved = new_cost, new_path, True
    return best_local_path, best_local_cost

for it in range(num_iterations):
    paths, costs = [], []
    for ant in range(num_ants):
        path = [0]
        unvisited = list(range(1, num_nodes))
        while unvisited:
            curr = path[-1]
            probs = np.array([(pheromone[curr][n] ** alpha) * ((1.0 / dist_matrix[curr][n]) ** beta) for n in unvisited])
            probs /= probs.sum()
            nxt = np.random.choice(unvisited, p=probs)
            path.append(nxt)
            unvisited.remove(nxt)
        path.append(0)
        path, cost = local_search_2opt(path, dist_matrix)
        paths.append(path); costs.append(cost)
        if cost < best_cost:
            best_cost, best_path = cost, path.copy()
    pheromone *= (1 - rho)
    for path, cost in zip(paths, costs):
        for i in range(len(path) - 1):
            pheromone[path[i]][path[i + 1]] += 1.0 / cost
    convergence.append(best_cost)

print(f"[LAB 01 - SUCESSO] Melhor Caminho: {[int(n) for n in best_path]} | Custo: {best_cost}")

plt.plot(convergence)
plt.xlabel("Iteração"); plt.ylabel("Melhor custo")
plt.title("Convergência do ACO Híbrido"); plt.grid()
plt.savefig("lab01_convergencia.png")
```

**Output:**
```
[LAB 01 - SUCESSO] Melhor Caminho: [0, 1, 3, 4, 2, 0] | Custo: 70
```
Gráfico de convergência: `lab01_convergencia.png`

**1 — Como a busca local 2-opt afeta o equilíbrio Exploration × Exploitation?**
As formigas constroem rotas de forma probabilística (feromônio + heurística), o que é a **exploração** do espaço. O 2-opt é aplicado a cada rota e a leva ao ótimo local mais próximo, o que é **exploitation** (refino). Com o 2-opt, o equilíbrio se desloca para a exploitation: cada formiga entrega uma solução já refinada, a convergência é mais rápida e o depósito de feromônio se concentra em rotas de boa qualidade. O custo é que a diversidade cai mais cedo e o algoritmo pode estagnar em um ótimo local. A exploração continua vindo da aleatoriedade na construção das rotas e da evaporação.

**2 — O que acontece se rho = 0.0?**
Sem evaporação, o feromônio só cresce. Rotas ruins das primeiras iterações nunca são "esquecidas", e as arestas mais depositadas dominam a probabilidade de escolha cada vez mais. A busca perde exploração e converge prematuramente (estagnação) para a primeira trilha boa encontrada, que pode ser um ótimo local. A memória do sistema deixa de ser adaptativa.

---

## LAB 02 — Algoritmo Genético (Mochila)

**Código (`lab02_aula07.py`):**
```python
import numpy as np
np.random.seed(42)

weights = np.array([12, 2, 1, 4, 1])
values = np.array([4, 2, 1, 10, 2])
max_weight = 15
pop_size = 10
num_genes = len(weights)
generations = 10
mutation_rate = 0.1

population = np.random.randint(0, 2, size=(pop_size, num_genes))

def calculate_fitness(ind):
    total_weight = np.sum(ind * weights)
    total_value = np.sum(ind * values)
    if total_weight > max_weight:
        return 0
    return total_value

def tournament_selection(pop, fitnesses):
    i, j = np.random.choice(len(pop), 2, replace=False)
    return pop[i].copy() if fitnesses[i] >= fitnesses[j] else pop[j].copy()

def crossover(parent1, parent2):
    point = np.random.randint(1, num_genes)
    child1 = np.concatenate([parent1[:point], parent2[point:]])
    child2 = np.concatenate([parent2[:point], parent1[point:]])
    return child1, child2

def mutate(ind):
    for i in range(num_genes):
        if np.random.rand() < mutation_rate:
            ind[i] = 1 - ind[i]
    return ind

for g in range(generations):
    fitnesses = np.array([calculate_fitness(ind) for ind in population])
    print(f"Geração {g:2d} | melhor fitness = {fitnesses.max():2d} | média = {fitnesses.mean():.1f}")
    new_population = []
    for _ in range(pop_size // 2):
        p1 = tournament_selection(population, fitnesses)
        p2 = tournament_selection(population, fitnesses)
        c1, c2 = crossover(p1, p2)
        new_population.extend([mutate(c1), mutate(c2)])
    population = np.array(new_population)

fitnesses = np.array([calculate_fitness(ind) for ind in population])
best = population[np.argmax(fitnesses)]
print(f"[LAB 02] Melhor indivíduo: {best} | Peso: {np.sum(best*weights)} | Valor: {fitnesses.max()}")
```

**Trechos preenchidos:**
```python
# TODO 1
if total_weight > max_weight:
    return 0
return total_value

# TODO 2
i, j = np.random.choice(len(pop), 2, replace=False)
return pop[i].copy() if fitnesses[i] >= fitnesses[j] else pop[j].copy()
```

**Output:**
```
Geração  0 | melhor fitness = 13 | média = 5.1
Geração  1 | melhor fitness = 13 | média = 7.9
Geração  2 | melhor fitness = 15 | média = 11.6
Geração  3 | melhor fitness = 15 | média = 10.8
Geração  4 | melhor fitness = 15 | média = 10.0
Geração  5 | melhor fitness = 15 | média = 9.3
Geração  6 | melhor fitness = 15 | média = 11.0
Geração  7 | melhor fitness = 15 | média = 11.8
Geração  8 | melhor fitness = 15 | média = 10.7
Geração  9 | melhor fitness = 15 | média = 12.8
[LAB 02] Melhor indivíduo: [0 1 1 1 1] | Peso: 8 | Valor: 15
```
O resultado (15) é o ótimo global: levar todos os ativos exceto o de peso 12.

**1 — Papel da mutação e taxa de 100%?**
A mutação inverte bits aleatoriamente e **introduz diversidade genética**: recupera genes perdidos e permite escapar de ótimos locais, evitando convergência prematura. Com taxa de 100%, todos os bits de todos os filhos são invertidos a cada geração, então o filho vira o **complemento** do que a seleção e o crossover produziram. A herança dos pais é destruída e o GA deixa de aprender, oscilando entre um indivíduo e seu complemento, sem convergir.

**2 — Por que penalizar o fitness com 0?**
A mochila tem uma restrição (peso ≤ 15), e o GA só "enxerga" o fitness. Sem penalização, indivíduos que estouram a capacidade (por exemplo, todos os itens, valor 19, peso 20) teriam o maior fitness e dominariam a seleção, levando a população para soluções **inviáveis**. Com fitness 0, eles perdem nos torneios e desaparecem, e a pressão seletiva empurra a população para a região viável e de alto valor.

---

## LAB 03 — PSO

**Código (`lab03_aula07.py`):**
```python
import numpy as np
np.random.seed(42)

def fitness_function(position):
    return np.sum(position**2)

num_particles, dimensions, max_iter = 10, 2, 15
X = np.random.uniform(-5, 5, (num_particles, dimensions))
V = np.random.uniform(-1, 1, (num_particles, dimensions))
pbest_X = np.copy(X)
pbest_fitness = np.array([fitness_function(p) for p in pbest_X])
gbest_index = np.argmin(pbest_fitness)
gbest_X = np.copy(pbest_X[gbest_index])
w, c1, c2 = 0.5, 1.5, 1.5

for t in range(max_iter):
    for i in range(num_particles):
        r1, r2 = np.random.rand(), np.random.rand()
        V[i] = (w * V[i]) + (c1 * r1 * (pbest_X[i] - X[i])) + (c2 * r2 * (gbest_X - X[i]))
        X[i] = X[i] + V[i]
        current_fitness = fitness_function(X[i])
        if current_fitness < pbest_fitness[i]:
            pbest_fitness[i] = current_fitness
            pbest_X[i] = X[i]
            if current_fitness < fitness_function(gbest_X):
                gbest_X = X[i].copy()  # .copy() evita que gbest seja uma "view" de X[i]
print(f"[LAB 03] Melhor posição encontrada pelo Enxame (gbest): {gbest_X}")
print(f"[LAB 03] Fitness de gbest: {fitness_function(gbest_X):.6f}")
```

**Trecho preenchido:**
```python
V[i] = (w * V[i]) + (c1 * r1 * (pbest_X[i] - X[i])) + (c2 * r2 * (gbest_X - X[i]))
```
Também corrigi um detalhe do roteiro: `gbest_X = X[i].copy()`. Sem o `.copy()`, `gbest_X` seria uma *view* de `X[i]` e mudaria junto com a partícula.

**Output:**
```
[LAB 03] Melhor posição encontrada pelo Enxame (gbest): [ 0.00742668 -0.0130891 ]
[LAB 03] Fitness de gbest: 0.000226
```
O mínimo global é (0, 0); o enxame chegou perto em 15 iterações.

**1 — O que acontece com c1 = 0?**
Desaparece a componente cognitiva (memória individual, pbest). As partículas passam a ser guiadas só pela inércia e pelo gbest (modelo *social-only*). A convergência tende a ser mais rápida, mas há menos exploração e mais risco de convergência prematura: todas correm para o mesmo ponto e, se o gbest estiver em um ótimo local, o enxame fica preso.

**2 — Função da inércia (w)?**
Controla quanto da velocidade anterior é mantido e regula o balanço entre exploração e exploitation. Um w alto (~0,9) dá passos longos e mais exploração global. Um w baixo (~0,4) dá movimento mais contido, com refino local. Uma prática comum é decair w ao longo das iterações. O termo também evita mudanças bruscas de direção e ajuda a atravessar regiões ruins.

---

## LAB 04 — ACO: Feromônio

**Código (`lab04_aula07.py`):**
```python
import numpy as np

latency_matrix = np.array([
    [0, 5, 2, 9],
    [5, 0, 3, 1],
    [2, 3, 0, 7],
    [9, 1, 7, 0]
])
num_nodes = len(latency_matrix)
pheromone = np.ones((num_nodes, num_nodes))
rho = 0.25

def update_pheromone(pheromone_matrix, paths, costs, rho):
    pheromone_matrix = (1 - rho) * pheromone_matrix
    for path, cost in zip(paths, costs):
        for i in range(len(path) - 1):
            u, v = path[i], path[i+1]
            pheromone_matrix[u][v] += 1.0 / cost
    return pheromone_matrix

mock_paths = [[0, 2, 1, 3], [0, 1, 3]]
mock_costs = [6.0, 6.0]
updated_pheromone = update_pheromone(pheromone, mock_paths, mock_costs, rho)
print("[LAB 04] Matriz de Feromônio Atualizada:\n", updated_pheromone)
```

**Trechos preenchidos:**
```python
pheromone_matrix = (1 - rho) * pheromone_matrix
...
pheromone_matrix[u][v] += 1.0 / cost
```

**Output:**
```
[LAB 04] Matriz de Feromônio Atualizada:
 [[0.75       0.91666667 0.91666667 0.75      ]
 [0.75       0.75       0.75       1.08333333]
 [0.75       0.91666667 0.75       0.75      ]
 [0.75       0.75       0.75       0.75      ]]
```
Verificação: todas as arestas vão de 1 para 0,75 pela evaporação (1 − 0,25). Cada depósito soma 1/6 ≈ 0,1667. A aresta (1→3) recebe dois depósitos, um de cada caminho: 0,75 + 0,3333 = 1,0833. As arestas (0→2), (2→1) e (0→1) recebem um depósito: 0,9167.

**1 — Por que a evaporação é necessária? O que ocorreria sem ela em grafos complexos?**
A evaporação é o mecanismo de **esquecimento**: reduz o peso de trilhas antigas ou ruins e mantém a exploração. Sem ela, o feromônio se acumula indefinidamente, as primeiras trilhas (mesmo subótimas) são reforçadas por autocatálise e dominam as escolhas, e o algoritmo estagna em ótimos locais. Em grafos complexos, com muitos caminhos possíveis, isso é ainda pior: o espaço é grande, e uma decisão precoce ruim nunca é corrigida. Os valores também crescem sem limite, o que reduz a diferença relativa entre arestas.

**2 — Relação entre latência e atratividade inicial (η)?**
A atratividade é o **inverso da latência**: η_ij = 1 / d_ij (elevada a β na regra de transição: p ∝ τ^α · η^β). Quanto menor a latência do enlace, maior a atratividade. No grafo do lab, η(1→3) = 1/1 = 1, enquanto η(0→3) = 1/9 ≈ 0,11.

---

## LAB 05 — Memético

**Código (`lab05_aula07.py`):**
```python
import numpy as np
np.random.seed(42)

def rastrigin(x):
    return 10 * len(x) + sum(x**2 - 10 * np.cos(2 * np.pi * x))

def local_search_hill_climbing(solution, step_size=0.01, max_steps=20):
    current_sol = np.copy(solution)
    current_fit = rastrigin(current_sol)
    for _ in range(max_steps):
        neighbor = current_sol + np.random.uniform(-step_size, step_size, size=len(solution))
        neighbor_fit = rastrigin(neighbor)
        if neighbor_fit < current_fit:
            current_sol, current_fit = neighbor, neighbor_fit
    return current_sol, current_fit

initial_solution = np.array([2.5, -3.1])
refined_solution, final_fit = local_search_hill_climbing(initial_solution)
print(f"[LAB 05] Solução Inicial: {initial_solution} | Fitness: {rastrigin(initial_solution):.4f}")
print(f"[LAB 05] Solução Refinada: {refined_solution} | Fitness: {final_fit:.4f}")
```

**Trecho preenchido:**
```python
neighbor = current_sol + np.random.uniform(-step_size, step_size, size=len(solution))
neighbor_fit = rastrigin(neighbor)
if neighbor_fit < current_fit:
    current_sol, current_fit = neighbor, neighbor_fit
```
(o ruído é somado à solução corrente, que é o que caracteriza o hill climbing).

**Output:**
```
[LAB 05] Solução Inicial: [ 2.5 -3.1] | Fitness: 37.7698
[LAB 05] Solução Refinada: [ 2.47553974 -3.04650038] | Fitness: 35.7154
```
A busca local melhorou o fitness, mas ficou no mesmo vale do mínimo local (perto de (3, −3), aproximadamente). Ela não escapa dos mínimos locais da Rastrigin, e é por isso que é combinada com uma meta-heurística global.

**1 — Diferença entre GA puro e Algoritmo Memético?**
O GA puro evolui a população apenas com seleção, crossover e mutação (aprendizado coletivo, evolução "genética"). O Memético (GA + busca local) acrescenta **aprendizado individual**: cada indivíduo é refinado por uma busca local (aqui, hill climbing), inspirada nos *memes* culturais que uma pessoa aprimora durante a vida. O GA faz a exploração global e a busca local faz a exploitation, o que em geral acelera a convergência e melhora a qualidade.

**2 — Custo computacional de aplicar a busca local em toda a população a cada geração?**
O custo aumenta bastante. Com população N e busca local de k avaliações, cada geração passa de ~N para ~N·(1+k) avaliações de fitness (aqui, 20 por indivíduo, cerca de 21× mais). Em troca, costuma-se precisar de menos gerações para convergir, e o que importa é o ganho líquido. Estratégias para reduzir o custo: aplicar a busca local só a uma fração da população ou só aos melhores, usar poucos passos, ou aplicá-la a cada várias gerações.
