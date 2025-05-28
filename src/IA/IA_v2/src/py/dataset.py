"""
Dataset personalizado para classificação de imagens com augmentation.
"""

import os
import cv2
import torch
import numpy as np
from torch.utils.data import Dataset, DataLoader
from typing import List, Tuple, Optional, Callable
import albumentations as A
from albumentations.pytorch import ToTensorV2

import sys
sys.path.append('vetores')
try:
    from vetores.image_filters import ImageFilters
    from vetores.square_padding import SquarePadding
    CUSTOM_FILTERS_AVAILABLE = True
except ImportError:
    CUSTOM_FILTERS_AVAILABLE = False

from config import Config


class ImageClassificationDataset(Dataset):
    """Dataset personalizado para classificação de imagens."""
    
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
        self.config = config or Config()
        self.cache_processed = cache_processed
        
        # Inicializar filtros se disponíveis
        if CUSTOM_FILTERS_AVAILABLE:
            self.image_filters = ImageFilters()
            self.square_padding = SquarePadding()
        
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
            
            # Aplicar filtros customizados se disponíveis e habilitados
            if CUSTOM_FILTERS_AVAILABLE:
                image = self._apply_custom_filters(image)
            
            if self.transform:
                transformed = self.transform(image=image)
                image = transformed['image']
            
            if self._image_cache is not None:
                self._image_cache[idx] = (image, label)
            
            return image, label
            
        except Exception as e:
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
    
    def _apply_custom_filters(self, image: np.ndarray) -> np.ndarray:
        """Aplica filtros customizados baseado na configuração."""
        try:
            # 1. CLAHE (se habilitado)
            if self.config.USE_CLAHE:
                image = self.image_filters.clahe(
                    image,
                    clip_limit=self.config.CLAHE_CLIP_LIMIT,
                    tile_grid_size=self.config.CLAHE_TILE_GRID_SIZE
                )
            
            # 2. Equalização (se habilitado)
            if self.config.USE_EQUALIZE:
                image = self.image_filters.equalize(image)
            
            # 3. Sharpening (se habilitado)
            if self.config.USE_SHARPEN:
                image = self.image_filters.sharpen(
                    image,
                    strength=self.config.SHARPEN_STRENGTH,
                    kernel_type=self.config.SHARPEN_KERNEL_TYPE
                )
            
            # 4. Square Padding (se habilitado)
            if self.config.USE_SQUARE_PADDING:
                image = self.square_padding.apply_padding(
                    image,
                    target_size=(self.config.IMAGE_SIZE, self.config.IMAGE_SIZE),
                    padding_color=self.config.SQUARE_PADDING_COLOR
                )
            
        except Exception as e:
            print(f"Erro ao aplicar filtros customizados: {e}")
            # Em caso de erro, retorna a imagem original
        
        return image

    
    def _create_fallback_image(self) -> np.ndarray:
        """Cria uma imagem de fallback quando há erro no carregamento."""
        return np.zeros((self.config.IMAGE_SIZE, self.config.IMAGE_SIZE, 3), dtype=np.uint8)
    
    def get_class_weights(self) -> torch.Tensor:
        """Calcula pesos das classes para lidar com desbalanceamento."""
        total_samples = len(self.labels)
        weights = []
        
        for class_idx in range(self.num_classes):
            class_count = self.class_counts[class_idx]
            weight = total_samples / (self.num_classes * class_count)
            weights.append(weight)
        
        return torch.tensor(weights, dtype=torch.float32)


class AugmentationFactory:
    """Factory para criar diferentes configurações de augmentation."""
    
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



