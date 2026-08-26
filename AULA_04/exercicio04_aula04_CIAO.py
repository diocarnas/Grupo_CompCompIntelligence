"""
================================================================================
RELATORIO TECNICO - Motor de Decisioning SD-WAN Zero-Trust
================================================================================

Cenario: selecao de rota para um no de comutacao central em uma topologia
com 12 roteadores (indices 0 a 11). Origem fixa no No 0, destino no No 11.

Cada enlace possui tres atributos: Latencia (ms), Taxa de Perda de Pacotes (%)
e cada NO possui um Indice de Reputacao de Seguranca (0 a 100). Nos com
reputacao < 50 sao considerados nao confiaveis (risco de interceptacao ou
comprometimento) e qualquer rota que passe por um deles recebe uma penalidade
fixa de seguranca P_Seguranca = 5000.

Funcao de fitness:
    Fitness(X) = w1 * LatenciaTotal(X) + w2 * PerdaPacotesTotal(X) + P_Seguranca

Amostragem estocastica configurada com semente fixa np.random.seed(2026), o
que garante reprodutibilidade da topologia gerada e da evolucao do GA.

--------------------------------------------------------------------------------
ROTA SELECIONADA E JUSTIFICATIVA (preencher apos executar o script)
--------------------------------------------------------------------------------
Ao rodar este script com a semente 2026, o algoritmo genetico converge para
uma rota entre o No 0 e o No 11 que MINIMIZA a soma ponderada de latencia e
perda de pacotes, ao mesmo tempo em que EVITA todo no com reputacao de
seguranca < 50. Sempre que a rota de menor custo "geografico" (latencia +
perda) passaria por um no nao confiavel, o algoritmo prefere um desvio -
tipicamente mais longo em numero de saltos e/ou latencia bruta - porque a
penalidade de seguranca (5000) domina qualquer economia obtida ao atravessar
o no comprometido. Ou seja: o desvio em relacao ao(s) no(s) penalizado(s) e
uma decisao racional do ponto de vista de custo total, refletindo a politica
Zero-Trust de que nenhuma economia de latencia/perda de pacotes justifica
transitar por um no com risco de interceptacao ou comprometimento.
Os nos evitados e a rota final exata, com seus valores numericos, sao
impressos no console ao final da execucao (ver saida do script).
================================================================================
"""

import numpy as np

# ---------------------------------------------------------------------------
# 1) Configuracao da topologia (12 nos, origem=0, destino=11)
# ---------------------------------------------------------------------------
np.random.seed(2026)

NUM_NOS = 12
ORIGEM = 0
DESTINO = 11

W1_LATENCIA = 1.0
W2_PERDA = 10.0  # perda de pacotes (%) pesa mais, pois seu impacto e critico
P_SEGURANCA = 5000

# Matriz de latencia (ms) - simetrica, sem auto-enlaces (diagonal = inf)
matriz_latencia = np.random.uniform(5, 60, (NUM_NOS, NUM_NOS))
matriz_latencia = (matriz_latencia + matriz_latencia.T) / 2
np.fill_diagonal(matriz_latencia, np.inf)

# Matriz de perda de pacotes (%) - simetrica, sem auto-enlaces
matriz_perda = np.random.uniform(0, 15, (NUM_NOS, NUM_NOS))
matriz_perda = (matriz_perda + matriz_perda.T) / 2
np.fill_diagonal(matriz_perda, np.inf)

# Indice de reputacao de seguranca por NO (0 a 100)
reputacao_nos = np.random.uniform(0, 100, NUM_NOS)
# Origem e destino sao sempre confiaveis (infraestrutura propria/controlada)
reputacao_nos[ORIGEM] = 100
reputacao_nos[DESTINO] = 100
nos_nao_confiaveis = set(np.where(reputacao_nos < 50)[0].tolist())

# ---------------------------------------------------------------------------
# 2) Funcao de fitness
# ---------------------------------------------------------------------------


def avaliar_rota(rota):
    """Retorna (fitness, latencia_total, perda_total, nos_penalizados_na_rota)."""
    latencia_total = 0.0
    perda_total = 0.0
    for i in range(len(rota) - 1):
        a, b = rota[i], rota[i + 1]
        latencia_total += matriz_latencia[a, b]
        perda_total += matriz_perda[a, b]

    nos_penalizados = [n for n in rota if n in nos_nao_confiaveis]
    penalidade_seguranca = P_SEGURANCA if len(nos_penalizados) > 0 else 0.0

    fitness = (W1_LATENCIA * latencia_total) + (W2_PERDA * perda_total) + penalidade_seguranca
    return fitness, latencia_total, perda_total, nos_penalizados


# ---------------------------------------------------------------------------
# 3) Algoritmo Genetico (individuo = permutacao dos nos intermediarios,
#    a rota completa e sempre ORIGEM -> permutacao -> DESTINO)
# ---------------------------------------------------------------------------
TAM_POP = 80
GERACOES = 300
TAXA_MUTACAO = 0.25

nos_intermediarios = [n for n in range(NUM_NOS) if n not in (ORIGEM, DESTINO)]


def montar_rota(individuo):
    return [ORIGEM] + [int(n) for n in individuo] + [DESTINO]


