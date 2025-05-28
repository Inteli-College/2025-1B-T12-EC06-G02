import os
import torch

class Config:
    """Configurações"""
    
    # Dados
    DATA_PATH = "../data/raw"
    PROCESSED_DATA_PATH = "../data/processed" 
    SPLITS_PATH = "../data/splits"
    MODELS_PATH = "models"
    
    # Classes do dataset
    CLASSES = ["retracao", "termicas"]
    NUM_CLASSES = len(CLASSES)
    
    # Configurações de imagem
    IMAGE_SIZE = 224
    IMAGE_CHANNELS = 3
    
    # === CONFIGURAÇÕES DE MODELO ===
    # Opções: 'custom_cnn', 'resnet'
    MODEL_TYPE = "resnet"
    
    # Configurações específicas por tipo de modelo
    MODEL_CONFIGS = {
        'custom_cnn': {
            'dropout_rate': 0.5
        },
        'resnet': {
            'model_name': 'resnet18',  # resnet18, resnet34, resnet50, resnet101
            'pretrained': True,
            'freeze_backbone': False  # True para fine-tuning apenas do classificador
        }
    }
    
    # Treinamento
    BATCH_SIZE = 32
    LEARNING_RATE = 0.001
    EPOCHS = 50
    OPTIMIZER = "adam"
    WEIGHT_DECAY = 1e-4
    SCHEDULER = "cosine"
    
    # Early stopping
    PATIENCE = 10
    MIN_DELTA = 0.001
    
    # Divisão dos dados
    TRAIN_SPLIT = 0.7
    VAL_SPLIT = 0.15
    TEST_SPLIT = 0.15
    RANDOM_SEED = 42
    
    # Augmentation
    HORIZONTAL_FLIP_PROB = 0.5
    VERTICAL_FLIP_PROB = 0.2
    ROTATION_LIMIT = 15
    ROTATION_PROB = 0.5
    BRIGHTNESS_CONTRAST_PROB = 0.5
    BLUR_PROB = 0.3
    NOISE_PROB = 0.3
    ZOOM_PROB = 0.3
    
    # Filtros personalizados - acoplar/desacoplar facilmente
    USE_CLAHE = True
    CLAHE_CLIP_LIMIT = 2.0
    CLAHE_TILE_GRID_SIZE = (8, 8)
    
    USE_SHARPEN = True
    SHARPEN_STRENGTH = 1.0
    SHARPEN_KERNEL_TYPE = "laplacian"
    
    USE_SQUARE_PADDING = True
    SQUARE_PADDING_COLOR = (0, 0, 0)
    
    USE_EQUALIZE = False  # Opcional
    
    # Sistema
    DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
    NUM_WORKERS = 4 if os.cpu_count() > 4 else 2
    PIN_MEMORY = True if DEVICE == "cuda" else False
    
    # MLflow (simplificado - desabilitado para evitar problemas)
    EXPERIMENT_NAME = "image_classification_retracao_termicas"
    USE_MLFLOW = False
    
    # Checkpoints
    SAVE_CHECKPOINTS = True
    CHECKPOINT_FREQ = 5
    LOG_INTERVAL = 10
    
    # Métricas
    CALCULATE_PRECISION = True
    CALCULATE_RECALL = True
    CALCULATE_F1 = True
    CALCULATE_CONFUSION_MATRIX = True
    
    @classmethod
    def get_model_config(cls):
        """Retorna a configuração do modelo atual."""
        return cls.MODEL_CONFIGS.get(cls.MODEL_TYPE, {})


# Configurações pré-definidas para diferentes cenários
class FastTrainingConfig(Config):
    """Configuração para treinamento rápido/teste."""
    MODEL_TYPE = "resnet"
    MODEL_CONFIGS = {
        **Config.MODEL_CONFIGS,
        'resnet': {
            'model_name': 'resnet18',
            'pretrained': True,
            'freeze_backbone': False
        }
    }
    BATCH_SIZE = 64
    EPOCHS = 20
    LEARNING_RATE = 0.001
    

class HighAccuracyConfig(Config):
    """Configuração para máxima acurácia."""
    MODEL_TYPE = "resnet"
    MODEL_CONFIGS = {
        **Config.MODEL_CONFIGS,
        'resnet': {
            'model_name': 'resnet50',
            'pretrained': True,
            'freeze_backbone': False
        }
    }
    BATCH_SIZE = 16  # Menor para modelos maiores
    EPOCHS = 100
    LEARNING_RATE = 0.0005
    PATIENCE = 15


class LightweightConfig(Config):
    """Configuração para modelos leves."""
    MODEL_TYPE = "custom_cnn"
    BATCH_SIZE = 64
    EPOCHS = 50
    LEARNING_RATE = 0.002


class FineTuningConfig(Config):
    """Configuração para fine-tuning."""
    MODEL_TYPE = "resnet"
    MODEL_CONFIGS = {
        **Config.MODEL_CONFIGS,
        'resnet': {
            'model_name': 'resnet50',
            'pretrained': True,
            'freeze_backbone': True  # Congela backbone, treina apenas classificador
        }
    }
    BATCH_SIZE = 32
    EPOCHS = 30
    LEARNING_RATE = 0.01  # LR maior para classificador
    PATIENCE = 8