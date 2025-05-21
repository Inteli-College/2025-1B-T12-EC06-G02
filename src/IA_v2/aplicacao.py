import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, UpSampling2D

# Função para criar um modelo simples de autoencoder (ANN)
def criar_modelo_ann():
    model = Sequential([
        # Encoder
        Conv2D(32, (3, 3), activation='relu', padding='same', input_shape=(None, None, 1)),
        MaxPooling2D((2, 2), padding='same'),
        Conv2D(16, (3, 3), activation='relu', padding='same'),
        MaxPooling2D((2, 2), padding='same'),
        
        # Decoder
        Conv2D(16, (3, 3), activation='relu', padding='same'),
        UpSampling2D((2, 2)),
        Conv2D(32, (3, 3), activation='relu', padding='same'),
        UpSampling2D((2, 2)),
        Conv2D(1, (3, 3), activation='sigmoid', padding='same')
    ])
    model.compile(optimizer='adam', loss='binary_crossentropy')
    return model

# Função para aplicar o filtro Sobel
def aplicar_sobel(imagem):
    # Converter para escala de cinza se for colorida
    if len(imagem.shape) == 3:
        gray = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
    else:
        gray = imagem
        
    # Calcular gradientes Sobel nas direções x e y
    sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
    sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
    
    # Calcular magnitude do gradiente
    magnitude = np.sqrt(sobelx**2 + sobely**2)
    
    # Normalizar para o intervalo 0-255
    magnitude = cv2.normalize(magnitude, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
    
    return magnitude

# Função para aplicar o filtro Canny
def aplicar_canny(imagem, limiar1=100, limiar2=200):
    # Converter para escala de cinza se for colorida
    if len(imagem.shape) == 3:
        gray = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
    else:
        gray = imagem
    
    # Aplicar filtro Canny
    bordas = cv2.Canny(gray, limiar1, limiar2)
    return bordas

# Função para aplicar o filtro ANN
def aplicar_ann(imagem, modelo):
    # Converter para escala de cinza se for colorida
    if len(imagem.shape) == 3:
        gray = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
    else:
        gray = imagem
    
    # Redimensionar para um tamanho adequado para a rede
    altura, largura = gray.shape
    gray_resized = cv2.resize(gray, (largura, altura))
    
    # Preparar imagem para o modelo
    img_entrada = gray_resized.astype('float32') / 255.0
    img_entrada = np.expand_dims(img_entrada, axis=0)
    img_entrada = np.expand_dims(img_entrada, axis=3)
    
    # Prever com o modelo
    saida = modelo.predict(img_entrada)
    
    # Converter de volta para formato de imagem
    saida = saida[0, :, :, 0] * 255.0
    saida = saida.astype(np.uint8)
    
    return saida

# Função principal
def main():
    # Criar o modelo ANN
    modelo = criar_modelo_ann()
    
    # Configurar interface gráfica
    root = tk.Tk()
    root.title("Processamento de Imagem com Filtros")
    root.geometry("1200x800")
    
    # Função para selecionar e processar imagem
    def selecionar_imagem():
        # Abrir seletor de arquivo
        caminho_arquivo = filedialog.askopenfilename()
        if not caminho_arquivo:
            return
        
        # Ler a imagem
        imagem = cv2.imread(caminho_arquivo)
        if imagem is None:
            print("Erro ao carregar a imagem.")
            return
        
        # Processar a imagem com diferentes filtros
        img_sobel = aplicar_sobel(imagem)
        img_canny = aplicar_canny(imagem)
        img_ann = aplicar_ann(imagem, modelo)
        
        # Exibir os resultados
        plt.figure(figsize=(12, 10))
        
        plt.subplot(2, 2, 1)
        plt.title("Imagem Original")
        plt.imshow(cv2.cvtColor(imagem, cv2.COLOR_BGR2RGB))
        plt.axis('off')
        
        plt.subplot(2, 2, 2)
        plt.title("Filtro Sobel")
        plt.imshow(img_sobel, cmap='gray')
        plt.axis('off')
        
        plt.subplot(2, 2, 3)
        plt.title("Filtro Canny")
        plt.imshow(img_canny, cmap='gray')
        plt.axis('off')
        
        plt.subplot(2, 2, 4)
        plt.title("Filtro ANN")
        plt.imshow(img_ann, cmap='gray')
        plt.axis('off')
        
        plt.tight_layout()
        plt.show()
        
        # Salvar imagens processadas
        cv2.imwrite("resultado_sobel.jpg", img_sobel)
        cv2.imwrite("resultado_canny.jpg", img_canny)
        cv2.imwrite("resultado_ann.jpg", img_ann)
        
        print("Imagens processadas salvas como 'resultado_sobel.jpg', 'resultado_canny.jpg' e 'resultado_ann.jpg'")
    
    # Criar botão para selecionar imagem
    botao_selecionar = tk.Button(root, text="Selecionar Imagem", command=selecionar_imagem,
                              font=("Arial", 14), padx=20, pady=10)
    botao_selecionar.pack(pady=50)
    
    # Adicionar texto explicativo
    texto_info = tk.Label(root, text="Este programa aplica os filtros Sobel, Canny e ANN a uma imagem.",
                       font=("Arial", 12), wraplength=600)
    texto_info.pack(pady=20)
    
    # Iniciar loop da interface
    root.mainloop()

if __name__ == "__main__":
    main()