
## 1. Desafio dos Extremos

### 1.1 Resultados medidos (saída do `lab01_aula10.py`)

| Cenário | (0, 0) | (100, 10) | (50, 5) |
|---|---|---|---|
| Baseline  (tri + centroide) | 4,33 | 87,50 | 67,50 |
| Abordagem A (trapmf + centroide) | 4,33 | 90,71 | 67,50 |
| Abordagem B (tri + MOM) | 0,00 | 87,50 | 67,50 |
| Abordagem A+B (trapmf + MOM) | 0,00 | 95,00 | 67,50 |
| Variante C (pico em 100 + MOM) | 0,00 | 100,00 | 67,50 |
| Variante D (pico em 100 + centroide) | 4,33 | 91,67 | 67,50 |

As funções de pertinência de saída usadas no baseline: Baixa `[0,0,13]`, Média `[5,30,55]`, Alta `[45,67.5,90]`, Crítica `[75,87.5,100]`. Com elas o sistema reproduz exatamente os valores 4,33% e 87,5% do enunciado.

### 1.2 Por que o centroide não atinge 0% nem 100%?

O centroide calcula o **centro de massa da área agregada** da saída: `x* = ∫ x·μ(x) dx / ∫ μ(x) dx`. Ele é uma **média ponderada** dos pontos do universo, e uma média só vale 0 ou 100 se toda a massa estiver concentrada exatamente nesse ponto, o que é impossível para uma função com área.

- Em (0, 0) só a regra "Impacto Baixo ∧ Explorabilidade Baixa → Urgência Baixa" dispara, com grau 1. A saída é o triângulo `[0,0,13]` inteiro, cujo centroide é (0+0+13)/3 = **4,33**. O triângulo tem massa à direita do zero, então o centro de massa fica deslocado.
- Em (100, 10) dispara apenas "Alto ∧ Alta → Crítica", com grau 1. O triângulo `[75,87.5,100]` tem centroide (75+87,5+100)/3 = **87,5**. Como o pico está em 87,5 e a base se estende para a esquerda de 100, o resultado fica abaixo do extremo.

Ou seja: não é erro de código. É uma propriedade matemática do centroide, que "puxa" a saída para o interior do universo (efeito de compressão nas bordas).

### 1.3 Abordagem A — Trapézio (`trapmf`) na borda superior da Crítica

Com `trapmf [75, 90, 100, 100]` a massa se desloca para a direita e o centroide sobe de 87,50 para **90,71**. Melhora, mas **não chega a 100**: continua sendo uma média ponderada e a área ainda se estende à esquerda. Mesmo com o pico em 100 (variante D) o centroide só chega a 91,67. Além disso, o extremo inferior (4,33) não muda, pois a Baixa não foi alterada. O trapézio resolve parcialmente e preserva a suavidade da superfície, porque o método de defuzzificação continua sendo o centroide (maior salto entre vizinhos da grade: 39,74, igual ao baseline).

### 1.4 Abordagem B — Defuzzificação por MOM (Mean of Maximum)

O MOM devolve a média dos pontos onde a saída agregada atinge o máximo, e não o centro de massa. Resultado:

- (0, 0) passa para **0,00**, pois o pico da Baixa está em 0.
- (100, 10) fica em 87,50 com os triângulos atuais, porque o pico da Crítica está em 87,5. **Só chega a 100 se o pico (ou platô) da Crítica estiver em 100** (variante C: 100,00).
- O preço é a **perda de suavidade**: o MOM só olha para o(s) conjunto(s) de maior ativação, então a superfície vira **degraus** (platôs em 67,5 etc.). O maior salto entre vizinhos da grade sobe de 39,74 para **63,40**, e valores intermediários de impacto/explorabilidade deixam de produzir saídas graduais (ex.: Impacto 30 a 70 com Explorabilidade 5 dá sempre 67,5).

### 1.5 Qual abordagem é mais recomendável?

