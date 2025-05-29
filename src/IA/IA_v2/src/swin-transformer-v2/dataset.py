import os
import cv2
import torch
import numpy as np
from torch.utils.data import Dataset, DataLoader
from typing import List, Tuple, Optional, Callable
import albumentations as A
from albumentations.pytorch import ToTensorV2

import sys
from pathlib import Path

# Adicionar o diretório pai (src) ao path
current_dir = Path(__file__).parent
src_dir = current_dir.parent
sys.path.insert(0, str(src_dir))

try:
    from modules.image_filters import ImageFilters
    from modules.square_padding import SquarePadding
    CUSTOM_FILTERS_AVAILABLE = True
except ImportError:
    CUSTOM_FILTERS_AVAILABLE = False

from config import Config
from modules.base_dataset import BaseImageDataset


class ImageClassificationDataset(BaseImageDataset):
    """Dataset específico para o Swin Transformer."""
    
    def __init__(self, 
                 image_paths: List[str],
                 labels: List[int],
                 transform: Optional[Callable] = None,
                 config: Config = None,
                 cache_processed: bool = False):
        
        super().__init__(image_paths, labels, transform, config, cache_processed)


class AugmentationFactory:
    """Factory para criar transformações específicas do Swin Transformer."""
    
    @staticmethod
    def get_training_transforms(config: Config) -> A.Compose:
        """Cria transformações robustas para treinamento."""
        transforms = [
            A.Resize(config.IMAGE_SIZE, config.IMAGE_SIZE, interpolation=cv2.INTER_AREA),
            
            # Augmentações geométricas
            A.HorizontalFlip(p=config.HORIZONTAL_FLIP_PROB),
            A.VerticalFlip(p=config.VERTICAL_FLIP_PROB),
            A.Rotate(
                limit=config.ROTATION_LIMIT, 
                p=config.ROTATION_PROB,
                border_mode=cv2.BORDER_REFLECT_101
            ),
            A.ShiftScaleRotate(
                shift_limit=0.1,
                scale_limit=0.1,
                rotate_limit=config.ROTATION_LIMIT,
                p=0.3,
                border_mode=cv2.BORDER_REFLECT_101
            ),
            
            # Augmentações de zoom
            A.RandomResizedCrop(
                size=(config.IMAGE_SIZE, config.IMAGE_SIZE),
                scale=(0.8, 1.0),
                ratio=(0.9, 1.1),
                p=config.ZOOM_PROB
            ),
            
            # Augmentações de cor
            A.RandomBrightnessContrast(
                brightness_limit=0.2,
                contrast_limit=0.2,
                p=config.BRIGHTNESS_CONTRAST_PROB
            ),
            A.HueSaturationValue(
                hue_shift_limit=10,
                sat_shift_limit=15,
                val_shift_limit=10,
                p=0.3
            ),
            A.CLAHE(
                clip_limit=config.CLAHE_CLIP_LIMIT,
                tile_grid_size=config.CLAHE_TILE_GRID_SIZE,
                p=0.3
            ),
            
            # Ruído e blur
            A.OneOf([
                A.GaussianBlur(blur_limit=(3, 5), p=1.0),
                A.MotionBlur(blur_limit=3, p=1.0),
                A.MedianBlur(blur_limit=3, p=1.0),
            ], p=config.BLUR_PROB),
            
            A.OneOf([
                A.GaussNoise(var_limit=(10, 50), p=1.0),
                A.ISONoise(color_shift=(0.01, 0.05), intensity=(0.1, 0.5), p=1.0),
            ], p=config.NOISE_PROB),
            
            # Dropout
            A.CoarseDropout(
                max_holes=8,
                max_height=16,
                max_width=16,
                min_holes=1,
                min_height=8,
                min_width=8,
                fill_value=0,
                p=0.2
            ),
            
            # Normalização
            A.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225],
                max_pixel_value=255.0
            ),
            ToTensorV2()
        ]
        
        return A.Compose(transforms)
    
    @staticmethod
    def get_validation_transforms(config: Config) -> A.Compose:
        """Cria transformações para validação (sem augmentation)."""
        transforms = [
            A.Resize(config.IMAGE_SIZE, config.IMAGE_SIZE, interpolation=cv2.INTER_AREA),
            A.CLAHE(
                clip_limit=config.CLAHE_CLIP_LIMIT * 0.8,
                tile_grid_size=config.CLAHE_TILE_GRID_SIZE,
                p=1.0
            ),
            A.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225],
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
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225],
                max_pixel_value=255.0
            ),
            ToTensorV2()
        ]
        
        return A.Compose(transforms)


def create_datasets(splits: dict, config: Config) -> Tuple[Dataset, Dataset, Dataset]:
    """Cria datasets de treino, validação e teste."""
    train_transforms = AugmentationFactory.get_training_transforms(config)
    val_transforms = AugmentationFactory.get_validation_transforms(config)
    test_transforms = AugmentationFactory.get_test_transforms(config)
    
    train_paths, train_labels = splits['train']
    val_paths, val_labels = splits['val']
    test_paths, test_labels = splits['test']
    
    train_dataset = ImageClassificationDataset(
        image_paths=train_paths,
        labels=train_labels,
        transform=train_transforms,
        config=config,
        cache_processed=False
    )
    
    val_dataset = ImageClassificationDataset(
        image_paths=val_paths,
        labels=val_labels,
        transform=val_transforms,
        config=config,
        cache_processed=True
    )
    
    test_dataset = ImageClassificationDataset(
        image_paths=test_paths,
        labels=test_labels,
        transform=test_transforms,
        config=config,
        cache_processed=True
    )
    
    return train_dataset, val_dataset, test_dataset


def create_dataloaders(train_dataset: Dataset, 
                      val_dataset: Dataset, 
                      test_dataset: Dataset,
                      config: Config) -> Tuple[DataLoader, DataLoader, DataLoader]:
    """Cria DataLoaders otimizados para os datasets."""
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



