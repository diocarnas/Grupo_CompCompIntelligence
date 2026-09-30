# Resultados — Aula 06 (ACO)

## Lab 01 — ACO: Otimização por Colônia de Formigas

### Output
```
Matriz inicial de feromônio:
[[1. 1. 1. 0. 0. 0.]
 [1. 1. 1. 1. 0. 0.]
 [1. 1. 1. 1. 1. 0.]
 [0. 1. 1. 1. 1. 1.]
 [0. 0. 1. 1. 1. 1.]
 [0. 0. 0. 1. 1. 1.]]
Vizinhos do nó 0: [1, 2]
Vizinhos do nó 2: [0, 1, 3, 4]

Rotas encontradas:
Formiga 1: [0, 1, 2, 3, 4, 5]
Formiga 2: [0, 1, 2, 3, 4, 5]
Formiga 3: [0, 1, 2, 3, 4, 5]
Formiga 4: [0, 1, 2, 3, 4, 5]
Formiga 5: [0, 2, 1, 3, 4, 5]

Rota: [0, 1, 2, 3, 4, 5]
Custo: 8.0

========== RESULTADO ==========
Melhor rota encontrada: [0, 1, 2, 3, 4, 5]
Melhor custo: 8.0

Matriz final de feromônio:
[[  0. 500.   0.   0.   0.   0.]
 [  0.   0. 500.   0.   0.   0.]
 [  0.   0.   0. 500.   0.   0.]
 [  0.   0.   0.   0. 500.   0.]
 [  0.   0.   0.   0.   0. 500.]
 [  0.   0.   0.   0.   0.   0.]]
Histórico (primeiras 5 iterações): [8.0, 8.0, 8.0, 8.0, 8.0]
```

Gráficos gerados: `lab01_convergencia.png` (curva de convergência) e `lab01_feromonio.png` (matriz final de feromônio).

**Observações:** a melhor rota foi [0, 1, 2, 3, 4, 5], com custo 8. A curva de convergência é uma reta em 8: como a rede é pequena, já na 1ª iteração alguma das 20 formigas achou a rota ótima. No mapa de feromônio, toda a concentração ficou exatamente nas conexões 0→1, 1→2, 2→3, 3→4 e 4→5 (as demais zeraram pela evaporação).

### Respostas

**1. Por que várias formigas?**
Como a escolha do próximo nó é probabilística, uma única formiga percorreria só um caminho por iteração e poderia ficar presa numa rota ruim. Com várias formigas, muitos caminhos diferentes são testados em paralelo, e a comparação entre seus custos é o que permite saber quais são melhores. Além disso, o feromônio é a "memória coletiva": quanto mais formigas, mais informação chega a essa memória. Explorar caminhos diferentes evita ficar preso em soluções medianas e permite descobrir rotas melhores que a mais óbvia.

**2. Por que rota de menor custo recebe mais feromônio?**
O depósito é `Q / custo`: custo menor gera depósito maior (ex.: custo 8 → 12,5 por enlace; custo 10 → 10). Assim, as arestas das boas rotas ficam mais fortes, aumentando a atratividade (`feromônio^ALPHA × (1/custo)^BETA`) e a probabilidade de as próximas formigas as escolherem. Isso cria um ciclo de reforço: boa rota → mais feromônio → mais formigas passam por ela → solução refinada.

**3. E sem evaporação?**
O feromônio só cresceria e as primeiras rotas encontradas, mesmo medíocres, acumulariam vantagem e dominariam as escolhas para sempre (convergência prematura / estagnação). Caminhos melhores descobertos depois teriam dificuldade de competir com trilhas já muito reforçadas. A evaporação "esquece" informações antigas e mantém a busca aberta a novas experiências.

---

## Lab 02 — Experimentando o ACO

Semente aleatória fixa (42) em todas as execuções para comparação justa.

