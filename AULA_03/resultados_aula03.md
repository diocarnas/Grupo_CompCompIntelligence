LAB 01

==================================================
ALGORITMO GENÉTICO PASSO A PASSO
==================================================

População inicial: [[0, 1, 1, 0, 1], [0, 0, 0, 0, 1], [0, 1, 0, 0, 0], [1, 0, 0, 1, 0], [1, 0, 1, 0, 0], [1, 0, 0, 1, 1]]

==================== GERAÇÃO 0 ====================

Avaliação dos indivíduos:
  [0, 1, 1, 0, 1] → x=13 → f(x)=169
  [0, 0, 0, 0, 1] → x= 1 → f(x)=  1
  [0, 1, 0, 0, 0] → x= 8 → f(x)= 64
  [1, 0, 0, 1, 0] → x=18 → f(x)=324
  [1, 0, 1, 0, 0] → x=20 → f(x)=400
  [1, 0, 0, 1, 1] → x=19 → f(x)=361

 Melhor: x = 20 → f(x) = 400

==================== GERAÇÃO 1 ====================

Avaliação dos indivíduos:
  [1, 0, 1, 0, 0] → x=20 → f(x)=400
  [1, 0, 0, 1, 1] → x=19 → f(x)=361
  [1, 0, 0, 1, 1] → x=19 → f(x)=361
  [1, 0, 1, 1, 1] → x=23 → f(x)=529
  [1, 0, 0, 1, 1] → x=19 → f(x)=361
  [1, 0, 0, 1, 0] → x=18 → f(x)=324

 Melhor: x = 23 → f(x) = 529

==================== GERAÇÃO 2 ====================

Avaliação dos indivíduos:
  [1, 0, 1, 1, 1] → x=23 → f(x)=529
  [1, 0, 0, 1, 1] → x=19 → f(x)=361
  [1, 0, 0, 1, 1] → x=19 → f(x)=361
  [1, 0, 0, 1, 0] → x=18 → f(x)=324
  [1, 0, 0, 1, 1] → x=19 → f(x)=361
  [1, 0, 0, 1, 1] → x=19 → f(x)=361

 Melhor: x = 23 → f(x) = 529

==================== GERAÇÃO 3 ====================

Avaliação dos indivíduos:
  [1, 0, 1, 1, 1] → x=23 → f(x)=529
  [1, 1, 0, 1, 1] → x=27 → f(x)=729
  [1, 0, 0, 1, 0] → x=18 → f(x)=324
  [1, 0, 0, 1, 1] → x=19 → f(x)=361
  [1, 0, 0, 1, 1] → x=19 → f(x)=361
  [1, 0, 0, 1, 0] → x=18 → f(x)=324

 Melhor: x = 27 → f(x) = 729

==================== GERAÇÃO 4 ====================

Avaliação dos indivíduos:
  [1, 1, 0, 1, 1] → x=27 → f(x)=729
  [1, 1, 0, 1, 1] → x=27 → f(x)=729
  [1, 1, 1, 1, 1] → x=31 → f(x)=961
  [1, 1, 0, 1, 1] → x=27 → f(x)=729
  [1, 0, 0, 1, 1] → x=19 → f(x)=361
  [0, 1, 0, 1, 1] → x=11 → f(x)=121

 Melhor: x = 31 → f(x) = 961

==================== GERAÇÃO 5 ====================

Avaliação dos indivíduos:
  [1, 1, 1, 1, 1] → x=31 → f(x)=961
  [1, 1, 0, 1, 1] → x=27 → f(x)=729
  [1, 1, 1, 1, 1] → x=31 → f(x)=961
  [0, 1, 0, 1, 1] → x=11 → f(x)=121
  [1, 1, 0, 1, 1] → x=27 → f(x)=729
  [1, 1, 1, 1, 1] → x=31 → f(x)=961

 Melhor: x = 31 → f(x) = 961

==================== GERAÇÃO 6 ====================

Avaliação dos indivíduos:
  [1, 1, 1, 1, 1] → x=31 → f(x)=961
  [1, 1, 0, 1, 1] → x=27 → f(x)=729
  [1, 1, 1, 1, 1] → x=31 → f(x)=961
  [0, 1, 1, 1, 1] → x=15 → f(x)=225
  [0, 1, 1, 1, 1] → x=15 → f(x)=225
  [1, 1, 1, 1, 1] → x=31 → f(x)=961

 Melhor: x = 31 → f(x) = 961

==================== GERAÇÃO 7 ====================

