from flask import Flask, request, jsonify
from modules.inference import classify_for_frontend, classify_grupos
from yolo.yolo_utils import train, detect_and_crop, send_to_classifier
import traceback
import uuid
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/ia/classify', methods=['POST'])
def classify():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "JSON inválido ou ausente"}), 400

        # Caso para rodar a detecção + recorte antes da classificação
        if data.get("run_detection"):
            pasta_imagens = data.get("pasta_imagens")
            if not pasta_imagens:
                return jsonify({"error": "'pasta_imagens' é obrigatório para detecção"}), 400
            
            peso_modelo = data.get("peso_modelo", "../../../../runs/detect/train/weights/best.pt")
            pasta_saida = data.get("pasta_saida", "crops")
            conf_thresh = float(data.get("conf_thresh", 0.3))
            iou_thresh = float(data.get("iou_thresh", 0.0))

            # Rodar detecção e recorte
            recortes = detect_and_crop(
                peso_modelo=peso_modelo,
                pasta_imagens=pasta_imagens,
                pasta_saida=pasta_saida,
                conf_thresh=conf_thresh,
                iou_thresh=iou_thresh,
                exibir=False
            )

            # Preparar lista para classificação
            imagens_para_classificacao = [
                {
                    "id": str(uuid.uuid4()),
                    "previewUrl": caminho
                }
                for caminho in recortes
            ]

            # Chamar classificador com os recortes
            results = classify_for_frontend(imagens_para_classificacao)

        # Caso grupos (como antes)
        elif "grupos" in data:
            results = classify_grupos(data)

        # Caso imagens já enviadas para classificação
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
    app.run(debug=True, port=5001) 