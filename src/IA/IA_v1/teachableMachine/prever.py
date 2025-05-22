import tensorflow as tf
import numpy as np
import h5py
from PIL import Image, ImageOps  # Install pillow instead of PIL
import os
from preProcessamento.preProcessamento import processa_imagem

MODEL_PATH = os.path.join(os.path.dirname(__file__), "keras_model.h5")
# Créditos Google AI Developers Forum --> Serve para tornar compatível as versões de tensorflow entre o teachable machine e a mais nova

f = h5py.File(MODEL_PATH, mode="r+")
model_config_string = f.attrs.get("model_config")
if model_config_string.find('"groups": 1,') != -1:
    model_config_string = model_config_string.replace('"groups": 1,', '')
    f.attrs.modify('model_config', model_config_string)
    f.flush()
    model_config_string = f.attrs.get("model_config")
    assert model_config_string.find('"groups": 1,') == -1

f.close()

# Créditos Teachable Machine
def prever(caminho):
    # (1) Carrega o modelo treinado
    modelo = tf.keras.models.load_model(MODEL_PATH)

    # (2) Estabelece os rótulos
    labels = {
        0: "Retracao",
        1: "Termica"
    }

    # (3) Preprocessa a imagem
    img_preprocessada = processa_imagem(caminho)

    # (4) Pre-processamentos adicionais
    # (4.1) Converte para o formato rgb para que o modelo aceite
    img_pill_rgb = Image.fromarray(img_preprocessada).convert("RGB")

    # (4.2) Redimensiona a imagem e corta o centro
    size = (224, 224)
    image_preproc_adc = ImageOps.fit(img_pill_rgb, size, Image.Resampling.LANCZOS)

    # (4.3) Converte para array
    img_array = np.asarray(image_preproc_adc)

    # (4.4) Normaliza o array
    normalized_img_array = (img_array.astype(np.float32) / 127.5) - 1

    # (4.5) Insere no tipo de array que o modelo aceita (imagem, width, height, canais)
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    data[0] = normalized_img_array

    # (5) Predição
    prediction = modelo.predict(data)
    index = np.argmax(prediction)
    classificacao = labels[index]
    confidence_score = float(prediction[0][index])

    # Retorna o resultado como dicionário para o backend
    return {
        "type": classificacao,
        "trustability": int(confidence_score * 100),
        "severity": int(confidence_score * 10),
    }