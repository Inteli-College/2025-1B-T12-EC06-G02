"""
Arquivo principal para execução da pipeline de treinamento.
"""

import os
import sys
from pathlib import Path

# Adicionar o diretório py ao path Python
current_dir = Path(__file__).parent
py_dir = current_dir / "py"
sys.path.insert(0, str(py_dir))

from config import Config
from pipeline import ModelPipeline

def main():
    print("=" * 60)
    
    try:
        config = Config()
        
        pipeline = ModelPipeline(
            config=config,
            experiment_name="retracao_vs_termicas_v2"
        )
        
        results = pipeline.run(apply_custom_filters=True)
        
        print("\nTreinamento concluído com sucesso!")
        print(f"Melhor acurácia: {results['best_val_accuracy']:.2f}%")
        print(f"Épocas treinadas: {results['epochs_trained']}")
        
        if 'history' in results:
            history = results['history']
            final_train_acc = history['train_accuracy'][-1]
            final_val_acc = history['val_accuracy'][-1]
            gap = final_train_acc - final_val_acc
            
            print(f"Acurácia final treino: {final_train_acc:.2f}%")
            print(f"Acurácia final validação: {final_val_acc:.2f}%")
            
            if gap > 10:
                print(f"Possível overfitting (gap: {gap:.1f}%)")
            else:
                print(f"Modelo balanceado (gap: {gap:.1f}%)")
        
        print("Modelo salvo e métricas registradas no MLflow")
        return results
        
    except KeyboardInterrupt:
        print("\nTreinamento interrompido pelo usuário")
        return None
        
    except Exception as e:
        print(f"\nErro durante o treinamento: {type(e).__name__}: {str(e)}")
        print("\nVerifique:")
        print("- Se as imagens estão no diretório correto (data/raw/)")
        print("- Se as dependências estão instaladas")
        print("- Se há espaço suficiente em disco")
        raise e


if __name__ == "__main__":
    # Verificar se o arquivo config.py existe
    config_path = Path(__file__).parent / "py" / "config.py"
    if not config_path.exists():
        print(f"Arquivo config.py não encontrado em: {config_path}")
        print("Execute este script do diretório src/")
        print("Comando: python main.py")
        sys.exit(1)
    
    main()
