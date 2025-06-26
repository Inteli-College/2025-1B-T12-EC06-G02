---
sidebar_position: 3
slug: /sprint-5/entrega-final
description: "Resumo da entrega final"
---

# Entrega Final

## Introdução

&nbsp;&nbsp;&nbsp;&nbsp;A detecção precoce de manifestações patológicas em edificações, como as fissuras em fachadas, constitui uma etapa fundamental para a manutenção da segurança estrutural e da durabilidade das construções. Entretanto, os métodos tradicionalmente empregados para essa finalidade atualmente baseiam-se, em grande parte, em inspeções visuais manuais, as quais apresentam limitações significativas em termos de padronização, precisão e reprodutibilidade dos resultados. Além disso, a ausência de registros e históricos compromete o acompanhamento da evolução dessas patologias, dificultando a formulação de diagnósticos e intervenções eficazes.

&nbsp;&nbsp;&nbsp;&nbsp;Com base nisso, há uma necessidade de soluções tecnológicas que viabilizem a automação e a qualificação dos processos de inspeção predial. O projeto atual, desenvolvido em parceria com o Instituto de Pesquisas Tecnológicas(IPT), propõe a implementação de um sistema inteligente de detecção e análise de fissuras, baseado em técnicas de visão computacional e aprendizagem profunda. A proposta visa mitigar os problemas associados à subjetividade das inspeções manuais, bem como fornecer subsídios técnicos para a tomada de decisões fundamentadas em dados quantitativos e estruturados.

&nbsp;&nbsp;&nbsp;&nbsp;A solução desenvolvida contempla um fluxo completo, que abrange desde a captura automatizada de imagens por meio de drones, até o processamento e classificação das fissuras por meio de redes neurais convolucionais. Os resultados obtidos demonstram a viabilidade técnica da abordagem e indicam seu potencial de aplicação em ambientes reais, contribuindo para o avanço das práticas de monitoramento de edificações e para a consolidação de estratégias de manutenção preditiva.

&nbsp;&nbsp;&nbsp;&nbsp;Esta documentação apresenta a fundamentação, o desenvolvimento metodológico, os resultados obtidos e as perspectivas futuras da solução proposta.

## O parceiro de projeto: IPT 

&nbsp;&nbsp;&nbsp;&nbsp;Como citado na introdução, o parceiro de projeto é o IPT. O Instituto de Pesquisas Tecnológicas do Estado de São Paulo (IPT) é uma instituição pública vinculada à Secretaria de Desenvolvimento Econômico do Estado de São Paulo. Com mais de 125 anos de atuação, o IPT é reconhecido por sua excelência em pesquisa aplicada, desenvolvimento tecnológico e prestação de serviços especializados.

&nbsp;&nbsp;&nbsp;&nbsp;Dentro desse contexto, destaca-se o Laboratório de Materiais para Produtos da Construção (LMPC), que desempenha um papel central neste projeto. O LMPC é responsável por pesquisas e testes de desempenho de materiais utilizados na construção civil e contribui significativamente para a qualidade, segurança e sustentabilidade dos edificios. Com sua parceria para este projeto, é garantido o embasamento técnico necessário para orientar o desenvolvimento da solução e validar seus resultados referente a identificação e classificação de fissuras.

## Problema

&nbsp;&nbsp;&nbsp;&nbsp;O desafio apresentado pelo IPT está relacionado à ausência de soluções automatizadas e precisas para a detecção de fissuras em fachadas de edificações. Atualmente, a maioria das inspeções é realizada de forma visual e manual, o que demanda tempo, depende da experiência dos técnicos e nem sempre garante a confiabilidade dos resultados. Além disso, a falta de registros históricos e acompanhamento da evolução das fissuras compromete a tomada de decisão e a efetividade das intervenções preventivas.

&nbsp;&nbsp;&nbsp;&nbsp;Esse cenário acarreta diversos problemas para o setor da construção civil, e entre eles:

- Aumento dos custos com manutenção corretiva, já que falhas são identificadas tardiamente;

