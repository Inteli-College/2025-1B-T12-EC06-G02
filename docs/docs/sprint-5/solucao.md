---
sidebar_position: 2
slug: /entrega-final/solucao
---

# Solução

&emsp; Em vias de resolver o problema descrito acima, criou-se o Sistema de Detecção de Fissuras da SOD. Retomando a introdução dessa documentação:

> "Um sistema para a detecção de fissuras em edificações que utiliza técnicas avançadas de processamento de imagens e inteligência artificial para identificar fissuras, permitindo manutenções preventivas e aumentando a segurança das edificações."

&emsp; Destrincharemos abaixo o significado desse resumo da solução em três partes:

- Sistema para Detecção de Fissuras;
- Processamento de imagem e IA
- Resultados do Sistema

## Sistema para Detecção de Fissuras

&emsp; Na primeira sprint do projeto, definiu-se os [requisitos funcionais](../sprint-1/especificacoes-tecnicas/Requisitos_Funcionais.md) e [não funcionais](../sprint-1/especificacoes-tecnicas/Requisitos_Nao_Funcionais.md) de um sistema que seria capaz de detectar fissuras em edificações. Além disso, concebeu-se a sua [arquitetura inicial](../sprint-1/especificacoes-tecnicas/Arquitetura_Inicial.md), a qual foi iterada na sprint 2 - ver [Atualizações na Arquitetura](../sprint-2/desenvolvimento-tecnico-do-sistema/proposta-da-arquitetura.md). Contemplava-se nessas seções um sistema dividido em três partes: Captura, Processamento e Análise.

&emsp; A primeira parte, integrada ao sistema _a posteriori_ e _ad captandum_, reserva-se ao piloto. À ele, é dada a tarefa de capturar fotos de fissuras por meio de drones como as que se seguem:

<p style={{textAlign: 'center'}}>Figura 1: Imagens de fissura tiradas por drone</p>
<div style={{margin: 25}}>
    <div style={{textAlign: 'center'}}>
        <img src={require("../../static/img/solucao/imagens-como.png").default} style={{width: 800}} alt="Duas imagens de fissura, uma de retração (à esquerda) e outra térmica (à direita)" />
        <br />
    </div>
</div>
<p style={{textAlign: 'center'}}>Fonte: Produzida pelos Autores (2025). </p>

