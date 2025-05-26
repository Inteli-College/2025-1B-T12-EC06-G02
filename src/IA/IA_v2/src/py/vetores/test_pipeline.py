"""
Pipeline simples para testar os filtros de pré-processamento de imagens
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
from image_filters import ImageFilters, apply_filter_sequence


def load_and_display_results(image_path: str):
    """
    Carrega uma imagem e aplica os filtros, mostrando os resultados
    
    Args:
        image_path: Caminho para a imagem de teste
    """
    # Carrega a imagem
    try:
        original_image = cv2.imread(image_path, cv2.IMREAD_COLOR)
        
        if original_image is None:
            print(f"Erro: Não foi possível carregar a imagem '{image_path}'")
            print("Verifique se:")
            print("1. O arquivo existe no diretório atual")
            print("2. O formato da imagem é suportado (jpg, png, bmp, etc.)")
            print("3. O caminho está correto")
            return False
        
        # Força o tipo correto e garante que seja contíguo
        original_image = np.array(original_image, dtype=np.uint8)
        original_image = np.ascontiguousarray(original_image)
        
        print(f"✓ Imagem carregada com sucesso!")
        print(f"  Shape: {original_image.shape}")
        print(f"  Tipo: {original_image.dtype}")
        print(f"  Contígua: {original_image.flags['C_CONTIGUOUS']}")
        
        # Converte BGR para RGB para exibição com matplotlib
        original_rgb = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)
        
    except Exception as e:
        print(f"Erro ao processar a imagem: {e}")
        return False
    
    # Aplica cada filtro individualmente
    filters = ImageFilters()
    
    equalized = filters.equalize(original_image)
    equalized_rgb = cv2.cvtColor(equalized, cv2.COLOR_BGR2RGB)
    
    clahe_applied = filters.clahe(original_image)
    clahe_rgb = cv2.cvtColor(clahe_applied, cv2.COLOR_BGR2RGB)
    
    sharpened = filters.sharpen(original_image)
    sharpened_rgb = cv2.cvtColor(sharpened, cv2.COLOR_BGR2RGB)
    
    # Aplica sequência de filtros
    filter_sequence = [
        'equalize',
        ('clahe', {'clip_limit': 3.0, 'tile_grid_size': (8, 8)}),
        ('sharpen', {'strength': 0.8, 'kernel_type': 'laplacian'})
    ]
    
    combined = apply_filter_sequence(original_image, filter_sequence)
    combined_rgb = cv2.cvtColor(combined, cv2.COLOR_BGR2RGB)
    
    # Exibe os resultados
    plt.figure(figsize=(15, 10))
    
    plt.subplot(2, 3, 1)
    plt.imshow(original_rgb)
    plt.title('Original')
    plt.axis('off')
    
    plt.subplot(2, 3, 2)
    plt.imshow(equalized_rgb)
    plt.title('Equalized')
    plt.axis('off')
    
    plt.subplot(2, 3, 3)
    plt.imshow(clahe_rgb)
    plt.title('CLAHE')
    plt.axis('off')
    
    plt.subplot(2, 3, 4)
    plt.imshow(sharpened_rgb)
    plt.title('Sharpened')
    plt.axis('off')
    
    plt.subplot(2, 3, 5)
    plt.imshow(combined_rgb)
    plt.title('Combined Pipeline')
    plt.axis('off')
    
    plt.tight_layout()
    plt.show()
    
    print("Pipeline executada com sucesso!")
    print(f"Filtros aplicados na sequência: {[f[0] if isinstance(f, tuple) else f for f in filter_sequence]}")


def test_with_sample_image():
    """
    Testa os filtros com uma imagem sintética caso não tenha arquivo disponível
    """
    print("Criando imagem sintética para teste...")
    
    # Cria uma imagem sintética com diferentes regiões de contraste
    height, width = 400, 600
    image = np.zeros((height, width, 3), dtype=np.uint8)
    
    # Garante que a imagem seja contígua na memória
    image = np.ascontiguousarray(image)
    
    # Adiciona formas geométricas com diferentes intensidades
    cv2.rectangle(image, (50, 50), (150, 150), (100, 100, 100), -1)
    cv2.rectangle(image, (200, 50), (300, 150), (150, 150, 150), -1)
    cv2.circle(image, (400, 100), 50, (200, 200, 200), -1)
    cv2.rectangle(image, (50, 200), (300, 350), (80, 120, 160), -1)
    
    # Adiciona ruído
    noise = np.random.randint(0, 50, (height, width, 3), dtype=np.uint8)
    image = cv2.add(image, noise)
    
    # Garante que a imagem final seja contígua
    image = np.ascontiguousarray(image, dtype=np.uint8)
    
    # Aplica os filtros
    filters = ImageFilters()
    
    equalized = filters.equalize(image)
    clahe_applied = filters.clahe(image, clip_limit=2.0)
    sharpened = filters.sharpen(image, strength=1.2)
    
    # Pipeline combinada
    filter_sequence = ['clahe', 'sharpen']
    combined = apply_filter_sequence(image, filter_sequence)
    
    # Converte para RGB para exibição
    images_rgb = [cv2.cvtColor(img, cv2.COLOR_BGR2RGB) for img in [image, equalized, clahe_applied, sharpened, combined]]
    titles = ['Original Sintética', 'Equalized', 'CLAHE', 'Sharpened', 'CLAHE + Sharpen']
    
    # Exibe resultados
    plt.figure(figsize=(15, 6))
    for i, (img, title) in enumerate(zip(images_rgb, titles)):
        plt.subplot(1, 5, i+1)
        plt.imshow(img)
        plt.title(title)
        plt.axis('off')
    
    plt.tight_layout()
    plt.show()
    
    print("Teste com imagem sintética concluído!")


def main():
    """Função principal para testar a pipeline"""
    print("=== TESTE DA PIPELINE DE FILTROS ===")
    
    # Tenta carregar uma imagem real primeiro
    test_image_path = "FR98.PNG"  # Seu arquivo PNG
    
    print(f"Tentando carregar: {test_image_path}")
    
    # Tenta carregar a imagem
    success = load_and_display_results(test_image_path)
    
    if not success:
        print(f"\nNão foi possível carregar '{test_image_path}'. Usando imagem sintética...")
        test_with_sample_image()
    
    print("\n=== TESTE DE FILTROS INDIVIDUAIS ===")
    
    # Teste rápido dos filtros individuais com imagem sintética pequena
    print("Criando imagem de teste pequena...")
    sample_image = np.random.randint(0, 255, (200, 200, 3), dtype=np.uint8)
    sample_image = np.ascontiguousarray(sample_image, dtype=np.uint8)
    
    filters = ImageFilters()
    
    try:
        print("✓ Testando equalize...")
        result1 = filters.equalize(sample_image)
        print(f"  Shape: {result1.shape}, Dtype: {result1.dtype}")
        
        print("✓ Testando CLAHE...")
        result2 = filters.clahe(sample_image)
        print(f"  Shape: {result2.shape}, Dtype: {result2.dtype}")
        
        print("✓ Testando sharpen...")
        result3 = filters.sharpen(sample_image)
        print(f"  Shape: {result3.shape}, Dtype: {result3.dtype}")
        
        print("✓ Testando pipeline combinada...")
        pipeline = ['equalize', 'clahe', 'sharpen']
        result4 = apply_filter_sequence(sample_image, pipeline)
        print(f"  Shape: {result4.shape}, Dtype: {result4.dtype}")
        
        print("\n🎉 Todos os testes passaram com sucesso!")
        
    except Exception as e:
        print(f"❌ Erro durante os testes: {e}")
        print("Verifique se todas as dependências foram instaladas corretamente.")


if __name__ == "__main__":
    main()