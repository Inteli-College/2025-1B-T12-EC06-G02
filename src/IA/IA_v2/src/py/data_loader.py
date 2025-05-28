"""
Módulo para carregamento e organização dos dados de imagem (sem sklearn).
"""

import os
import glob
import random
import numpy as np
from typing import List, Tuple, Dict

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
                print(f"Aviso: Pasta {class_path} não encontrada!")
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
            print(f"Classe '{class_name}': {len(class_images)} imagens encontradas")
            
            image_paths.extend(class_images)
            labels.extend([class_idx] * len(class_images))
        
        print(f"Total: {len(image_paths)} imagens encontradas")
        return image_paths, labels
    
    def stratified_split(self, image_paths: List[str], labels: List[int]) -> Dict[str, Tuple[List[str], List[int]]]:
        """Split estratificado manual (sem sklearn)."""
        # Agrupar por classe
        class_data = {}
        for path, label in zip(image_paths, labels):
            if label not in class_data:
                class_data[label] = []
            class_data[label].append(path)
        
        train_paths, train_labels = [], []
        val_paths, val_labels = [], []
        test_paths, test_labels = [], []
        
        # Para cada classe, fazer split proporcional
        for class_idx, paths in class_data.items():
            # Embaralhar
            shuffled_paths = paths.copy()
            random.shuffle(shuffled_paths)
            
            n_total = len(shuffled_paths)
            n_train = int(n_total * self.config.TRAIN_SPLIT)
            n_val = int(n_total * self.config.VAL_SPLIT)
            
            # Garantir que cada split tenha pelo menos 1 imagem (se possível)
            if n_total >= 3:
                if n_train == 0:
                    n_train = 1
                if n_val == 0:
                    n_val = 1
            
            # Split
            class_train = shuffled_paths[:n_train]
            class_val = shuffled_paths[n_train:n_train + n_val]
            class_test = shuffled_paths[n_train + n_val:]
            
            # Adicionar às listas finais
            train_paths.extend(class_train)
            train_labels.extend([class_idx] * len(class_train))
            
            val_paths.extend(class_val)
            val_labels.extend([class_idx] * len(class_val))
            
            test_paths.extend(class_test)
            test_labels.extend([class_idx] * len(class_test))
            
            print(f"Classe {class_idx}: {len(class_train)} treino, {len(class_val)} val, {len(class_test)} teste")
        
        return {
            'train': (train_paths, train_labels),
            'val': (val_paths, val_labels),
            'test': (test_paths, test_labels)
        }
    
    def create_splits(self, image_paths: List[str], labels: List[int]) -> Dict[str, Tuple[List[str], List[int]]]:
        """Cria as divisões de treino, validação e teste."""
        random.seed(self.config.RANDOM_SEED)
        
        return self.stratified_split(image_paths, labels)
    
    def get_splits(self) -> Dict[str, Tuple[List[str], List[int]]]:
        """Obtém as divisões do dataset."""
        image_paths, labels = self.discover_images()
        
        if len(image_paths) == 0:
            raise ValueError("Nenhuma imagem encontrada no dataset!")
        
        return self.create_splits(image_paths, labels)