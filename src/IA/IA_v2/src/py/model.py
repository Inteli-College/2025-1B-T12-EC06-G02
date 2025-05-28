import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision.models as models
from typing import Optional


class CustomCNN(nn.Module):
    """CNN personalizada otimizada para classificação de imagens médicas/industriais."""
    
    def __init__(self, num_classes: int, dropout_rate: float = 0.5):
        super(CustomCNN, self).__init__()
        self.num_classes = num_classes
        
        # Bloco 1: Features iniciais
        self.conv1 = nn.Conv2d(3, 64, kernel_size=7, stride=2, padding=3, bias=False)
        self.bn1 = nn.BatchNorm2d(64)
        self.maxpool1 = nn.MaxPool2d(kernel_size=3, stride=2, padding=1)
        
        # Bloco 2: Features intermediárias
        self.conv2_1 = nn.Conv2d(64, 128, kernel_size=3, padding=1, bias=False)
        self.bn2_1 = nn.BatchNorm2d(128)
        self.conv2_2 = nn.Conv2d(128, 128, kernel_size=3, padding=1, bias=False)
        self.bn2_2 = nn.BatchNorm2d(128)
        self.maxpool2 = nn.MaxPool2d(kernel_size=2, stride=2)
        
        # Bloco 3: Features avançadas
        self.conv3_1 = nn.Conv2d(128, 256, kernel_size=3, padding=1, bias=False)
        self.bn3_1 = nn.BatchNorm2d(256)
        self.conv3_2 = nn.Conv2d(256, 256, kernel_size=3, padding=1, bias=False)
        self.bn3_2 = nn.BatchNorm2d(256)
        self.conv3_3 = nn.Conv2d(256, 256, kernel_size=3, padding=1, bias=False)
        self.bn3_3 = nn.BatchNorm2d(256)
        self.maxpool3 = nn.MaxPool2d(kernel_size=2, stride=2)
        
        # Bloco 4: Features de alto nível
        self.conv4_1 = nn.Conv2d(256, 512, kernel_size=3, padding=1, bias=False)
        self.bn4_1 = nn.BatchNorm2d(512)
        self.conv4_2 = nn.Conv2d(512, 512, kernel_size=3, padding=1, bias=False)
        self.bn4_2 = nn.BatchNorm2d(512)
        self.conv4_3 = nn.Conv2d(512, 512, kernel_size=3, padding=1, bias=False)
        self.bn4_3 = nn.BatchNorm2d(512)
        self.maxpool4 = nn.MaxPool2d(kernel_size=2, stride=2)
        
        # Global Average Pooling
        self.global_avgpool = nn.AdaptiveAvgPool2d((1, 1))
        
        # Classificador
        self.dropout = nn.Dropout(dropout_rate)
        self.fc1 = nn.Linear(512, 256)
        self.fc2 = nn.Linear(256, 128)
        self.fc3 = nn.Linear(128, num_classes)
        
        # Inicialização dos pesos
        self._initialize_weights()
    
    def _initialize_weights(self):
        """Inicializa os pesos da rede."""
        for m in self.modules():
            if isinstance(m, nn.Conv2d):
                nn.init.kaiming_normal_(m.weight, mode='fan_out', nonlinearity='relu')
            elif isinstance(m, nn.BatchNorm2d):
                nn.init.constant_(m.weight, 1)
                nn.init.constant_(m.bias, 0)
            elif isinstance(m, nn.Linear):
                nn.init.normal_(m.weight, 0, 0.01)
                nn.init.constant_(m.bias, 0)
    
    def forward(self, x):
        # Bloco 1
        x = F.relu(self.bn1(self.conv1(x)))
        x = self.maxpool1(x)
        
        # Bloco 2
        x = F.relu(self.bn2_1(self.conv2_1(x)))
        x = F.relu(self.bn2_2(self.conv2_2(x)))
        x = self.maxpool2(x)
        
        # Bloco 3
        x = F.relu(self.bn3_1(self.conv3_1(x)))
        x = F.relu(self.bn3_2(self.conv3_2(x)))
        x = F.relu(self.bn3_3(self.conv3_3(x)))
        x = self.maxpool3(x)
        
        # Bloco 4
        x = F.relu(self.bn4_1(self.conv4_1(x)))
        x = F.relu(self.bn4_2(self.conv4_2(x)))
        x = F.relu(self.bn4_3(self.conv4_3(x)))
        x = self.maxpool4(x)
        
        # Global pooling e classificação
        x = self.global_avgpool(x)
        x = torch.flatten(x, 1)
        
        x = self.dropout(x)
        x = F.relu(self.fc1(x))
        x = self.dropout(x)
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        
        return x


class ResNetPreTrained(nn.Module):
    """ResNet pré-treinado com fine-tuning."""
    
    def __init__(self, num_classes: int, model_name: str = 'resnet50', pretrained: bool = True, freeze_backbone: bool = False):
        super(ResNetPreTrained, self).__init__()
        self.num_classes = num_classes
        
        # Carregar modelo pré-treinado
        if model_name == 'resnet18':
            self.backbone = models.resnet18(weights='IMAGENET1K_V1' if pretrained else None)
            feature_dim = 512
        elif model_name == 'resnet34':
            self.backbone = models.resnet34(weights='IMAGENET1K_V1' if pretrained else None)
            feature_dim = 512
        elif model_name == 'resnet50':
            self.backbone = models.resnet50(weights='IMAGENET1K_V1' if pretrained else None)
            feature_dim = 2048
        elif model_name == 'resnet101':
            self.backbone = models.resnet101(weights='IMAGENET1K_V1' if pretrained else None)
            feature_dim = 2048
        else:
            raise ValueError(f"Modelo {model_name} não suportado")
        
        # Congelar backbone se necessário
        if freeze_backbone:
            for param in self.backbone.parameters():
                param.requires_grad = False
        
        # Substituir a última camada
        self.backbone.fc = nn.Sequential(
            nn.Dropout(0.5),
            nn.Linear(feature_dim, 512),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(512, 256),
            nn.ReLU(),
            nn.Linear(256, num_classes)
        )
    
    def forward(self, x):
        return self.backbone(x)


def create_model(num_classes: int, model_type: str = 'custom_cnn', **kwargs) -> nn.Module:
    """
    Factory function para criar diferentes tipos de modelos.
    
    Args:
        num_classes: Número de classes para classificação
        model_type: Tipo do modelo ('custom_cnn', 'resnet')
        **kwargs: Argumentos específicos do modelo
    
    Returns:
        Modelo PyTorch configurado
    """
    
    if model_type == 'custom_cnn':
        dropout_rate = kwargs.get('dropout_rate', 0.5)
        return CustomCNN(num_classes=num_classes, dropout_rate=dropout_rate)
    
    elif model_type == 'resnet':
        model_name = kwargs.get('model_name', 'resnet50')
        pretrained = kwargs.get('pretrained', True)
        freeze_backbone = kwargs.get('freeze_backbone', False)
        return ResNetPreTrained(
            num_classes=num_classes,
            model_name=model_name,
            pretrained=pretrained,
            freeze_backbone=freeze_backbone
        )
    
    else:
        raise ValueError(f"Tipo de modelo '{model_type}' não suportado. "
                        f"Opções: 'custom_cnn', 'resnet'")