### Output
```
#### EXPERIMENTO 1 — ALPHA ####

========== RESULTADO DO EXPERIMENTO ==========
Número de formigas: 20
Número de iterações: 50
ALPHA: 1.0
BETA: 2.0
Taxa de evaporação: 0.5
Melhor rota: [0, 1, 2, 3, 4, 5]
Melhor custo: 8.0
Iteração em que o melhor custo foi achado: 1
% de formigas da última iteração na melhor rota: 100%
Feromônio máx. / total: 500.0 / 2500.0

========== RESULTADO DO EXPERIMENTO ==========
Número de formigas: 20
Número de iterações: 50
ALPHA: 0.1
BETA: 2.0
Taxa de evaporação: 0.5
Melhor rota: [0, 1, 2, 3, 4, 5]
Melhor custo: 8.0
Iteração em que o melhor custo foi achado: 1
% de formigas da última iteração na melhor rota: 55%
Feromônio máx. / total: 392.52 / 2181.49

========== RESULTADO DO EXPERIMENTO ==========
Número de formigas: 20
Número de iterações: 50
ALPHA: 5.0
BETA: 2.0
Taxa de evaporação: 0.5
Melhor rota: [0, 1, 2, 3, 4, 5]
Melhor custo: 8.0
Iteração em que o melhor custo foi achado: 1
% de formigas da última iteração na melhor rota: 100%
Feromônio máx. / total: 500.0 / 2500.0

#### EXPERIMENTO 2 — BETA ####

========== RESULTADO DO EXPERIMENTO ==========
Número de formigas: 20
Número de iterações: 50
ALPHA: 1.0
BETA: 2.0
Taxa de evaporação: 0.5
Melhor rota: [0, 1, 2, 3, 4, 5]
Melhor custo: 8.0
Iteração em que o melhor custo foi achado: 1
% de formigas da última iteração na melhor rota: 100%
Feromônio máx. / total: 500.0 / 2500.0

========== RESULTADO DO EXPERIMENTO ==========
Número de formigas: 20
Número de iterações: 50
ALPHA: 1.0
BETA: 0.5
Taxa de evaporação: 0.5
Melhor rota: [0, 1, 2, 3, 4, 5]
Melhor custo: 8.0
Iteração em que o melhor custo foi achado: 1
% de formigas da última iteração na melhor rota: 100%
Feromônio máx. / total: 500.0 / 2500.0

========== RESULTADO DO EXPERIMENTO ==========
Número de formigas: 20
Número de iterações: 50
ALPHA: 1.0
BETA: 5.0
Taxa de evaporação: 0.5
Melhor rota: [0, 1, 2, 3, 4, 5]
Melhor custo: 8.0
Iteração em que o melhor custo foi achado: 1
% de formigas da última iteração na melhor rota: 100%
Feromônio máx. / total: 500.0 / 2500.0

#### EXPERIMENTO 3 — EVAPORAÇÃO ####

========== RESULTADO DO EXPERIMENTO ==========
Número de formigas: 20
Número de iterações: 50
ALPHA: 1.0
BETA: 2.0
Taxa de evaporação: 0.5
Melhor rota: [0, 1, 2, 3, 4, 5]
Melhor custo: 8.0
Iteração em que o melhor custo foi achado: 1
% de formigas da última iteração na melhor rota: 100%
Feromônio máx. / total: 500.0 / 2500.0

========== RESULTADO DO EXPERIMENTO ==========
Número de formigas: 20
Número de iterações: 50
ALPHA: 1.0
BETA: 2.0
Taxa de evaporação: 0.1
Melhor rota: [0, 1, 2, 3, 4, 5]
Melhor custo: 8.0
Iteração em que o melhor custo foi achado: 1
% de formigas da última iteração na melhor rota: 100%
Feromônio máx. / total: 2486.51 / 12430.38

========== RESULTADO DO EXPERIMENTO ==========
Número de formigas: 20
Número de iterações: 50
ALPHA: 1.0
BETA: 2.0
Taxa de evaporação: 0.9
Melhor rota: [0, 1, 2, 3, 4, 5]
Melhor custo: 8.0
Iteração em que o melhor custo foi achado: 1
% de formigas da última iteração na melhor rota: 100%
Feromônio máx. / total: 277.78 / 1388.89

#### EXPERIMENTO 4 — NÚMERO DE FORMIGAS ####

========== RESULTADO DO EXPERIMENTO ==========
Número de formigas: 20
Número de iterações: 50
ALPHA: 1.0
BETA: 2.0
Taxa de evaporação: 0.5
Melhor rota: [0, 1, 2, 3, 4, 5]
Melhor custo: 8.0
Iteração em que o melhor custo foi achado: 1
% de formigas da última iteração na melhor rota: 100%
Feromônio máx. / total: 500.0 / 2500.0

========== RESULTADO DO EXPERIMENTO ==========
Número de formigas: 5
Número de iterações: 50
ALPHA: 1.0
BETA: 2.0
Taxa de evaporação: 0.5
Melhor rota: [0, 1, 2, 3, 4, 5]
Melhor custo: 8.0
Iteração em que o melhor custo foi achado: 1
% de formigas da última iteração na melhor rota: 100%
Feromônio máx. / total: 125.0 / 625.0

========== RESULTADO DO EXPERIMENTO ==========
Número de formigas: 50
Número de iterações: 50
ALPHA: 1.0
BETA: 2.0
Taxa de evaporação: 0.5
Melhor rota: [0, 1, 2, 3, 4, 5]
Melhor custo: 8.0
Iteração em que o melhor custo foi achado: 1
% de formigas da última iteração na melhor rota: 100%
Feromônio máx. / total: 1250.0 / 6250.0
```

