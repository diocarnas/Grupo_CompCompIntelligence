# Resultados — Aula 04 (lab01_aula04) — Resumo

**Integrantes:** _(preencher nomes da dupla/trio)_
**Data:** 07/10/2026

## O que é

Um controlador fuzzy de ventilador feito com `scikit-fuzzy`. A entrada é a temperatura (0 a 40 °C) e a saída é a velocidade (0 a 100 %).

## O que a lógica fuzzy realiza

Em vez de "frio ou não frio", a lógica fuzzy usa **graus de pertinência** entre 0 e 1. Assim, 20 °C é 50 % frio e 50 % morno ao mesmo tempo. A entrada numérica vira uma saída numérica suave, sem saltos entre faixas.

## Como funciona

1. Define as variáveis `temperatura` e `velocidade`.
2. Cria conjuntos sobrepostos: frio, morno e quente na entrada; baixa, média e alta na saída.
3. Aplica as regras: frio → baixa, morno → média, quente → alta.
4. Calcula a saída com `compute()`: fuzzifica, infere (Mamdani), agrega e defuzzifica pelo centroide.

## Resultados

| Temperatura | Pertinências | Velocidade |
|---|---|---|
| 10 °C | frio = 1,0 | 16,67 % |
| 20 °C | frio = 0,5 / morno = 0,5 | 44,05 % |
| 25 °C | morno = 1,0 | 50,00 % |
| 30 °C | morno = 0,5 / quente = 0,5 | 55,95 % |
| 38 °C | quente = 1,0 | 83,33 % |

> Inserir aqui os prints dos gráficos de `temperatura.view()` e `velocidade.view()`.

## Considerações da dupla/trio

- Com **uma regra ativa** (10, 25 e 38 °C), a saída é o centroide do conjunto inteiro.
- Com **duas regras ativas** (20 e 30 °C), a saída é uma mistura ponderada, e a velocidade sobe de forma gradual.
- A saída **não chega a 0 % nem a 100 %**, porque o centroide é a média da área. Dá para chegar mais perto dos extremos ajustando os triângulos de saída ou trocando o método de defuzzificação (por exemplo, `'mom'`).
- _(Acrescentar dúvidas, dificuldades ou observações próprias.)_
