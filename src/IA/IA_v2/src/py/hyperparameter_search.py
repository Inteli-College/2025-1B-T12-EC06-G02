import itertools
import copy
from config import Config
from pipeline import ModelPipeline

# Espaço de busca dos hiperparâmetros
grid = {
    'LEARNING_RATE': [0.001, 0.0005],
    'BATCH_SIZE': [16, 32],
    'MODEL_TYPE': ['resnet', 'custom_cnn'],
    'EPOCHS': [30],  # Para teste rápido, aumente depois
}

# Gera todas as combinações possíveis
def get_param_grid(grid):
    keys = list(grid.keys())
    values = list(grid.values())
    for combo in itertools.product(*values):
        yield dict(zip(keys, combo))

def main():
    best_acc = 0.0
    best_params = None
    best_model_path = None
    results_list = []

    for params in get_param_grid(grid):
        print(f"\nTestando combinação: {params}")
        # Cria uma nova config para cada rodada
        config = copy.deepcopy(Config)
        for k, v in params.items():
            setattr(config, k, v)
        pipeline = ModelPipeline(config())
        try:
            results = pipeline.run()
            acc = results['best_val_accuracy']
            results_list.append((params, acc))
            if acc > best_acc:
                best_acc = acc
                best_params = params.copy()
                best_model_path = f"{config.MODELS_PATH}/best_model.pth"
        except Exception as e:
            print(f"Erro com params {params}: {e}")

    print("\n=== MELHOR CONFIGURAÇÃO ===")
    print(f"Acurácia: {best_acc:.2f}%")
    print(f"Parâmetros: {best_params}")
    print(f"Modelo salvo em: {best_model_path}")
    print("\nResumo de todas as execuções:")
    for params, acc in results_list:
        print(f"{params} -> {acc:.2f}%")

if __name__ == "__main__":
    main() 