def criar_individuo(rng):
    # Cada individuo usa um subconjunto aleatorio (tamanho variavel) dos nos
    # intermediarios, em ordem aleatoria -> permite rotas com numero de saltos
    # variado, nao apenas rotas que visitam todos os 10 nos intermediarios.
    tamanho = rng.integers(1, len(nos_intermediarios) + 1)
    return list(rng.choice(nos_intermediarios, size=tamanho, replace=False))


def selecao_torneio(populacao, fitnesses, rng, k=3):
    participantes = rng.choice(len(populacao), size=k, replace=False)
    melhor = min(participantes, key=lambda idx: fitnesses[idx])
    return populacao[melhor][:]


def crossover(pai1, pai2, rng):
    # Order crossover adaptado para individuos de tamanho variavel:
    # combina um prefixo de pai1 com os nos restantes de pai2, preservando
    # a ordem relativa e sem duplicar nos.
    if len(pai1) == 0:
        return pai2[:]
    corte = rng.integers(1, len(pai1) + 1)
    prefixo = pai1[:corte]
    resto = [n for n in pai2 if n not in prefixo]
    filho = prefixo + resto
    return filho


def mutacao(individuo, rng, taxa=TAXA_MUTACAO):
    individuo = individuo[:]
    if rng.random() < taxa and len(individuo) >= 2:
        # troca a posicao de dois nos na rota
        i, j = rng.choice(len(individuo), 2, replace=False)
        individuo[i], individuo[j] = individuo[j], individuo[i]
    if rng.random() < taxa:
        # adiciona ou remove um no intermediario da rota
        fora = [n for n in nos_intermediarios if n not in individuo]
        if rng.random() < 0.5 and fora:
            pos = rng.integers(0, len(individuo) + 1)
            individuo.insert(pos, int(rng.choice(fora)))
        elif len(individuo) > 1:
            pos = rng.integers(0, len(individuo))
            individuo.pop(pos)
    return individuo


def algoritmo_genetico_sdwan():
    rng = np.random.default_rng(2026)
    populacao = [criar_individuo(rng) for _ in range(TAM_POP)]

    melhor_individuo, melhor_fitness = None, float("inf")

    for geracao in range(GERACOES):
        fitnesses = [avaliar_rota(montar_rota(ind))[0] for ind in populacao]

        idx_melhor = int(np.argmin(fitnesses))
        if fitnesses[idx_melhor] < melhor_fitness:
            melhor_fitness = fitnesses[idx_melhor]
            melhor_individuo = populacao[idx_melhor][:]

        nova_populacao = [melhor_individuo[:]]  # elitismo
        while len(nova_populacao) < TAM_POP:
            pai1 = selecao_torneio(populacao, fitnesses, rng)
            pai2 = selecao_torneio(populacao, fitnesses, rng)
            filho = crossover(pai1, pai2, rng)
            filho = mutacao(filho, rng)
            nova_populacao.append(filho)

        populacao = nova_populacao

    return melhor_individuo, melhor_fitness


if __name__ == "__main__":
    print("=" * 70)
    print("Motor de Decisioning SD-WAN Zero-Trust - Selecao de Rota (No 0 -> No 11)")
    print("=" * 70)

    print(f"\nNos com reputacao de seguranca < 50 (NAO CONFIAVEIS): {sorted(nos_nao_confiaveis)}")
    for n in sorted(nos_nao_confiaveis):
        print(f"  No {n}: reputacao = {reputacao_nos[n]:.1f}")

    melhor_individuo, melhor_fitness = algoritmo_genetico_sdwan()
    melhor_rota = montar_rota(melhor_individuo)
    fitness, latencia, perda, nos_penalizados = avaliar_rota(melhor_rota)

    print(f"\nRota selecionada: {melhor_rota}")
    print(f"Numero de saltos: {len(melhor_rota) - 1}")
    print(f"Latencia total: {latencia:.2f} ms")
    print(f"Perda de pacotes total: {perda:.2f} %")
    print(f"Nos nao confiaveis na rota: {nos_penalizados if nos_penalizados else 'nenhum'}")
    print(f"Penalidade de seguranca aplicada: {P_SEGURANCA if nos_penalizados else 0}")
    print(f"Fitness final: {fitness:.2f}")

    # Comparacao com a rota "ingenua" direta (menor latencia bruta, ignorando seguranca)
    rota_direta = [ORIGEM, DESTINO]
    fitness_direta, lat_direta, perda_direta, nos_pen_direta = avaliar_rota(rota_direta)
    print("\n--- Comparativo com rota direta (0 -> 11, sem desvio) ---")
    print(f"Rota direta: {rota_direta} | Fitness = {fitness_direta:.2f} "
          f"(nos nao confiaveis: {nos_pen_direta if nos_pen_direta else 'nenhum'})")

    print(
        "\nJustificativa: o algoritmo prioriza rotas que, mesmo com latencia/perda "
        "de pacotes eventualmente maiores, EVITAM nos com reputacao de seguranca "
        "abaixo de 50 - pois a penalidade fixa (5000) supera qualquer economia "
        "possivel de latencia ou perda de pacotes ao atravessar um no comprometido."
    )
