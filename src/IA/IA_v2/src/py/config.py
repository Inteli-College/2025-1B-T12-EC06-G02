class Config:
    # Dados
    DATA_PATH = "data/raw"
    IMAGE_SIZE = 224
    BATCH_SIZE = 32
    
    # Treino
    EPOCHS = 50
    LEARNING_RATE = 0.001
    NUM_CLASSES = 10
    
    # Divisão dos dados
    TRAIN_SPLIT = 0.7
    VAL_SPLIT = 0.10
    TEST_SPLIT = 0.10
    
    # Device
    DEVICE = "cuda"
