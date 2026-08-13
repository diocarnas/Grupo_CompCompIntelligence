LAB 1

Total de solucoes avaliadas: 64
Tempo de execucao: 0.000477 segundos
Melhor valor encontrado: 8
Combinacao otima (0=nao leva, 1=leva): (1, 0, 1, 1, 0, 0)

Itens escolhidos:
 - Livro (peso: 2 , valor: 3 )
 - Camiseta (peso: 1 , valor: 2 )
 - Carregador (peso: 2 , valor: 3 )

 - #PERGUNTAS:
# 1. Por que o total de soluções avaliadas e exatamente 32?
  R: Cada um dos 5 itens tem 2 escolhas possíveis, ou ele entra na mochila (1), ou fica de fora (0). Aí multiplicamos as possibilidades de cada um.
  como temos 5 itens e 2 escolhas fazemos o calculo de todas as possibilidades 2^5 = 32 

# 2. O que aconteceria se eu colocasse 15 itens?
 R: Se colocamos 15 itens teríamos 32.768 de soluções é o tempo de execução seria maior.
 
# 3.Voces conseguem imaginar um problema da vida real que seja parecido com este?
R: Um problema que seja parecido com esse seria em empresas de frete que dependeria do peso de carga de cada viagem e poderia utilizar um script desse.

LAB 2 

=================================================================
RESULTADOS DA FORCA-BRUTA NO TSP
=================================================================

>>> 4 cidades
    Rotas avaliadas : 6
    Melhor custo    : 80
    Melhor rota     : (0, 1, 3, 2, 0)
    Tempo (segundos): 0.000079

>>> 5 cidades
    Rotas avaliadas : 24
    Melhor custo    : 41
    Melhor rota     : (0, 1, 2, 3, 4, 0)
    Tempo (segundos): 0.000062

>>> 6 cidades
    Rotas avaliadas : 120
    Melhor custo    : 91
    Melhor rota     : (0, 1, 3, 4, 5, 2, 0)
    Tempo (segundos): 0.000305

=================================================================
OBSERVE: o numero de rotas cresce como (n-1)!  (fatorial)
4 cidades -> 6 rotas | 5 -> 24 | 6 -> 120 | 10 -> 362880 | 15 -> 87 bilhoes
=================================================================

# Perguntas de reflexao (obrigatorias)
# 16.	O numero de rotas cresce de forma linear, quadratica ou muito mais rapido? Explique com as quantidades que voce coletou.
R: Ele cresce de forma fatorial um exemplo de 4 cidades aonde gera 6 rotas diferentes e com um custo de 80.

# 17.	Com base no padrão observado, estime (mesmo que de forma grosseira) quanto tempo levaria para 10 cidades no mesmo computador.
R: Teria 362.880 rotas e o tempo levaria cerca de 1 a 2 segundos.

# 18.	Por que dizemos que o TSP e um problema “dificil”? A resposta nao e “porque e complicado de entender”, e sim por causa do crescimento do tempo.
R: devido à explosão combinatória no tempo de execução.


LAB3

Rodando 20 instancias...
Instancia  1 | Otimo:  199 | Gulosa:  199 | Gap:   0.0%
Instancia  2 | Otimo:  170 | Gulosa:  170 | Gap:   0.0%
Instancia  3 | Otimo:  155 | Gulosa:  155 | Gap:   0.0%
Instancia  4 | Otimo:  147 | Gulosa:  147 | Gap:   0.0%
Instancia  5 | Otimo:  261 | Gulosa:  261 | Gap:   0.0%
Instancia  6 | Otimo:  214 | Gulosa:  214 | Gap:   0.0%
Instancia  7 | Otimo:  191 | Gulosa:  187 | Gap:   2.1%
Instancia  8 | Otimo:  183 | Gulosa:  183 | Gap:   0.0%
Instancia  9 | Otimo:  215 | Gulosa:  206 | Gap:   4.2%
Instancia 10 | Otimo:  174 | Gulosa:  174 | Gap:   0.0%
Instancia 11 | Otimo:  262 | Gulosa:  262 | Gap:   0.0%
Instancia 12 | Otimo:  206 | Gulosa:  206 | Gap:   0.0%
Instancia 13 | Otimo:  231 | Gulosa:  231 | Gap:   0.0%
Instancia 14 | Otimo:  309 | Gulosa:  309 | Gap:   0.0%
Instancia 15 | Otimo:  294 | Gulosa:  294 | Gap:   0.0%
Instancia 16 | Otimo:  247 | Gulosa:  247 | Gap:   0.0%
Instancia 17 | Otimo:  136 | Gulosa:  134 | Gap:   1.5%
Instancia 18 | Otimo:  212 | Gulosa:  212 | Gap:   0.0%
Instancia 19 | Otimo:  243 | Gulosa:  243 | Gap:   0.0%
Instancia 20 | Otimo:  193 | Gulosa:  193 | Gap:   0.0%




# O que entregar / discutir:
# 19.	Codigo completo (com a funcao calcular_gap implementada e o loop funcionando).

# 20.	Valor do gap medio obtido.
R:
===== RESUMO =====
Gap medio     : 0.39%
Gap minimo    : 0.00%
Gap maximo    : 4.19%
Desvio padrao : 1.03%

# 21.	Resposta: “A heuristica gulosa e boa o suficiente para este problema? Em quais situacoes voce usaria ela e em quais preferiria gastar mais tempo para achar o otimo?”
Eu usuária em situações em escala são prioritárias; perder 2% a 5% de eficiência não é um problema um exemplo seria em um sistema de rastreamento como o do ifood.
Onde vale a pena gastar mais tempo para achar o ótimo O custo do erro é altíssimo; 2% de perda representa milhões de reais ou riscos à vida .
