---
sidebar_position: 3
slug: /desenvolvimento-tecnico/ia-classificacao/segundo-modelo
description: "Apresentação do Segundo Modelo de IA para classificação - Swin Transformer V2"
---

# Segundo Modelo - Swin Transformer V2

&emsp; Após a análise dos resultados obtidos com o [primeiro modelo baseado em Teachable Machine](../../sprint-2/desenvolvimento-tecnico-do-sistema/IA%20de%20Classificação/primeiro-modelo.md), que apresentou uma acurácia média de 75%, foi necessário buscar uma abordagem mais avançada para atender ao [requisito não funcional 8](../../sprint-1/especificacoes-tecnicas/Requisitos_Funcionais.md) de acurácia mínima de 85%. Nessa sprint, a SOD desenvolveu um segundo modelo baseado no **Swin Transformer V2**, representando um salto significativo em complexidade e performance. O modelo treinado está na pasta [`src/IA/IA_v2/src/swin-transformer-v2`].

## Por que usar o Swin Transformer V2?

&emsp; O Swin Transformer V2 foi escolhido como segunda abordagem pelos seguintes motivos técnicos e estratégicos:

- **Estado da arte em visão computacional**: O Swin Transformer representa o estado da arte em tarefas de classificação de imagens, superando modelos baseados em CNN tradicionais;
- **Arquitetura hierárquica**: Capacidade de capturar características em múltiplas escalas através de janelas deslizantes hierárquicas;
- **Robustez a variações**: Maior resistência a variações de escala, posição e iluminação nas imagens;
- **Mecanismo de atenção otimizado**: Processamento mais eficiente de relações espaciais complexas nas fissuras;
- **Melhor generalização**: Capacidade superior de lidar com datasets limitados através de técnicas de transfer learning.

&emsp; Diferentemente da abordagem anterior com Teachable Machine, esta solução permite total controle sobre o processo de treinamento, permitindo implementar técnicas avançadas de otimização e regularização.

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

&emsp; Esta arquitetura totaliza aproximadamente **87.9M de parâmetros**, sendo substancialmente mais complexa que o modelo anterior, permitindo capturar padrões mais sutis nas fissuras.

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

&emsp; Manteve-se o mesmo [pré-processamento base da primeira versão](../../sprint-2/desenvolvimento-tecnico-do-sistema/IA%20de%20Classificação/preparacao.md), mas com melhorias:

### Filtros Aplicados
- **CLAHE**: Clip limit de 3.0 e tile grid de (8,8) para melhoria de contraste
- **Equalização de histograma**: Aplicada seletivamente
- **Sharpening**: Filtro Laplaciano com força 1.2 para realce de bordas
- **Square Padding**: Garantia de imagens quadradas sem distorção

### Data Augmentation

Adicionamos transformações para aumentar a diversidade e do dataset, visto que e um conjunto de imagens pequenos. Isso ajuda a previnir overfitting e aumenta ea generalização.

- **Transformações geométricas**: Rotação (±20°), flip horizontal (50%) e vertical (30%)
- **Transformações de cor**: Brilho e contraste (±20%)
- **Ruído e blur**: Adição controlada 
- **Dropout espacial**: Coarse dropout para simular oclusões

## Resultados e Métricas

&emsp; O modelo Swin Transformer V2 apresentou resultados excepcionais, superando significativamente o primeiro modelo:

<p style={{textAlign: 'center'}}>Tabela 1: Comparação de Métricas</p>
<div style={{margin: 25, textAlign: 'center', display: 'flex'}}>
    <table style={{margin: 'auto'}}>
        <thead>
          <tr>
            <th>Métrica</th>
            <th>Teachable Machine</th>
            <th>Swin Transformer V2</th>
            <th>Melhoria</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>Acurácia</td>
            <td>75.0%</td>
            <td>96.9%</td>
            <td>+21.9%</td>
          </tr>
          <tr>
            <td>Precisão</td>
            <td>100.0%</td>
            <td>97.0%</td>
            <td>-3.0%</td>
          </tr>
          <tr>
            <td>Recall</td>
            <td>50.0%</td>
            <td>96.9%</td>
            <td>+46.9%</td>
          </tr>
          <tr>
            <td>F1-Score</td>
            <td>66.7%</td>
            <td>96.9%</td>
            <td>+30.2%</td>
          </tr>
          <tr>
            <td>AUC</td>
            <td>N/A</td>
            <td>100.0%</td>
            <td>-</td>
          </tr>
        </tbody>
    </table>
</div>
<p style={{textAlign: 'center'}}>Fonte: Produzida pelos Autores (2025). </p>

### Análise dos Resultados

&emsp; Os resultados obtidos demonstram performance excepcional do modelo:

- **Acurácia de Validação**: 96.9% (superando amplamente o requisito de 85%)
- **Precisão Equilibrada**: 97.0% com classificação balanceada entre as classes
- **Recall Excelente**: 96.9%, indicando baixa taxa de falsos negativos
- **AUC Perfeita**: 100%, demonstrando capacidade de separação total entre classes

&emsp; Diferentemente do primeiro modelo, que apresentou forte viés para classificação de fissuras térmicas, o Swin Transformer demonstrou classificação equilibrada para ambas as classes.

## Implementação e Inferência

&emsp; Para atender ao [RF01](../../sprint-1/especificacoes-tecnicas/Requisitos_Funcionais.md), foi desenvolvido um sistema unificado de inferência no arquivo [`src/IA/IA_v2/src/modules/inference.py`] que:

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
2. **Classificação equilibrada**: Eliminação completa do viés do modelo anterior
3. **Robustez técnica**: Implementação de técnicas state-of-the-art
4. **Separação perfeita**: AUC de 100% indica capacidade de distinção ideal

