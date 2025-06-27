---
sidebar_position: 3
slug: /inteligencia-artificial/primeiro-modelo-s3
description: "Primeiro Modelo ResNet-18 - Baseline Bem-Sucedida"
---

# Primeiro Modelo - ResNet-18

&emsp; Este modelo desenvolvido pela SOD utiliza a arquitetura **ResNet-18** como baseline inicial para classificação de fissuras. O modelo apresentou resultados satisfatórios e serviu como uma implementação sólida para validação da abordagem técnica.

## Por que Começar com ResNet-18?

&emsp; O ResNet-18 foi selecionado como ponto de partida pelos seguintes critérios:

- **Prototipagem rápida**: 11.7M parâmetros, adequado para validação inicial
- **Transfer learning**: Aproveitamento de conhecimento pré-treinado no ImageNet  
- **Baseline estabelecida**: Referência para desenvolvimento de modelos avançados
- **Implementação conhecida**: Arquitetura bem documentada para desenvolvimento ágil

## Configurações e Implementação

### Arquitetura
- **Base**: ResNet-18 pré-treinado no ImageNet
- **Entrada**: Imagens 224×224 pixels, 3 canais RGB
- **Classificador**: Três camadas lineares (512→256→2) com dropout

### Treinamento
- **Épocas**: 50 com early stopping (paciência 10)
- **Batch Size**: 32
- **Learning Rate**: 1e-3 com scheduler Cosine Annealing
- **Data Augmentation**: Rotação, flips, variação de brilho/contraste, CLAHE

## Resultados Obtidos

&emsp; O ResNet-18 apresentou resultados consistentes e satisfatórios para a tarefa de classificação de fissuras:

<p style={{textAlign: 'center'}}>Tabela 1: Métricas do ResNet-18</p>
<div style={{margin: 25, textAlign: 'center', display: 'flex'}}>
    <table style={{margin: 'auto'}}>
        <thead>
          <tr>
            <th>Métrica</th>
            <th>Valor</th>
            <th>Avaliação</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>Acurácia</td>
            <td>91.5%</td>
            <td>Resultado satisfatório</td>
          </tr>
          <tr>
            <td>Precisão</td>
            <td>92.3%</td>
            <td>Boa capacidade de classificação</td>
          </tr>
          <tr>
            <td>Recall</td>
            <td>90.8%</td>
            <td>Detecção adequada de fissuras</td>
          </tr>
          <tr>
            <td>F1-Score</td>
            <td>91.5%</td>
            <td>Desempenho equilibrado</td>
          </tr>
        </tbody>
    </table>
</div>
<p style={{textAlign: 'center'}}>Fonte: Experimentos realizados pelos Autores com validação cruzada 5-fold (2025). </p>

&emsp; **Embasamento das métricas**: Os valores foram obtidos através de múltiplas execuções com diferentes seeds aleatórias, demonstrando consistência nos resultados e validando a eficácia da abordagem.

## Desempenho e Características

### Pontos Fortes
&emsp; O modelo ResNet-18 demonstrou:

- **Generalização adequada**: Performance consistente entre treino e validação
- **Estabilidade**: Métricas reproducíveis entre diferentes execuções  
- **Eficiência**: Tempo de treinamento e inferência adequados
- **Robustez**: Comportamento confiável em imagens de teste

### Análise Técnica
&emsp; A implementação apresentou características positivas:

1. **Aprendizado efetivo**: Boa capacidade de distinção entre fissuras e não-fissuras
2. **Utilização de features**: Aproveitamento adequado do conhecimento pré-treinado
3. **Arquitetura apropriada**: Capacidade suficiente para o problema específico
4. **Desempenho consistente**: Resultados estáveis em diferentes cenários

## Decisão de Implementação

&emsp; Embora o ResNet-18 tenha apresentado resultados satisfatórios, a equipe optou por:

- **Implementar o Swin Transformer V2** no frontend do sistema SOD
- **Manter o ResNet-18** como modelo alternativo válido
- **Utilizar ambos os modelos** para comparação e validação
- **Focar no Swin Transformer V2** como solução principal

## Contribuições para o Projeto

&emsp; O ResNet-18 forneceu:

- **Validação do pipeline**: Estabelecimento da infraestrutura de treinamento
- **Benchmark sólido**: Referência para avaliar outras abordagens
- **Aprendizado técnico**: Insights sobre o problema de classificação de fissuras
- **Base para comparação**: Modelo de referência para avaliar melhorias

## Conclusões

&emsp; O modelo ResNet-18 demonstrou ser uma solução eficaz para classificação de fissuras, cumprindo adequadamente seu papel como baseline inicial. Seus resultados satisfatórios validaram a abordagem técnica e forneceram uma base sólida para o desenvolvimento do projeto.

&emsp; A escolha pelo [Swin Transformer V2](./segundo-modelo) para implementação no frontend representa uma decisão estratégica para explorar arquiteturas mais modernas, mantendo o ResNet-18 como uma alternativa comprovadamente eficaz.

&emsp; Esta abordagem dupla demonstra a maturidade técnica do projeto, oferecendo tanto uma solução consolidada (ResNet-18) quanto uma implementação de vanguarda (Swin Transformer V2) para classificação de fissuras em inspeção de infraestrutura.

&emsp; A experiência com o ResNet-18 estabeleceu uma base sólida de conhecimento que informou as decisões subsequentes no desenvolvimento da solução de IA, contribuindo para o sucesso geral do sistema SOD.

## Bibliografia

* HE, Kaiming et al. Deep Residual Learning for Image Recognition. **IEEE CVPR**, 2016.
* GOODFELLOW, Ian; BENGIO, Yoshua; COURVILLE, Aaron. Deep Learning. **MIT Press**, 2016.