import os
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
import mlflow
import mlflow.pytorch
from typing import Tuple, Dict, Any, Optional
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

from config import Config
from data_loader import DataOrganizer
from dataset import create_datasets, create_dataloaders
from model import create_model


class ModelPipeline:
    """Pipeline principal para treinamento de modelos de classificação."""
    
    def __init__(self, config: Config = None, experiment_name: str = None):
        self.config = config or Config()
        self.experiment_name = experiment_name or self.config.EXPERIMENT_NAME
        self.device = torch.device(self.config.DEVICE)
        
        self.data_organizer = DataOrganizer(self.config)
        
        # Variáveis de estado
        self.splits = None
        self.train_dataset = None
        self.val_dataset = None
        self.test_dataset = None
        self.train_loader = None
        self.val_loader = None
        self.test_loader = None
        self.model = None
        self.optimizer = None
        self.scheduler = None
        self.criterion = None
        
        os.makedirs(self.config.MODELS_PATH, exist_ok=True)
    
    def prepare_data(self) -> None:
        """Prepara todos os dados para treinamento."""
        print("Preparando dados...")
        
        # Mostrar filtros que serão aplicados
        filters_info = []
        if self.config.USE_CLAHE:
            filters_info.append(f"CLAHE (clip={self.config.CLAHE_CLIP_LIMIT})")
        if self.config.USE_EQUALIZE:
            filters_info.append("Equalização")
        if self.config.USE_SHARPEN:
            filters_info.append(f"Sharpening (força={self.config.SHARPEN_STRENGTH})")
        if self.config.USE_SQUARE_PADDING:
            filters_info.append("Square Padding")
        
        if filters_info:
            print(f"Filtros ativos: {', '.join(filters_info)}")
        else:
            print("Nenhum filtro personalizado ativo")
        
        self.splits = self.data_organizer.get_splits()
        
        self.train_dataset, self.val_dataset, self.test_dataset = create_datasets(
            splits=self.splits,
            config=self.config
        )
        
        self.train_loader, self.val_loader, self.test_loader = create_dataloaders(
            train_dataset=self.train_dataset,
            val_dataset=self.val_dataset,
            test_dataset=self.test_dataset,
            config=self.config
        )
        
        print(f"Treino: {len(self.train_dataset)} imagens, Validação: {len(self.val_dataset)} imagens")
    
    def setup_model(self) -> None:
        """Configura o modelo, otimizador, scheduler e função de perda."""
        print("Configurando modelo...")
        
        self.model = create_model(num_classes=self.config.NUM_CLASSES)
        self.model = self.model.to(self.device)
        
        # Configurar otimizador
        if self.config.OPTIMIZER.lower() == "adam":
            self.optimizer = optim.Adam(
                self.model.parameters(),
                lr=self.config.LEARNING_RATE,
                weight_decay=self.config.WEIGHT_DECAY
            )
        elif self.config.OPTIMIZER.lower() == "adamw":
            self.optimizer = optim.AdamW(
                self.model.parameters(),
                lr=self.config.LEARNING_RATE,
                weight_decay=self.config.WEIGHT_DECAY
            )
        elif self.config.OPTIMIZER.lower() == "sgd":
            self.optimizer = optim.SGD(
                self.model.parameters(),
                lr=self.config.LEARNING_RATE,
                momentum=0.9,
                weight_decay=self.config.WEIGHT_DECAY
            )
        
        # Configurar scheduler
        if self.config.SCHEDULER.lower() == "cosine":
            self.scheduler = optim.lr_scheduler.CosineAnnealingLR(
                self.optimizer,
                T_max=self.config.EPOCHS
            )
        elif self.config.SCHEDULER.lower() == "step":
            self.scheduler = optim.lr_scheduler.StepLR(
                self.optimizer,
                step_size=self.config.EPOCHS // 3,
                gamma=0.1
            )
        elif self.config.SCHEDULER.lower() == "plateau":
            self.scheduler = optim.lr_scheduler.ReduceLROnPlateau(
                self.optimizer,
                mode='max',
                factor=0.5,
                patience=self.config.PATIENCE // 2
            )
        
        # Configurar função de perda
        if hasattr(self.train_dataset, 'get_class_weights'):
            class_weights = self.train_dataset.get_class_weights().to(self.device)
            self.criterion = nn.CrossEntropyLoss(weight=class_weights)
        else:
            self.criterion = nn.CrossEntropyLoss()
    
    def train_epoch(self, epoch: int) -> Dict[str, float]:
        """Executa uma época de treinamento."""
        self.model.train()
        
        running_loss = 0.0
        correct_predictions = 0
        total_samples = 0
        
        for batch_idx, (images, labels) in enumerate(self.train_loader):
            images = images.to(self.device, non_blocking=True)
            labels = labels.to(self.device, non_blocking=True)
            
            self.optimizer.zero_grad()
            
            outputs = self.model(images)
            loss = self.criterion(outputs, labels)
            
            loss.backward()
            self.optimizer.step()
            
            running_loss += loss.item()
            _, predicted = torch.max(outputs.data, 1)
            total_samples += labels.size(0)
            correct_predictions += (predicted == labels).sum().item()
            
            if batch_idx % self.config.LOG_INTERVAL == 0:
                batch_accuracy = 100.0 * correct_predictions / total_samples
                print(f"Batch {batch_idx}/{len(self.train_loader)} | Loss: {loss.item():.4f} | Acc: {batch_accuracy:.2f}%")
        
        epoch_loss = running_loss / len(self.train_loader)
        epoch_accuracy = 100.0 * correct_predictions / total_samples
        
        return {
            'train_loss': epoch_loss,
            'train_accuracy': epoch_accuracy
        }
    
    def validate_epoch(self) -> Dict[str, float]:
        """Executa validação completa."""
        self.model.eval()
        
        running_loss = 0.0
        correct_predictions = 0
        total_samples = 0
        
        with torch.no_grad():
            for images, labels in self.val_loader:
                images = images.to(self.device, non_blocking=True)
                labels = labels.to(self.device, non_blocking=True)
                
                outputs = self.model(images)
                loss = self.criterion(outputs, labels)
                
                running_loss += loss.item()
                _, predicted = torch.max(outputs.data, 1)
                total_samples += labels.size(0)
                correct_predictions += (predicted == labels).sum().item()
        
        val_loss = running_loss / len(self.val_loader)
        val_accuracy = 100.0 * correct_predictions / total_samples
        
        return {
            'val_loss': val_loss,
            'val_accuracy': val_accuracy
        }
    
    def train_model(self) -> Dict[str, Any]:
        """Executa o treinamento completo do modelo."""
        print("Iniciando treinamento...")
        
        if self.train_loader is None:
            raise ValueError("Dados não preparados! Execute prepare_data() primeiro.")
        
        if self.model is None:
            raise ValueError("Modelo não configurado! Execute setup_model() primeiro.")
        
        mlflow.set_experiment(self.experiment_name)
        
        with mlflow.start_run():
            config_dict = {k: v for k, v in vars(self.config).items() 
                          if not callable(v) and not k.startswith('_')}
            mlflow.log_params(config_dict)
            
            best_val_accuracy = 0.0
            patience_counter = 0
            training_history = {
                'train_loss': [],
                'train_accuracy': [],
                'val_loss': [],
                'val_accuracy': [],
                'learning_rates': []
            }
            
            for epoch in range(self.config.EPOCHS):
                print(f"\nÉpoca {epoch+1}/{self.config.EPOCHS}")
                
                train_metrics = self.train_epoch(epoch)
                val_metrics = self.validate_epoch()
                
                if self.scheduler is not None:
                    if isinstance(self.scheduler, optim.lr_scheduler.ReduceLROnPlateau):
                        self.scheduler.step(val_metrics['val_accuracy'])
                    else:
                        self.scheduler.step()
                
                current_lr = self.optimizer.param_groups[0]['lr']
                
                training_history['train_loss'].append(train_metrics['train_loss'])
                training_history['train_accuracy'].append(train_metrics['train_accuracy'])
                training_history['val_loss'].append(val_metrics['val_loss'])
                training_history['val_accuracy'].append(val_metrics['val_accuracy'])
                training_history['learning_rates'].append(current_lr)
                
                mlflow.log_metrics({
                    **train_metrics,
                    **val_metrics,
                    'learning_rate': current_lr
                }, step=epoch)
                
                print(f"Treino - Loss: {train_metrics['train_loss']:.4f} | Acc: {train_metrics['train_accuracy']:.2f}%")
                print(f"Validação - Loss: {val_metrics['val_loss']:.4f} | Acc: {val_metrics['val_accuracy']:.2f}%")
                
                if val_metrics['val_accuracy'] > best_val_accuracy:
                    best_val_accuracy = val_metrics['val_accuracy']
                    patience_counter = 0
                    
                    if self.config.SAVE_CHECKPOINTS:
                        self._save_checkpoint(epoch, val_metrics['val_accuracy'], is_best=True)
                    
                    print(f"Nova melhor acurácia: {best_val_accuracy:.2f}%")
                else:
                    patience_counter += 1
                
                if self.config.SAVE_CHECKPOINTS and (epoch + 1) % self.config.CHECKPOINT_FREQ == 0:
                    self._save_checkpoint(epoch, val_metrics['val_accuracy'], is_best=False)
                
                if patience_counter >= self.config.PATIENCE:
                    print(f"Early stopping após {epoch+1} épocas. Melhor acurácia: {best_val_accuracy:.2f}%")
                    break
            
            print(f"\nTreinamento concluído. Melhor acurácia: {best_val_accuracy:.2f}%")
            
            mlflow.log_metric("best_val_accuracy", best_val_accuracy)
            mlflow.pytorch.log_model(self.model, "final_model")
            
            return {
                'best_val_accuracy': best_val_accuracy,
                'history': training_history,
                'epochs_trained': epoch + 1
            }
    
    def _save_checkpoint(self, epoch: int, accuracy: float, is_best: bool = False) -> None:
        """Salva checkpoint do modelo."""
        checkpoint = {
            'epoch': epoch + 1,
            'model_state_dict': self.model.state_dict(),
            'optimizer_state_dict': self.optimizer.state_dict(),
            'accuracy': accuracy,
            'config': vars(self.config)
        }
        
        if self.scheduler is not None:
            checkpoint['scheduler_state_dict'] = self.scheduler.state_dict()
        
        if is_best:
            checkpoint_path = os.path.join(self.config.MODELS_PATH, "best_model.pth")
        else:
            checkpoint_path = os.path.join(self.config.MODELS_PATH, f"checkpoint_epoch_{epoch+1}.pth")
        
        torch.save(checkpoint, checkpoint_path)
    
    def run(self) -> Dict[str, Any]:
        """Executa a pipeline completa de treinamento."""
        print("Executando pipeline completa...")
        
        try:
            self.prepare_data()
            
            self.setup_model()
            
            results = self.train_model()
            
            print("Pipeline executada com sucesso!")
            return results
            
        except Exception as e:
            print(f"Erro na pipeline: {e}")
            raise e


def main():
    """Função principal para executar a pipeline."""
    config = Config()
    pipeline = ModelPipeline(config)
    
    # Para testar diferentes filtros, modifique o config.py:
    # config.USE_CLAHE = False  # Desabilitar CLAHE
    # config.SHARPEN_STRENGTH = 2.0  # Aumentar força do sharpening
    # config.USE_SQUARE_PADDING = False  # Desabilitar padding
    
    results = pipeline.run()
    
    print(f"Treinamento finalizado com acurácia de {results['best_val_accuracy']:.2f}%")


if __name__ == "__main__":
    main()