- **Para preservar a suavidade no meio da escala:** o centroide (baseline ou Abordagem A). O MOM é descontínuo e prejudica a interpretação gradual de risco.
- **Para cravar 0% e 100% nos extremos:** apenas o MOM com picos em 0 e 100 (variante C) fez isso nos testes. O trapézio sozinho não resolve.
- **Recomendação:** a **Abordagem A (trapézio + centroide)** quando a prioridade é uma superfície contínua e defensável, aceitando que os extremos ficam em ~4% e ~91% (e, se necessário, ajustando também a Baixa para um trapézio à esquerda). Se o requisito do negócio exigir estritamente 0% e 100% nos extremos, usar MOM com picos nas bordas, assumindo a superfície em degraus. Nenhuma das duas entrega as duas propriedades ao mesmo tempo; uma alternativa comum é manter o centroide e **reescalar linearmente** a saída pela faixa [min, max] obtida do sistema, o que preserva a suavidade e crava 0 e 100. (Essa alternativa não foi implementada neste laboratório.)

## 2. Matriz de Regras 3×3 codificada

| Impacto \ Explorabilidade | Baixa (0–4) | Moderada (2–8) | Alta (6–10) |
|---|---|---|---|
| **Baixo (0–40)** | Urgência Baixa | Urgência Baixa | Urgência Média |
| **Médio (20–80)** | Urgência Média | Urgência Alta | Urgência Alta |
| **Alto (60–100)** | Urgência Crítica | Urgência Crítica | Urgência Crítica |

As 9 combinações estão codificadas em `lab01_aula10.py` (operador AND = mínimo, agregação = máximo). Como os conjuntos de entrada se sobrepõem e cobrem todo o universo, não há lacunas de cobertura: toda entrada ativa pelo menos uma regra.

## 3. Análise da Superfície de Decisão 3D (`superficie_decisao.png`)

Urgência (%) calculada pelo centroide (linhas: Explorabilidade, colunas: Impacto):

| Expl \ Imp | 0 | 20 | 40 | 60 | 80 | 100 |
|---|---|---|---|---|---|---|
| **0** | 4,3 | 5,1 | 30,0 | 30,0 | 87,5 | 87,5 |
| **2** | 5,1 | 5,1 | 30,0 | 30,0 | 87,5 | 87,5 |
| **4** | 4,7 | 5,1 | 67,5 | 67,5 | 87,5 | 87,5 |
| **6** | 4,7 | 5,1 | 67,5 | 67,5 | 87,5 | 87,5 |
| **8** | 30,0 | 30,0 | 67,5 | 67,5 | 87,5 | 87,5 |
| **10** | 30,0 | 30,0 | 67,5 | 67,5 | 87,5 | 87,5 |

Maior salto entre pontos vizinhos da grade: centroide 39,74, trapézio 39,74, MOM 63,40.

- **Monotonicidade:** a urgência cresce com o Impacto e, em menor grau, com a Explorabilidade, coerente com a matriz de regras.
- **Impacto domina:** para Impacto ≥ ~70 a superfície forma um platô alto (Crítica), independentemente da explorabilidade, refletindo a linha "Alto" inteira mapeada para Crítica.
- **Zona de transição:** entre Impacto ≈ 20 e 40 há uma rampa íngreme (de ~5% para ~55–67%), onde os conjuntos de saída Baixa e Média/Alta estão distantes; ali pequenas variações de entrada causam saltos grandes de saída.
- **Baixo impacto:** a explorabilidade só eleva a urgência (para "Média") quando está alta (≥ ~6).
- **Continuidade:** com o centroide, a superfície é contínua, sem buracos nem regiões sem resposta (confirmando a cobertura das 9 regras). Com MOM (painel da direita) a superfície é em degraus, evidenciando a descontinuidade.
- **Extremos:** o ponto mais baixo é 4,33 e o mais alto 87,5 (centroide), mostrando a compressão discutida no item 1.2.