Avaliação dos indivíduos:
  [1, 1, 1, 1, 1] → x=31 → f(x)=961
  [1, 1, 1, 1, 1] → x=31 → f(x)=961
  [1, 1, 1, 1, 1] → x=31 → f(x)=961
  [1, 1, 0, 1, 1] → x=27 → f(x)=729
  [1, 1, 1, 0, 1] → x=29 → f(x)=841
  [1, 1, 1, 1, 1] → x=31 → f(x)=961

 Melhor: x = 31 → f(x) = 961

==================================================
RESULTADO FINAL
==================================================

Melhor indivíduo: [1, 1, 1, 1, 1]
x = 31
f(x) = 961

Ótimo global: x = 31, f(x) = 961
Erro: 0
<img width="850" height="393" alt="image" src="https://github.com/user-attachments/assets/524a955b-8424-468f-a486-77a46b23e444" />

Comentários:
Os resultados mostram que o algoritmo genético evoluiu progressivamente para soluções melhores ao longo das gerações. O melhor indivíduo passou de 
x=20, na geração 0, para x=31, na geração 4, mantendo esse resultado até a geração 7.

O indivíduo [1,1,1,1,1] representa o maior valor possível com 5 bits, x=31, resultando em f(x)=961. 
Assim, o algoritmo encontrou o ótimo global, apresentando erro igual a 0 e demonstrando uma boa convergência da população.


LAB 02

==================================================
ONEMAX - AG com 30 indivíduos, 50 gerações
==================================================
Geração   0: Melhor = 15/20, Média = 10.90
Geração  10: Melhor = 20/20, Média = 19.63
Geração  20: Melhor = 20/20, Média = 19.57
Geração  30: Melhor = 20/20, Média = 19.43
Geração  40: Melhor = 20/20, Média = 19.53

 MELHOR FITNESS: 20/20
   Ótimo = 20 (todos os bits são 1)
<img width="1188" height="390" alt="image" src="https://github.com/user-attachments/assets/95e43ff0-1490-4cf4-8d0b-fb6ab79e71c7" />
<img width="1188" height="390" alt="image" src="https://github.com/user-attachments/assets/04386bb3-fd47-4e90-8c35-d557f9614c2d" />


==================================================
DESAFIO: Mude os parâmetros e veja o que acontece!
==================================================
1. Aumente a TAXA_MUT para 0.1. O que acontece? aumenta a diversidade da população, mas também pode dificultar a convergência por alterar indivíduos que já são bons.
2. Diminua POPULACAO para 10. O que acontece? diminui a diversidade genética, podendo tornar a busca menos eficiente e aumentar a chance de convergência prematura
3. Aumente GERACOES para 100. O que acontece? oferece mais tempo para o algoritmo evoluir, aumentando a chance de manter ou encontrar a solução ótima.
4. Mude ELITE para 0. O que acontece? nenhum indivíduo é preservado diretamente para a próxima geração. Isso pode fazer com que soluções boas sejam perdidas, tornando a evolução menos estável.

Comentários:
Os resultados mostram que o algoritmo genético conseguiu encontrar o ótimo do problema ONEMAX, atingindo fitness 20/20, com todos os bits iguais a 1. 
A média da população também aumentou, indicando evolução ao longo das gerações. Ao aumentar a mutação, há mais diversidade, mas pode haver maior instabilidade; com uma população menor, a diversidade diminui; 
com mais gerações, há mais tempo para encontrar a solução ideal; e sem elitismo, boas soluções podem ser perdidas. Portanto, a escolha dos parâmetros influencia diretamente a eficiência e a estabilidade do algoritmo.


LAB 03
==================================================
OTIMIZANDO f(x) = x * sin(3x)
==================================================
Geração   0: Melhor f(x) = 8.0645 (x = 9.0588)
Geração  10: Melhor f(x) = 8.9019 (x = 8.9020)
Geração  20: Melhor f(x) = 8.9019 (x = 8.9020)
Geração  30: Melhor f(x) = 8.9019 (x = 8.9020)
Geração  40: Melhor f(x) = 8.9019 (x = 8.9020)
<img width="1189" height="490" alt="image" src="https://github.com/user-attachments/assets/0670ae5f-551b-452f-8026-db706b81526e" />
![Uploading image.png…]()


 MELHOR SOLUÇÃO: x = 8.9020, f(x) = 8.9019

Comentários:
Os resultados mostram que o algoritmo genético conseguiu melhorar a solução ao longo das gerações, passando de 
f(x) = 8,0645 na geração 0 para f(x)=8,9019
na geração 10. A partir daí, o resultado permaneceu estável, indicando que o algoritmo convergiu para uma boa solução. 
O melhor resultado encontrado foi x = 8,9020, com f(x) = 8,9019, demonstrando que o algoritmo conseguiu otimizar a função com sucesso.
