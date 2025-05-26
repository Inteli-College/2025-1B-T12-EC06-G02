"""
Módulo de filtros para pré-processamento de imagens
Contém implementações dos filtros: equalize, CLAHE e sharpen
Módulo completamente independente - não importa outros módulos customizados
"""

import cv2
import numpy as np
from typing import Tuple


class ImageFilters:
    """Classe que encapsula os filtros de pré-processamento de imagens"""
    
    @staticmethod
    def equalize(image: np.ndarray) -> np.ndarray:
        """
        Aplica equalização de histograma na imagem
        
        Args:
            image: Imagem de entrada (BGR ou Grayscale)
            
        Returns:
            Imagem com histograma equalizado
        """
        # Garante que a imagem seja um array numpy válido
        image = np.array(image, dtype=np.uint8)
        image = np.ascontiguousarray(image)
        
        if len(image.shape) == 3:
            # Imagem colorida - converte para YUV e equaliza apenas o canal Y
            yuv = cv2.cvtColor(image, cv2.COLOR_BGR2YUV)
            yuv[:, :, 0] = cv2.equalizeHist(yuv[:, :, 0])
            return cv2.cvtColor(yuv, cv2.COLOR_YUV2BGR)
        else:
            # Imagem em grayscale
            return cv2.equalizeHist(image)
    
    @staticmethod
    def clahe(image: np.ndarray, clip_limit: float = 2.0, tile_grid_size: Tuple[int, int] = (8, 8)) -> np.ndarray:
        """
        Aplica CLAHE (Contrast Limited Adaptive Histogram Equalization)
        
        Args:
            image: Imagem de entrada (BGR ou Grayscale)
            clip_limit: Limite de contraste para evitar amplificação excessiva de ruído
            tile_grid_size: Tamanho da grade de tiles (largura, altura)
            
        Returns:
            Imagem com CLAHE aplicado
        """
        # Garante que a imagem seja um array numpy válido
        image = np.array(image, dtype=np.uint8)
        image = np.ascontiguousarray(image)
        
        clahe_filter = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=tile_grid_size)
        
        if len(image.shape) == 3:
            # Imagem colorida - converte para LAB e aplica CLAHE no canal L
            lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
            lab[:, :, 0] = clahe_filter.apply(lab[:, :, 0])
            return cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
        else:
            # Imagem em grayscale
            return clahe_filter.apply(image)
    
    @staticmethod
    def sharpen(image: np.ndarray, strength: float = 1.0, kernel_type: str = 'laplacian') -> np.ndarray:
        """
        Aplica filtro de nitidez (sharpening) na imagem
        
        Args:
            image: Imagem de entrada
            strength: Intensidade do filtro (1.0 = intensidade padrão)
            kernel_type: Tipo de kernel ('laplacian' ou 'unsharp')
            
        Returns:
            Imagem com filtro de nitidez aplicado
        """
        # Garante que a imagem seja um array numpy válido
        image = np.asarray(image, dtype=np.uint8)
        
        if kernel_type == 'laplacian':
            # Kernel Laplaciano para detecção de bordas
            kernel = np.array([
                [0, -1, 0],
                [-1, 5, -1],
                [0, -1, 0]
            ], dtype=np.float32)
            
            # Ajusta a intensidade do kernel
            kernel = kernel * strength
            kernel[1, 1] = 4 * strength + 1  # Ajusta o centro para manter o balanço
            
            # Garante que o kernel seja contíguo na memória
            kernel = np.ascontiguousarray(kernel, dtype=np.float32)
            
            return cv2.filter2D(image, -1, kernel)
            
        elif kernel_type == 'unsharp':
            # Unsharp masking
            gaussian = cv2.GaussianBlur(image, (0, 0), 2.0)
            return cv2.addWeighted(image, 1.0 + strength, gaussian, -strength, 0)
        
        else:
            raise ValueError("kernel_type deve ser 'laplacian' ou 'unsharp'")


# Funções de conveniência para uso direto do módulo
def equalize_image(image: np.ndarray) -> np.ndarray:
    """Função de conveniência para equalização de histograma"""
    return ImageFilters.equalize(image)


def clahe_image(image: np.ndarray, clip_limit: float = 2.0, tile_grid_size: Tuple[int, int] = (8, 8)) -> np.ndarray:
    """Função de conveniência para CLAHE"""
    return ImageFilters.clahe(image, clip_limit, tile_grid_size)


def sharpen_image(image: np.ndarray, strength: float = 1.0, kernel_type: str = 'laplacian') -> np.ndarray:
    """Função de conveniência para sharpening"""
    return ImageFilters.sharpen(image, strength, kernel_type)


if __name__ == "__main__":
    """Teste independente do módulo de filtros"""
    print("=== TESTE INDEPENDENTE DOS FILTROS ===")
    
    # Cria imagem sintética para teste
    test_image = np.zeros((200, 300, 3), dtype=np.uint8)
    cv2.rectangle(test_image, (50, 50), (250, 150), (100, 150, 200), -1)
    cv2.circle(test_image, (150, 100), 30, (200, 100, 150), -1)
    
    # Adiciona ruído
    noise = np.random.randint(0, 30, test_image.shape, dtype=np.uint8)
    test_image = cv2.add(test_image, noise)
    test_image = np.ascontiguousarray(test_image, dtype=np.uint8)
    
    filters = ImageFilters()
    
    print("✓ Testando equalize...")
    equalized = filters.equalize(test_image)
    print(f"  Input: {test_image.shape}, Output: {equalized.shape}")
    
    print("✓ Testando CLAHE...")
    clahe_result = filters.clahe(test_image, clip_limit=3.0)
    print(f"  Input: {test_image.shape}, Output: {clahe_result.shape}")
    
    print("✓ Testando sharpen...")
    sharpened = filters.sharpen(test_image, strength=1.5)
    print(f"  Input: {test_image.shape}, Output: {sharpened.shape}")
    
    print("✓ Testando funções de conveniência...")
    conv_equalized = equalize_image(test_image)
    conv_clahe = clahe_image(test_image)
    conv_sharpen = sharpen_image(test_image)
    
    print(f"  Todas as funções funcionando: {conv_equalized.shape == conv_clahe.shape == conv_sharpen.shape}")
    
    print("\n🎉 Módulo de filtros testado com sucesso!")
    print("Este módulo é completamente independente e pode ser usado sozinho.")
    print("Importações: apenas cv2, numpy e typing")