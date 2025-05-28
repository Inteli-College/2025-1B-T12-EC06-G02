#!/usr/bin/env python3
"""
Quick Start - Classificador de Fissuras com Swin Transformer

Script de exemplo para treinar e testar rapidamente o modelo.
"""

import os
import sys
from pathlib import Path

# Detectar diretório do projeto automaticamente
current_dir = Path(__file__).parent.resolve()
src_dir = current_dir / "src"
py_dir = src_dir / "py"

# Verificar se os diretórios existem
if not src_dir.exists():
    print(f"ERRO: Diretório src não encontrado em {current_dir}")
    print("Certifique-se de estar executando o script do diretório correto.")
    sys.exit(1)

if not py_dir.exists():
    print(f"ERRO: Diretório py não encontrado em {src_dir}")
    print("Estrutura esperada: IA_v2/src/py/")
    sys.exit(1)

# Adicionar path do código
sys.path.insert(0, str(py_dir))

print(f"Diretório atual: {current_dir}")
print(f"Diretório src: {src_dir}")
print(f"Diretório py: {py_dir}")

def check_data_structure():
    """Verifica se a estrutura de dados está correta."""
    data_path = src_dir / "data" / "raw"
    retracao_path = data_path / "retracao"
    termicas_path = data_path / "termicas"
    
    print("\nVerificando estrutura de dados...")
    print(f"Procurando dados em: {data_path}")
    
    if not data_path.exists():
        print("Pasta data/raw não encontrada!")
        print("Criando estrutura de diretórios...")
        data_path.mkdir(parents=True, exist_ok=True)
        retracao_path.mkdir(parents=True, exist_ok=True)
        termicas_path.mkdir(parents=True, exist_ok=True)
        print("Estrutura criada! Agora coloque as imagens em:")
        print(f"   {retracao_path}  <- imagens de fissuras de retração")
        print(f"   {termicas_path}  <- imagens de fissuras térmicas")
        return False
    
    if not retracao_path.exists() or not termicas_path.exists():
        print("Pastas de classes não encontradas!")
        print("Criando pastas de classes...")
        retracao_path.mkdir(parents=True, exist_ok=True)
        termicas_path.mkdir(parents=True, exist_ok=True)
        print("Pastas criadas:")
        print(f"   {retracao_path}")
        print(f"   {termicas_path}")
        print("Coloque as imagens nas pastas correspondentes.")
        return False
    
    # Contar imagens (buscar por vários formatos)
    image_extensions = ["*.jpg", "*.jpeg", "*.png", "*.bmp", "*.tiff", "*.tif"]
    
    retracao_imgs = []
    termicas_imgs = []
    
    for ext in image_extensions:
        retracao_imgs.extend(list(retracao_path.glob(ext)))
        retracao_imgs.extend(list(retracao_path.glob(ext.upper())))
        termicas_imgs.extend(list(termicas_path.glob(ext)))
        termicas_imgs.extend(list(termicas_path.glob(ext.upper())))
    
    print(f"Estrutura de dados OK!")
    print(f"   Retração: {len(retracao_imgs)} imagens em {retracao_path}")
    print(f"   Térmicas: {len(termicas_imgs)} imagens em {termicas_path}")
    
    if len(retracao_imgs) < 10 or len(termicas_imgs) < 10:
        print("AVISO: Poucas imagens! Recomendado: 100+ por classe para bons resultados")
        if len(retracao_imgs) == 0 or len(termicas_imgs) == 0:
            print("ERRO: Pelo menos uma classe está vazia!")
            return False
    
    return True