- Risco à segurança estrutural, devido à ausência de monitoramento contínuo;

- Dificuldade de priorização das intervenções, em função da carência de dados quantitativos e históricos;

- Baixa eficiência no uso de recursos, por falta de sistemas integrados de apoio à decisão.

&nbsp;&nbsp;&nbsp;&nbsp;Diante disso, o IPT propôs o desenvolvimento de um algoritmo de detecção e análise de fissuras, com apoio de visão computacional e inteligência artificial, visando automatizar o processo, gerar relatórios técnicos com dados estruturados e permitir o monitoramento contínuo da evolução das patologias. A proposta traz um alto potencial de impacto no setor, tanto por aumentar a segurança das edificações, quanto por reduzir custos e melhorar a eficiência operacional.

## Solução

&emsp; Em vias de resolver o problema descrito acima, criou-se o Sistema de Detecção de Fissuras da SOD. Retomando a introdução dessa documentação:

> "Um sistema para a detecção de fissuras em edificações que utiliza técnicas avançadas de processamento de imagens e inteligência artificial para identificar fissuras, permitindo manutenções preventivas e aumentando a segurança das edificações."

&emsp; Destrincharemos abaixo o significado desse resumo da solução em três partes:

- Sistema para Detecção de Fissuras;
- Processamento de imagem e IA
- Resultados do Sistema

### Sistema para Detecção de Fissuras

&emsp; Na primeira sprint do projeto, definiu-se os [requisitos funcionais](../sprint-1/especificacoes-tecnicas/Requisitos_Funcionais.md) e [não funcionais](../sprint-1/especificacoes-tecnicas/Requisitos_Nao_Funcionais.md) de um sistema que seria capaz de detectar fissuras em edificações. Além disso, concebeu-se a sua [arquitetura inicial](../sprint-1/especificacoes-tecnicas/Arquitetura_Inicial.md), a qual foi iterada na sprint 2 - ver [Atualizações na Arquitetura](../sprint-2/desenvolvimento-tecnico-do-sistema/proposta-da-arquitetura.md). Contemplava-se nessas seções um sistema dividido em três partes: Captura, Processamento e Análise.

&emsp; A primeira parte, integrada ao sistema _a posteriori_, reserva-se ao piloto. À ele, é dada a tarefa de capturar fotos de fissuras por meio de drones como as que se seguem:

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

&emsp; Então, inicia-se a etapa do processamento. Primeiro, uma inteligência artificial detecta onde estão as fissuras em cada imagem recebida. Essas detecções aparecem como quadrados na figura - exemplos de detecções reais podem ser vistas abaixo.

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

&emsp; Em seguida, cada imagem de fissura passa por um processamento que a padroniza para ser adequamente recebida pela próxima IA. Esse processo foi finalizado na [sprint 4](../sprint-4/inteligencia-artificial/modelos/yolov8.md).

&emsp; Por fim, inicia-se a etapa de análise, responsável pelo auxílio real ao pesquisador. Primeiro, outra inteligência artificial recebe essas imagens. Ela, então, analisa cada uma para decidir:

- É uma fissura **de retração**;
- ou é uma fissura **térmica**.