### Tabela-resumo

| Experimento | Configuração | Melhor rota | Custo | % formigas na melhor rota (última iteração) | Feromônio máx. |
|---|---|---|---|---|---|
| Alpha | 1.0 (base) | [0,1,2,3,4,5] | 8 | 100% | 500 |
| Alpha | 0.1 | [0,1,2,3,4,5] | 8 | 55% | 392,5 |
| Alpha | 5.0 | [0,1,2,3,4,5] | 8 | 100% | 500 |
| Beta | 0.5 | [0,1,2,3,4,5] | 8 | 100% | 500 |
| Beta | 5.0 | [0,1,2,3,4,5] | 8 | 100% | 500 |
| Evaporação | 0.1 | [0,1,2,3,4,5] | 8 | 100% | 2486,5 |
| Evaporação | 0.9 | [0,1,2,3,4,5] | 8 | 100% | 277,8 |
| Formigas | 5 | [0,1,2,3,4,5] | 8 | 100% | 125 |
| Formigas | 50 | [0,1,2,3,4,5] | 8 | 100% | 1250 |

### Discussão

**Alpha.** Ao aumentar ALPHA, a influência da experiência acumulada (feromônio) **aumenta**. Com ALPHA = 0.1 o feromônio quase não pesa: só 55% das formigas finais seguiram a melhor rota (mais exploração). Com ALPHA = 5 a colônia segue o feromônio quase cegamente (100%), o que acelera a convergência mas, em redes maiores, aumenta o risco de estagnar numa rota subótima.

**Beta.** BETA baixo reduz a influência do custo (as formigas dependem mais do feromônio); BETA alto torna as rotas baratas muito atraentes desde o início (comportamento mais "guloso"). Nesta rede pequena todos os valores chegaram ao mesmo resultado.

**Evaporação.** Com 0.1 o algoritmo lembra muito tempo (feromônio acumulado ~2486, contra 500 na base): convergência estável, mas com risco de "congelar" cedo numa solução. Com 0.9 esquece rápido (feromônio máx. ~278): a memória é fraca e a busca fica mais exploratória/instável; em problemas difíceis isso pode impedir o aprendizado. Aqui o resultado final foi o mesmo.

**Número de formigas.** Com 5 formigas há menos exploração por iteração e menos feromônio depositado (máx. 125); com 50 há mais exploração e mais reforço (máx. 1250), ao custo de mais computação por iteração.

**Nota:** como a rede tem só 6 nós e o ótimo (custo 8) é encontrado já na iteração 1 em todos os casos, os efeitos aparecem principalmente na intensidade do feromônio e na fração de formigas que seguem a melhor rota, e não no custo final.

---

## Lab 03 — Completando o ACO

