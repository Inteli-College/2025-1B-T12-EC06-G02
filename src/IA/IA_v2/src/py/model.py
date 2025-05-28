import torch
import torch.nn as nn
import timm
from typing import Optional
import math


class SwinTransformerClassifier(nn.Module):
    """
    Modelo baseado em Swin Transformer V2 para classificação de fissuras.
    """
    
    def __init__(self, num_classes: int = 2, model_name: str = "swinv2_cr_base_ns_224", 
                 pretrained: bool = True, dropout_rate: float = 0.2):
        super(SwinTransformerClassifier, self).__init__()
        
        self.num_classes = num_classes
        self.model_name = model_name
        
        # Carrega o modelo Swin Transformer pré-treinado
        self.backbone = timm.create_model(
            model_name,
            pretrained=pretrained,
            num_classes=0,  # Remove classifier head
            global_pool='avg'  # Average pooling
        )
        
        # Obtém o número de features do backbone
        with torch.no_grad():
            dummy_input = torch.randn(1, 3, 224, 224)
            features = self.backbone(dummy_input)
            self.feature_dim = features.shape[1]
        
        # Classifier head customizado
        self.classifier = nn.Sequential(
            nn.Dropout(dropout_rate),
            nn.Linear(self.feature_dim, 512),
            nn.BatchNorm1d(512),
            nn.GELU(),
            nn.Dropout(dropout_rate / 2),
            nn.Linear(512, 256),
            nn.BatchNorm1d(256),
            nn.GELU(),
            nn.Dropout(dropout_rate / 4),
            nn.Linear(256, num_classes)
        )
        
        # Inicialização dos pesos
        self._init_weights()
    
    def _init_weights(self):
        """Inicializa os pesos do classifier."""
        for m in self.classifier.modules():
            if isinstance(m, nn.Linear):
                nn.init.trunc_normal_(m.weight, std=0.02)
                if m.bias is not None:
                    nn.init.constant_(m.bias, 0)
            elif isinstance(m, nn.BatchNorm1d):
                nn.init.constant_(m.weight, 1)
                nn.init.constant_(m.bias, 0)
    
    def forward(self, x):
        # Extrai features usando Swin Transformer
        features = self.backbone(x)
        
        # Classifica usando nossa head customizada
        logits = self.classifier(features)
        
        return logits
    
    def get_feature_maps(self, x):
        """Retorna feature maps para visualização e análise."""
        features = self.backbone(x)
        return features


class EfficientNetClassifier(nn.Module):
    """
    Alternativa baseada em EfficientNet V2.
    Mais leve que Swin Transformer mas ainda eficaz.
    """
    
    def __init__(self, num_classes: int = 2, model_name: str = "efficientnetv2_m", 
                 pretrained: bool = True, dropout_rate: float = 0.3):
        super(EfficientNetClassifier, self).__init__()
        
        self.backbone = timm.create_model(
            model_name,
            pretrained=pretrained,
            num_classes=0,
            global_pool='avg'
        )
        
        # Obtém dimensão das features
        with torch.no_grad():
            dummy_input = torch.randn(1, 3, 224, 224)
            features = self.backbone(dummy_input)
            self.feature_dim = features.shape[1]
        
        self.classifier = nn.Sequential(
            nn.Dropout(dropout_rate),
            nn.Linear(self.feature_dim, 256),
            nn.BatchNorm1d(256),
            nn.SiLU(),
            nn.Dropout(dropout_rate / 2),
            nn.Linear(256, num_classes)
        )
        
        self._init_weights()
    
    def _init_weights(self):
        for m in self.classifier.modules():
            if isinstance(m, nn.Linear):
                nn.init.trunc_normal_(m.weight, std=0.02)
                if m.bias is not None:
                    nn.init.constant_(m.bias, 0)
    
    def forward(self, x):
        features = self.backbone(x)
        logits = self.classifier(features)
        return logits


def create_model(num_classes: int = 2, model_type: str = "swin", **kwargs):
    """
    Factory function para criar modelos.
    
    Args:
        num_classes: Número de classes (2 para retração vs térmica)
        model_type: Tipo do modelo ('swin', 'efficientnet')
        **kwargs: Argumentos adicionais do modelo
    
    Returns:
        Modelo PyTorch configurado
    """
    
    if model_type.lower() == "swin":
        model = SwinTransformerClassifier(
            num_classes=num_classes,
            model_name=kwargs.get("model_name", "swinv2_cr_base_ns_224"),
            pretrained=kwargs.get("pretrained", True),
            dropout_rate=kwargs.get("dropout_rate", 0.2)
        )
        print(f"Criado Swin Transformer com {sum(p.numel() for p in model.parameters())/1e6:.1f}M parâmetros")
        
    elif model_type.lower() == "efficientnet":
        model = EfficientNetClassifier(
            num_classes=num_classes,
            model_name=kwargs.get("model_name", "efficientnetv2_m"),
            pretrained=kwargs.get("pretrained", True),
            dropout_rate=kwargs.get("dropout_rate", 0.3)
        )
        print(f"Criado EfficientNet com {sum(p.numel() for p in model.parameters())/1e6:.1f}M parâmetros")
        
    else:
        raise ValueError(f"Modelo '{model_type}' não suportado. Use 'swin' ou 'efficientnet'")
    
    return model


def create_best_model(num_classes: int = 2):
    """Cria o modelo com melhor acurácia esperada para fissuras."""
    return create_model(
        num_classes=num_classes,
        model_type="swin",
        model_name="swinv2_cr_base_ns_224",
        pretrained=True,
        dropout_rate=0.2
    )
