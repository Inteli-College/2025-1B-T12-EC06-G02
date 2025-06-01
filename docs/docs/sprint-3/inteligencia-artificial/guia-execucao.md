---
sidebar_position: 1
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
cd IA_v2/src/

# Instalar dependências
pip install -r requirements.txt

# Verificar instalação
python -c "import torch; print(f'PyTorch: {torch.__version__}')"
python -c "import torch; print(f'CUDA: {torch.cuda.is_available()}')"
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
# Navegar para diretório
cd swin-transformer-v2/

# Treinamento completo
python main.py train

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

## Solução de Problemas

### Erro de Memória
```python
# Reduzir batch size
BATCH_SIZE = 8  # Em vez de 16/32

# Usar mixed precision (Swin Transformer)
USE_MIXED_PRECISION = True

# Limpar cache GPU
import torch
torch.cuda.empty_cache()
```

### Performance Lenta
```bash
# Verificar uso de GPU
nvidia-smi

# Otimizar workers (ajustar no config.py)
NUM_WORKERS = 0   # Windows
NUM_WORKERS = 4   # Linux/Mac
```

### Problemas de Importação
```python
# Verificar instalação
pip list | grep torch
pip list | grep albumentations

# Reinstalar se necessário
pip install --upgrade torch torchvision
```

## Deployment em Produção

### Docker Container
```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    libglib2.0-0 libsm6 libxext6 libxrender-dev libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements e instalar
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código
COPY . .

# Expor porta
EXPOSE 8000

# Comando de inicialização
CMD ["python", "app.py"]
```

### Build e Execução
```bash
# Build da imagem
docker build -t sod-ia-classifier .

# Executar container
docker run -p 8000:8000 -v $(pwd)/models:/app/models sod-ia-classifier

# Testar
curl -X POST http://localhost:8000/classify \
  -H "Content-Type: application/json" \
  -d '{"image_path": "/path/to/image.jpg"}'
```

## Recomendações

### Para Desenvolvimento
- **Usar Swin Transformer V2** para desenvolvimento ativo
- **ResNet-18 apenas para referência** e comparação
- **Sempre validar** em conjunto de teste independente
- **Monitorar com MLflow** para tracking de experimentos

### Para Produção
- **Swin Transformer V2 exclusivamente** para aplicações críticas
- **Pipeline unificada** para flexibilidade
- **Docker containers** para deployment consistente
- **Monitoramento de logs** para debugging

### Boas Práticas
1. **Backup de modelos**: Manter cópias dos melhores checkpoints
2. **Versionamento**: Usar MLflow para controle de versões
3. **Validação**: Sempre testar em dados nunca vistos
4. **Logging**: Registrar todas as predições para auditoria

&emsp; Para dúvidas específicas sobre implementação ou problemas não cobertos neste guia, consulte a documentação técnica dos modelos individuais: [ResNet-18](./primeiro-modelo), [Swin Transformer V2](./segundo-modelo) ou [Pipeline Unificada](./pipeline-unificada).