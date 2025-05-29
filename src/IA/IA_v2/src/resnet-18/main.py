#!/usr/bin/env python3
"""
Main script para execução do modelo ResNet-18
Suporte para treinamento, inferência e avaliação
"""

import argparse
import sys
import os
from pathlib import Path
import torch

# Adicionar o diretório modules ao path
current_dir = Path(__file__).parent
modules_dir = current_dir.parent / "modules"
sys.path.insert(0, str(modules_dir))

from config import Config
from pipeline import ModelPipeline


def train_model(config_name: str = None):
    """Treina o modelo ResNet-18."""
    print("=== TREINAMENTO RESNET-18 ===")
    
    # Usar configuração específica se fornecida
    if config_name:
        print(f"Usando configuração: {config_name}")
        # Aqui você poderia carregar diferentes configs se tivesse
    
    config = Config()
    config.ensure_directories()
    
    # Mostrar configurações principais
    print(f"Device: {config.DEVICE}")
    print(f"Modelo: {config.MODEL_NAME}")
    print(f"Épocas: {config.EPOCHS}")
    print(f"Batch Size: {config.BATCH_SIZE}")
    print(f"Learning Rate: {config.LEARNING_RATE}")
    print("-" * 50)
    
    # Executar pipeline
    pipeline = ModelPipeline(config)
    results = pipeline.run()
    
    # Resultados finais
    print("\n" + "="*50)
    print("TREINAMENTO CONCLUÍDO")
    print("="*50)
    print(f"Melhor acurácia: {results['best_val_accuracy']:.2f}%")
    print(f"Épocas treinadas: {results['epochs_trained']}")
    print(f"Modelo salvo em: {config.MODELS_PATH}/best_model.pth")
    
    return results


def evaluate_model(model_path: str, data_path: str = None):
    """Avalia um modelo treinado."""
    print("=== AVALIAÇÃO DO MODELO ===")
    
    if not os.path.exists(model_path):
        print(f"Erro: Modelo não encontrado: {model_path}")
        return
    
    config = Config()
    if data_path:
        config.DATA_PATH = data_path
    
    print(f"Carregando modelo: {model_path}")
    print(f"Dados: {config.DATA_PATH}")
    
    # TODO: Implementar avaliação completa
    print("Aviso: Avaliação ainda não implementada completamente")
    print("Será implementada na próxima versão")


def run_inference(model_path: str, image_path: str):
    """Executa inferência em uma imagem."""
    print("=== INFERÊNCIA ===")
    
    if not os.path.exists(model_path):
        print(f"Erro: Modelo não encontrado: {model_path}")
        return
    
    if not os.path.exists(image_path):
        print(f"Erro: Imagem não encontrada: {image_path}")
        return
    
    print(f"Modelo: {model_path}")
    print(f"Imagem: {image_path}")
    
    # TODO: Implementar inferência
    print("Aviso: Inferência ainda não implementada completamente")
    print("Será implementada na próxima versão")


def list_models(models_dir: str = None):
    """Lista modelos salvos."""
    config = Config()
    models_path = Path(models_dir) if models_dir else Path(config.MODELS_PATH)
    
    print(f"=== MODELOS SALVOS ===")
    print(f"Diretório: {models_path}")
    
    if not models_path.exists():
        print("Erro: Diretório de modelos não encontrado")
        return
    
    model_files = list(models_path.glob("*.pth")) + list(models_path.glob("*.pt"))
    
    if not model_files:
        print("Erro: Nenhum modelo encontrado")
        return
    
    print(f"\nModelos encontrados ({len(model_files)}):")
    for i, model_file in enumerate(model_files, 1):
        size_mb = model_file.stat().st_size / (1024 * 1024)
        print(f"{i:2d}. {model_file.name} ({size_mb:.1f} MB)")


def main():
    """Função principal com argumentos de linha de comando."""
    parser = argparse.ArgumentParser(
        description="ResNet-18 para Classificação de Rachaduras",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
  python main.py train                           # Treinar modelo
  python main.py train --config fast            # Treinar com config específica
  python main.py eval models/best_model.pth     # Avaliar modelo
  python main.py infer models/best_model.pth image.jpg  # Inferência
  python main.py list                           # Listar modelos salvos
        """
    )
    
    parser.add_argument('command', 
                       choices=['train', 'eval', 'infer', 'list'],
                       help='Comando a executar')
    
    parser.add_argument('args', nargs='*', 
                       help='Argumentos específicos do comando')
    
    parser.add_argument('--config', '-c', 
                       help='Nome da configuração a usar')
    
    parser.add_argument('--data-path', '-d',
                       help='Caminho alternativo para os dados')
    
    parser.add_argument('--gpu', action='store_true',
                       help='Forçar uso de GPU')
    
    parser.add_argument('--cpu', action='store_true',
                       help='Forçar uso de CPU')
    
    args = parser.parse_args()
    
    # Configurar device se especificado
    if args.gpu and torch.cuda.is_available():
        os.environ['CUDA_VISIBLE_DEVICES'] = '0'
        print("Forçando uso de GPU")
    elif args.cpu:
        os.environ['CUDA_VISIBLE_DEVICES'] = ''
        print("Forçando uso de CPU")
    
    try:
        if args.command == 'train':
            train_model(args.config)
        
        elif args.command == 'eval':
            if not args.args:
                print("Erro: especifique o caminho do modelo")
                parser.print_help()
                return
            evaluate_model(args.args[0], args.data_path)
        
        elif args.command == 'infer':
            if len(args.args) < 2:
                print("Erro: especifique o modelo e a imagem")
                parser.print_help()
                return
            run_inference(args.args[0], args.args[1])
        
        elif args.command == 'list':
            models_dir = args.args[0] if args.args else None
            list_models(models_dir)
    
    except KeyboardInterrupt:
        print("\nAviso: Execução interrompida pelo usuário")
    except Exception as e:
        print(f"\nErro: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
