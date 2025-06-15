# YOLOv8 Ultralytics – Detecção de Objetos

    Nesta sprint, buscamos explorar um novo caminho: utilizar **um único modelo capaz de detectar e classificar fissuras** em imagens — distinguindo entre fissuras de retração e fissuras térmicas. Para isso, foi adotado o modelo **YOLOv8**, da Ultralytics, amplamente reconhecido por sua eficiência em tarefas de detecção de objetos.


## 1. Instalação de Dependências

```python
!pip install ultralytics roboflow 
```

Instalação das bibliotecas necessárias:

* **ultralytics**: Biblioteca oficial para uso do YOLOv8, com suporte a detecção, segmentação e classificação.
* **roboflow**: Facilita a importação e gerenciamento de datasets anotados, especialmente os provenientes da plataforma Roboflow.

## 2. Importação de Bibliotecas

```python
from ultralytics import YOLO
import os
import numpy as np
import cv2
```

Explicação das bibliotecas utilizadas:

* `YOLO`: Classe principal da Ultralytics para trabalhar com modelos YOLOv8.
* `os`: Permite manipulação de diretórios e arquivos.
* `numpy`: Biblioteca para cálculos numéricos, útil na manipulação de arrays de imagem.
* `cv2`: OpenCV para leitura, exibição e modificação de imagens.


## 3. Carregamento e Treinamento do Modelo

```python
# Carrega um modelo pré-treinado
model = YOLO('yolov8n.pt')  # Também pode-se usar: 'yolov8s.pt', 'yolov8m.pt', 'yolov8l.pt', 'yolov8x.pt'

# Inicia o treinamento com parâmetros específicos
model.train(data='data/data.yaml', epochs=50, imgsz=640, batch=16)
```

Detalhes do processo:

* Carrega um modelo base treinado no COCO, adaptável ao seu dataset customizado.
* O treinamento é realizado com base nas anotações definidas no arquivo `data.yaml`, que especifica caminhos para os conjuntos de `train`, `val` e `test`.

Parâmetros:

* `epochs=50`: Número de ciclos completos de treinamento.
* `imgsz=640`: Redimensionamento das imagens de entrada para 640x640.
* `batch=16`: Número de imagens processadas simultaneamente.


## 4. Predição no Conjunto de Teste

```python
from ultralytics import YOLO
import os
from pathlib import Path

# Carrega o modelo treinado
model = YOLO('../../../../../runs/detect/train/weights/best.pt')

# Diretório com imagens de teste
test_images_dir = Path('data/test/images')

# Loop pelas imagens
for image_file in test_images_dir.glob('*.jpg'):
    print(f'Processando {image_file.name}...')

    # Realiza a predição
    results = model.predict(source=str(image_file), save=True, conf=0.3)

    # Exibe imagem com as predições (opcional)
    results[0].show()

    # Quantidade de objetos detectados
    boxes = results[0].boxes
    print(f'Detectado {len(boxes)} objeto(s) em {image_file.name}')
```

### Explicação:

* O modelo treinado é carregado e utilizado para inferência sobre as imagens do conjunto de teste.
* As detecções são salvas automaticamente em uma pasta de saída (`runs/`).
* A predição inclui a localização (bounding boxes) e a classe da fissura detectada.
* A confiança mínima para a detecção é ajustada com `conf=0.3`.


## Observações Importantes

* **Estrutura do dataset**: Verifique se o `data.yaml` aponta corretamente para os diretórios de treino, validação e teste.
* **Ajuste de parâmetros**: É possível adaptar `epochs`, `batch`, `imgsz`, `conf` e outros conforme os recursos disponíveis e a complexidade do problema.
* **Saídas do treinamento**: Os modelos e métricas são salvos no diretório `runs/detect/train/`, sendo `best.pt` o modelo com melhor desempenho durante o treino.


## Resultados

Durante os testes, observou-se que o modelo YOLOv8 foi **mais preciso na detecção de fissuras de retração** do que nas fissuras térmicas. Isso sugere que há espaço para melhoria na capacidade de **classificação do tipo de fissura**, apesar da detecção em si ser promissora.


## Próximos Passos

* Avaliar formas de **melhorar a acurácia da classificação**, possivelmente através de:

  * Ajuste fino de hiperparâmetros.
  * Aplicação de filtros ou estratégias de pré-processamento de imagem.
* Considerar o uso do YOLOv8 **apenas para localização** das fissuras, integrando-o com um segundo modelo especializado na **classificação do tipo**.
* Explorar outras arquiteturas ou variantes do YOLO (como segmentação) para capturar detalhes mais sutis nas imagens.