from flask import Flask, request, jsonify
from modules.inference import classify_for_frontend, classify_grupos
import traceback
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

@app.route('/api/ia/classify', methods=['POST'])
def classify():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "JSON inválido ou ausente"}), 400

        # Verifica se os dados estão em formato de grupos ou formato simples
        if "grupos" in data:
            results = classify_grupos(data)
        else:
            images = data.get("images", [])
            if not images:
                return jsonify({"error": "'images' é obrigatório e não pode ser vazio"}), 400
            results = classify_for_frontend(images)

        return jsonify(results)

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000) 