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

## Estratégia de Pré-processamento da SOD

&emsp; A equipe desenvolveu um pipeline robusto que evoluiu consideravelmente ao longo do projeto. Inicialmente utilizavam-se técnicas mais simples, mas conforme os testes avançaram e o aprendizado se acumulou, foram incorporados métodos mais sofisticados para extrair o máximo de qualidade das imagens.

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

&emsp; Após extensivos testes, a equipe descobriu que a técnica **CLAHE (Contrast Limited Adaptive Histogram Equalization)** oferece resultados excepcionais para realçar fissuras que às vezes são quase imperceptíveis:

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

## Evolução da Abordagem

&emsp; Uma das características mais interessantes do projeto foi observar como os métodos de pré-processamento se aperfeiçoaram conforme o conhecimento se acumulava:

<p style={{textAlign: 'center'}}>Tabela 1: Evolução do Pré-processamento</p>
<div style={{margin: 25, textAlign: 'center', display: 'flex'}}>
    <table style={{margin: 'auto'}}>
        <thead>
          <tr>
            <th>Técnica</th>
            <th>Versão 1 (ResNet-18)</th>
            <th>Versão 2 (Swin Transformer)</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>CLAHE</td>
            <td>Clip limit: 2.0</td>
            <td>Clip limit: 3.0 (otimizado)</td>
          </tr>
          <tr>
            <td>Tile Grid</td>
            <td>(4,4)</td>
            <td>(8,8) - maior resolução</td>
          </tr>
          <tr>
            <td>Sharpening</td>
            <td>Strength: 1.0</td>
            <td>Strength: 1.2 - realce aprimorado</td>
          </tr>
          <tr>
            <td>Square Padding</td>
            <td>Implementação básica</td>
            <td>Centralização otimizada</td>
          </tr>
          <tr>
            <td>Validação</td>
            <td>Formatos limitados</td>
            <td>Suporte amplo (.jpg, .png, .bmp, .tiff)</td>
          </tr>
        </tbody>
    </table>
</div>
<p style={{textAlign: 'center'}}>Fonte: Desenvolvimento iterativo da SOD com validação empírica (2025). </p>

### Fundamentos das Melhorias

&emsp; As otimizações implementadas na segunda versão basearam-se em:

1. **Experimentação sistemática**: Múltiplas configurações testadas até identificar as mais eficazes
2. **Validação empírica**: Experimentos com diferentes parâmetros em subconjuntos dos dados
3. **Pesquisa especializada**: Incorporação de técnicas avançadas para imagens de infraestrutura
4. **Feedback dos modelos**: Ajustes baseados na resposta dos classificadores

## Técnicas Avançadas de Data Augmentation

&emsp; Além do pré-processamento fundamental, a equipe implementou técnicas para simular diferentes condições que os modelos podem encontrar em aplicações reais:

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

## Impacto Quantificado do Pré-processamento

&emsp; O pipeline otimizado demonstrou impacto substancial na performance dos modelos:

<p style={{textAlign: 'center'}}>Tabela 2: Impacto do Pré-processamento na Performance</p>
<div style={{margin: 25, textAlign: 'center', display: 'flex'}}>
    <table style={{margin: 'auto'}}>
        <thead>
          <tr>
            <th>Métrica</th>
            <th>Sem Pré-processamento</th>
            <th>Com Pipeline SOD</th>
            <th>Melhoria</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>Acurácia</td>
            <td>78.3%</td>
            <td>96.9%</td>
            <td>+18.6%</td>
          </tr>
          <tr>
            <td>Precisão</td>
            <td>75.1%</td>
            <td>97.0%</td>
            <td>+21.9%</td>
          </tr>
          <tr>
            <td>Recall</td>
            <td>81.2%</td>
            <td>96.9%</td>
            <td>+15.7%</td>
          </tr>
          <tr>
            <td>Robustez</td>
            <td>Baixa (σ=4.2%)</td>
            <td>Alta (σ=0.8%)</td>
            <td>Estabilidade 5x</td>
          </tr>
        </tbody>
    </table>
</div>
<p style={{textAlign: 'center'}}>Fonte: Experimentos controlados com modelo Swin Transformer V2 (2025). </p>

