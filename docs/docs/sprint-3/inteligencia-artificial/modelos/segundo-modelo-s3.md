---
sidebar_position: 4
slug: /inteligencia-artificial/segundo-modelo
description: "Apresentação do Segundo Modelo de IA para classificação - Swin Transformer V2"
---

# Segundo Modelo - Swin Transformer V2

&emsp; Após identificar limitações significativas no [primeiro modelo ResNet-18](./primeiro-modelo-s3), incluindo suspeitas de overfitting e baixa confiabilidade de generalização, foi necessário desenvolver uma solução mais robusta para atender ao [requisito não funcional 8](../../../sprint-1/especificacoes-tecnicas/Requisitos_Nao_Funcionais.md) de acurácia mínima de 85%. A SOD desenvolveu um segundo modelo baseado no **Swin Transformer V2**, que se tornou a solução implementada no frontend do sistema. O modelo treinado está na pasta [`src/IA/IA_v2/src/swin-transformer-v2`].

## A Escolha do Swin Transformer V2

&emsp; O Swin Transformer V2 foi escolhido como segunda abordagem pelos seguintes motivos técnicos e estratégicos:

- Melhor capacidade de capturar características hierárquicas em diferentes escalas
- Performance superior em tarefas de visão computacional
- Maior robustez a variações de escala e posição nas imagens
- Capacidade de lidar com datasets maiores e mais complexos
- Estado da arte em diversas tarefas de visão computacional

## Arquitetura do Modelo

&emsp; O modelo implementado pela SOD utiliza uma arquitetura híbrida baseada no **Swin Transformer V2** com as seguintes características:

### Backbone: Swin Transformer V2
- **Modelo base**: `swin_base_patch4_window7_224`
- **Pré-treinamento**: Modelo pré-treinado no ImageNet
- **Entrada**: Imagens de 224x224 pixels com 3 canais (RGB)
- **Extração de características**: Janelas deslizantes hierárquicas de tamanho 7x7

### Classificador Customizado
- **Camada 1**: Linear (feature_dim → 512) + BatchNorm + GELU + Dropout(0.2)
- **Camada 2**: Linear (512 → 256) + BatchNorm + GELU + Dropout(0.1)
- **Camada 3**: Linear (256 → 2) para classificação binária

&emsp; Esta arquitetura totaliza aproximadamente 87.9M de parâmetros, sendo mais complexa que o modelo anterior, permitindo capturar padrões mais sutis nas fissuras.

## Configurações de Treinamento

&emsp; O treinamento seguiu uma abordagem sistemática com as seguintes configurações otimizadas:

### Hiperparâmetros Principais
- **Épocas**: 100 (com early stopping após 15 épocas sem melhoria)
- **Batch Size**: 16 (limitado pela memória da GPU)
- **Learning Rate**: 3e-5 (específico para transformers)
- **Otimizador**: AdamW com weight decay de 1e-2
- **Scheduler**: Cosine Annealing com warmup de 5 épocas

### Divisão dos Dados
- **Treinamento**: 70% (150 imagens)
- **Validação**: 15% (32 imagens)
- **Teste**: 15% (32 imagens)

&emsp; Manteve-se a mesma divisão estratificada do primeiro modelo para permitir comparação direta dos resultados.

### Técnicas Avançadas Implementadas

&emsp; O segundo modelo incorpora diversas técnicas modernas de deep learning:

1. **Mixed Precision Training**: Redução do uso de memória e aceleração do treinamento
2. **Gradient Clipping**: Estabilização do treinamento com clipping em 1.0
3. **Label Smoothing**: Regularização com fator 0.1 para reduzir overfitting
4. **Test Time Augmentation (TTA)**: Múltiplas inferências (5 steps) para maior robustez

## Pré-processamento Avançado

&emsp; Manteve-se o mesmo [pré-processamento base da primeira versão](../../../sprint-2/desenvolvimento-tecnico-do-sistema/IA%20de%20Classificação/preparacao.md), mas com melhorias:

### Filtros Aplicados
- **CLAHE**: Clip limit de 3.0 e tile grid de (8,8) para melhoria de contraste
- **Equalização de histograma**: Aplicada seletivamente
- **Sharpening**: Filtro Laplaciano com força 1.2 para realce de bordas
- **Square Padding**: Garantia de imagens quadradas sem distorção

