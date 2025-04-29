---
sidebar_position: 2
custom_edit_url: null
---

# Matriz de Riscos

## Introdução

&nbsp;&nbsp;&nbsp;&nbsp;A matriz de riscos é uma ferramenta fundamental de gestão que permite visualizar, classificar e priorizar os potenciais riscos e oportunidades associados a um projeto. Esta representação gráfica cruza a probabilidade de ocorrência de cada evento com seu respectivo impacto, permitindo uma avaliação sistemática que serve de base para decisões estratégicas e alocação de recursos. No contexto do desenvolvimento de soluções tecnológicas inovadoras, como o algoritmo de processamento digital de imagens para identificação de fissuras proposto pelo IPT, a matriz de riscos torna-se particularmente valiosa, pois projetos pioneiros carregam consigo tanto grandes desafios quanto oportunidades transformadoras.

<p style={{textAlign: 'center'}}>Figura 1 - Matriz de Riscos</p>

<div style={{margin: 25}}>
    <div style={{textAlign: 'center'}}>
        <img src={require("../../../static/img/matrizes-de-riscos.png").default} style={{width: 800}} alt="Matriz de Riscos" />
        <br />
    </div>
</div>

<p style={{textAlign: 'center'}}>Fonte: Os autores (2025)</p>

&nbsp;&nbsp;&nbsp;&nbsp;Nossa matriz de riscos está estruturada em duas seções complementares: ameaças e oportunidades. As ameaças representam eventos que podem prejudicar o sucesso do projeto, enquanto as oportunidades indicam caminhos para potencializar resultados positivos. A análise utiliza uma escala de probabilidade gradativa (10%, 30%, 50%, 70% e 90%) combinada com níveis de impacto que variam de "Muito Baixo" a "Muito Alto". Esta estrutura permite mapear cenários desde desafios técnicos específicos (como insuficiência de dados para reconhecimento de padrões complexos e limitações dos algoritmos preditivos em estruturas não convencionais) até barreiras de implementação (como resistência à adoção por falta de familiaridade com tecnologias digitais e restrições orçamentárias), bem como benefícios potenciais (como economia em manutenções preventivas e automação de relatórios técnicos detalhados).

&nbsp;&nbsp;&nbsp;&nbsp;Ao analisar esta matriz no contexto do projeto de identificação de fissuras em edificações, obtemos uma visão abrangente dos fatores que podem influenciar o sucesso da iniciativa, desde os desafios de implementação da tecnologia até seu potencial de transformação no mercado. Esta compreensão holística permite o desenvolvimento de estratégias robustas de mitigação de riscos e aproveitamento de oportunidades, maximizando as chances de entrega de uma solução que efetivamente atenda às necessidades do setor e gere valor tanto para o IPT quanto para os usuários finais da tecnologia.

## Análise das Ameaças

### Ameaças de Alta Probabilidade (90%)
- **Dificuldades na validação em campo** (Impacto Alto): Representa um risco crítico, indicando obstáculos significativos para testar o algoritmo em condições reais como acesso limitado a estruturas comprometidas, variabilidade nas condições de iluminação e obstáculos físicos que impedem a captura adequada de imagens, potencialmente atrasando a validação da solução.

### Ameaças de Probabilidade Significativa (70%)
- **Condições climáticas afetando capturas** (Impacto Baixo): Chuvas excessivas, baixa luminosidade ou reflexos solares intensos podem prejudicar a qualidade das imagens coletadas, alterando a percepção de textura e profundidade das fissuras, mas possui impacto relativamente controlável através de protocolos de captura.

- **Dificuldade na classificação de fissuras** (Impacto Moderado): Especificamente relacionada à incapacidade do algoritmo em distinguir entre fissuras estruturais e não-estruturais em superfícies com texturas heterogêneas, padrões de pintura irregulares ou materiais compostos. Também inclui dificuldades na diferenciação entre fissuras reais e manchas, sujeiras ou imperfeições superficiais que se assemelham visualmente a rachaduras.

- **Falhas no sistema de previsão** (Impacto Muito Alto): Risco associado à incapacidade dos modelos matemáticos implementados em prever corretamente a progressão das fissuras devido a: 1) insuficiência de dados históricos para estabelecer padrões confiáveis de evolução; 2) incapacidade de considerar adequadamente variáveis ambientais como temperatura e umidade que afetam a dilatação dos materiais; e 3) falha na incorporação de dados sobre características específicas dos materiais de construção que influenciam o comportamento das fissuras ao longo do tempo.

### Ameaças de Média Probabilidade (50%)
- **Resistência à adoção** (Impacto Alto): Resistência específica por parte de engenheiros civis e técnicos experientes que preferem métodos tradicionais de inspeção visual e manual, combinada com preocupações sobre a confiabilidade da tecnologia em substituir o julgamento humano especializado em análises estruturais críticas.

