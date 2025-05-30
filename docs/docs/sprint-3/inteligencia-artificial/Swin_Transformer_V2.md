---
sidebar_position: 4
custom_edit_url: null
---

# Swin Transformer V2

O Swin Transformer V2 representa a segunda iteração do nosso modelo de classificação de fissuras, buscando superar as limitações encontradas no primeiro modelo baseado em Teachable Machine. Este modelo foi escolhido por sua arquitetura avançada e capacidade de processamento hierárquico de características visuais.

## Por que usar o Swin Transformer V2?

O Swin Transformer V2 foi selecionado como nossa segunda abordagem pelos seguintes motivos:
- Melhor capacidade de capturar características hierárquicas em diferentes escalas
- Performance superior em tarefas de visão computacional
- Maior robustez a variações de escala e posição nas imagens
- Capacidade de lidar com datasets maiores e mais complexos
- Estado da arte em diversas tarefas de visão computacional

## Arquitetura do Modelo

O Swin Transformer V2 apresenta as seguintes características principais:
- Janelas deslizantes hierárquicas para captura de características em múltiplas escalas
- Mecanismo de atenção otimizado para processamento de imagens
- Normalização pós-atenção para treinamento mais estável
- Arquitetura modular e escalável

# Training and Configuration

O treinamento do modelo seguiu as seguintes etapas:

1. Pré-processamento do dataset:
   - Transformação para escala de cinza
   - Normalização das imagens
   - Aumento de dados (data augmentation) para melhorar a generalização

2. Configurações de treinamento:
   - Épocas: 100
   - Batch Size: 32
   - Otimizador: AdamW
   - Learning Rate: 0.00001
   - Weight Decay: 0.05

3. Divisão do dataset:
   - Treinamento: 70%
   - Validação: 15%
   - Teste: 15%

## Resultados e Métricas

O modelo apresentou melhorias significativas em relação à primeira versão:

| Métrica | Valor |
|---------|-------|
| Acurácia | 91.5% |
| Precisão | 92.3% |
| Recall | 90.8% |
| F1-Score | 91.5% |

Estas métricas representam uma melhoria considerável em relação ao modelo anterior baseado em Teachable Machine, superando o requisito de acurácia mínima de 85% estabelecido pelo parceiro.

## Discussão e Conclusões

O Swin Transformer V2 demonstrou ser uma escolha acertada para a evolução do nosso sistema de classificação de fissuras, apresentando:

1. Maior precisão na classificação geral
2. Melhor capacidade de generalização
3. Menor taxa de falsos positivos
4. Performance mais equilibrada entre as classes

Apesar dos resultados positivos, ainda existem oportunidades de melhoria:
- Expandir o dataset com mais exemplos variados
- Explorar técnicas adicionais de aumento de dados
- Otimizar hiperparâmetros para casos específicos

## Referências

* LIU, Ze et al. Swin Transformer V2: Scaling Up Capacity and Resolution. In: Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, 2022.
* MICROSOFT RESEARCH. Swin Transformer: Hierarchical Vision Transformer using Shifted Windows. 2021.



