"""
Dataset para ResNet-18 com transformações otimizadas.
"""

import sys
import os
import cv2
import torch
import numpy as np
from pathlib import Path
from typing import List, Tuple, Optional, Callable
from torch.utils.data import Dataset, DataLoader

# Adicionar o diretório modules ao path
current_dir = Path(__file__).parent
modules_dir = current_dir.parent / "modules"
sys.path.insert(0, str(modules_dir))

from data_loader import DataOrganizer
import albumentations as A
from albumentations.pytorch import ToTensorV2

from config import Config


class ResNetDataset(Dataset):
    """Dataset otimizado para ResNet-18 com transformações consistentes."""
    
    def __init__(self, 
                 image_paths: List[str],
                 labels: List[int],
                 transform: Optional[Callable] = None,
                 config: Config = None,
                 cache_processed: bool = False):
        
        if len(image_paths) != len(labels):
            raise ValueError(f"Número de imagens ({len(image_paths)}) deve ser igual ao número de labels ({len(labels)})")
        
        self.image_paths = image_paths
        self.labels = labels
        self.transform = transform
        self.config = config
        self.cache_processed = cache_processed
        
        self._image_cache = {} if cache_processed else None
        self.num_classes = len(set(labels))
        self.class_counts = {i: labels.count(i) for i in range(self.num_classes)}
        
    def __len__(self) -> int:
        return len(self.image_paths)
    
    def __getitem__(self, idx: int) -> Tuple[torch.Tensor, int]:
        if self._image_cache is not None and idx in self._image_cache:
            return self._image_cache[idx]
        
        image_path = self.image_paths[idx]
        label = self.labels[idx]
        
        try:
            image = self._load_image(image_path)
            
            if self.transform:
                transformed = self.transform(image=image)
                image = transformed['image']
            
            if self._image_cache is not None:
                self._image_cache[idx] = (image, label)
            
            return image, label
            
        except Exception as e:
            print(f"Erro ao carregar imagem {image_path}: {e}")
            fallback_image = self._create_fallback_image()
            
            if self.transform:
                transformed = self.transform(image=fallback_image)
                fallback_image = transformed['image']
            
            return fallback_image, label
    
    def _load_image(self, image_path: str) -> np.ndarray:
        """Carrega uma imagem de forma robusta."""
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Arquivo não encontrado: {image_path}")
        
        image = cv2.imread(image_path, cv2.IMREAD_COLOR)
        
        if image is None:
            image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
            
            if image is None:
                raise ValueError(f"Não foi possível carregar a imagem: {image_path}")
            
            if len(image.shape) == 2:
                image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
            elif len(image.shape) == 3 and image.shape[2] == 4:
                image = cv2.cvtColor(image, cv2.COLOR_BGRA2RGB)
            elif len(image.shape) == 3 and image.shape[2] == 3:
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        else:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        image = np.ascontiguousarray(image, dtype=np.uint8)
        return image
    
    def _create_fallback_image(self) -> np.ndarray:
        """Cria uma imagem de fallback quando há erro no carregamento."""
        image_size = getattr(self.config, 'IMAGE_SIZE', 224) if self.config else 224
        return np.zeros((image_size, image_size, 3), dtype=np.uint8)
    
    def get_class_weights(self) -> torch.Tensor:
        """Calcula pesos das classes para lidar com desbalanceamento."""
        total_samples = len(self.labels)
        weights = []
        
        for class_idx in range(self.num_classes):
            class_count = self.class_counts[class_idx]
            weight = total_samples / (self.num_classes * class_count)
            weights.append(weight)
        
        return torch.tensor(weights, dtype=torch.float32)


