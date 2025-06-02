---
sidebar_position: 1
slug: /inteligencia-artificial/preprocessamento-imagens
description: "Técnicas de pré-processamento de imagens para otimização da classificação de fissuras"
---

# Pré-processamento de Imagens

&emsp; O desenvolvimento do sistema de classificação de fissuras da SOD revelou rapidamente que as imagens brutas capturadas pelos drones necessitam de tratamento especializado antes da análise pelos modelos de inteligência artificial. Assim como um chef prepara cuidadosamente os ingredientes antes de cozinhar, o pré-processamento adequado é fundamental para obter os melhores resultados na classificação.

## Por que o Pré-processamento É Fundamental?

&emsp; O sistema da SOD precisa lidar com centenas de fotografias de estruturas capturadas em condições completamente diferentes: algumas sob sol intenso, outras em dias nublados, algumas muito próximas da estrutura, outras mais distantes. Os modelos de IA precisam conseguir identificar fissuras em todas essas situações diversas. É nesse contexto que o pré-processamento se torna essencial:

- **Padronização de entrada**: Garantia de formato consistente esperado pelos modelos
- **Melhoria de qualidade**: Realce das características relevantes para detecção de fissuras
- **Redução de ruído**: Eliminação de elementos que podem confundir os classificadores
- **Normalização**: Ajuste de brilho e contraste para condições variadas de iluminação
- **Aumento de robustez**: Preparação para diferentes condições de captura em campo

## Validação Manual Inicial

&emsp; Antes de implementar o pipeline final, foi feita uma validação manual para identificar as técnicas mais eficazes. Este processo experimental foi fundamental para entender quais filtros e transformações realmente faziam diferença na qualidade das imagens de fissuras.

### Ferramentas de Teste Desenvolvidas

&emsp; Para facilitar a experimentação, foram desenvolvidas três ferramentas específicas de validação:

**1. Sistema de Comparação de Filtros (`filter-test.py`)**
- Aplicação automática de diferentes filtros (Sobel, Canny, simulação de ANN)
- Geração de comparações lado a lado para análise visual
- Redimensionamento padronizado para avaliação consistente

**2. Teste de Redimensionamento (`image-scaling-test.py`)**
- Validação da técnica de Square Padding
- Teste com diferentes cores de preenchimento
- Verificação da preservação de proporções

**3. Interface Interativa (`streamlit-preview-preprocess.py`)**
- Aplicação de filtros sequenciais em tempo real
- Teste interativo de parâmetros
- Capacidade de aplicar até 8 filtros em sequência para análise

### Processo de Validação

&emsp; A validação manual seguiu uma metodologia sistemática:

1. **Coleta de amostras**: Seleção de imagens representativas com diferentes tipos de fissuras
2. **Teste individual**: Aplicação isolada de cada filtro para entender seus efeitos
3. **Combinação sequencial**: Teste de diferentes sequências de filtros
4. **Análise visual**: Avaliação qualitativa da visibilidade das fissuras
5. **Validação quantitativa**: Medição de contraste e nitidez das bordas

### Descobertas da Validação

&emsp; O processo manual revelou informações que influenciaram o pipeline final:

- **CLAHE demonstrou superioridade**: Entre todas as técnicas de melhoria de contraste testadas, o CLAHE com clip limit 3.0 apresentou os melhores resultados
- **Sequência importa**: A ordem de aplicação dos filtros afeta significativamente o resultado final
- **Square Padding preserva informação**: Comparado ao redimensionamento direto, o padding evita distorções nas características das fissuras
- **Sharpening sutil é eficaz**: Valores de strength entre 1.0 e 1.2 realçam bordas sem introduzir artefatos

### Impacto na Implementação Final

&emsp; Os resultados da validação manual foram diretamente incorporados ao pipeline automatizado:

```python
# Sequência otimizada descoberta na validação manual
def pipeline_validado_manualmente(image):
    # 1. Square padding (validado como superior)
    image = square_pad_resize(image, target_size)
    
    # 2. CLAHE com parâmetros testados manualmente
    image = apply_clahe(image, clip_limit=3.0, tile_grid_size=(8, 8))
    
    # 3. Sharpening com strength otimizada
    image = apply_sharpening(image, strength=1.2)
    
    # 4. Equalização seletiva (quando necessária)
    image = selective_histogram_equalization(image)
    
    return image
```

## Estratégia de Pré-processamento da SOD

&emsp; A foi desenvolvido um pipeline que evoluiu consideravelmente ao longo do projeto.

### Etapa 1: Validação e Carregamento

```python
# Formatos suportados pelo sistema
SUPPORTED_FORMATS = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']

# Verificação de formato válido
def validate_image_format(image_path: str) -> bool:
    return Path(image_path).suffix.lower() in SUPPORTED_FORMATS
```

&emsp; A decisão foi suportar os principais formatos encontrados em equipamentos profissionais de captura, garantindo compatibilidade com a maioria das câmeras que podem ser embarcadas em drones.

### Etapa 2: Redimensionamento Inteligente

&emsp; A equipe optou por uma abordagem criativa. Em vez de simplesmente esticar ou cortar as imagens, foi implementada uma técnica chamada **Square Padding** que preserva as proporções originais:

