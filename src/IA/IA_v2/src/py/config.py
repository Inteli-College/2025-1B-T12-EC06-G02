import os
from pathlib import Path

# Import torch only when CUDA check is needed
def _get_device():
    """Get device (cuda/cpu) with lazy torch import."""
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
    """Configurações para o modelo de classificação de fissuras"""
    
    # Detectar diretório base automaticamente
    BASE_DIR = _get_base_dir()
    
    # Dados - usando pathlib para compatibilidade cross-platform
    DATA_PATH = str(BASE_DIR / "data" / "raw")
    PROCESSED_DATA_PATH = str(BASE_DIR / "data" / "processed")
    SPLITS_PATH = str(BASE_DIR / "data" / "splits")
    MODELS_PATH = str(BASE_DIR / "models")
    
    # Criar diretórios se não existirem
    @classmethod
    def ensure_directories(cls):
        """Cria diretórios necessários se não existirem."""
        dirs_to_create = [
            cls.DATA_PATH,
            cls.PROCESSED_DATA_PATH, 
            cls.SPLITS_PATH,
            cls.MODELS_PATH
        ]
        
        for dir_path in dirs_to_create:
            os.makedirs(dir_path, exist_ok=True)
            
        print(f"Diretório base: {cls.BASE_DIR}")
        print(f"Dados em: {cls.DATA_PATH}")
        print(f"Modelos em: {cls.MODELS_PATH}")
        
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
    MODEL_TYPE = "swin"
    MODEL_NAME = "swin_base_patch4_window7_224"
    PRETRAINED = True
    DROPOUT_RATE = 0.2
    
    # Treinamento
    BATCH_SIZE = 16
    LEARNING_RATE = 3e-5
    WEIGHT_DECAY = 1e-2
    EPOCHS = 100
    
    # Optimizer e Scheduler
    OPTIMIZER = "adamw"
    BETAS = (0.9, 0.999)
    EPS = 1e-8
    
    # Learning Rate Scheduler
    SCHEDULER = "cosine_warmup"
    WARMUP_EPOCHS = 5
    MIN_LR = 1e-7
    
    # Early stopping
    PATIENCE = 15
    MIN_DELTA = 0.0005
    
    # Divisão dos dados
    TRAIN_SPLIT = 0.7
    VAL_SPLIT = 0.15
    TEST_SPLIT = 0.15
    RANDOM_SEED = 42
    
    # Data Augmentation
    HORIZONTAL_FLIP_PROB = 0.5
    VERTICAL_FLIP_PROB = 0.3
    ROTATION_LIMIT = 20
    ROTATION_PROB = 0.6
    BRIGHTNESS_CONTRAST_PROB = 0.7
    BRIGHTNESS_LIMIT = 0.2
    CONTRAST_LIMIT = 0.2
    BLUR_PROB = 0.4
    BLUR_LIMIT = 3
    NOISE_PROB = 0.4
    NOISE_VAR_LIMIT = (10, 30)
    ZOOM_PROB = 0.5
    ZOOM_SCALE = (0.8, 1.2)
    
    # Augmentations específicas
    ELASTIC_TRANSFORM_PROB = 0.3
    GRID_DISTORTION_PROB = 0.3
    OPTICAL_DISTORTION_PROB = 0.3
    
    # Filtros de pré-processamento
    USE_CLAHE = True
    CLAHE_CLIP_LIMIT = 3.0
    CLAHE_TILE_GRID_SIZE = (8, 8)
    
    USE_SHARPEN = True
    SHARPEN_STRENGTH = 1.2
    SHARPEN_KERNEL_TYPE = "laplacian"
    
    USE_SQUARE_PADDING = True
    SQUARE_PADDING_COLOR = (0, 0, 0)
    
    USE_EQUALIZE = True
    
    # Normalização ImageNet
    NORMALIZE_MEAN = [0.485, 0.456, 0.406]
    NORMALIZE_STD = [0.229, 0.224, 0.225]
    
    # Sistema
    DEVICE = _get_device()  # Lazy import do torch
    NUM_WORKERS = 8 if os.cpu_count() > 8 else 4
    PIN_MEMORY = True if DEVICE == "cuda" else False
    MIXED_PRECISION = True
    
    # MLflow
    EXPERIMENT_NAME = "crack_classification_swin_transformer"
    TRACKING_URI = "file:./mlruns"
    
    # Checkpoints
    SAVE_CHECKPOINTS = True
    SAVE_BEST_ONLY = True
    CHECKPOINT_FREQ = 10
    LOG_INTERVAL = 5
    
    # Métricas e avaliação
    CALCULATE_PRECISION = True
    CALCULATE_RECALL = True
    CALCULATE_F1 = True
    CALCULATE_CONFUSION_MATRIX = True
    CALCULATE_AUC = True
    
    # Técnicas avançadas
    LABEL_SMOOTHING = 0.1
    GRADIENT_CLIPPING = 1.0
    
    # Teste Time Augmentation (TTA)
    USE_TTA = True
    TTA_STEPS = 5
    
    @classmethod
    def get_model_config(cls):
        """Retorna configuração específica do modelo."""
        return {
            "num_classes": cls.NUM_CLASSES,
            "model_type": cls.MODEL_TYPE,
            "model_name": cls.MODEL_NAME,
            "pretrained": cls.PRETRAINED,
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
            "scheduler": cls.SCHEDULER,
            "warmup_epochs": cls.WARMUP_EPOCHS,
            "min_lr": cls.MIN_LR,
            "gradient_clipping": cls.GRADIENT_CLIPPING,
            "label_smoothing": cls.LABEL_SMOOTHING,
            "mixed_precision": cls.MIXED_PRECISION
        }