- **Baixa precisão do algoritmo em condições adversas** (Impacto Alto): O sistema pode apresentar queda significativa de precisão (abaixo de 70%) quando exposto a condições como iluminação extremamente baixa, superfícies muito reflexivas ou altamente texturizadas, e em edificações com materiais não contemplados na fase de treinamento do modelo, comprometendo a confiabilidade da análise.

### Ameaças de Menor Probabilidade (30%-10%)
- **Restrições orçamentárias para equipamentos de alta resolução** (Impacto Moderado): Limitação específica na aquisição de câmeras termográficas e sensores de profundidade necessários para análises complementares, podendo restringir a capacidade de detecção em camadas mais profundas das estruturas.

- **Limitações na integração com equipamentos de inspeção existentes** (Impacto Alto): Incompatibilidade técnica com drones e câmeras já utilizados por empresas do setor, necessitando desenvolvimento de interfaces de comunicação personalizadas ou substituição de equipamentos, aumentando custos de implementação.

- **Falta de dados reais para treinamento em edificações históricas** (Impacto Baixo): Escassez específica de exemplos de treinamento para o algoritmo em construções com técnicas construtivas antigas ou materiais não convencionais, limitando a aplicabilidade em patrimônios históricos.

## Análise das Oportunidades

### Oportunidades de Alta Probabilidade (90%-70%)
- **Melhorias no pipeline de desenvolvimento de softwares similares** (Impacto Moderado): Ganhos de eficiência no processo de desenvolvimento através da reutilização de componentes de processamento de imagem e frameworks de machine learning otimizados durante este projeto.

- **Automação de relatórios técnicos detalhados com registro histórico** (Impacto Alto): Capacidade de gerar automaticamente documentação técnica completa incluindo evolução temporal das fissuras, severidade classificada por padrões normativos e recomendações específicas de intervenção baseadas em casos similares.

- **Economia em manutenções preventivas baseadas em dados** (Impacto Moderado): Redução quantificável de 15-30% nos custos de manutenção predial através da identificação precoce de problemas estruturais e priorização precisa de intervenções baseada na gravidade real das fissuras.

### Oportunidades de Média Probabilidade (50%)
- **Parcerias estratégicas com construtoras e empresas de engenharia diagnóstica** (Impacto Alto): Desenvolvimento de integrações exclusivas com sistemas de gestão predial e programas de manutenção já utilizados pelas grandes construtoras, criando um ecossistema tecnológico integrado para monitoramento estrutural.

### Oportunidades de Menor Probabilidade (30%-10%)
- **Diminuição mensurável de acidentes estruturais em edificações monitoradas** (Impacto Muito Alto): Potencial de reduzir em até 40% a ocorrência de falhas estruturais graves em edifícios que implementarem o sistema continuamente, através da detecção ultraprecoce de sinais de comprometimento estrutural que passariam despercebidos em inspeções convencionais.

## Análise de Padrões

1. **Riscos Técnicos Específicos**: A maioria das ameaças está relacionada a desafios técnicos bem definidos (como a incapacidade do algoritmo em diferenciar tipos específicos de fissuras, limitações dos modelos preditivos em considerar variáveis ambientais, e problemas de integração com hardware existente), indicando que o projeto tem componentes tecnológicos complexos e inovadores que requerem soluções direcionadas.

2. **Oportunidades de Negócio Quantificáveis**: As oportunidades estão mais concentradas em benefícios de negócio mensuráveis (economia percentual em manutenções, melhorias específicas na documentação técnica, redução quantificada de acidentes), sugerindo que, se os desafios técnicos forem superados, o potencial de mercado é significativo e demonstrável.

3. **Concentração de Riscos Críticos**: Os riscos de maior gravidade (vermelho) estão principalmente nas células de alta probabilidade e alto impacto, indicando que o projeto tem desafios importantes que precisam ser endereçados prioritariamente com planos de contingência bem elaborados.

## Conclusão

&nbsp;&nbsp;&nbsp;&nbsp;A matriz de riscos apresenta um projeto com desafios técnicos significativos e claramente identificados, mas com potencial de mercado promissor e mensurável. Os riscos estão bem caracterizados em termos de suas causas específicas e distribuídos de forma realista entre probabilidade e impacto, permitindo o desenvolvimento de estratégias precisas de mitigação. O balanceamento entre ameaças detalhadas e oportunidades quantificáveis sugere um projeto inovador que, apesar dos desafios técnicos complexos, tem potencial para trazer benefícios transformadores para o setor de construção civil através da identificação precisa, classificação confiável e previsão embasada da evolução de fissuras estruturais.