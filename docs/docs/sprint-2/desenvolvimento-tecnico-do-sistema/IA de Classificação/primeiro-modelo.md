---
sidebar_position: 2
slug: /desenvolvimento-tecnico/ia-classificacao/primeiro-modelo
---

# Primeiro Modelo

&emsp; Como exposto no [Business Model Canva](../../../sprint-1/analise-de-negocios/business_model_canvas.md), uma das atividades chave da SOD é o "Desenvolvimento do algoritmo principal, com IA treinada para detecção e **classificação de fissuras**". Nessa sprint focamos na segunda parte dessa atividade, a IA para a classificação de fissuras. O modelo treinado está em [``src/IA_classificacao/teachableMachine/keras_model.h5``](../../../../../src/IA_classificacao/teachableMachine/keras_model.h5). Nessa seção, visualizar-se-á o processo de criação deste primeiro modelo desde a escolha da _Teachable Machine_ até a aplicação das métricas.

## Por que usar a _Teachable Machine_?

&emsp; O _Teachable Machine_ é uma ferramenta web criada pelo Google Creative Lab - Experiments with Google para _deep learning_ (Google, 2019). A ferramenta é baseada no TensorFlow.js e ajuda os usuários a criar e exportar modelos de classificação sem a necessidade de código (Google, 2019). Apesar de ter ferramentas para classificar imagens, sons e poses, para este projeto, a classificação de imagens foi suficiente.

&emsp; Essa ferramenta foi a primeira candidata para o modelo de IA da SOD devido aos seguintes motivos:
- Facilidade de uso;
- Treinamento rápido;
- Confiabilidade do provedor (Google);

&emsp; Observa-se que, por meio dessa plataforma, consegue-se treinar e avaliar um modelo confiável rapidamente. Sendo assim, foi possível angariar os primeiros resultados do [pré-processamento apresentado na seção anterior](./preparacao.md) antes da Review dessa sprint e assim, elaborar junto ao parceiro, hipóteses de filtro que melhorem o desempenho do algoritmo.

## Treinando o modelo

&emsp; Em vias de treinar o modelo, os seguintes passos foram tomados:
1. Pré-processamento do _dataset_ usando a função presente no arquivo [``src/IA_classificacao/preProcessamento/preProcessamento.py``](../../../../../src/IA_classificacao/preProcessamento/preProcessamento.py);
2. Separação das imagens pré-processadas de forma randomizada em três categorias com balanceamento das classes: 
    - Treinamento (80%)
    - Validação(10%)
    - Teste(10%);
3. Treinamento da _Teachable Machine_ usando as duas classes (Retração e Térmicas), o conjunto de treinamento e as seguintes configurações:
    - Épocas: 500
    - Batch Size: 16
    - Taxa de Aprendizado: 0,00209;

:::info[Informação]

&emsp; Essas configurações foram atingidas após diversos testes para melhorar as métricas de acurácia da validação

:::

4. Exportação do modelo treinado usando Keras.

## Adequando o modelo

&emsp; Após a exportação do modelo, era necessário, para atingir o [RF01](../../../sprint-1/especificacoes-tecnicas/Requisitos_Funcionais.md), uma função que recebesse apenas o caminho de uma imagem, a pré-processasse e devolvesse a previsão do modelo. Essa função está no arquivo [``src/IA_classificacao/teachableMachine/prever.py``](../../../../../src/IA_classificacao/teachableMachine/prever.py).

&emsp; Em primeiro lugar, o arquivo adequa a versão do modelo exportado pela Teachable Machine à versão mais recente do Tensorflow por meio de um [algoritmo criado pelo usuário Jurgen_Thomas do Google AI Developers Forum no tópico "Cannot load .h5 model"](https://discuss.ai.google.dev/t/cannot-load-h5-model/42465/3). Em seguida, a função prever é definida. Nela, carrega-se o modelo e os _labels_, e pré-processa-se a imagem usando a função ``processa_imagem`` apresentada na [seção anterior](./preparacao.md).

&emsp; Após isso, fez-se um pré-processamento adicional, necessário para modelos baseados na _Teachable Machine_:
- Converteu-se a imagem de volta para RGB e formato compatível com a biblioteca Pillow;
- 






