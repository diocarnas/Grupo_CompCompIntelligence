# Resultados Aula 13 - CIAO

## a) Diferença prática entre variáveis contínuas e inteiras

Com `IntegerRandomSampling` e `RoundingRepair` (no SBX e na PM), o NSGA-II só
produz valores inteiros (ex.: 12 pods e 5 analistas), sem frações de
servidores ou analistas. Observações práticas:

- **Soluções implantáveis:** nos exercícios 1, 2 e 6 toda solução da fronteira
  é uma configuração real. Com variáveis contínuas (exercícios 3, 4 e 5)
  aparecem valores como 7,3 GB de RAM ou 12,8 réplicas, que precisariam ser
  arredondados depois, podendo piorar os objetivos ou violar restrições.
- **Fronteira de Pareto discreta:** o espaço de busca é finito, então a
  fronteira inteira tem poucos pontos e forma "degraus". A contínua é densa e
  suave.
- **Papel do reparo:** o SBX e a PM trabalham em ponto flutuante
  (`vtype=float`). O `RoundingRepair` arredonda os filhos para o inteiro mais
  próximo, mantendo-os viáveis. Sem ele, as soluções voltariam a ser
  fracionárias.
- **`eliminate_duplicates=True`:** é importante no caso inteiro, pois o
  arredondamento gera muitos indivíduos repetidos.

## b) Hipervolume do Exercício 4 (ref_point = [400, 600])

| Gerações | Hipervolume |
|----------|-------------|
| 10       | **PREENCHER** |
| 80       | **PREENCHER** |

Os valores saem de `python aula13_lab04.py`. Esperado: HV(80) ≥ HV(10), pois
mais gerações levam a uma fronteira mais convergida e melhor distribuída.

## c) Escala hospitalar recomendada (Exercício 6, pesos 40% custo / 60% espera)

| Item | Valor |
|------|-------|
| Médicos | **PREENCHER** |
| Enfermeiros | **PREENCHER** |
| Custo do plantão | **PREENCHER** |
| Tempo médio de espera | **PREENCHER** (deve ser ≤ 25,0 min) |

Os valores saem de `python aula13_lab06.py`.

> Referência de conferência (não é a saída do pymoo): calculei por força bruta
> a fronteira de Pareto exata, restrita a espera ≤ 25, e apliquei a fórmula do
> PseudoWeights com pesos [0,40; 0,60]. Resultado: 16 médicos, 34 enfermeiros,
> R$ 34.500,00 e 18,31 min. Como a fronteira exata tem 76 pontos e a população
> é de 40, o NSGA-II pode achar um subconjunto e escolher outra escala próxima.
> Registre o que o seu script imprimir.
