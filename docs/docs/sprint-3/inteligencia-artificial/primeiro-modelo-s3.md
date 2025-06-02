---
sidebar_position: 3
slug: /inteligencia-artificial/primeiro-modelo-s3
description: "Primeiro Modelo ResNet-18 - Baseline com Limitações Identificadas"
---

# Primeiro Modelo - ResNet-18

&emsp; Este modelo desenvolvido pela SOD utiliza a arquitetura **ResNet-18** como baseline inicial para classificação de fissuras. Durante o desenvolvimento, foram identificadas limitações significativas que levaram ao desenvolvimento de uma solução mais robusta.

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

## Resultados Iniciais

&emsp; Os resultados iniciais do ResNet-18, embora aparentemente promissores, revelaram limitações significativas durante validação rigorosa:

<p style={{textAlign: 'center'}}>Tabela 1: Métricas do ResNet-18</p>
<div style={{margin: 25, textAlign: 'center', display: 'flex'}}>
    <table style={{margin: 'auto'}}>
        <thead>
          <tr>
            <th>Métrica</th>
            <th>Valor</th>
            <th>Observação</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>Acurácia</td>
            <td>91.5%</td>
            <td>⚠️ Suspeita de overfitting</td>
          </tr>
          <tr>
            <td>Precisão</td>
            <td>92.3%</td>
            <td>⚠️ Validação necessária</td>
          </tr>
          <tr>
            <td>Recall</td>
            <td>90.8%</td>
            <td>⚠️ Gap treino/validação</td>
          </tr>
          <tr>
            <td>F1-Score</td>
            <td>91.5%</td>
            <td>⚠️ Confiabilidade questionável</td>
          </tr>
        </tbody>
    </table>
</div>
<p style={{textAlign: 'center'}}>Fonte: Experimentos realizados pelos Autores com validação cruzada 5-fold (2025). </p>

&emsp; **Embasamento das métricas**: Os valores foram obtidos através de múltiplas execuções com diferentes seeds aleatórias, revelando alta variância nos resultados (desvio padrão > 3%), indicativo de instabilidade do modelo.

## Limitações Identificadas

### Problemas de Generalização
&emsp; Durante a validação, foram identificados sinais claros de **overfitting**:

- **Gap significativo** entre performance de treino e validação
- **Instabilidade** nas métricas entre diferentes execuções  
- **Sensibilidade excessiva** às técnicas de data augmentation
- **Comportamento suspeito** em imagens de teste independentes

### Análise Crítica
&emsp; A análise técnica revelou que o modelo apresentava:

1. **Memorização do dataset**: Alta acurácia em treino, baixa generalização
2. **Dependência de artifacts**: Aprendizado de características não relacionadas às fissuras
3. **Instabilidade arquitetural**: Capacidade limitada para o problema específico
4. **Falta de robustez**: Performance inconsistente em cenários reais

## Decisão de Desenvolvimento

&emsp; Com base nas limitações identificadas, a equipe decidiu:

- **Não utilizar o ResNet-18** no frontend do sistema SOD
- **Desenvolver modelo mais robusto** baseado em Swin Transformer V2
- **Manter código ResNet-18** apenas para referência e comparação
- **Focar recursos** no desenvolvimento de solução confiável

## Contribuições para o Projeto

&emsp; Apesar das limitações, o ResNet-18 forneceu:

- **Validação do pipeline**: Estabelecimento da infraestrutura de treinamento
- **Benchmark inicial**: Referência para avaliar melhorias
- **Aprendizado técnico**: Identificação de armadilhas em datasets pequenos
- **Base para evolução**: Fundação para desenvolvimento do modelo final

## Conclusões

&emsp; O modelo ResNet-18 cumpriu seu papel como baseline inicial, mas suas limitações de generalização tornaram necessário o desenvolvimento de uma solução mais robusta. A experiência com este modelo foi fundamental para o desenvolvimento bem-sucedido do [Swin Transformer V2](./segundo-modelo), que se tornou a solução implementada no sistema SOD.

&emsp; Esta abordagem iterativa demonstra a importância da validação rigorosa em projetos de machine learning aplicado, especialmente em domínios críticos como inspeção de infraestrutura. As lições aprendidas com o ResNet-18 informaram diretamente as decisões arquiteturais do modelo subsequente, estabelecendo uma progressão natural no desenvolvimento da solução de IA para classificação de fissuras.

&emsp; A transição para o Swin Transformer V2 representa não apenas uma evolução técnica, mas também um amadurecimento metodológico na abordagem de problemas de visão computacional aplicada à engenharia civil.

## Bibliografia

* HE, Kaiming et al. Deep Residual Learning for Image Recognition. **IEEE CVPR**, 2016.
* GOODFELLOW, Ian; BENGIO, Yoshua; COURVILLE, Aaron. Deep Learning. **MIT Press**, 2016.