### Análise Comparativa dos Modelos

&emsp; A evolução do primeiro para o segundo modelo evidencia a importância da escolha arquitetural adequada. Enquanto o modelo baseado em Teachable Machine apresentou limitações severas de generalização, especialmente para fissuras de retração (recall de apenas 50%), o Swin Transformer demonstrou capacidade equilibrada de classificação.

&emsp; **Teachable Machine vs. Swin Transformer:**
- **Viés eliminado**: O primeiro modelo classificava incorretamente 100% das fissuras de retração como térmicas em alguns casos
- **Generalização superior**: Gap de apenas 1% entre treino e validação no segundo modelo vs. variações maiores no primeiro
- **Robustez aumentada**: Técnicas de regularização avançadas previnem overfitting
- **Interpretabilidade mantida**: Apesar da complexidade, o modelo mantém predições confiáveis

### Impacto no Sistema SOD

&emsp; Os resultados obtidos habilitam a SOD a avançar com confiança para a próxima fase do projeto:

1. **Requisitos atendidos**: Superação significativa da acurácia mínima de 85% estabelecida
2. **Confiabilidade operacional**: Métricas consistentes permitem deployment em ambiente de produção
3. **Escalabilidade técnica**: Arquitetura preparada para integração com sistemas de maior escala
4. **Validação científica**: Resultados comparáveis a trabalhos acadêmicos na área

### Limitações e Considerações Técnicas

&emsp; Apesar dos resultados excepcionais, algumas considerações técnicas merecem atenção:

**Dataset e Generalização:**
- O conjunto de dados, embora expandido, ainda representa um cenário controlado
- Validação em campo com condições de iluminação e ângulos variados é recomendada
- Diversidade geográfica das amostras pode impactar a generalização

**Complexidade Computacional:**
- Modelo de 87.9M parâmetros requer recursos computacionais significativos
- Tempo de inferência pode ser consideração em aplicações real-time
- Otimizações como quantização podem ser exploradas sem perda significativa de performance

**Maturidade da Solução:**
- Apesar dos excelentes resultados em laboratório, validação prolongada em campo é essencial
- Monitoramento contínuo da performance em produção deve ser implementado
- Feedback de especialistas do IPT será crucial para validação final

### Contribuições Metodológicas

&emsp; O desenvolvimento deste modelo contribui para o estado da arte em inspeção automatizada de infraestrutura:

1. **Aplicação bem-sucedida de transformers**: Demonstração da eficácia de arquiteturas de atenção em classificação de fissuras
2. **Pipeline robusta**: Desenvolvimento de framework completo desde pré-processamento até inferência
3. **Reprodutibilidade**: Implementação com versionamento e tracking completo via MLflow
4. **Transferência de conhecimento**: Metodologia aplicável a outros problemas de inspeção civil

### Próximos Passos

&emsp; Para futuras iterações, a SOD recomenda:

1. **Expansão do dataset**: Coleta de mais exemplos diversificados
2. **Ensemble methods**: Combinação com outros modelos para maior robustez
3. **Otimização de deployment**: Quantização para reduzir requisitos computacionais
4. **Validação externa**: Teste em imagens de fontes independentes

### Reflexões Finais

&emsp; A evolução de 75% para 96.9% de acurácia ilustra o impacto da escolha arquitetural adequada e da aplicação rigorosa de técnicas modernas de deep learning. 

Os próximos passos naturais incluem a validação em campo com condições reais de operação, integração com o sistema de drone para coleta automatizada - que será finalizado na próxima sprint, e exploração de técnicas de explicabilidade para aumentar a confiança dos engenheiros especialistas. 

Um aspecto não explorado, mas promissor, é o potencial de adaptação desta metodologia para outros tipos de patologias estruturais como corrosão, eflorescência e descolamento de revestimentos, expandindo significativamente o escopo de aplicação da solução - mas que podem ser próximos passos interessantes para o parceiro. 

A robustez do pipeline desenvolvido, combinada com a infraestrutura de MLflow, facilita esta expansão futura e consolida a base tecnológica para um sistema abrangente de monitoramento automatizado de estruturas. Embora o modelo tenha superado as expectativas e já ser discutinda o futuro dele, recomenda-se validação adicional com o IPT.

&emsp; Em conclusão, o Swin Transformer V2 estabelece uma base sólida para o sistema de classificação de fissuras, demonstrando que técnicas modernas de deep learning podem efetivamente superar abordagens mais simples quando aplicadas adequadamente ao domínio específico da inspeção de infraestrutura.

## Bibliografia

* LIU, Ze et al. Swin Transformer V2: Scaling Up Capacity and Resolution. In: **Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition**, 2022.

* DOSOVITSKIY, Alexey et al. An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale. **arXiv preprint arXiv:2010.11929**, 2020.

* CHUN, P.; IZUMI, S.; YAMANE, T. Automatic detection method of cracks from concrete surface imagery using two‐step light gradient boosting machine. **Computer-Aided Civil and Infrastructure Engineering**, v. 36, n. 1, p. 61–72, 20 maio 2020.

* LOSHCHILOV, Ilya; HUTTER, Frank. Decoupled weight decay regularization. **arXiv preprint arXiv:1711.05101**, 2017.

* MICROSOFT RESEARCH. Swin Transformer: Hierarchical Vision Transformer using Shifted Windows. **GitHub Repository**, 2021. Disponível em: https://github.com/microsoft/Swin-Transformer. 