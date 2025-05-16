import cv2
import numpy as np

size = (640, 640) # Tamanho das imagens

def processa_imagem(caminho):
    img = cv2.imread(caminho)
    img = cv2.resize(img, size) # (1) Redimensiona a Imagem

    # (2) Converte para cinza
    img_cinza = img.max(axis=2).astype(np.uint8)

    # (3) Aplica o filtro mediano com kernel 41x41
    img_mediana = cv2.medianBlur(img_cinza.astype(np.uint8), ksize=41).astype(np.float32)

    # (4) Definir o valor máximo de pixel
    bm = 255.0

    # (5) Aplicar a equação (1): Ia(i,j) = (Ib * 0.5 * bm) / Im
    img_corrigida = (img_cinza * 0.5 * bm) / (img_mediana + 1e-5) # Adicionamos um valor pequeno (1e-5) ao denominador para evitar divisão por zero

    # Clipping e conversão para uint8
    img_corrigida = np.clip(img_corrigida, 0, 255).astype(np.uint8)

    return img_corrigida




    
    