&emsp; **Metodologia de avaliação**: Comparação realizada com o mesmo modelo (Swin Transformer V2) treinado em condições idênticas, variando exclusivamente a aplicação do pipeline de pré-processamento.

## Implementação Unificada

&emsp; Todo o desenvolvimento culminou em uma função integrada que qualquer membro da equipe pode utilizar facilmente:

```python
def preprocess_for_classification(image_path: str, 
                                target_size: int = 224) -> torch.Tensor:
    """
    Pipeline completo de pré-processamento desenvolvido pela SOD
    """
    # 1. Validação de formato
    if not validate_image_format(image_path):
        raise ValueError(f"Formato não suportado: {image_path}")
    
    image = cv2.imread(image_path)
    
    # 2. Redimensionamento preservando proporções
    image = square_pad_resize(image, target_size)
    
    # 3. Melhoramento de contraste
    image = apply_clahe(image, clip_limit=3.0, tile_grid_size=(8, 8))
    
    # 4. Realce de bordas
    image = apply_sharpening(image, strength=1.2)
    
    # 5. Equalização seletiva
    image = selective_histogram_equalization(image)
    
    # 6. Preparação para o modelo
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = image.astype(np.float32) / 255.0
    
    # 7. Transformação em tensor
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],  # Padrão ImageNet
            std=[0.229, 0.224, 0.225]
        )
    ])
    
    return transform(image)
```

## Considerações de Performance

&emsp; O pipeline foi otimizado para equilibrar qualidade e eficiência operacional:

- **Tempo de processamento**: ~45ms por imagem em CPU moderna
- **Uso de memória**: Otimizado para processamento em lote
- **Paralelização**: Compatibilidade com processamento multi-thread
- **Escalabilidade**: Adequado para volumes de produção

## Conclusões e Direções Futuras

&emsp; O desenvolvimento do pipeline de pré-processamento pela SOD demonstra a importância crítica desta etapa no sucesso de sistemas de classificação de imagens. As melhorias implementadas resultaram em ganhos substantivos de performance, estabelecendo fundamentos sólidos para os modelos de classificação.

### Contribuições Principais

1. **Pipeline robusto**: Técnicas validadas especificamente para imagens de fissuras
2. **Melhoria contínua**: Evolução baseada em resultados práticos e feedback
3. **Flexibilidade**: Adaptabilidade a diferentes modelos e condições de captura
4. **Reprodutibilidade**: Implementação padronizada e documentada

### Desenvolvimentos Futuros

&emsp; As próximas iterações do pipeline podem incluir:

- **Adaptação automática**: Ajuste dinâmico de parâmetros baseado na qualidade da imagem
- **Especialização por estrutura**: Técnicas específicas para diferentes tipos de infraestrutura
- **Otimização de hardware**: Implementação GPU para processamento em tempo real
- **Validação em campo**: Ajustes baseados em condições reais de operação

&emsp; O trabalho estabelecido nesta etapa fornece os fundamentos necessários para a implementação bem-sucedida dos [modelos de classificação](./primeiro-modelo-s3) e da [pipeline unificada](./pipeline-unificada), garantindo que o sistema SOD opere com máxima eficiência e confiabilidade na detecção de fissuras em infraestrutura.

## Bibliografia

* PIZER, Stephen M. et al. Adaptive histogram equalization and its variations. **Computer Vision, Graphics, and Image Processing**, v. 39, n. 3, p. 355-368, 1987.

* ZUIDERVELD, Karel. Contrast limited adaptive histogram equalization. **Graphics Gems IV**, p. 474-485, 1994.

* GONZALEZ, Rafael C.; WOODS, Richard E. Digital Image Processing. **4th Edition**, Pearson, 2018.

* SHORTEN, Connor; KHOSHGOFTAAR, Taghi M. A survey on image data augmentation for deep learning. **Journal of Big Data**, v. 6, n. 1, p. 1-48, 2019.

* BUSLAEV, Alexander et al. Albumentations: fast and flexible image augmentations. **Information**, v. 11, n. 2, p. 125, 2020. 