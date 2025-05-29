import sys
import json
from teachableMachine.prever import prever


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--image_path", required=True)
    args = parser.parse_args()

    # Chama prever e garante que retorna um dicionário
    resultado = prever(args.image_path)
    if not isinstance(resultado, dict):
        # Se prever retornar None ou string, retorna um JSON padrão de erro
        resultado = {"error": "prever() não retornou um dicionário", "raw": str(resultado)}
    print(json.dumps(resultado))