# Projeto Fuzzy — Semáforo inteligente (Aula 09)

**Data:** 07/10/2026
---

## Etapa 1 — Definição do problema

Em muitos cruzamentos o tempo de verde é fixo, definido por um técnico de trânsito, e não se adapta ao movimento real. Com a fila grande, os carros ficam parados. Com a fila pequena, o verde é desperdiçado e os pedestres esperam sem necessidade. O projeto calcula o **tempo de verde para os veículos** a partir de duas entradas:

- **Fila de veículos** (0 a 40 carros)
- **Pedestres aguardando** para atravessar (0 a 30 pessoas)

**Saída:** tempo de verde para veículos (10 a 60 s).

Fuzzy é adequado porque ninguém define um limite exato entre fila "média" e "longa" ou entre pedestres "moderados" e "muitos". A decisão de um operador é do tipo "fila grande, mas com muita gente atravessando, dá um tempo intermediário". Um `if fila > 30` seria brusco e injusto nos limites.

---

## Etapa 2 — Modelagem

### Universos de discurso e termos

| Variável | Universo | Termos (função de pertinência) |
|---|---|---|
| Fila (carros) | 0 a 40 | curta `trap[0,0,5,15]`, média `tri[8,20,32]`, longa `trap[25,35,40,40]` |
| Pedestres (pessoas) | 0 a 30 | poucos `trap[0,0,3,10]`, moderados `tri[5,15,25]`, muitos `trap[18,25,30,30]` |
| Verde (s), saída | 10 a 60 | curto `trap[10,10,15,25]`, médio `tri[20,35,50]`, longo `trap[45,55,60,60]` |

Usamos trapézios nas pontas, porque os extremos do universo valem 1, e triângulos no meio. Os conjuntos se sobrepõem para que a transição seja gradual.

### Base de regras (8 regras)

| # | Regra |
|---|---|
| R1 | SE fila é curta **E** pedestres são poucos → verde curto |
| R2 | SE fila é curta **E** pedestres são moderados → verde curto |
| R3 | SE fila é curta **E** pedestres são muitos → verde curto |
| R4 | SE fila é média **E** pedestres são poucos → verde médio |
| R5 | SE fila é média **E** pedestres são moderados → verde médio |
| R6 | SE fila é média **E** pedestres são muitos → verde curto |
| R7 | SE fila é longa **E** (pedestres são poucos **OU** moderados) → verde longo |
| R8 | SE fila é longa **E** pedestres são muitos → verde médio |

**E** = mínimo, **OU** = máximo (a R7 usa os dois). Inferência de Mamdani, agregação por máximo e defuzzificação pelo **centroide**.

### Funções de pertinência


---

## Etapa 3 — Implementação

O arquivo `semaforo_fuzzy.py` implementa tudo do zero:

- `trapmf` e `trimf`: funções de pertinência.
- `fuzzificar`: calcula o grau de pertinência de cada entrada em cada termo.
- `inferir`: aplica as 8 regras, corta cada conjunto de saída na ativação, une os cortes e calcula o centroide.
- `rodar_testes`, `plotar_pertinencias` e `plotar_resultado`: testes e gráficos.

---

## Etapa 4 — Testes

As faixas esperadas foram definidas antes de rodar, pelo raciocínio de um operador de trânsito.

| # | Fila | Pedestres | Saída do sistema | Esperado | Bateu? | Situação |
|---|---|---|---|---|---|---|
| 1 | 3 | 2 | **15,3 s** | 10–25 s | sim | Pouco movimento, verde curto |
| 2 | 20 | 8 | **35,0 s** | 28–42 s | sim | Fila média, poucos pedestres |
| 3 | 36 | 4 | **54,5 s** | 45–60 s | sim | Fila enorme, quase sem pedestres |
| 4 | 36 | 28 | **35,0 s** | 28–42 s | sim | Fila enorme, mas muitos pedestres |
| 5 | 20 | 27 | **15,3 s** | 10–25 s | sim | Fila média, muitos pedestres: prioriza pedestres |
| 6 | 38 | 14 | **54,6 s** | 45–60 s | sim | Fila enorme, pedestres moderados |




### Análise

- **Casos 1, 5 e 6:** em cada um só uma regra dispara por completo (R1, R6 e R7), e a saída fica perto do centroide do conjunto correspondente.
- **Caso 2:** o valor 8 de pedestres cai na zona de sobreposição entre "poucos" (0,29) e "moderados" (0,30). As regras R4 e R5 disparam juntas, mas as duas apontam para "verde médio", então a saída é 35 s.
- **Casos 3 e 6:** a saída fica perto de 54 a 55 s, e não em 60 s, porque o centroide é a média da área e não o pico do conjunto.
- **Casos 4 e 5:** mostram o efeito dos pedestres. Com fila enorme e muita gente (caso 4) o verde cai de longo para médio. Com fila média e muita gente (caso 5) cai para curto.
- **Limitação:** nenhuma regra manda o verde ficar "longo" quando os pedestres são muitos, mesmo com fila longa. Se o cruzamento tiver pouca travessia de pedestres, as regras R6 e R8 poderiam ser revistas.

---

## Etapa 5 — Entrega

- Código-fonte executável: `semaforo_fuzzy.py`
  - `python semaforo_fuzzy.py` roda os testes e mostra os gráficos.
  - `python semaforo_fuzzy.py 20 8` calcula para um caso específico.
  - `python semaforo_fuzzy.py --sem-grafico` roda só os testes.
- Este relatório: `resultados_aula09.md`
- Imagens usadas no relatório: `semaforo_pertinencias.png` e `semaforo_resultado.png`
