margin 2,5
colw 13,6

col1 13,6 + 2,5 = 16,1
col2 16,1 + 13,6 = 29,7
col3 29.7 + 13,6 = 43,3


# Poster

## Introdução

Neste trabalho analisamos, experimentalmente, a aplicação de métodos morfológicos à segmentação de páginas, etapa importante na análise de documentos que busca extrair informações sobre a sua estrutura: regiões com títulos, figuras e parágrafos. A qualidade da solução obtida foi medida e comparada a soluções consideradas estado da arte por pesquisadores da área.

## Segmentação de páginas de documentos

Segmentação de página refere-se à tarefa de separar e rotular os diferentes componentes que fazem parte da estrutura das páginas de um documento. Um exemplo de segmentação é apresentado na figura 2.

______
_fig2_
______

Em geral, a segmentação de página é um dos primeiros passos no
processo de entendimento de um documento. Uma vez identificados os blocos estruturais, processamentos específicos para cada tipo de bloco podem ser aplicados. Por exemplo, no caso de blocos de textos é conveniente fazer o reconhecimento de texto para que o mesmo possa ser armazenado em formato texto (e não imagem). Documentos digitalizados podem ser processados
eficientemente em processos que envolvem armazenamento, edição,
transmissão, ou busca, por exemplo.

## Operadores morfológicos binários

Operadores morfológicos binários constituem uma classe de transformações sobre imagens que tem por objetivo analisar características geométricas da mesma. Um exemplo básico é o do operador elementar erosão ilustrado na figura 3.

______
_fig3_
______

## Operadores morfológicos automaticamente gerados

Em problemas complexos como o de segmentação de página, construir um operador morfológico através da combinação de diferentes operadores mais simples é uma tarefa que requer muito esforço e experiência. Desta forma utilizamos uma técnica de aprendizado computacional para construção automática de operadores.

- Conclusão

Ajustar o tamanho da janela é um problema computacionalmente custoso porém muito importante para conseguir bons resultados. Janelas muito pequenas costumam apresentar taxas de erro mais altas pois ocorrem muitos conflitos na etapa de contagem de frequência dos padrões. Já as janelas muito grandes sofrem com as lacunas de padrões que nunca ocorrem nos exemplos.
Componentes maiores e mais densas, como os títulos, apresentam resultados melhores com janelas esparsas enquanto os parágrafos se comportam melhor com janelas densas.

1x1
0.016375
0.016375
0.012606
0.012606
3x3
0.016375
0.016375
0.012606
0.050985
5x5
0.010816
0.011849
0.007992
0.008784
7x7
0.005740
0.009602
0.004328
0.031419
9x9
0.002289
0.006593
0.001840
0.004435
11x11
0.001023
0.006157
0.000867
0.020701


function drawVisualization() {
  // Create and populate the data table.
  var data = google.visualization.arrayToDataTable([
    ['x', 'Parágrafos com janelas densas', 'Parágrafos com janelas esparsas', 'Títulos com janelas densas', 'Títulos com janelas esparsas'],
    ['1x1','0.016375','0.016375','0.012606','0.012606'],
    ['3x3','0.016375','0.016375','0.012606','0.050985'],
    ['5x5','0.010816','0.011849','0.007992','0.008784'],
    ['7x7','0.005740','0.009602','0.004328','0.031419'],
    ['9x9','0.002289','0.006593','0.001840','0.004435'],
    ['11x11','0.001023','0.006157','0.000867','0.020701']
  ]);

  // Create and draw the visualization.
  new google.visualization.LineChart(document.getElementById('visualization')).
      draw(data, {curveType: "function",
                  width: 500, height: 400,
                  vAxis: {maxValue: 10}}
          );
}
​

# Perguntas

Quão bem um OM classifica uma região?
- tipo de região
- tamanho da janela

Fixada a janela 9x9, construir operadores utilizando subconjuntos das imagens de teste

Quão bem um OM treinado com um conjunto X generaliza para um conj. Y?

# Sensibilidade à quantidade de amostra X janela X generalização
1. gerar imgsets para treinamento de cada publicação de cada região com subconjuntos das páginas de cada publicação. 1/3 e 2/3

2. Criar operadores de 2x2 à 4x4 esparsos para cada imgset (região)

4. Gerar imgsets de teste com todas as páginas das publicações.

3. Aplicar operadores à imgsets de teste de cada publicação.

4. gráficos com janelas na absissa, curvas para diferentes tamanhos de trainingsets, diferentes regiões, diferentes publicações.