```python
def square_pad_resize(image, target_size=224):
    """
    Redimensiona mantendo a proporção original com padding
    """
    h, w = image.shape[:2]
    max_dim = max(h, w)
    
    # Criar um canvas quadrado
    square_image = np.zeros((max_dim, max_dim, 3), dtype=np.uint8)
    
    # Centralizar a imagem original
    y_offset = (max_dim - h) // 2
    x_offset = (max_dim - w) // 2
    square_image[y_offset:y_offset+h, x_offset:x_offset+w] = image
    
    # Redimensionar para o tamanho necessário
    return cv2.resize(square_image, (target_size, target_size))
```

**Vantagens da abordagem:**
- **Preservação das proporções**: Evita distorção das características das fissuras
- **Consistência dimensional**: Todas as imagens resultam em 224×224 pixels
- **Manutenção de informação**: Não há perda por cropping agressivo

### Etapa 3: Melhoramento de Contraste

&emsp; Após extensivos testes, foi aplicado o **CLAHE (Contrast Limited Adaptive Histogram Equalization)**, que oferece resultados ótimos para realçar fissuras que às vezes são quase imperceptíveis:

```python
def apply_clahe(image, clip_limit=3.0, tile_grid_size=(8, 8)):
    """
    Aplica CLAHE para melhorar o contraste local
    """
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    lab_planes = cv2.split(lab)
    
    clahe = cv2.createCLAHE(clipLimit=clip_limit, 
                           tileGridSize=tile_grid_size)
    lab_planes[0] = clahe.apply(lab_planes[0])
    
    lab = cv2.merge(lab_planes)
    return cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
```

**Configurações otimizadas:**
- **Clip Limit**: 3.0 (equilíbrio ideal entre contraste e ruído)
- **Tile Grid**: (8,8) (resolução adequada para imagens de fissuras)
- **Espaço de cor**: LAB (preservação superior das informações cromáticas)

### Etapa 4: Realce de Bordas

&emsp; Considerando que as fissuras representam mudanças bruscas na superfície, foi necessário implementar algo que realçasse essas transições. O **Sharpening Laplaciano** demonstrou ser ideal para essa finalidade:

```python
def apply_sharpening(image, strength=1.2):
    """
    Aplica filtro de sharpening para realçar bordas
    """
    kernel = np.array([[-1, -1, -1],
                       [-1,  9, -1], 
                       [-1, -1, -1]], dtype=np.float32)
    
    kernel = kernel * strength
    kernel[1, 1] = kernel[1, 1] - (strength - 1) * 8
    
    sharpened = cv2.filter2D(image, -1, kernel)
    return np.clip(sharpened, 0, 255).astype(np.uint8)
```

**Configuração otimizada:**
- **Strength**: 1.2 (realce efetivo sem introdução de artefatos)
- **Kernel Laplaciano**: Matriz 3×3 para detecção de bordas omnidirecional

### Etapa 5: Equalização Seletiva

&emsp; A equalização de histograma não é sempre necessária, mas quando aplicada, é feita de forma inteligente para preservar informações cromáticas:

```python
def selective_histogram_equalization(image, apply_condition=True):
    """
    Equalização aplicada seletivamente conforme necessidade
    """
    if apply_condition:
        # Conversão para YUV para preservar informações de cor
        yuv = cv2.cvtColor(image, cv2.COLOR_BGR2YUV)
        yuv[:,:,0] = cv2.equalizeHist(yuv[:,:,0])
        return cv2.cvtColor(yuv, cv2.COLOR_YUV2BGR)
    return image
```

## Técnicas Avançadas de Data Augmentation

&emsp; Além do pré-processamento fundamental, foram implementadas técnicas para simular diferentes condições que os modelos podem encontrar em aplicações reais:

### Transformações Geométricas Relevantes
```python
def geometric_augmentations():
    return A.Compose([
        A.Rotate(limit=15, p=0.5),           # Rotação controlada
        A.HorizontalFlip(p=0.5),             # Espelhamento horizontal
        A.VerticalFlip(p=0.3),               # Espelhamento vertical  
        A.RandomBrightnessContrast(          # Variação de brilho/contraste
            brightness_limit=0.2, 
            contrast_limit=0.2, 
            p=0.5
        ),
        A.GaussNoise(var_limit=(10.0, 50.0), p=0.3),  # Ruído simulado
    ])
```

### Test Time Augmentation (TTA) - Estratégia Avançada

&emsp; Para o Swin Transformer V2, foi implementada uma técnica sofisticada: múltiplas predições da mesma imagem com pequenas variações, seguidas por cálculo da média. Essa abordagem aumenta significativamente a confiabilidade:

```python
def predict_with_tta(model, image, num_tta=5):
    """
    Predição com múltiplas augmentações para maior confiabilidade
    """
    predictions = []
    
    for _ in range(num_tta):
        # Aplicar variação controlada
        augmented = tta_transform(image)
        pred = model(augmented)
        predictions.append(pred)
    
    # Média das predições para resultado robusto
    return torch.mean(torch.stack(predictions), dim=0)
```

&emsp; O trabalho estabelecido nesta etapa fornece os fundamentos necessários para a implementação bem-sucedida dos [modelos de classificação](./primeiro-modelo-s3) e da [pipeline unificada](./pipeline-unificada), garantindo que o sistema SOD opere com máxima eficiência e confiabilidade na detecção de fissuras em infraestrutura.