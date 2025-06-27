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

import sys
from pathlib import Path

# Adicionar diretório pai para importar módulos compartilhados
current_dir = Path(__file__).parent
src_dir = current_dir.parent
sys.path.insert(0, str(src_dir))

from config import Config
from modules.data_loader import DataOrganizer
from dataset import create_datasets, create_dataloaders
from model import create_model, create_best_model
from trainer import AdvancedTrainer


class ModelPipeline:
    """Pipeline para treinamento de modelos de classificação com Swin Transformer."""
    
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
        self.trainer = None
        
        os.makedirs(self.config.MODELS_PATH, exist_ok=True)
        
        print(f"Pipeline iniciado - Modelo: {self.config.MODEL_NAME}")
        print(f"Device: {self.device}")
    
    def prepare_data(self) -> None:
        """Prepara dados para treinamento."""
        print("\nPreparando dados...")
        
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
        
        print(f"Dados preparados:")
        print(f"   Treino: {len(self.train_dataset)} imagens")
        print(f"   Validação: {len(self.val_dataset)} imagens")
        print(f"   Teste: {len(self.test_dataset)} imagens")
        print(f"   Batch size: {self.config.BATCH_SIZE}")
    
    def setup_model(self) -> None:
        """Configura o modelo e trainer."""
        print(f"\nConfigurando modelo {self.config.MODEL_NAME}...")
        
        # Criar modelo usando factory function
        self.model = create_model(**self.config.get_model_config())
        
        # Mover para device
        self.model = self.model.to(self.device)
        
        # Inicializar trainer
        self.trainer = AdvancedTrainer(
            model=self.model,
            config=self.config,
            device=self.device
        )
        
        print(f"Modelo configurado:")
        print(f"   Parâmetros: {sum(p.numel() for p in self.model.parameters())/1e6:.1f}M")
        print(f"   Optimizer: {self.config.OPTIMIZER}")
        print(f"   Scheduler: {self.config.SCHEDULER}")
        print(f"   Classes: {self.config.CLASSES}")
    
    def train_model(self) -> Dict[str, Any]:
        """Executa o treinamento."""
        print(f"\nIniciando treinamento...")
        
        results = self.trainer.train(
            train_loader=self.train_loader,
            val_loader=self.val_loader,
            save_dir=self.config.MODELS_PATH
        )
        
        return results
    
    def evaluate_model(self, model_path: str = None) -> Dict[str, Any]:
        """Avalia o modelo no conjunto de teste."""
        print(f"\nAvaliando modelo no conjunto de teste...")
                
        if model_path and os.path.exists(model_path):
            # Carregar melhor modelo
            checkpoint = torch.load(model_path, map_location=self.device, weights_only=False)
            self.model.load_state_dict(checkpoint['model_state_dict'])
            print(f"Modelo carregado de: {model_path}")
        
        # Avaliar no conjunto de teste
        test_results = self.trainer.validate_epoch(self.test_loader)
        
        print(f"Resultados no teste:")
        print(f"   Acurácia: {test_results['accuracy']:.2f}%")
        print(f"   Precisão: {test_results['precision']:.2f}%")
        print(f"   Recall: {test_results['recall']:.2f}%")
        print(f"   F1-Score: {test_results['f1']:.2f}%")
        if 'auc' in test_results:
            print(f"   AUC: {test_results['auc']:.2f}%")
        
        return test_results
    
    def run(self, apply_custom_filters: bool = True) -> Dict[str, Any]:
        """Executa pipeline completo de treinamento e avaliação."""
        print("=" * 80)
        print("PIPELINE DE CLASSIFICAÇÃO DE FISSURAS - SWIN TRANSFORMER")
        print("=" * 80)
        
        try:
            # Preparar dados
            self.prepare_data()
            
            # Configurar modelo
            self.setup_model()
            
            # Treinar modelo
            training_results = self.train_model()
            
            # Avaliar no teste se temos um modelo treinado
            test_results = None
            if training_results.get('best_model_path'):
                test_results = self.evaluate_model(training_results['best_model_path'])
                training_results['test_results'] = test_results
            
            print("\n" + "=" * 80)
            print("RESULTADOS FINAIS")
            print("=" * 80)
            print(f"Melhor acurácia validação: {training_results['best_val_accuracy']:.2f}%")
            if test_results:
                print(f"Acurácia no teste: {test_results['accuracy']:.2f}%")
                print(f"F1-Score no teste: {test_results['f1']:.2f}%")
            print(f"Modelo salvo em: {training_results.get('best_model_path', 'N/A')}")
            print(f"Épocas treinadas: {training_results.get('epochs_trained', 'N/A')}")
            print("=" * 80)
            
            return training_results
            
        except Exception as e:
            print(f"\nErro durante o pipeline: {str(e)}")
            raise e


def main():
    """Função principal para executar a pipeline."""
    config = Config()
    pipeline = ModelPipeline(config)
    
    results = pipeline.run()
    
    print(f"Treinamento finalizado com acurácia de {results['best_val_accuracy']:.2f}%")


if __name__ == "__main__":
    main()
