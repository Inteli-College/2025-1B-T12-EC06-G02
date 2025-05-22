import cv2
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from typing import List, Tuple


class BaseImageFilter(BaseEstimator, TransformerMixin):
    """Classe base para todos os filtros"""
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        if not isinstance(X, np.ndarray):
            X = np.array(X)
        return np.array([self._process_single_image(img) for img in X])
    
    def _process_single_image(self, image):
        raise NotImplementedError("Implementar em subclasses")


class ClaheFilter(BaseImageFilter):
    """CLAHE usando apenas OpenCV"""
    
    def __init__(self, clip_limit=3.0, tile_grid_size=(8, 8)):
        self.clip_limit = clip_limit
        self.tile_grid_size = tile_grid_size
    
    def _process_single_image(self, image):
        clahe = cv2.createCLAHE(clipLimit=self.clip_limit, tileGridSize=self.tile_grid_size)
        
        if len(image.shape) == 3:
            # Imagem colorida - aplicar no canal L do LAB
            lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
            lab[:, :, 0] = clahe.apply(lab[:, :, 0])
            return cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
        else:
            # Imagem em escala de cinza
            return clahe.apply(image)


class SharpenFilter(BaseImageFilter):
    """Filtro de nitidez usando apenas OpenCV"""
    
    def __init__(self, strength=1.0, sigma=1.0):
        self.strength = strength
        self.sigma = sigma
    
    def _process_single_image(self, image):
        # Unsharp mask simples
        blurred = cv2.GaussianBlur(image, (0, 0), self.sigma)
        mask = image.astype(np.float32) - blurred.astype(np.float32)
        sharpened = image.astype(np.float32) + self.strength * mask
        return np.clip(sharpened, 0, 255).astype(np.uint8)


class MedianBlurFilter(BaseImageFilter):
    """Filtro mediano"""
    
    def __init__(self, kernel_size=5):
        self.kernel_size = kernel_size if kernel_size % 2 == 1 else kernel_size + 1
    
    def _process_single_image(self, image):
        return cv2.medianBlur(image, self.kernel_size)


class GaussianBlurFilter(BaseImageFilter):
    """Filtro Gaussiano"""
    
    def __init__(self, kernel_size=5, sigma=0):
        self.kernel_size = kernel_size if kernel_size % 2 == 1 else kernel_size + 1
        self.sigma = sigma
    
    def _process_single_image(self, image):
        return cv2.GaussianBlur(image, (self.kernel_size, self.kernel_size), self.sigma)


class ContrastBrightnessFilter(BaseImageFilter):
    """Ajuste de contraste e brilho"""
    
    def __init__(self, alpha=1.0, beta=0):
        self.alpha = alpha  # contraste
        self.beta = beta    # brilho
    
    def _process_single_image(self, image):
        return cv2.convertScaleAbs(image, alpha=self.alpha, beta=self.beta)


class EdgeDetectionFilter(BaseImageFilter):
    """Detecção de bordas"""
    
    def __init__(self, method='canny', threshold1=50, threshold2=150):
        self.method = method.lower()
        self.threshold1 = threshold1
        self.threshold2 = threshold2
    
    def _process_single_image(self, image):
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image.copy()
        
        if self.method == 'canny':
            return cv2.Canny(gray, self.threshold1, self.threshold2)
        elif self.method == 'sobel':
            dx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
            dy = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
            return np.sqrt(dx**2 + dy**2).astype(np.uint8)
        else:
            return gray


class CompositeFilter(BaseImageFilter):
    """Combina múltiplos filtros"""
    
    def __init__(self, filters: List[BaseImageFilter]):
        self.filters = filters
    
    def fit(self, X, y=None):
        for filter_obj in self.filters:
            filter_obj.fit(X, y)
        return self
    
    def transform(self, X):
        X_transformed = X
        for filter_obj in self.filters:
            X_transformed = filter_obj.transform(X_transformed)
        return X_transformed


# Lista dos filtros disponíveis
__all__ = [
    'ClaheFilter',
    'SharpenFilter', 
    'MedianBlurFilter',
    'GaussianBlurFilter',
    'ContrastBrightnessFilter',
    'EdgeDetectionFilter',
    'CompositeFilter'
]