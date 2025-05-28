"""
Módulo para carregamento e organização dos dados de imagem.
"""

import os
import glob
import random
import numpy as np
from typing import List, Tuple, Dict
from sklearn.model_selection import train_test_split

from config import Config


class DataOrganizer:
    """Organiza e divide os dados de treino/validação/teste."""
    
    def __init__(self, config: Config = None):
        self.config = config or Config()
        self.supported_extensions = ['.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.tif']
        
    def discover_images(self) -> Tuple[List[str], List[int]]:
        """Descobre automaticamente todas as imagens no dataset."""
        image_paths = []
        labels = []
        
        for class_idx, class_name in enumerate(self.config.CLASSES):
            class_path = os.path.join(self.config.DATA_PATH, class_name)
            if not os.path.exists(class_path):
                continue
            
            class_images = []
            
            for ext in self.supported_extensions:
                pattern = os.path.join(class_path, f"*{ext}")
                found_images = glob.glob(pattern, recursive=False)
                class_images.extend(found_images)
                
                pattern_upper = os.path.join(class_path, f"*{ext.upper()}")
                found_images_upper = glob.glob(pattern_upper, recursive=False)
                class_images.extend(found_images_upper)
            
            class_images = sorted(list(set(class_images)))
            image_paths.extend(class_images)
            labels.extend([class_idx] * len(class_images))
        
        return image_paths, labels
    
    def create_splits(self, image_paths: List[str], labels: List[int]) -> Dict[str, Tuple[List[str], List[int]]]:
        """Cria as divisões de treino, validação e teste."""
        random.seed(self.config.RANDOM_SEED)
        np.random.seed(self.config.RANDOM_SEED)
        
        train_val_paths, test_paths, train_val_labels, test_labels = train_test_split(
            image_paths, labels,
            test_size=self.config.TEST_SPLIT,
            random_state=self.config.RANDOM_SEED,
            stratify=labels
        )
        
        train_size_relative = self.config.TRAIN_SPLIT / (self.config.TRAIN_SPLIT + self.config.VAL_SPLIT)
        
        train_paths, val_paths, train_labels, val_labels = train_test_split(
            train_val_paths, train_val_labels,
            train_size=train_size_relative,
            random_state=self.config.RANDOM_SEED,
            stratify=train_val_labels
        )
        
        return {
            'train': (train_paths, train_labels),
            'val': (val_paths, val_labels),
            'test': (test_paths, test_labels)
        }
    
    def get_splits(self) -> Dict[str, Tuple[List[str], List[int]]]:
        """Obtém as divisões do dataset."""
        image_paths, labels = self.discover_images()
        
        if len(image_paths) == 0:
            raise ValueError("Nenhuma imagem encontrada no dataset!")
        
        return self.create_splits(image_paths, labels) 