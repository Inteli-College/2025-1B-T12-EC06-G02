---
sidebar_position: 1
slug: /desenvolvimento-tecnico/ia-classificacao/preparacao
---

# Preparação dos Dados

## Dataset

&emsp; Para o desenvolvimento de um modelo de Inteligência Artificial de Classificação, como é o caso da IA deste projeto, o primeiro passo é elaborar um _dataset_. Esse passo foi cumprido pelo próprio parceiro do projeto, o IPT, o qual reuniu sessenta imagens de drones:
- 30 imagens de **fissuras térmicas** (primeira categoria);
- 30 imagens de **fissuras de retração** (segunda categoria);

:::warning[Aviso]
Percebe-se que esse _dataset_ não é abrangente. Portanto, há um risco maior de falhas no modelo devido à falta de dados.
:::

## Pré-processamento

&emsp; O segundo passo é o pré-processamento dos dados. Abaixo vê-se o exemplo de uma das imagens que a SOD recebeu.

<p style={{textAlign: 'center'}}>Figura 1: Fissura de Retração Antes do Processamento</p>
<div style={{margin: 25}}>
    <div style={{textAlign: 'center'}}>
        <img src={require("../../../../static/img/retracao.png").default} alt="Imagem de fissura de retração sem qualquer tratamento" />
        <br />
    </div>
</div>
<p style={{textAlign: 'center'}}>Fonte: IPT (2024?). </p>

&emsp; Para tratar essas imagens, resolveu-se por seguir o pré-processamento realizado por especialistas, como se segue:
- Redimensionamento de 640x640 (Ultranalytics, 2023)
- Conversão para a escala de cinza (CHUN, P. et _al_, 2020)
- Correção com filtro mediano (ibid.) 

&emsp; A primeira transformação foi feita para que o _dataset_ se adequasse ao _dataset_ de trincas criado pela Ultranalytics. Visa-se, com isso, reaproveitar imagens dessa coleção no treinamento ou na validação da primeira (filtro para fissuras) ou da segunda IA (classificação de fissuras).

&emsp; A segunda transformação foi feita visando diminuir o tempo de cálculo da IA. Evidencia-se, porém, que para a seleção do valor do pixel central, não foi usada qualquer média do RGB. Em vez disso, aplicou-se o valor máximo dentre os canais, a fim de clarear a superfície que contém a rachadura, deixando-a mais evidente (ibid.).

&emsp; A terceira transformação foi feita para que se diminuísse o efeito de sombras e contaminações nas imagens. Para tanto, aplicou-se o filtro mediano de 41x41, utilizando a biblioteca [OpenCV](https://opencv.org/). Segundo CHUN, P. et _al_(2020), apesar do tamanho do filtro não ter uma forte influência no resultado das imagens - filtros menores deixam as fissuras mais finas e vice-versa, o tamanho 41x41 permite a correção, sem grande influência no tamanho da fissura. Em seguida, aplicou-se a fórmula que se segue na imagem:

<p style={{textAlign: 'center'}}>Figura 2: Fórmula de Correção</p>
<div style={{margin: 25}}>
    <div style={{textAlign: 'center'}}>
        <img src={require("../../../../static/img/formula.png").default} alt="Fórmula de correção" />
        <br />
    </div>
</div>
<p style={{textAlign: 'center'}}>Fonte: CHUN, P. et <i>al</i> (2020). </p>

Em que:
- Ia = imagem após a correção
- Ib = imagem antes da correção
- Im = filtro de mediana antes da correção
- bm = valor máximo do pixel (ibid.)

&emsp; Isso permite que se corrija diferenças em contrastes e sombras sem que se perca variações locais pequenas, como as rachaduras. Isso pode ser percebido na Figura 3.

<p style={{textAlign: 'center'}}>Figura 3: Fórmula de Correção</p>
<div style={{margin: 25}}>
    <div style={{textAlign: 'center'}}>
        <img src={require("../../../../static/img/efeito-correcao.png").default} style={{width: 800}} alt="Imagem de fissura de retração sem qualquer tratamento" />
        <br />
    </div>
</div>
<p style={{textAlign: 'center'}}>Fonte: CHUN, P. et <i>al</i> (2020). </p>

&emsp; Todas essas transformações estão expostas no seguinte arquivo: [``src/IA_classificacao/preProcessamento/preProcessamento.py``](../../../../../src/IA_classificacao/preProcessamento/preProcessamento.py) em que se define uma função para processar cada imagem e retorna a própria imagem filtrada.

## Resultado

&emsp; Abaixo, compara-se a imagem antes do tratamento e após o tratamento. 

<p style={{textAlign: 'center'}}>Figura 4: Comparação</p>
<div style={{margin: 25}}>
    <div style={{textAlign: 'center'}}>
        <img src={require("../../../../static/img/comparacao.png").default} style={{width: 800}} alt="Comparação entre a imagem sem correção e a imagem pré-processada" />
        <br />
    </div>
</div>
<p style={{textAlign: 'center'}}>Fonte: CHUN, P. et <i>al</i> (2020). <br/> <small> Legenda: À esquerda vê-se a imagem sem correção. À direita, a imagem pré-processada. <br/> OBS: Para efeitos de comparação, redimensionou-se ambas as imagens.</small></p>

&emsp; Como se percebe, remove-se a complexidade da imagem transformando-a em escala de cinza. Além disso, as rachaduras estão mais realçadas (na medida do possível), enquanto algumas manchas, principalmente no centro da parede foram retiradas. Imagens como essa serão usadas no treinamento da IA na seção que se segue.


## Bibliografia

* CHUN, P.; IZUMI, S.; YAMANE, T. Automatic detection method of cracks from concrete surface imagery using two‐step light gradient boosting machine. Computer-Aided Civil and Infrastructure Engineering, v. 36, n. 1, p. 61–72, 20 maio 2020.

* ULTRALYTICS. Crack Segmentation Dataset. Disponível em: https://docs.ultralytics.com/datasets/segment/crack-seg/. Acesso em: 8 maio. 2025. 


