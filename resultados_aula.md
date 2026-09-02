# AC-2 Parte 1 — Resultados e Relatório Final (PSO)

**Cenário:** posicionar 5 centros de distribuição para minimizar o custo total de entrega
(distância × demanda) para 50 clientes, usando Particle Swarm Optimization (PSO).

---

## Missão 1 — A Partícula Solitária

`f(x) = x²`, domínio `x ∈ [-10, 10]`, 20 iterações, `w=0.8, c1=1.5, c2=1.5`.

- Posição inicial: `x = 2.7885` (fitness `7.7759`)
- Posição final: `x = -0.0273` (fitness `0.000744`)
- Erro final em relação ao ótimo (`x=0`): `0.0273`
- A partícula já fica com erro < 0.03 desde a iteração 6.

**A partícula encontrou o mínimo?** Sim (ficou muito próxima de `x=0`, com fitness praticamente zero).

## Missão 2 — O Enxame de Partículas

Função de Rosenbrock `f(x,y) = (1-x)² + 100(y-x²)²`, ótimo em `(1,1)`.
20 partículas, 50 iterações, `w=0.7, c1=1.8, c2=1.8`.

- Fitness inicial do enxame: `3.363231`
- Fitness final: `0.000348`
- Posição final: `(1.0111, 1.0208)` — muito próxima do ótimo `(1,1)`

**O enxame encontrou o mínimo global?** Sim, com alta precisão.
**Foi mais rápido/melhor que a Missão 1?** Não é diretamente comparável (funções diferentes),
mas o enxame resolveu um problema 2D bem mais difícil (Rosenbrock tem um "vale" estreito e
curvo, clássico desafio para otimizadores) e ainda assim convergiu de forma consistente,
mostrando o ganho de robustez de ter várias partículas cooperando via `gBest`.

## Missão 3 — O Problema Corporativo (Otimização Logística)

50 clientes, 5 centros, 30 partículas, 100 iterações, `w=0.7, c1=1.8, c2=1.8`.

> **Bug de sinal corrigido:** o enunciado sugeria `fitness = -custo_total`, mas o algoritmo
> sempre minimiza `fitness` (`if fitness < pBest_fit`). Com o sinal negativo, o PSO na prática
> **maximizava** o custo (testado: os 5 centros colapsavam nos cantos do mapa, custo final
> `16955.05`, pior que um único centro central). A correção foi fazer `fitness` retornar o
> `custo_total` positivo diretamente.

Resultado após a correção:

- Custo inicial de referência (1 único centro no centroide dos 50 clientes): `10429.49`
- Custo total final (PSO, 5 centros): `3514.93`
- **Melhoria: 66,3%**
- Tempo de execução: `0.70 s`

Centros de distribuição encontrados:

| Centro | X | Y |
|---|---|---|
| 1 | 2.70 | 5.32 |
| 2 | 0.59 | 8.65 |
| 3 | 5.47 | 1.76 |
| 4 | 0.90 | 1.94 |
| 5 | 7.74 | 6.12 |

**O custo melhorou em relação ao inicial?** Sim, 66,3% de redução.
**Quantos centros foram alocados?** 5 (conforme o enunciado).

## Missão 4 — Otimização de Parâmetros

Mesmo problema logístico, 6 configurações testadas (5 execuções cada, média/desvio-padrão):

| Experimento | Custo Médio | Melhor Custo | Pior Custo |
|---|---|---|---|
| Padrão (w=0.7, c1=1.8, c2=1.8, 30 partículas) | 3638.88 | 3547.08 | 3712.66 |
| Inércia Alta (w=0.9) | 3951.15 | 3772.40 | 4145.73 |
| Inércia Baixa (w=0.5) | 3647.04 | 3514.29 | 3797.89 |
| Cognitivo Alto (c1=2.5) | 3750.04 | 3671.45 | 3808.38 |
| Social Alto (c2=2.5) | 3952.36 | 3890.59 | 4051.99 |
| **Mais Partículas (60)** | **3635.02** | 3523.28 | 3677.28 |

**Melhor configuração:** Mais Partículas (custo médio `3635.02`)
**Pior configuração:** Social Alto (custo médio `3952.36`)

---

## PARTE 1: O que você aprendeu?

**1. Explique com suas palavras o que é o PSO e como ele funciona.**

O PSO (Particle Swarm Optimization / Otimização por Enxame de Partículas) é um algoritmo de
otimização inspirado no comportamento coletivo de bandos de pássaros ou cardumes de peixes. Em vez
de usar seleção natural, cruzamento e mutação (como os Algoritmos Genéticos), o PSO mantém um
conjunto fixo de "partículas" que nunca morrem nem se reproduzem: elas simplesmente se movem
continuamente pelo espaço de busca, ajustando sua velocidade a cada iteração. Essa velocidade é
resultado de três forças combinadas: a inércia (tendência de manter a direção atual), o componente
cognitivo (atração pela melhor posição que a própria partícula já visitou, `pBest`) e o componente
social (atração pela melhor posição encontrada por qualquer partícula do enxame, `gBest`). Repetindo
esse processo — avaliar, atualizar velocidade, atualizar posição — por várias iterações, o enxame
inteiro converge gradualmente para (ou perto de) a melhor solução do espaço de busca.