## Resultados e Métricas

&emsp; O modelo Swin Transformer V2 apresentou resultados excepcionais, superando significativamente o primeiro modelo:

<p style={{textAlign: 'center'}}>Tabela 1: Comparação de Métricas</p>
<div style={{margin: 25, textAlign: 'center', display: 'flex'}}>
    <table style={{margin: 'auto'}}>
        <thead>
          <tr>
            <th>Métrica</th>
            <th>ResNet-18</th>
            <th>Swin Transformer V2</th>
            <th>Melhoria</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>Acurácia</td>
            <td>91.5% (suspeito)</td>
            <td>96.9%</td>
            <td>+5.4% confiável</td>
          </tr>
          <tr>
            <td>Precisão</td>
            <td>92.3% (instável)</td>
            <td>97.0%</td>
            <td>+4.7% estável</td>
          </tr>
          <tr>
            <td>Recall</td>
            <td>90.8% (gap alto)</td>
            <td>96.9%</td>
            <td>+6.1% robusto</td>
          </tr>
          <tr>
            <td>F1-Score</td>
            <td>91.5% (questionável)</td>
            <td>96.9%</td>
            <td>+5.4% confiável</td>
          </tr>
          <tr>
            <td>AUC</td>
            <td>N/A</td>
            <td>100.0%</td>
            <td>Separação perfeita</td>
          </tr>
        </tbody>
    </table>
</div>
<p style={{textAlign: 'center'}}>Fonte: Experimentos controlados com validação cruzada estratificada e múltiplas execuções para garantir reprodutibilidade (2025). </p>

&emsp; **Embasamento das métricas**: 
- **ResNet-18**: Médias de 10 execuções com seeds diferentes, apresentando desvio padrão de 3.2% na acurácia
- **Swin Transformer V2**: Médias de 5 execuções independentes, com desvio padrão inferior a 0.8%, demonstrando estabilidade superior
- **Metodologia**: Validação baseada em estratificação por classe e hold-out final de 15% nunca visto durante desenvolvimento

### Análise Comparativa dos Modelos

&emsp; A evolução do ResNet-18 para o Swin Transformer V2 evidencia a importância da escolha arquitetural adequada:

<p style={{textAlign: 'center'}}>Tabela 2: Comparação ResNet-18 vs Swin Transformer V2</p>
<div style={{margin: 25, textAlign: 'center', display: 'flex'}}>
    <table style={{margin: 'auto'}}>
        <thead>
          <tr>
            <th>Aspecto</th>
            <th>ResNet-18</th>
            <th>Swin Transformer V2</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>Acurácia</td>
            <td>91.5% (suspeito)</td>
            <td>96.9% (confiável)</td>
          </tr>
          <tr>
            <td>Generalização</td>
            <td>Overfitting detectado</td>
            <td>Gap < 1% treino/validação</td>
          </tr>
          <tr>
            <td>Estabilidade</td>
            <td>Métricas instáveis</td>
            <td>Resultados consistentes</td>
          </tr>
          <tr>
            <td>Implementação</td>
            <td>Descartado do frontend</td>
            <td>Modelo de produção</td>
          </tr>
        </tbody>
    </table>
</div>
<p style={{textAlign: 'center'}}>Fonte: Produzida pelos Autores (2025). </p>

**Principais melhorias do Swin Transformer V2:**
- **Robustez de generalização**: Eliminação do overfitting observado no ResNet-18
- **Confiabilidade operacional**: Métricas consistentes e estáveis
- **Adequação arquitetural**: Capacidade superior para modelagem de padrões complexos em fissuras

### Análise dos Resultados

&emsp; Os resultados obtidos demonstram performance excepcional e confiável do modelo:

- **Acurácia de Validação**: 96.9% (superando amplamente o requisito de 85%)
- **Precisão Equilibrada**: 97.0% com classificação balanceada entre as classes
- **Recall Excelente**: 96.9%, indicando baixa taxa de falsos negativos
- **AUC Perfeita**: 100%, demonstrando capacidade de separação total entre classes

&emsp; Diferentemente do primeiro modelo, que apresentou sinais de overfitting, o Swin Transformer demonstrou classificação equilibrada e generalização confiável para ambas as classes.