### Trechos completados
```python
atratividade = (fer ** ALPHA) * ((1 / custo) ** BETA)          # calcular_atratividade
feromonio = feromonio * (1 - TAXA_EVAPORACAO)                   # evaporar_feromonio
deposito = Q / custo                                            # depositar_feromonio
feromonio[origem][destino] += deposito
atratividades = [calcular_atratividade(atual, no) for no in candidatos]   # construir_rota
probabilidades = [a / sum(atratividades) for a in atratividades]
proximo = random.choices(candidatos, weights=probabilidades, k=1)[0]
```

### Output
```
Teste calcular_atratividade(0,1): 0.25 (esperado 0.25)
Teste calcular_atratividade(0,2): 0.0625 (esperado 0.0625)
Melhor rota: [0, 1, 2, 3, 4, 5]
Melhor custo: 8.0
```

### Respostas

**1. Por que 1/custo e não o custo?**
Queremos que caminhos **mais baratos** sejam **mais atrativos**. Usar o custo diretamente faria o oposto: custo maior → atratividade maior. O inverso transforma "menor custo" em "maior atratividade" (ex.: custo 2 → 0,5; custo 4 → 0,25).

**2. O que acontece com a atratividade quando a rota recebe mais feromônio?**
A atratividade aumenta, pois ela é proporcional a `feromônio^ALPHA`. Consequentemente, cresce a probabilidade de as formigas escolherem esse caminho, reforçando-o ainda mais (realimentação positiva).

**3. Por que impedir revisitar nós?**
Sem essa restrição a formiga poderia andar em ciclos (ex.: 1→2→1→2…), gerando rotas longas e inúteis, desperdiçando custo e podendo até nunca chegar ao destino. Impedir revisitas garante rotas simples (sem laços) que terminam.

---

## Lab 04 — ACO do zero

### Output
```
========== RESULTADO ==========

Melhor rota encontrada:
[0, 1, 2, 3, 4, 5]

Melhor custo:
8.0

Gráfico salvo em lab04_evolucao.png
```

Gráfico: `lab04_evolucao.png`.

### Variação de parâmetros
As alterações de NUM_FORMIGAS, ALPHA, BETA e TAXA_EVAPORACAO foram testadas no Lab 02 (mesmo algoritmo). Resumo: todos os valores testados encontraram a rota [0, 1, 2, 3, 4, 5] com custo 8; o que mudou foi o quanto as formigas se concentraram nela (ALPHA 0.1 → 55%) e a magnitude do feromônio acumulado (evaporação 0.1 → ~2486; 0.9 → ~278).

### Questões finais

**1. Como o feromônio ajuda o ACO a aprender?**
O feromônio é uma memória compartilhada. Cada formiga deposita nas arestas que usou uma quantidade inversamente proporcional ao custo da sua rota. Arestas de rotas boas acumulam mais feromônio e ficam mais prováveis para as próximas formigas, enquanto as de rotas ruins recebem pouco e evaporam. Com as iterações, a colônia "aprende" quais caminhos valem a pena sem que ninguém conheça a solução de antemão.

**2. Explorar vs. aproveitar.**
*Explorar* é testar caminhos novos ou pouco usados, o que pode revelar soluções melhores mas custa tentativas ruins. *Aproveitar* (explotação) é seguir caminhos que já provaram ser bons, o que refina a solução atual, mas pode prender a busca num ótimo local. No ACO, a aleatoriedade, BETA/ALPHA baixos e a evaporação favorecem a exploração; ALPHA alto e evaporação baixa favorecem o aproveitamento. O equilíbrio entre os dois é o ponto central do desempenho.

**3. O que investigar primeiro numa rede muito maior?**
Investigaria primeiro a **taxa de evaporação** junto com o **ALPHA/BETA** (equilíbrio exploração × explotação). Em redes grandes há muito mais rotas, então evaporação baixa ou ALPHA alto fazem a colônia convergir cedo para uma rota ruim, enquanto evaporação alta perde o aprendizado. Em seguida, ajustaria o número de formigas e de iterações, pois o espaço de busca cresce muito e 20 formigas × 50 iterações podem ser insuficientes.
