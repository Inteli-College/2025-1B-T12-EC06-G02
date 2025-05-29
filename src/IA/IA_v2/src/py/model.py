import torch
import torch.nn as nn

class BaseModel(nn.Module):
    
    def __init__(self, num_classes):
        super(BaseModel, self).__init__()
        self.num_classes = num_classes
        
        self.features = nn.Sequential(
            nn.Linear(224*224*3, 128),  # Input placeholder
            nn.ReLU(),
            nn.Dropout(0.5)
        )
        
        self.classifier = nn.Linear(128, num_classes)
    
    def forward(self, x):
        
        x = x.view(x.size(0), -1)  # Flatten
        x = self.features(x)
        x = self.classifier(x)
        return x

def create_model(num_classes, **kwargs):

    return BaseModel(num_classes)
