import torch
import torch.nn as nn
import torch.optim as optim
from torch.cuda.amp import GradScaler, autocast
from torch.optim.lr_scheduler import CosineAnnealingLR, OneCycleLR
import numpy as np
import time
from tqdm import tqdm
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, confusion_matrix, roc_auc_score
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Tuple, Optional
import mlflow
import mlflow.pytorch
from pathlib import Path


class AdvancedTrainer:
    """
    Trainer avançado para modelos de classificação de fissuras.
    Inclui mixed precision, gradient clipping, label smoothing e MLflow integration.
    """
    
    def __init__(self, model, config, device):
        self.model = model.to(device)
        self.config = config
        self.device = device
        
        # Mixed precision
        self.scaler = GradScaler() if config.MIXED_PRECISION else None
        
        # Optimizer
        self.optimizer = self._create_optimizer()
        
        # Loss function com label smoothing
        self.criterion = nn.CrossEntropyLoss(
            label_smoothing=config.LABEL_SMOOTHING if hasattr(config, 'LABEL_SMOOTHING') else 0.0
        )
        
        # Scheduler
        self.scheduler = None
        
        # Metrics tracking
        self.history = {
            'train_loss': [], 'val_loss': [],
            'train_accuracy': [], 'val_accuracy': [],
            'train_f1': [], 'val_f1': [],
            'learning_rate': []
        }
        
        # Best model tracking
        self.best_val_accuracy = 0.0
        self.best_model_path = None
        self.patience_counter = 0
        
        # MLflow
        self.experiment_name = config.EXPERIMENT_NAME
        
    def _create_optimizer(self):
        """Cria optimizer."""
        if self.config.OPTIMIZER.lower() == "adamw":
            return optim.AdamW(
                self.model.parameters(),
                lr=self.config.LEARNING_RATE,
                weight_decay=self.config.WEIGHT_DECAY,
                betas=getattr(self.config, 'BETAS', (0.9, 0.999)),
                eps=getattr(self.config, 'EPS', 1e-8)
            )
        elif self.config.OPTIMIZER.lower() == "adam":
            return optim.Adam(
                self.model.parameters(),
                lr=self.config.LEARNING_RATE,
                weight_decay=self.config.WEIGHT_DECAY
            )
        else:
            raise ValueError(f"Optimizer {self.config.OPTIMIZER} não suportado")
    
    def _create_scheduler(self, total_steps):
        """Cria scheduler com warmup."""
        scheduler_type = getattr(self.config, 'SCHEDULER', 'cosine')
        
        if scheduler_type == "cosine_warmup":
            warmup_epochs = getattr(self.config, 'WARMUP_EPOCHS', 5)
            # Garantir que warmup não seja maior que total de épocas
            warmup_epochs = min(warmup_epochs, self.config.EPOCHS - 1)
            warmup_steps = warmup_epochs * (total_steps // self.config.EPOCHS)
            pct_start = max(0.1, min(0.3, warmup_steps / total_steps))  # Entre 0.1 e 0.3
            
            return optim.lr_scheduler.OneCycleLR(
                self.optimizer,
                max_lr=self.config.LEARNING_RATE,
                total_steps=total_steps,
                pct_start=pct_start,
                anneal_strategy='cos',
                div_factor=25.0,
                final_div_factor=10000.0
            )
        elif scheduler_type == "cosine":
            return CosineAnnealingLR(
                self.optimizer,
                T_max=self.config.EPOCHS,
                eta_min=getattr(self.config, 'MIN_LR', 1e-7)
            )
        else:
            return None
    
    def train_epoch(self, train_loader) -> Dict[str, float]:
        """Treina uma época."""
        self.model.train()
        
        total_loss = 0.0
        all_preds = []
        all_labels = []
        
        pbar = tqdm(train_loader, desc="Training")
        
        for batch_idx, (data, target) in enumerate(pbar):
            data, target = data.to(self.device), target.to(self.device)
            
            self.optimizer.zero_grad()
            
            # Forward pass com mixed precision
            if self.scaler:
                with autocast():
                    output = self.model(data)
                    loss = self.criterion(output, target)
                
                # Backward pass com scaling
                self.scaler.scale(loss).backward()
                
                # Gradient clipping
                if hasattr(self.config, 'GRADIENT_CLIPPING'):
                    self.scaler.unscale_(self.optimizer)
                    torch.nn.utils.clip_grad_norm_(
                        self.model.parameters(), 
                        self.config.GRADIENT_CLIPPING
                    )
                
                self.scaler.step(self.optimizer)
                self.scaler.update()
            else:
                output = self.model(data)
                loss = self.criterion(output, target)
                loss.backward()
                
                # Gradient clipping
                if hasattr(self.config, 'GRADIENT_CLIPPING'):
                    torch.nn.utils.clip_grad_norm_(
                        self.model.parameters(), 
                        self.config.GRADIENT_CLIPPING
                    )
                
                self.optimizer.step()
            
            # Update scheduler se for step-wise
            if self.scheduler and hasattr(self.scheduler, 'step') and \
               isinstance(self.scheduler, optim.lr_scheduler.OneCycleLR):
                self.scheduler.step()
            
            # Collect predictions
            total_loss += loss.item()
            preds = torch.argmax(output, dim=1)
            all_preds.extend(preds.cpu().numpy())
            all_labels.extend(target.cpu().numpy())
            
            # Update progress bar
            pbar.set_postfix({
                'Loss': f'{loss.item():.4f}',
                'LR': f'{self.optimizer.param_groups[0]["lr"]:.2e}'
            })
        
        # Calcular métricas
        avg_loss = total_loss / len(train_loader)
        accuracy = accuracy_score(all_labels, all_preds) * 100
        precision, recall, f1, _ = precision_recall_fscore_support(
            all_labels, all_preds, average='weighted', zero_division=0
        )
        
        return {
            'loss': avg_loss,
            'accuracy': accuracy,
            'precision': precision * 100,
            'recall': recall * 100,
            'f1': f1 * 100
        }
    
    def validate_epoch(self, val_loader) -> Dict[str, float]:
        """Valida o modelo."""
        self.model.eval()
        
        total_loss = 0.0
        all_preds = []
        all_labels = []
        all_probs = []
        
        with torch.no_grad():
            for data, target in tqdm(val_loader, desc="Validating"):
                data, target = data.to(self.device), target.to(self.device)
                
                # Test Time Augmentation
                if getattr(self.config, 'USE_TTA', False):
                    tta_outputs = []
                    tta_steps = getattr(self.config, 'TTA_STEPS', 5)
                    
                    for _ in range(tta_steps):
                        if self.scaler:
                            with autocast():
                                output = self.model(data)
                        else:
                            output = self.model(data)
                        tta_outputs.append(torch.softmax(output, dim=1))
                    
                    output = torch.mean(torch.stack(tta_outputs), dim=0)
                    loss = self.criterion(torch.log(output + 1e-8), target)
                else:
                    if self.scaler:
                        with autocast():
                            output = self.model(data)
                    else:
                        output = self.model(data)
                    loss = self.criterion(output, target)
                
                total_loss += loss.item()
                
                # Predictions and probabilities
                probs = torch.softmax(output, dim=1)
                preds = torch.argmax(output, dim=1)
                
                all_preds.extend(preds.cpu().numpy())
                all_labels.extend(target.cpu().numpy())
                all_probs.extend(probs.cpu().numpy())
        
        # Calcular métricas
        avg_loss = total_loss / len(val_loader)
        accuracy = accuracy_score(all_labels, all_preds) * 100
        precision, recall, f1, _ = precision_recall_fscore_support(
            all_labels, all_preds, average='weighted', zero_division=0
        )
        
        # AUC para classificação binária
        auc = 0.0
        if len(np.unique(all_labels)) == 2:
            try:
                all_probs_np = np.array(all_probs)
                auc = roc_auc_score(all_labels, all_probs_np[:, 1]) * 100
            except:
                auc = 0.0
        
        return {
            'loss': avg_loss,
            'accuracy': accuracy,
            'precision': precision * 100,
            'recall': recall * 100,
            'f1': f1 * 100,
            'auc': auc,
            'confusion_matrix': confusion_matrix(all_labels, all_preds),
            'all_preds': all_preds,
            'all_labels': all_labels
        }
    
    def train(self, train_loader, val_loader, save_dir: str = "models"):
        """Pipeline de treinamento."""
        
        # Criar diretório de salvamento
        save_path = Path(save_dir)
        save_path.mkdir(exist_ok=True)
        
        # Calcular total de steps para scheduler
        total_steps = len(train_loader) * self.config.EPOCHS
        self.scheduler = self._create_scheduler(total_steps)
        
        # MLflow
        with mlflow.start_run(experiment_id=self._get_experiment_id()):
            
            # Log config
            self._log_config()
            
            print(f"Iniciando treinamento - Device: {self.device}")
            print(f"Modelo: {self.config.MODEL_NAME}")
            print(f"Épocas: {self.config.EPOCHS}, Batch Size: {self.config.BATCH_SIZE}")
            print(f"Learning Rate: {self.config.LEARNING_RATE}")
            print("-" * 60)
            
            for epoch in range(1, self.config.EPOCHS + 1):
                start_time = time.time()
                
                # Treinar
                train_metrics = self.train_epoch(train_loader)
                
                # Validar
                val_metrics = self.validate_epoch(val_loader)
                
                # Update scheduler se for epoch-wise
                if self.scheduler and not isinstance(self.scheduler, optim.lr_scheduler.OneCycleLR):
                    self.scheduler.step()
                
                # Tempo da época
                epoch_time = time.time() - start_time
                
                # Salvar métricas
                self._update_history(train_metrics, val_metrics, epoch)
                
                # Log metrics
                self._log_metrics(train_metrics, val_metrics, epoch)
                
                # Print progress
                self._print_epoch_results(epoch, train_metrics, val_metrics, epoch_time)
                
                # Save best model
                if val_metrics['accuracy'] > self.best_val_accuracy:
                    self.best_val_accuracy = val_metrics['accuracy']
                    self.best_model_path = save_path / f"best_model_epoch_{epoch}.pt"
                    self._save_model(self.best_model_path, epoch, val_metrics)
                    self.patience_counter = 0
                    print(f"Novo melhor modelo salvo! Acurácia: {val_metrics['accuracy']:.2f}%")
                else:
                    self.patience_counter += 1
                
                # Early stopping
                if self.patience_counter >= self.config.PATIENCE:
                    print(f"Early stopping após {epoch} épocas")
                    break
                
                print("-" * 60)
            
            # Final results
            print(f"Melhor acurácia de validação: {self.best_val_accuracy:.2f}%")
            
            # Plot training curves
            self._plot_training_curves(save_path)
            
            # Log final model
            if self.best_model_path:
                mlflow.pytorch.log_model(
                    pytorch_model=self.model,
                    artifact_path="model",
                    registered_model_name=f"{self.config.MODEL_NAME}_crack_classifier"
                )
        
        return {
            'best_val_accuracy': self.best_val_accuracy,
            'history': self.history,
            'best_model_path': str(self.best_model_path),
            'epochs_trained': epoch
        }
    
    def _update_history(self, train_metrics, val_metrics, epoch):
        """Atualiza histórico de treinamento."""
        self.history['train_loss'].append(train_metrics['loss'])
        self.history['val_loss'].append(val_metrics['loss'])
        self.history['train_accuracy'].append(train_metrics['accuracy'])
        self.history['val_accuracy'].append(val_metrics['accuracy'])
        self.history['train_f1'].append(train_metrics['f1'])
        self.history['val_f1'].append(val_metrics['f1'])
        self.history['learning_rate'].append(self.optimizer.param_groups[0]['lr'])
    
    def _print_epoch_results(self, epoch, train_metrics, val_metrics, epoch_time):
        """Imprime resultados da época."""
        print(f"Época {epoch:3d}/{self.config.EPOCHS}")
        print(f"  Treino   - Loss: {train_metrics['loss']:.4f} | Acc: {train_metrics['accuracy']:6.2f}% | F1: {train_metrics['f1']:6.2f}%")
        print(f"  Validação- Loss: {val_metrics['loss']:.4f} | Acc: {val_metrics['accuracy']:6.2f}% | F1: {val_metrics['f1']:6.2f}%")
        if 'auc' in val_metrics:
            print(f"  AUC: {val_metrics['auc']:6.2f}%")
        print(f"  Tempo: {epoch_time:.1f}s | LR: {self.optimizer.param_groups[0]['lr']:.2e}")
    
    def _save_model(self, path, epoch, metrics):
        """Salva modelo com metadados."""
        torch.save({
            'epoch': epoch,
            'model_state_dict': self.model.state_dict(),
            'optimizer_state_dict': self.optimizer.state_dict(),
            'scheduler_state_dict': self.scheduler.state_dict() if self.scheduler else None,
            'metrics': metrics,
            'config': self.config,
            'best_val_accuracy': self.best_val_accuracy
        }, path)
    
    def _plot_training_curves(self, save_dir):
        """Plota curvas de treinamento."""
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        
        # Loss
        axes[0, 0].plot(self.history['train_loss'], label='Treino', color='blue')
        axes[0, 0].plot(self.history['val_loss'], label='Validação', color='red')
        axes[0, 0].set_title('Loss')
        axes[0, 0].set_xlabel('Época')
        axes[0, 0].set_ylabel('Loss')
        axes[0, 0].legend()
        axes[0, 0].grid(True)
        
        # Accuracy
        axes[0, 1].plot(self.history['train_accuracy'], label='Treino', color='blue')
        axes[0, 1].plot(self.history['val_accuracy'], label='Validação', color='red')
        axes[0, 1].set_title('Acurácia')
        axes[0, 1].set_xlabel('Época')
        axes[0, 1].set_ylabel('Acurácia (%)')
        axes[0, 1].legend()
        axes[0, 1].grid(True)
        
        # F1 Score
        axes[1, 0].plot(self.history['train_f1'], label='Treino', color='blue')
        axes[1, 0].plot(self.history['val_f1'], label='Validação', color='red')
        axes[1, 0].set_title('F1 Score')
        axes[1, 0].set_xlabel('Época')
        axes[1, 0].set_ylabel('F1 Score (%)')
        axes[1, 0].legend()
        axes[1, 0].grid(True)
        
        # Learning Rate
        axes[1, 1].plot(self.history['learning_rate'], color='green')
        axes[1, 1].set_title('Learning Rate')
        axes[1, 1].set_xlabel('Época')
        axes[1, 1].set_ylabel('Learning Rate')
        axes[1, 1].set_yscale('log')
        axes[1, 1].grid(True)
        
        plt.tight_layout()
        plt.savefig(save_dir / 'training_curves.png', dpi=300, bbox_inches='tight')
        plt.close()
    
    def _get_experiment_id(self):
        """Obtém ou cria experiment ID do MLflow."""
        try:
            experiment = mlflow.get_experiment_by_name(self.experiment_name)
            if experiment:
                return experiment.experiment_id
            else:
                return mlflow.create_experiment(self.experiment_name)
        except:
            return mlflow.create_experiment(self.experiment_name)
    
    def _log_config(self):
        """Log configurações no MLflow."""
        config_dict = {k: v for k, v in vars(self.config).items() 
                      if not k.startswith('_') and not callable(v)}
        mlflow.log_params(config_dict)
    
    def _log_metrics(self, train_metrics, val_metrics, epoch):
        """Log métricas no MLflow."""
        metrics_to_log = {}
        
        for key, value in train_metrics.items():
            if key != 'confusion_matrix':
                metrics_to_log[f"train_{key}"] = value
        
        for key, value in val_metrics.items():
            if key not in ['confusion_matrix', 'all_preds', 'all_labels']:
                metrics_to_log[f"val_{key}"] = value
        
        metrics_to_log['learning_rate'] = self.optimizer.param_groups[0]['lr']
        
        mlflow.log_metrics(metrics_to_log, step=epoch) 