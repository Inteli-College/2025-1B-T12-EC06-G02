---
sidebar_position: 2
slug: /inteligencia-artificial/roboflow
description: "Ferramenta utilizada para fazer labels no dataset"
---

# Dataset

&emsp; Para o desenvolvimento do nosso sistema de segmentação e detecção de fissuras em imagens, foi necessário montar um dataset com anotações específicas que representassem com precisão os elementos de interesse, no caso, as fissuras com seus diferentes tipos. Para isso, utilizamos o **Roboflow**, uma plataforma online que fornece um conjunto robusto de ferramentas para gerenciamento e anotação de dados em projetos de visão computacional. A escolha por essa plataforma se deu pela sua facilidade de uso, compatibilidade com múltiplos formatos de exportação, recursos de anotação colaborativa e automações úteis, como divisão automática do conjunto de dados e aplicação de aumentações, nos auxiliando muito no processo de desenvolvimento dos modelos de IA nessa sprint.

## Roboflow

&emsp; O Roboflow é uma ferramenta que permite aos usuários criar, anotar, transformar e exportar datasets para tarefas de visão computacional, como detecção de objetos, classificação de imagens e segmentação de instâncias. A plataforma suporta diversos formatos de anotação, incluindo YOLO, COCO, Pascal VOC, entre outros. Além disso, ela oferece integração com frameworks populares de machine learning, tornando o processo de treinamento e validação de modelos mais acessível e eficienten nos permitindo criar e treinar os modelos dentro do próprio site (porém, não foi o caso de uso do grupo). Para o nosso projeto e o desenvolvimento dessa sprint, utilizamos o Roboflow para criar nosso dataset com as labels corretas para, depois de finalizado, exportarmos para o uso no modelo. A usabilidade intuitiva e as funcionalidades de versionamento tornam o Roboflow uma opção ideal para um projeto organizado.

## Processo de criação do DATASET

&emsp; O processo de criação do dataset começou com a criação de um novo projeto na plataforma. Para isso, acessamos o site oficial do Roboflow e, após realizar login com uma conta institucional, iniciamos um novo projeto, selecionando o tipo "Object Detection", já que o objetivo era detectar fissuras por meio de caixas delimitadoras (bounding boxes). Também escolhemos o formato de anotação YOLOv5, que é compatível com os modelos e ferramentas que estávamos utilizando.

&emsp; Em seguida, realizamos o upload das imagens. As imagens foram carregadas diretamente para o projeto, podendo ser organizadas posteriormente entre os conjuntos de treino, validação e teste. O Roboflow oferece a possibilidade de realizar essa divisão automaticamente com base em proporções definidas pelo usuário, o que utilizamos para separar 70% das imagens para treino, 20% para validação e 10% para teste.

&emsp; O próximo passo foi a anotação das imagens. As anotações foram realizadas diretamente na interface do Roboflow, que permite desenhar bounding boxes sobre as imagens e atribuir a elas classes específicas — neste caso, a classe principal foi "fissuras", mas fizemos a separação de quias eram de retração e quais eram térmicas. A interface de anotação é intuitiva e possibilita zoom, movimentação da imagem, revisão das anotações já feitas e sugestões automáticas com ferramentas de AutoLabel, que podem acelerar o processo em datasets maiores. Também é possível revisar as anotações manualmente antes de seguir para a próxima etapa.

&emsp; Após as anotações, utilizamos o recurso de geração do Roboflow para criar uma versão do dataset consolidada. Essa versão foi exportada em formato YOLOv5, que consiste em arquivos .txt contendo as anotações de cada imagem no seguinte formato: <class_id> <x_center> <y_center> <width> <height>, todos com valores normalizados entre 0 e 1. O arquivo de anotação acompanha cada imagem e é armazenado na mesma pasta. A estrutura final gerada pela exportação incluía diretórios separados para treino, validação e teste, cada um contendo suas respectivas imagens e anotações.

## Conclusão

&emsp; O uso do Roboflow na geração do nosso dataset foi essencial para garantir a qualidade e a padronização das anotações, o que era de extrema importância para conseguirmos treinar bons modelos para detecção ou segmentação das fissuras. A plataforma não apenas facilitou a organização dos dados, mas também permitiu maior controle sobre a preparação e manipulação do conjunto de imagens. Com isso, obtivemos um dataset limpo, bem estruturado e pronto para uso em treinamentos com modelos como o YOLO e o Segment Anything (SAM), os dois modelos testados durante a Sprint 4 de desenvolvimento do projeto.