&emsp; Essas decisões individuais são condensadas em um relatório conforme _template_ do IPT. Essa etapa foi finalizada na [sprint 3](../sprint-3/inteligencia-artificial/modelos/segundo-modelo-s3.md) e integrada na última sprint. [Um dos relatórios produzidos podem ser acessados via Google Drive, clicando aqui.](https://drive.google.com/file/d/1PvO6_B9amQCWWPqQ5Z1rJVm6Q_GNVlK6/view?usp=sharing)


### Processamento de Imagem e IA

&emsp; Para a implementação do sistema de classificação, foram utilizados dois modelos distintos. O **ResNet-18** foi empregado como um modelo experimental de classificação, utilizado para testes e comparações iniciais, permitindo avaliar a viabilidade da abordagem proposta. Enquanto, o **Swin Transformer V2** foi selecionado como o modelo de classificação implementado em produção, escolhido por sua capacidade de generalização e melhor desempenho na tarefa de classificação de fissuras em diferentes condições de captura.

&emsp; Então, para padronizar as entradas do Swin Transformer V2 frente a diversas condições de captura é realizado automaticamente um pré-processamento. Esse pré-processamneto, realizado na etapa geral de [processamento](#problema) é descrito abaixo:

1.  **Carregamento:** Suporte a formatos de imagem comuns (`.jpg`, `.jpeg`, `.png`, `.bmp`, `.tiff`).
2.  **Redimensionamento:** Utilização da técnica de **Square Padding** para preservar as proporções originais das imagens, resultando em um tamanho consistente de 224x224 pixels, evitando distorções.
3.  **Melhoramento de Contraste:** Aplicação do **CLAHE** com `clipLimit=3.0` e `tileGridSize=(8,8)` no espaço de cor LAB para realçar fissuras sutis.
4.  **Realce de Bordas:** Uso do **Sharpening Laplaciano** com `strength=1.2` para destacar as transições que caracterizam as fissuras.
5.  **Equalização Seletiva:** Aplicação condicional de equalização de histograma no espaço de cor YUV para preservar informações cromáticas.

&emsp; Além do modelo de classificação, na etapa de detecção, foi utilizado [YOLOv8](https://yolov8.com/), empregado para identificar a localização das fissuras nas imagens. [Esse modelo é amplamente reconhecido por sua eficiência em tarefas de detecção de objetos.](../sprint-4/inteligencia-artificial/modelos/yolov8.md)

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

## Testes 

&emsp; Este documento apresenta os resultados de uma série de testes de usuário conduzidos com o objetivo de avaliar a usabilidade e a experiência geral de um novo sistema. Os testes foram desenhados para simular cenários de uso reais, abrangendo desde o processo inicial de cadastro e login até tarefas mais complexas, como o upload e organização de imagens para processamento por inteligência artificial, download de relatórios e registro de projetos. Durante as sessões, foram observadas as interações dos participantes com o sistema, registrando-se as dificuldades encontradas, os pontos fortes e as áreas que necessitam de melhoria.

Link para a tabela de testes: [Testes](https://docs.google.com/spreadsheets/d/1at2blUQKvejzAVJVXDZdqZFijH8p6N0RNbcikerFWuM/edit?usp=sharing)


## Próximos Passos

&emsp; A solução apresentada nessa seção se trata de uma Prova de Conceito (POC). Não obstante, a equipe realizou uma análise financeira que suporta a implementação real do projeto no IPT ou em qualquer outra instituição no mesmo ramo, conforme o [Business Model Canva da SOD](../sprint-1/analise-de-negocios/business_model_canvas.md). Essa análise pode ser encontrada [aqui](../sprint-4/analise-financeira/analise-financeira-solucao-final.md). Adianta-se, porém, que o preço da solução ficou em R$ 481.951,22 para desenvolvimento e implementação, seguido de uma manutenção anual de R$ 166.829,27.

&emsp; Ademais, a equipe idealizou próximos passos que podem definir o próximo nível dessa tecnologia:

1. Adaptar o aplicativo para controlar outros drones, além do DIJ Tello;
2. Implementar o processo de auditoria humana, conforme o [RF07](../sprint-1/especificacoes-tecnicas/Requisitos_Funcionais.md)
3. Conseguir classificar outros tipos de fissura;
4. Implementar uma inteligência artificial para prever a evolução da fissura;

&emsp; A realização desses passos permitirá elevar a maturidade tecnológica da solução, aproximando-a de um produto pronto para o mercado. Com a adaptação para outros modelos de drone, amplia-se a aplicabilidade em diferentes contextos operacionais. A implementação de auditoria humana aumentaria a acurácia da solução, enquanto a classificação de diferentes tipos de fissura poderá ampliar o escopo de uso em inspeções diversas. Por fim, o desenvolvimento de uma IA preditiva representará um avanço significativo, permitindo que as instituições atuem de forma preventiva, evitando danos maiores e reduzindo custos operacionais ao longo do tempo.