&emsp; Essas imagens são, então, enviadas para a cloud (servidor no [Supabase](https://supabase.com/)). Desta forma, o pesquisador no IPT é capaz de recuperá-las para inserí-las no sistema.

&emsp; Na sprint 3, conforme a arquitetura final, essa funcionalidade foi adicionada ao sistema. Para tanto, criou-se o SOD App via Android Studio - ver [Instruções de como rodar o aplicativo](./instrucao-de-execucao-do-projeto.md#passo-a-passo-para-executar-o-app). Esse aplicativo permite ao usuário se conectar de forma segura com um drone da DIJ chamado Tello. Nele, o usuário pode capturar imagens e enviar ao servidor diretamente. Vê-se, portanto, como a captura se integrou ao sistema. Essa parte do sistema foi finalizada nesta sprint.

&emsp; Após a captura, dá-se o processamento da imagem. Esse processo acontece, na visão do usuário, em conjunto com a análise. Antes, porém, o pesquisador separa as imagens recebidas manualmente em andar e direção da fachada, como no vídeo a seguir.

<p style={{textAlign: 'center'}}>Vídeo 1: Separação manual por direção e andar</p>
<div style={{margin: 25}}>
    <div style={{textAlign: 'center'}}>
<iframe width="560" height="315" src="https://www.youtube.com/embed/47Vk3KuNCsI?si=8K_6Gw1xhDmdRnCS" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
</div>
</div>
<p style={{textAlign: 'center'}}>Fonte: Produzida pelos Autores (2025). </p>

&emsp; Então, o sistema entra a etapa do processamento. Primeiro, uma inteligência artificial detecta onde estão as fissuras em cada imagem recebida. Essas detecções aparecem como quadrados na figura - exemplos de detecções reais podem ser vistas abaixo

<p style={{textAlign: 'center'}}>Figura 2: Detecções reais de fissuras</p>
<div style={{margin: 25}}>
    <div style={{textAlign: 'center'}}>
        <img src={require("../../static/img/solucao/yolov8.png").default} style={{width: 800}} alt="Várias imagens demonstrando o processo de detecção." />
        <br />
    </div>
</div>
<p style={{textAlign: 'center'}}>Fonte: Produzida pelos Autores (2025). </p>

&emsp; Por fim, essas imagens são cortadas e enviadas para a classificação. Um exemplo ilustrativo está apresentado no vídeo 2.

<p style={{textAlign: 'center'}}>Vídeo 2: Detecção de fissuras</p>
<div style={{margin: 25}}>
    <div style={{textAlign: 'center'}}>
<iframe width="560" height="315" src="https://www.youtube.com/embed/d-1TvYRvA-4?si=GV5WAivGdrknwp-e" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
</div>
</div>
<p style={{textAlign: 'center'}}>Fonte: Produzida pelos Autores (2025). </p>

&emsp; Então, cada imagem de fissura passa por um processamento que a padroniza para ser adequamente recebida pela próxima IA. Esse processo foi finalizado na [sprint 4](../sprint-4/inteligencia-artificial/modelos/yolov8.md).

&emsp; A última etapa do processo é a análise, responsável pelo auxílio real ao pesquisador. Após o processamento, outra inteligência artificial recebe essas imagens. Ela, então, analisa cada uma para decidir:

- É uma fissura **de retração**;
- ou é uma fissura **térmica**.

&emsp; Essas decisões individuais são condensadas em um relatório conforme _template_ do IPT. Essa etapa foi finalizada na [sprint 3](../sprint-3/inteligencia-artificial/modelos/segundo-modelo-s3.md) e integrada na última sprint.

## Processamento de Imagem e IA

&emsp; Para a implementação do sistema de classificação, foram utilizados dois modelos distintos. O **ResNet-18** foi empregado como um modelo experimental de classificação, utilizado para testes e comparações iniciais, permitindo avaliar a viabilidade da abordagem proposta. Enquanto, o **Swin Transformer V2** foi selecionado como o modelo de classificação implementado em produção, escolhido por sua capacidade de generalização e melhor desempenho na tarefa de classificação de fissuras em diferentes condições de captura.

&emsp; Então, para padronizar as entradas do Swin Transformer V2 frente a diversas condições de captura é realizado automaticamente um pré-processamento. Esse pré-processamneto é descrito abaixo:

1.  **Carregamento:** Suporte a formatos de imagem comuns (`.jpg`, `.jpeg`, `.png`, `.bmp`, `.tiff`).
2.  **Redimensionamento:** Utilização da técnica de **Square Padding** para preservar as proporções originais das imagens, resultando em um tamanho consistente de 224x224 pixels, evitando distorções.
3.  **Melhoramento de Contraste:** Aplicação do **CLAHE** com `clipLimit=3.0` e `tileGridSize=(8,8)` no espaço de cor LAB para realçar fissuras sutis.
4.  **Realce de Bordas:** Uso do **Sharpening Laplaciano** com `strength=1.2` para destacar as transições que caracterizam as fissuras.
5.  **Equalização Seletiva:** Aplicação condicional de equalização de histograma no espaço de cor YUV para preservar informações cromáticas.

&emsp; Além do modelo de classificação, na etapa de detecção, foi utilizado [YOLOv8](https://yolov8.com/), empregado para identificar a localização das fissuras nas imagens.

## Resultados do Sistema

&emsp; O Sistema de Detecção de Fissuras da SOD foi concebido para fornecer uma solução completa, desde a captura das imagens até a análise final das fissuras, com o objetivo de permitir manutenções preventivas e aumentar a segurança das edificações. Nesse sentido, apresenta-se os resultados obtidos a partir de dois modelos de rede neural convolucional: ResNet18 e Swin Transformer V2. Segue abaixo os dados obtidos de cada modelo:

| Métrica - ResNet18      | Valor  |
| ----------------------- | ------ |
| Acurácia de validação   | 100%   |
| Loss de validação       | 0.0211 |
| Acurácia de treinamento | 95.31% |
| Loss de treinamento     | 0.0928 |

| Métrica - Swin Transformer V2 | Valor  |
| ----------------------------- | ------ |
| Acurácia de validação         | 96.87% |
| Loss de validação             | 0.223  |
| Acurácia de treinamento       | 97.92% |
| Loss de treinamento           | 0.252  |

&emsp; Com base nos resultados apresentados, o sistema demonstra ser uma ferramenta promissora para a manutenção preventiva e o aumento da segurança em edificações, ao automatizar a detecção e análise de fissuras.
