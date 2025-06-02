---
sidebar_position: 2
slug: /inteligencia-artificial/guia-execucao
description: "Instruções para executar e usar os modelos de IA"
---

# Guia de Execução

&emsp; Este guia fornece instruções práticas para executar, treinar e usar os modelos de classificação de fissuras desenvolvidos pela SOD.

## Configuração Inicial

### Pré-requisitos
```bash
# Python 3.8 ou superior
python --version

# Verificar CUDA (opcional, para GPU)
nvidia-smi
```

### Instalação
```bash
# Clonar repositório e navegar
cd src/IA/IA_v2

# Criar uma venv 
python -m venv venv

# Instalar dependências
pip install -r requirements.txt
```

### Estrutura de Dados
```
IA_v2/src/data/raw/
├── retracao/          # Fissuras de retração
│   ├── img_001.jpg
│   └── ...
└── termicas/          # Fissuras térmicas
    ├── img_001.jpg
    └── ...
```

**Formatos aceitos**: `.jpg`, `.jpeg`, `.png`, `.bmp`, `.tiff`

## Execução dos Modelos

### Swin Transformer V2 (Produção)

```bash
# Navegar para diretório estando em 
cd src/swin-transformer-v2/

python main.py

# Treinamento com configurações específicas
python main.py train --gpu    # Forçar GPU
python main.py train --cpu    # Forçar CPU

# Monitorar treinamento
mlflow ui --backend-store-uri file:./mlruns
# Acesse: http://localhost:5000
```

#### Configurações Importantes
```python
# Editar config.py se necessário
BATCH_SIZE = 16           # Ajustar conforme memória GPU
LEARNING_RATE = 3e-5      # Otimizado para transformers
EPOCHS = 100
USE_MIXED_PRECISION = True
```

### ResNet-18 (Experimental)

```bash
# Navegar para diretório
cd resnet-18/

# Treinamento básico
python main.py train

# Listar modelos salvos
python main.py list

# Avaliar modelo específico
python main.py eval models/best_model.pth
```

#### Configurações Básicas
```python
# config.py
BATCH_SIZE = 32
LEARNING_RATE = 0.001
EPOCHS = 50
MODEL_NAME = "resnet18"
```

## Pipeline Unificada (Recomendado)

### Inferência Simples
```python
from modules.inference import UnifiedCrackClassifier

# Carregar modelo (detecta automaticamente o tipo)
classifier = UnifiedCrackClassifier("caminho/para/modelo.pth")

# Classificar uma imagem
resultado = classifier.predict("imagem_teste.jpg")

print(f"Classe: {resultado['predicted_class']}")
print(f"Confiança: {resultado['confidence']:.1f}%")
print(f"Probabilidades: {resultado['probabilities']}")
```

### Inferência em Lote
```python
from modules.inference import classify_for_frontend

# Preparar dados
image_paths = ["img1.jpg", "img2.jpg", "img3.jpg"]
image_ids = ["id1", "id2", "id3"]
preview_urls = ["url1", "url2", "url3"]
model_path = "swin-transformer-v2/models/best_model.pth"

# Classificar em lote
results = classify_for_frontend(
    image_paths, image_ids, preview_urls, model_path
)

# Resultado:
# [
#     {"id": "id1", "previewUrl": "url1", "prev": "retracao"},
#     {"id": "id2", "previewUrl": "url2", "prev": "termica"},
#     ...
# ]
```

### API para Integração
```python
from flask import Flask, request, jsonify
from modules.inference import load_classifier

app = Flask(__name__)

# Carregar modelo uma vez
classifier = load_classifier("swin-transformer-v2/models/best_model.pth")

@app.route('/classify', methods=['POST'])
def classify():
    image_path = request.json['image_path']
    
    try:
        result = classifier.predict(image_path)
        return jsonify({
            "success": True,
            "prediction": result['predicted_class'],
            "confidence": result['confidence']
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
```

## Comandos Úteis

### Gerenciamento de Modelos
```bash
# Listar modelos disponíveis
python main.py list

# Avaliar modelo específico
python main.py eval models/best_model.pth

# Inferência em imagem única
python main.py infer models/best_model.pth imagem.jpg
```

### Busca de Hiperparâmetros
```bash
# ResNet-18 - Grid search automático
cd resnet-18/
python hyperparameter_search.py

# Personalizar editando hyperparameter_search.py
grid = {
    'LEARNING_RATE': [0.001, 0.0005],
    'BATCH_SIZE': [16, 32],
    'EPOCHS': [30, 50]
}
```

### Monitoramento MLflow
```bash
# Iniciar interface web
mlflow ui --backend-store-uri file:./mlruns

# Comparar experimentos
# Acessar: http://localhost:5000
# Filtrar por métricas, visualizar curvas, comparar modelos
```

&emsp; Para dúvidas específicas sobre implementação ou problemas não cobertos neste guia, consulte a documentação técnica dos modelos individuais: [ResNet-18](./modelos/primeiro-modelo-s3.md), [Swin Transformer V2](./modelos/segundo-modelo-s3.md) ou [Pipeline Unificada](./pipeline-unificada).