**2. Qual a diferença entre pBest e gBest? Por que ambos são importantes?**

`pBest` é a melhor posição que uma partícula individual já visitou por conta própria — representa a
"experiência pessoal" dela. `gBest` é a melhor posição encontrada por qualquer partícula em todo o
enxame — representa o "conhecimento coletivo" do grupo. Os dois são importantes porque equilibram
exploração e explotação: se só existisse `pBest`, cada partícula otimizaria isoladamente, sem
aproveitar descobertas de outras partículas (convergência lenta, redundância de esforço). Se só
existisse `gBest`, todas as partículas seriam atraídas cedo demais para um único ponto, perdendo
diversidade e arriscando ficar presas em mínimos locais. A combinação das duas informações é o que
faz o "inteligência coletiva" do PSO funcionar: cada partícula aprende com sua própria experiência
sem abrir mão do que o grupo já descobriu.

## PARTE 2: Experiência com as missões

**Missão 1 — A Partícula Solitária:**
- A partícula encontrou o mínimo? **(x) Sim ( ) Não**
- Quantas iterações foram necessárias? **~6 iterações** para erro < 0.03 (das 20 rodadas)
- Dificuldade: **( ) Fácil (x) Médio ( ) Difícil** — a lógica é simples, mas exige atenção ao
  fato de que `pBest = gBest` neste caso (só uma partícula).

**Missão 2 — O Enxame:**
- O enxame encontrou o mínimo global? **(x) Sim ( ) Não**
- Comparado à Missão 1, o enxame foi "mais rápido"? **(x) Sim ( ) Não** — resolveu um problema
  bem mais difícil (Rosenbrock 2D, com vale estreito e curvo) com alta precisão em poucas
  iterações, graças à cooperação via `gBest`.
- Dificuldade: **( ) Fácil (x) Médio ( ) Difícil** — vetorizar as fórmulas para 2D com NumPy
  exige cuidado extra em relação à versão 1D.

**Missão 3 — Problema Corporativo:**
- Custo melhorou em relação ao inicial? **(x) Sim ( ) Não** — melhoria de 66,3%
- Quantos centros foram alocados? **5**
- Dificuldade: **( ) Fácil ( ) Médio (x) Difícil** — o bug de sinal na função fitness
  (`-custo_total` vs. `custo_total`) foi a parte mais traiçoeira: o código "rodava" sem erros,
  mas otimizava na direção errada, e só foi perceptível comparando o resultado do PSO com um
  baseline simples (um único centro no centroide).

**Missão 4 — Otimização de Parâmetros:**
- Melhor configuração encontrada: **w=0.7, c1=1.8, c2=1.8, partículas=60**
- Pior configuração encontrada: **w=0.7, c1=1.8, c2=2.5, partículas=30** (Social Alto)
- Dificuldade: **( ) Fácil (x) Médio ( ) Difícil** — o código em si já estava pronto, mas
  interpretar os resultados exige entender o papel de cada parâmetro.

---

## Efeito observado dos parâmetros (Missão 4)

- **Inércia (w):** aumentar `w` para `0.9` piorou bastante o resultado (custo médio subiu de
  `3638.88` para `3951.15`) — inércia alta faz as partículas "resistirem" mais a mudar de
  direção, dificultando a convergência fina perto do ótimo. Reduzir para `0.5` teve efeito
  pequeno e levemente positivo neste problema.
- **Cognitivo (c1):** aumentar para `2.5` piorou o resultado (`3750.04` vs `3638.88`) — peso
  cognitivo excessivo faz cada partícula "teimar" demais em seguir sua própria melhor posição,
  reduzindo a cooperação do grupo.
- **Social (c2):** aumentar para `2.5` foi o pior resultado de todos (`3952.36`) — peso social
  excessivo faz o enxame convergir cedo demais para a região do `gBest` atual, perdendo
  diversidade e ficando preso em mínimos locais antes de explorar o espaço adequadamente.
- **Número de partículas:** dobrar de 30 para 60 partículas trouxe a melhor média (`3635.02`) e o
  menor desvio-padrão relativo, à custa de dobrar o tempo de computação por iteração — mais
  partículas exploram mais pontos do espaço simultaneamente, reduzindo a chance de ficar preso em
  um mínimo local ruim.

## 4. Qual configuração você recomenda para este problema? Por quê?

Recomendo a configuração **"Mais Partículas" (w=0.7, c1=1.8, c2=1.8, 60 partículas)**, pois obteve
o melhor custo médio (`3635.02`) e um dos menores desvios-padrão entre as execuções — ou seja, além
de encontrar boas soluções, é mais consistente/confiável de uma execução para outra. O custo
computacional extra (mais partículas) é aceitável neste problema de porte pequeno/médio (10
dimensões, 100 iterações rodam em menos de 1 segundo), então o ganho em qualidade de solução
compensa. Caso o tempo de execução fosse uma restrição real (problema em escala muito maior), a
configuração **Padrão** seria uma alternativa quase tão boa (`3638.88`) com metade do custo
computacional.

---

## Arquivos entregues

- `AC2_PSO_missoes.ipynb` — notebook com as 4 missões, código, saídas e gráficos
- `resultados_aula.md` — este relatório