def train_model():
    """Treina o modelo Swin Transformer."""
    print("\nIniciando treinamento do Swin Transformer...")
    
    try:
        from config import Config
        from pipeline import ModelPipeline
        
        # Inicializar configuração e criar diretórios
        config = Config()
        config.ensure_directories()
        
        # Configuração otimizada para teste rápido
        config.EPOCHS = 20  # Reduzido para teste rápido
        config.BATCH_SIZE = 8  # Menor para compatibilidade
        config.PATIENCE = 8   # Early stopping mais rápido
        
        print(f"\nConfiguração:")
        print(f"   Épocas: {config.EPOCHS}")
        print(f"   Batch Size: {config.BATCH_SIZE}")
        print(f"   Modelo: {config.MODEL_NAME}")
        print(f"   Device: {config.DEVICE}")
        print(f"   Dados: {config.DATA_PATH}")
        
        # Executar pipeline
        pipeline = ModelPipeline(config=config)
        results = pipeline.run()
        
        print(f"\nTreinamento concluído!")
        print(f"Melhor acurácia: {results['best_val_accuracy']:.2f}%")
        print(f"Modelo salvo em: {results.get('best_model_path', 'N/A')}")
        
        return results
        
    except Exception as e:
        print(f"Erro durante o treinamento: {str(e)}")
        print(f"Tipo do erro: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        print("\nPossíveis soluções:")
        print("   1. Verificar se as dependências estão instaladas: pip install -r requirements.txt")
        print("   2. Verificar se há GPU disponível")
        print("   3. Reduzir BATCH_SIZE se erro de memória")
        print("   4. Verificar se as imagens estão nos diretórios corretos")
        return None

def test_model(model_path=None):
    """Testa o modelo treinado."""
    print("\nTestando modelo...")
    
    try:
        from inference import CrackClassifier
        
        # Encontrar modelo se não especificado
        if model_path is None:
            models_dir = src_dir / "models"
            if models_dir.exists():
                model_files = list(models_dir.glob("best_model_*.pt"))
                if model_files:
                    model_path = str(model_files[0])
                else:
                    print("Nenhum modelo treinado encontrado!")
                    return
            else:
                print("Pasta de modelos não encontrada!")
                return
        
        print(f"Carregando modelo: {model_path}")
        
        # Carregar classificador
        classifier = CrackClassifier.load_model(model_path)
        
        # Testar com imagens de exemplo
        data_path = src_dir / "data" / "raw"
        test_images = []
        
        # Pegar algumas imagens de cada classe
        for class_name in ["retracao", "termicas"]:
            class_path = data_path / class_name
            if class_path.exists():
                imgs = list(class_path.glob("*.jpg"))[:2]  # 2 por classe
                test_images.extend(imgs)
        
        if not test_images:
            print("Nenhuma imagem de teste encontrada!")
            return
        
        print(f"Testando com {len(test_images)} imagens...")
        
        # Processar imagens
        correct = 0
        total = 0
        
        for img_path in test_images:
            # Determinar classe real pelo nome da pasta
            true_class = img_path.parent.name
            
            # Predizer
            result = classifier.predict(str(img_path))
            predicted_class = result['predicted_class']
            confidence = result['confidence']
            
            is_correct = predicted_class == true_class
            if is_correct:
                correct += 1
            total += 1
            
            status = "OK" if is_correct else "ERRO"
            print(f"   {status} {img_path.name}: {predicted_class} ({confidence:.1f}%)")
        
        accuracy = (correct / total) * 100 if total > 0 else 0
        print(f"\nAcurácia no teste: {accuracy:.1f}% ({correct}/{total})")
        
        # Exemplo de visualização (primeira imagem)
        if test_images:
            print(f"\nGerando visualização para: {test_images[0].name}")
            classifier.visualize_prediction(
                str(test_images[0]), 
                save_path=str(current_dir / "test_prediction.png")
            )
        
    except Exception as e:
        print(f"Erro durante o teste: {str(e)}")

def main():
    """Função principal - execução completa."""
    print("=" * 80)
    print("QUICK START - CLASSIFICADOR DE FISSURAS")
    print("Swin Transformer V2 para Classificação de Fissuras")
    print("=" * 80)
    
    # Mudar para diretório de trabalho
    os.chdir(src_dir)
    
    # 1. Verificar dados
    if not check_data_structure():
        print("\nEstrutura de dados incorreta. Corrija e execute novamente.")
        return
    
    # 2. Perguntar se deseja treinar
    print("\n" + "="*50)
    response = input("Deseja treinar um novo modelo? (s/n): ").strip().lower()
    
    model_path = None
    if response in ['s', 'sim', 'y', 'yes']:
        results = train_model()
        if results:
            model_path = results.get('best_model_path')
    
    # 3. Testar modelo
    print("\n" + "="*50)
    response = input("Deseja testar o modelo? (s/n): ").strip().lower()
    
    if response in ['s', 'sim', 'y', 'yes']:
        test_model(model_path)
    
    print("\n" + "="*80)
    print("EXECUÇÃO CONCLUÍDA!")
    print("="*80)

if __name__ == "__main__":
    main() 