class ResNetAugmentationFactory:
    """Factory para criar transformações específicas do ResNet."""
    
    @staticmethod
    def get_training_transforms(config: Config) -> A.Compose:
        """Cria transformações para treinamento do ResNet."""
        transforms = [
            # Redimensionar para base maior para permitir augmentations
            A.Resize(256, 256, interpolation=cv2.INTER_AREA),
            
            # Augmentações geométricas
            A.HorizontalFlip(p=config.HORIZONTAL_FLIP_PROB),
            A.VerticalFlip(p=config.VERTICAL_FLIP_PROB),
            A.Rotate(
                limit=config.ROTATION_LIMIT, 
                p=config.ROTATION_PROB,
                border_mode=cv2.BORDER_REFLECT_101
            ),
            
            # Augmentações de cor
            A.RandomBrightnessContrast(
                brightness_limit=config.BRIGHTNESS_LIMIT,
                contrast_limit=config.CONTRAST_LIMIT,
                p=config.BRIGHTNESS_CONTRAST_PROB
            ),
            
            # CLAHE para melhoria de contraste
            A.CLAHE(
                clip_limit=config.CLAHE_CLIP_LIMIT,
                tile_grid_size=config.CLAHE_TILE_GRID_SIZE,
                p=0.3
            ),
            
            # Blur e ruído
            A.GaussianBlur(blur_limit=(3, 5), p=config.BLUR_PROB),
            A.GaussNoise(var_limit=50, p=config.NOISE_PROB),
            
            # Crop/resize final para garantir tamanho consistente
            A.RandomResizedCrop(
                size=(config.IMAGE_SIZE, config.IMAGE_SIZE),
                scale=(0.8, 1.0),
                ratio=(0.9, 1.1),
                interpolation=cv2.INTER_AREA,
                p=1.0
            ),
            
            # Normalização ImageNet
            A.Normalize(
                mean=config.NORMALIZE_MEAN,
                std=config.NORMALIZE_STD,
                max_pixel_value=255.0
            ),
            ToTensorV2()
        ]
        
        return A.Compose(transforms)
    
    @staticmethod
    def get_validation_transforms(config: Config) -> A.Compose:
        """Cria transformações para validação."""
        transforms = [
            A.Resize(config.IMAGE_SIZE, config.IMAGE_SIZE, interpolation=cv2.INTER_AREA),
            A.CLAHE(
                clip_limit=config.CLAHE_CLIP_LIMIT * 0.8,
                tile_grid_size=config.CLAHE_TILE_GRID_SIZE,
                p=1.0
            ),
            A.Normalize(
                mean=config.NORMALIZE_MEAN,
                std=config.NORMALIZE_STD,
                max_pixel_value=255.0
            ),
            ToTensorV2()
        ]
        
        return A.Compose(transforms)
    
    @staticmethod
    def get_test_transforms(config: Config) -> A.Compose:
        """Cria transformações para teste."""
        transforms = [
            A.Resize(config.IMAGE_SIZE, config.IMAGE_SIZE, interpolation=cv2.INTER_AREA),
            A.Normalize(
                mean=config.NORMALIZE_MEAN,
                std=config.NORMALIZE_STD,
                max_pixel_value=255.0
            ),
            ToTensorV2()
        ]
        
        return A.Compose(transforms)


def create_resnet_datasets(splits: dict, config: Config) -> Tuple[Dataset, Dataset, Dataset]:
    """Cria datasets específicos do ResNet."""
    train_transforms = ResNetAugmentationFactory.get_training_transforms(config)
    val_transforms = ResNetAugmentationFactory.get_validation_transforms(config)
    test_transforms = ResNetAugmentationFactory.get_test_transforms(config)
    
    train_paths, train_labels = splits['train']
    val_paths, val_labels = splits['val']
    test_paths, test_labels = splits['test']
    
    print(f"Criando datasets ResNet...")
    print(f"Treino: {len(train_paths)} imagens")
    print(f"Validação: {len(val_paths)} imagens") 
    print(f"Teste: {len(test_paths)} imagens")
    
    train_dataset = ResNetDataset(
        image_paths=train_paths,
        labels=train_labels,
        transform=train_transforms,
        config=config,
        cache_processed=False
    )
    
    val_dataset = ResNetDataset(
        image_paths=val_paths,
        labels=val_labels,
        transform=val_transforms,
        config=config,
        cache_processed=True
    )
    
    test_dataset = ResNetDataset(
        image_paths=test_paths,
        labels=test_labels,
        transform=test_transforms,
        config=config,
        cache_processed=True
    )
    
    return train_dataset, val_dataset, test_dataset


def create_resnet_dataloaders(train_dataset: Dataset, 
                             val_dataset: Dataset, 
                             test_dataset: Dataset,
                             config: Config) -> Tuple[DataLoader, DataLoader, DataLoader]:
    """Cria DataLoaders para o ResNet."""
    train_loader = DataLoader(
        train_dataset,
        batch_size=config.BATCH_SIZE,
        shuffle=True,
        num_workers=config.NUM_WORKERS,
        pin_memory=config.PIN_MEMORY,
        drop_last=True,
        persistent_workers=config.NUM_WORKERS > 0
    )
    
    val_loader = DataLoader(
        val_dataset,
        batch_size=config.BATCH_SIZE,
        shuffle=False,
        num_workers=config.NUM_WORKERS,
        pin_memory=config.PIN_MEMORY,
        drop_last=False,
        persistent_workers=config.NUM_WORKERS > 0
    )
    
    test_loader = DataLoader(
        test_dataset,
        batch_size=config.BATCH_SIZE,
        shuffle=False,
        num_workers=config.NUM_WORKERS,
        pin_memory=config.PIN_MEMORY,
        drop_last=False,
        persistent_workers=config.NUM_WORKERS > 0
    )
    
    return train_loader, val_loader, test_loader


# Aliases para compatibilidade
def create_datasets(splits: dict, config: Config) -> Tuple[Dataset, Dataset, Dataset]:
    """Wrapper para manter compatibilidade."""
    return create_resnet_datasets(splits, config)

def create_dataloaders(train_dataset: Dataset, 
                      val_dataset: Dataset, 
                      test_dataset: Dataset,
                      config: Config) -> Tuple[DataLoader, DataLoader, DataLoader]:
    """Wrapper para manter compatibilidade."""
    return create_resnet_dataloaders(train_dataset, val_dataset, test_dataset, config)