from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.base import BaseEstimator, TransformerMixin
import numpy as np
import cv2

# Importar nossos filtros mínimos
from image_filters_minimal import (
    ClaheFilter,
    SharpenFilter,
    MedianBlurFilter,
    CompositeFilter
)


class SimpleFlattener(BaseEstimator, TransformerMixin):
    """Simples: transforma imagem em vetor"""
    
    def __init__(self, target_size=(32, 32)):
        self.target_size = target_size
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        flattened = []
        for img in X:
            # Redimensionar se necessário
            if img.shape[:2] != self.target_size:
                img = cv2.resize(img, self.target_size)
            flattened.append(img.flatten())
        return np.array(flattened)


def create_simple_pipeline():
    """Pipeline super simples que sempre funciona"""
    return Pipeline([
        ('clahe', ClaheFilter(clip_limit=2.5)),
        ('flatten', SimpleFlattener(target_size=(32, 32))),
        ('scaler', StandardScaler()),
        ('classifier', SVC())
    ])


def create_enhanced_pipeline():
    """Pipeline com mais filtros"""
    return Pipeline([
        ('denoise', MedianBlurFilter(kernel_size=3)),
        ('enhance', ClaheFilter(clip_limit=3.0)),
        ('sharpen', SharpenFilter(strength=0.8)),
        ('flatten', SimpleFlattener(target_size=(32, 32))),
        ('scaler', StandardScaler()),
        ('classifier', RandomForestClassifier(n_estimators=50))
    ])


# Parâmetros simples
SIMPLE_PARAMS = {
    'clahe__clip_limit': [2.0, 3.0],
    'classifier__C': [1, 10]
}

ENHANCED_PARAMS = {
    'denoise__kernel_size': [3, 5],
    'enhance__clip_limit': [2.5, 3.0],
    'classifier__n_estimators': [50, 100]
}