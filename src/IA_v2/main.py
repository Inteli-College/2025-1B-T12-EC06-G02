import numpy as np
import cv2
import matplotlib.pyplot as plt
from PIL import Image

def preprocess_square_with_padding(image_path, target_size=(300, 300), padding_color=(0, 0, 0)):
    # Carrega a imagem usando OpenCV (que carrega como BGR)
    img = cv2.imread(image_path)
    
    # Verifica se a imagem foi carregada corretamente
    if img is None:
        raise ValueError(f"Não foi possível carregar a imagem: {image_path}")
    
    # Converte BGR para RGB
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # Obtém dimensões da imagem
    height, width = img.shape[:2]
    
    # Determina o lado maior
    max_side = max(height, width)
    
    # Cria uma imagem quadrada com o tamanho do lado maior
    square_img = np.ones((max_side, max_side, 3), dtype=np.uint8) * np.array(padding_color, dtype=np.uint8)
    
    # Calcula os offsets para centralizar a imagem original
    y_offset = (max_side - height) // 2
    x_offset = (max_side - width) // 2
    
    # Insere a imagem original no centro da imagem quadrada
    square_img[y_offset:y_offset+height, x_offset:x_offset+width] = img
    
    # Redimensiona a imagem quadrada para o tamanho alvo
    resized_img = cv2.resize(square_img, target_size, interpolation=cv2.INTER_AREA)
    
    return resized_img

def test_preprocessing(image_path, padding_color=(0, 0, 0), verbose=True):
    """
    Testa o pré-processamento em uma imagem e mostra os resultados
    
    Args:
        image_path: Caminho para a imagem de entrada
        padding_color: Cor do padding em RGB (default: preto)
        verbose: Se True, exibe as imagens com matplotlib
        
    Returns:
        A imagem processada pronta para o EfficientNetB3
    """
    try:
        # Carrega a imagem original
        original_img = cv2.imread(image_path)
        if original_img is None:
            print(f"ERRO: Não foi possível carregar a imagem em {image_path}")
            return None
            
        original_img = cv2.cvtColor(original_img, cv2.COLOR_BGR2RGB)
        
        # Obtém dimensões da imagem
        height, width = original_img.shape[:2]
        
        # Processa a imagem
        processed_img = preprocess_square_with_padding(image_path, padding_color=padding_color)
        
        # Verifica as dimensões
        if processed_img.shape[:2] != (300, 300):
            print(f"AVISO: A imagem resultante tem tamanho {processed_img.shape[:2]}, esperado (300, 300)")
        
        if verbose:
            # Visualiza
            fig, axes = plt.subplots(1, 2, figsize=(12, 6))
            
            axes[0].imshow(original_img)
            axes[0].set_title(f"Original: {width}x{height}")
            axes[0].axis('off')
            
            axes[1].imshow(processed_img)
            axes[1].set_title(f"Processada: 300x300")
            axes[1].axis('off')
            
            plt.tight_layout()
            plt.show()
        
        # Normaliza para uso com redes neurais
        normalized_img = processed_img.astype(np.float32) / 255.0
        
        print(f"Processamento concluído com sucesso!")
        print(f"Dimensões originais: {width}x{height}")
        print(f"Dimensões após processamento: {processed_img.shape[1]}x{processed_img.shape[0]}")
        
        return processed_img, normalized_img
        
    except Exception as e:
        print(f"Erro durante o processamento: {str(e)}")
        return None

# Exemplo de uso do script
if __name__ == "__main__":
    import sys
    
    # Verifica se o caminho da imagem foi fornecido como argumento
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
    else:
        # Solicita o caminho da imagem ao usuário
        image_path = input("Digite o caminho completo para sua imagem: ")
    
    # Opcionalmente, permite que o usuário escolha a cor do padding
    use_custom_color = input("Deseja usar uma cor personalizada para o padding? (s/n): ").lower() == 's'
    
    if use_custom_color:
        try:
            r = int(input("Valor R (0-255): "))
            g = int(input("Valor G (0-255): "))
            b = int(input("Valor B (0-255): "))
            padding_color = (r, g, b)
        except ValueError:
            print("Valores inválidos, usando preto como padrão.")
            padding_color = (0, 0, 0)
    else:
        padding_color = (0, 0, 0)  # Preto como padrão
    
    # Testa o processamento
    result = test_preprocessing(image_path, padding_color=padding_color)
    
    if result is not None:
        processed_img, normalized_img = result
        print("\nA imagem está pronta para uso com EfficientNetB3!")
        
        # Opcionalmente, salvar a imagem processada
        save_img = input("Deseja salvar a imagem processada? (s/n): ").lower() == 's'
        if save_img:
            output_path = input("Digite o caminho para salvar a imagem processada: ")
            if not output_path:
                output_path = "processed_" + image_path.split("/")[-1]
            
            # Converte RGB para BGR (formato esperado pelo OpenCV)
            save_img = cv2.cvtColor(processed_img, cv2.COLOR_RGB2BGR)
            cv2.imwrite(output_path, save_img)
            print(f"Imagem salva em: {output_path}")