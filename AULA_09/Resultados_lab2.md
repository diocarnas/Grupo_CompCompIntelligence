# Resultados — Aula 04 (lab01_aula04)

**Data:** 07/10/2026

## 1. Objetivo

Resolver o problema da **gorjeta** com lógica fuzzy usando `scikit-fuzzy`. As entradas são a nota do serviço e a nota da comida (0 a 10), e a saída é a gorjeta sugerida (0 a 25 % da conta).

## 2. O que a lógica fuzzy realiza

A lógica clássica só aceita verdadeiro ou falso. Já a lógica fuzzy trabalha com **graus de pertinência** entre 0 e 1. Um serviço de nota 7 é ao mesmo tempo "médio" (0,6) e "bom" (0,4). O sistema converte notas numéricas em uma gorjeta numérica de forma suave, seguindo regras escritas em linguagem natural, como o raciocínio de uma pessoa.

### Etapas do código

1. **Variáveis linguísticas:** `servico` e `comida` (entradas) e `gorjeta` (saída).
2. **Conjuntos fuzzy:** `ruim`, `medio` e `bom` nas entradas; `baixa`, `media` e `alta` na saída, todos triangulares e sobrepostos.
3. **Regras:**
   - Serviço ruim **OU** comida ruim → gorjeta baixa.
   - Serviço médio → gorjeta média.
   - Serviço bom **OU** comida boa → gorjeta alta.
4. **Inferência (Mamdani):** cada regra corta o conjunto de saída no seu grau de ativação (OU = máximo, E = mínimo). Os cortes são unidos (agregação).
5. **Defuzzificação:** o **centroide** da área agregada vira um único valor.

## 3. Resultados da execução

Entrada padrão do código (serviço = 7, comida = 3):

```
=> Gorjeta sugerida: 12.6%
```

Neste caso as três regras disparam: baixa = 0,4, média = 0,6 e alta = 0,4. A saída fica perto de 13 %, que é o centro do conjunto "média".

| Serviço | Comida | Gorjeta |
|---|---|---|
| 7 | 3 | 12,55 % |
| 0 | 0 | 4,33 % |
| 10 | 10 | 21,00 % |
| 5 | 5 | 12,67 % |

> Inserir aqui os prints dos 3 gráficos (`servico.view()`, `comida.view()` e `gorjeta.view(sim=sim)`).

## 4. Experimentos

**Exp. 1 — regra 2 como `servico["medio"] & comida["medio"]`:**
Para (7, 3) a gorjeta continua em **12,55 %**. Como o serviço = 7 tem pertinência 0,6 em "médio" e a comida = 3 também tem 0,6 em "médio", o mínimo (E) é igual ao valor usado antes. A regra só muda o resultado quando as duas notas dão pertinências diferentes.

**Exp. 2 — outras formas de função de pertinência no serviço:**

| Forma | (7, 3) | (0, 0) | (10, 10) | (5, 5) |
|---|---|---|---|---|
| Triângulo (original) | 12,55 | 4,33 | 21,00 | 12,67 |
| Trapézio | 13,59 | 4,33 | 21,00 | 12,67 |
| Gaussiana | 12,28 | 5,42 | 19,76 | 12,66 |

Os trapézios têm um "platô" de pertinência 1, então o serviço 7 passa a contar mais como "médio". As gaussianas dão uma transição mais suave, mas ficam mais afastadas dos extremos.

**Exp. 3 — método de defuzzificação:**

| Método | (7, 3) | (0, 0) | (10, 10) | (5, 5) |
|---|---|---|---|---|
| centroid | 12,55 | 4,33 | 21,00 | 12,67 |
| bisector | 12,58 | 3,81 | 21,49 | 12,75 |
| mom | 12,75 | 0,00 | 25,00 | 13,00 |
| som | 7,80 | 0,00 | 25,00 | 13,00 |
| lom | 17,80 | 0,00 | 25,00 | 13,00 |

`centroid` e `bisector` dão valores parecidos. Os métodos `mom`, `som` e `lom` olham só o pico do conjunto, então geram resultados mais "extremos": 0 % e 25 % nas pontas. Para (7, 3), `som` usa o menor valor do platô de máximo e `lom` o maior, daí a grande diferença (7,8 contra 17,8).

**Exp. 4 — conjunto "excelente" no serviço (nova regra: serviço excelente → gorjeta alta):**
Redistribuímos o serviço em quatro triângulos (ruim, médio, bom, excelente). Para (7, 3), a gorjeta subiu de 12,55 % para **14,52 %**. Para (5, 5) subiu de 12,67 % para **14,04 %**. Isso mostra que mudar a modelagem do universo muda a resposta do sistema, mesmo com a mesma nota.

**Exp. 5 — casos de teste:**

| Caso | Gorjeta | Esperado? |
|---|---|---|
| (0, 0) | 4,33 % | Baixa, mas não chega a 0 %, porque o centroide é a média da área. |
| (10, 10) | 21,00 % | Alta, mas não chega a 25 % pelo mesmo motivo. |
| (5, 5) | 12,67 % | Média, perto do centro de "média" (13 %). |

## 5. Considerações da dupla/trio

- A lógica fuzzy permite que mais de uma regra dispare ao mesmo tempo, e a saída é uma combinação ponderada delas. Por isso a gorjeta varia gradualmente com as notas, sem saltos.
- Os operadores `|` (OU, máximo) e `&` (E, mínimo) mudam o grau de ativação de cada regra. Isso só altera o resultado final quando as pertinências envolvidas são diferentes.
- A forma das funções de pertinência e o método de defuzzificação influenciam bastante o resultado. O centroide é o mais suave e o mais usado, e não chega aos extremos.
- _(Acrescentar dúvidas, dificuldades ou observações próprias.)_
