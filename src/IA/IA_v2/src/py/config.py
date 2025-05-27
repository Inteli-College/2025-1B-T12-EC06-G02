import os
import torch

class Config:
    """Configurações"""
    
    # Dados
    DATA_PATH = "data/raw"
    PROCESSED_DATA_PATH = "data/processed" 
    SPLITS_PATH = "data/splits"
    MODELS_PATH = "models"
    
    # Classes do dataset
    CLASSES = ["retracao", "termicas"]
    NUM_CLASSES = len(CLASSES)
    
    # Configurações de imagem
    IMAGE_SIZE = 224
    IMAGE_CHANNELS = 3
    
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
    
    # MLflow
    EXPERIMENT_NAME = "image_classification_retracao_termicas"
    TRACKING_URI = "file:./mlruns"
    
    # Checkpoints
    SAVE_CHECKPOINTS = True
    CHECKPOINT_FREQ = 5
    LOG_INTERVAL = 10
    
    # Métricas
    CALCULATE_PRECISION = True
    CALCULATE_RECALL = True
    CALCULATE_F1 = True
    CALCULATE_CONFUSION_MATRIX = True
