import os
from pathlib import Path

def _get_device():
    try:
        import torch
        return "cuda" if torch.cuda.is_available() else "cpu"
    except ImportError:
        return "cpu"

def _get_base_dir():
    """Detecta o diretório base do projeto automaticamente."""
    current_file = Path(__file__).resolve()
    
    # Procurar pela pasta 'data' subindo na hierarquia
    for parent in current_file.parents:
        # Procurar por src/data
        data_dir = parent / "src" / "data"
        if data_dir.exists():
            return parent / "src"
        
        # Procurar diretamente pela pasta data
        data_dir = parent / "data"
        if data_dir.exists():
            return parent
            
        # Procurar por IA_v2/src/data
        ia_data_dir = parent / "IA_v2" / "src" / "data"
        if ia_data_dir.exists():
            return parent / "IA_v2" / "src"
    
    # Se não encontrar, usar o diretório do arquivo atual como base
    return current_file.parent.parent

class Config:
    
    # Detectar diretório base automaticamente
    BASE_DIR = _get_base_dir()
    
    # Dados - usando pathlib para compatibilidade cross-platform
    DATA_PATH = str(BASE_DIR / "data" / "raw")
    PROCESSED_DATA_PATH = str(BASE_DIR / "data" / "processed")
    SPLITS_PATH = str(BASE_DIR / "data" / "splits")
    
    # Modelos específicos desta versão do modelo
    MODEL_DIR = Path(__file__).parent
    MODELS_PATH = str(MODEL_DIR / "models")
    MLFLOW_PATH = str(MODEL_DIR / "mlruns")
    
    # Criar diretórios se não existirem
    @classmethod
    def ensure_directories(cls):
        """Cria diretórios necessários se não existirem."""
        dirs_to_create = [
            cls.DATA_PATH,
            cls.PROCESSED_DATA_PATH, 
            cls.SPLITS_PATH,
            cls.MODELS_PATH,
            cls.MLFLOW_PATH
        ]
        
        for dir_path in dirs_to_create:
            os.makedirs(dir_path, exist_ok=True)
            
        print(f"Diretório base: {cls.BASE_DIR}")
        print(f"Dados em: {cls.DATA_PATH}")
        print(f"Modelos em: {cls.MODELS_PATH}")
        print(f"MLflow em: {cls.MLFLOW_PATH}")
        
        # Verificar se as pastas de classes existem
        retracao_path = Path(cls.DATA_PATH) / "retracao"
        termicas_path = Path(cls.DATA_PATH) / "termicas"
        
        if not retracao_path.exists():
            retracao_path.mkdir(parents=True, exist_ok=True)
            print(f"Criada pasta: {retracao_path}")
            
        if not termicas_path.exists():
            termicas_path.mkdir(parents=True, exist_ok=True)
            print(f"Criada pasta: {termicas_path}")
    
    # Classes do dataset
    CLASSES = ["retracao", "termicas"]
    NUM_CLASSES = len(CLASSES)
    
    # Configurações de imagem
    IMAGE_SIZE = 224
    IMAGE_CHANNELS = 3
    
    # Modelo
    MODEL_TYPE = "resnet"
    MODEL_NAME = "resnet18"
    PRETRAINED = True
    FREEZE_BACKBONE = False
    DROPOUT_RATE = 0.5
    
    # Treinamento
    BATCH_SIZE = 32
    LEARNING_RATE = 0.001
    WEIGHT_DECAY = 1e-4
    EPOCHS = 50
    
    # Optimizer e Scheduler
    OPTIMIZER = "adam"
    SCHEDULER = "cosine"
    
    # Early stopping
    PATIENCE = 10
    MIN_DELTA = 0.001
    
    # Divisão dos dados
    TRAIN_SPLIT = 0.7
    VAL_SPLIT = 0.15
    TEST_SPLIT = 0.15
    RANDOM_SEED = 42
    
    # Data Augmentation
    HORIZONTAL_FLIP_PROB = 0.5
    VERTICAL_FLIP_PROB = 0.2
    ROTATION_LIMIT = 15
    ROTATION_PROB = 0.5
    BRIGHTNESS_CONTRAST_PROB = 0.5
    BRIGHTNESS_LIMIT = 0.2
    CONTRAST_LIMIT = 0.2
    BLUR_PROB = 0.3
    NOISE_PROB = 0.3
    ZOOM_PROB = 0.3
    
    # Configurações de pré-processamento
    CLAHE_CLIP_LIMIT = 2.0
    CLAHE_TILE_GRID_SIZE = (8, 8)
    
    # Filtros customizados (desabilitados para evitar problemas de dimensão)
    USE_CLAHE = False
    USE_SHARPEN = False
    USE_SQUARE_PADDING = False
    USE_EQUALIZE = False
    
    # Normalização ImageNet
    NORMALIZE_MEAN = [0.485, 0.456, 0.406]
    NORMALIZE_STD = [0.229, 0.224, 0.225]
    
    # Sistema
    DEVICE = _get_device()
    NUM_WORKERS = 0  # Mantém 0 para Windows (funciona melhor)
    PIN_MEMORY = True if DEVICE == "cuda" else False
    
    # MLflow - específico para este modelo
    EXPERIMENT_NAME = "resnet18_crack_classification"
    TRACKING_URI = f"file://{MLFLOW_PATH}"
    USE_MLFLOW = True
    
    # Checkpoints
    SAVE_CHECKPOINTS = True
    SAVE_BEST_ONLY = True
    CHECKPOINT_FREQ = 5
    LOG_INTERVAL = 10
    
    # Métricas e avaliação
    CALCULATE_PRECISION = True
    CALCULATE_RECALL = True
    CALCULATE_F1 = True
    CALCULATE_CONFUSION_MATRIX = True
    
    @classmethod
    def get_model_config(cls):
        """Retorna configuração específica do modelo."""
        return {
            "model_name": cls.MODEL_NAME,
            "pretrained": cls.PRETRAINED,
            "freeze_backbone": cls.FREEZE_BACKBONE,
            "dropout_rate": cls.DROPOUT_RATE
        }
    
    @classmethod
    def get_training_config(cls):
        """Retorna configuração de treinamento."""
        return {
            "batch_size": cls.BATCH_SIZE,
            "learning_rate": cls.LEARNING_RATE,
            "weight_decay": cls.WEIGHT_DECAY,
            "epochs": cls.EPOCHS,
            "optimizer": cls.OPTIMIZER,
            "scheduler": cls.SCHEDULER
        } 