## Implementação e Inferência

&emsp; Para atender ao [RF01](../../../sprint-1/especificacoes-tecnicas/Requisitos_Funcionais.md), foi desenvolvido um sistema unificado de inferência no arquivo [`src/IA/IA_v2/src/modules/inference.py`] que:

1. **Detecta automaticamente** o tipo de modelo (Swin ou ResNet, por enquanto - desenvolveremos mais modelos no futuro)
2. **Carrega as configurações** específicas de cada arquitetura
3. **Aplica pré-processamento** adequado para cada modelo
4. **Retorna resultados** no formato unificado para integração com o frontend

### Função de Predição

```python
def predict(self, image_path: str) -> Dict:
```

## Monitoramento e Experimentos

&emsp; O treinamento foi monitorado através do **MLflow** com tracking completo de:

- **Hiperparâmetros**: Todas as configurações de treinamento
- **Métricas por época**: Loss, acurácia, precisão, recall e F1-score
- **Curvas de aprendizado**: Visualização da evolução do treinamento
- **Modelos**: Versionamento automático dos melhores checkpoints

&emsp; O experimento foi registrado como `swin_transformer_v2_crack_classification` permitindo reprodutibilidade.

## Discussões e Conclusões

&emsp; O desenvolvimento do Swin Transformer V2 representa um marco significativo no projeto da SOD, demonstrando a evolução natural de uma abordagem experimental para uma solução robusta e confiável para classificação de fissuras em infraestrutura.

### Principais Avanços

1. **Acurácia excepcional**: Superação do requisito mínimo com margem de 11.9%
2. **Classificação equilibrada**: Eliminação completa do overfitting do modelo anterior
3. **Robustez técnica**: Implementação de técnicas state-of-the-art
4. **Separação perfeita**: AUC de 100% indica capacidade de distinção ideal

**Complexidade Computacional:**
- Modelo de 87.9M parâmetros requer recursos computacionais significativos
- Tempo de inferência pode ser consideração em aplicações real-time
- Otimizações como quantização podem ser exploradas sem perda significativa de performance

### Reflexões Finais

&emsp; A evolução do ResNet-18 (com problemas de overfitting) para 96.9% de acurácia confiável ilustra o impacto da escolha arquitetural adequada e da aplicação rigorosa de técnicas modernas de deep learning. 

Os próximos passos naturais incluem a validação em campo com condições reais de operação, integração com o sistema de drone para coleta automatizada - que será finalizado na próxima sprint, e exploração de técnicas de explicabilidade para aumentar a confiança dos engenheiros especialistas. 

&emsp; Em conclusão, o Swin Transformer V2 estabelece uma base sólida para o sistema de classificação de fissuras, demonstrando que técnicas modernas de deep learning podem efetivamente superar abordagens mais simples quando aplicadas adequadamente ao domínio específico da inspeção de infraestrutura.

### Continuidade para a Próxima Sprint

&emsp; Com o modelo de IA consolidado e validado, este trabalho estabelece os fundamentos para a próxima fase do projeto: a integração completa com o sistema de drones e a implementação da [pipeline unificada](./pipeline-unificada) em ambiente de produção. A robustez demonstrada pelo Swin Transformer V2 garante confiabilidade para as próximas etapas de desenvolvimento do sistema SOD.

## Bibliografia

* LIU, Ze et al. Swin Transformer V2: Scaling Up Capacity and Resolution. In: **Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition**, 2022.

* DOSOVITSKIY, Alexey et al. An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale. **arXiv preprint arXiv:2010.11929**, 2020.

* CHUN, P.; IZUMI, S.; YAMANE, T. Automatic detection method of cracks from concrete surface imagery using two‐step light gradient boosting machine. **Computer-Aided Civil and Infrastructure Engineering**, v. 36, n. 1, p. 61–72, 20 maio 2020.

* LOSHCHILOV, Ilya; HUTTER, Frank. Decoupled weight decay regularization. **arXiv preprint arXiv:1711.05101**, 2017.

* MICROSOFT RESEARCH. Swin Transformer: Hierarchical Vision Transformer using Shifted Windows. **GitHub Repository**, 2021. Disponível em: https://github.com/microsoft/Swin-Transformer.