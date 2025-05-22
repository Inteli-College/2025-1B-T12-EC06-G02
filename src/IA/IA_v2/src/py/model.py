import torch.nn as nn
import torchvision.models as models

def create_model(num_classes, pretrained=True):
    model = models.resnet50(pretrained=pretrained)
    model.fc = nn.Linear(model.fc.in_features, num_classes)
    return model
