import os
import cv2
import torch
import numpy as np
from torch.utils.data import Dataset, DataLoader
from typing import List, Tuple, Optional, Callable, Any
import albumentations as A
from albumentations.pytorch import ToTensorV2

try:
    from image_filters import ImageFilters
    from square_padding import SquarePadding
    CUSTOM_FILTERS_AVAILABLE = True
except ImportError:
    CUSTOM_FILTERS_AVAILABLE = False


class BaseImageDataset(Dataset):
    """Dataset base para classificação de imagens."""
    
    def __init__(self, 
                 image_paths: List[str],
                 labels: List[int],
                 transform: Optional[Callable] = None,
                 config: Any = None,
                 cache_processed: bool = False):
        
        if len(image_paths) != len(labels):
            raise ValueError(f"Número de imagens ({len(image_paths)}) deve ser igual ao número de labels ({len(labels)})")
        
        self.image_paths = image_paths
        self.labels = labels
        self.transform = transform
        self.config = config
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
            if CUSTOM_FILTERS_AVAILABLE and self.config:
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
            if hasattr(self.config, 'USE_CLAHE') and self.config.USE_CLAHE:
                image = self.image_filters.clahe(
                    image,
                    clip_limit=getattr(self.config, 'CLAHE_CLIP_LIMIT', 3.0),
                    tile_grid_size=getattr(self.config, 'CLAHE_TILE_GRID_SIZE', (8, 8))
                )
            
            # 2. Equalização (se habilitado)
            if hasattr(self.config, 'USE_EQUALIZE') and self.config.USE_EQUALIZE:
                image = self.image_filters.equalize(image)
            
            # 3. Sharpening (se habilitado)
            if hasattr(self.config, 'USE_SHARPEN') and self.config.USE_SHARPEN:
                image = self.image_filters.sharpen(
                    image,
                    strength=getattr(self.config, 'SHARPEN_STRENGTH', 1.2),
                    kernel_type=getattr(self.config, 'SHARPEN_KERNEL_TYPE', 'laplacian')
                )
            
            # 4. Square Padding (se habilitado)
            if hasattr(self.config, 'USE_SQUARE_PADDING') and self.config.USE_SQUARE_PADDING:
                image_size = getattr(self.config, 'IMAGE_SIZE', 224)
                padding_color = getattr(self.config, 'SQUARE_PADDING_COLOR', (0, 0, 0))
                image = self.square_padding.apply_padding(
                    image,
                    target_size=(image_size, image_size),
                    padding_color=padding_color
                )
            
        except Exception as e:
            print(f"Erro ao aplicar filtros customizados: {e}")
            # Em caso de erro, retorna a imagem original
        
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


def create_basic_transforms(image_size: int = 224) -> A.Compose:
    """Cria transformações básicas que funcionam para qualquer modelo."""
    transforms = [
        A.Resize(image_size, image_size),
        A.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225],
            max_pixel_value=255.0
        ),
        ToTensorV2()
    ]
    
    return A.Compose(transforms)


def create_basic_dataloaders(train_dataset: Dataset, 
                            val_dataset: Dataset, 
                            test_dataset: Dataset,
                            batch_size: int = 16,
                            num_workers: int = 4) -> Tuple[DataLoader, DataLoader, DataLoader]:
    """Cria DataLoaders básicos."""
    train_loader = DataLoader(
        train_dataset,
        batch_size=batch_size,
        shuffle=True,
        num_workers=num_workers,
        pin_memory=True,
        drop_last=True
    )
    
    val_loader = DataLoader(
        val_dataset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=num_workers,
        pin_memory=True,
        drop_last=False
    )
    
    test_loader = DataLoader(
        test_dataset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=num_workers,
        pin_memory=True,
        drop_last=False
    )
    
    return train_loader, val_loader, test_loader 