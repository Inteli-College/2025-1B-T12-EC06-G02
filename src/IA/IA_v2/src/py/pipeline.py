import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, random_split
import mlflow
import mlflow.pytorch
from config import Config
from dataset import ImageDataset, get_transforms
from model import create_model

class Pipeline:
    def __init__(self):
        self.config = Config()
        self.device = torch.device(self.config.DEVICE)
    
    def prepare_data(self):
        image_paths, labels = self.load_data_paths()
        
        # Criar datasets
        full_dataset = ImageDataset(image_paths, labels, 
                                  get_transforms(self.config.IMAGE_SIZE, True))
        
        # Dividir dados
        train_size = int(self.config.TRAIN_SPLIT * len(full_dataset))
        val_size = int(self.config.VAL_SPLIT * len(full_dataset))
        test_size = len(full_dataset) - train_size - val_size
        
        train_ds, val_ds, test_ds = random_split(full_dataset, 
                                               [train_size, val_size, test_size])
        
        # Criar DataLoaders
        train_loader = DataLoader(train_ds, batch_size=self.config.BATCH_SIZE, 
                                shuffle=True)
        val_loader = DataLoader(val_ds, batch_size=self.config.BATCH_SIZE)
        test_loader = DataLoader(test_ds, batch_size=self.config.BATCH_SIZE)
        
        return train_loader, val_loader, test_loader
    
    def train_model(self, model, train_loader, val_loader):
        optimizer = optim.Adam(model.parameters(), lr=self.config.LEARNING_RATE)
        criterion = nn.CrossEntropyLoss()
        
        for epoch in range(self.config.EPOCHS):
            # Treino
            model.train()
            train_loss = 0
            for batch_idx, (data, target) in enumerate(train_loader):
                data, target = data.to(self.device), target.to(self.device)
                
                optimizer.zero_grad()
                output = model(data)
                loss = criterion(output, target)
                loss.backward()
                optimizer.step()
                
                train_loss += loss.item()
            
            # Validação
            val_accuracy = self.validate(model, val_loader)
            
            # Log métricas
            mlflow.log_metrics({
                "train_loss": train_loss/len(train_loader),
                "val_accuracy": val_accuracy
            }, step=epoch)
    
    def validate(self, model, val_loader):
        model.eval()
        correct = 0
        total = 0
        
        with torch.no_grad():
            for data, target in val_loader:
                data, target = data.to(self.device), target.to(self.device)
                outputs = model(data)
                _, predicted = torch.max(outputs.data, 1)
                total += target.size(0)
                correct += (predicted == target).sum().item()
        
        return correct / total
    
    def run(self):
        mlflow.set_experiment("image_classification")
        
        with mlflow.start_run():
            # Log configurações
            mlflow.log_params(vars(self.config))
            
            # Preparar dados
            train_loader, val_loader, test_loader = self.prepare_data()
            
            # Criar modelo
            model = create_model(self.config.NUM_CLASSES)
            model = model.to(self.device)
            
            # Treinar
            self.train_model(model, train_loader, val_loader)
            
            # Salvar modelo
            mlflow.pytorch.log_model(model, "model")
            
            return model
    
    def load_data_paths(self):
        pass
