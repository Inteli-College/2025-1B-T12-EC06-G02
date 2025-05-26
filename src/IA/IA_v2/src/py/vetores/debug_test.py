"""
Script de debug para testar problemas de compatibilidade do OpenCV
"""

import cv2
import numpy as np
import os

def debug_opencv():
    """Testa a compatibilidade do OpenCV"""
    print("=== DEBUG OPENCV ===")
    print(f"OpenCV version: {cv2.__version__}")
    print(f"NumPy version: {np.__version__}")
    
    # Verifica se o arquivo existe
    image_path = "FR98.PNG"
    print(f"\nArquivo '{image_path}' existe: {os.path.exists(image_path)}")
    
    if os.path.exists(image_path):
        print(f"Tamanho do arquivo: {os.path.getsize(image_path)} bytes")
    
    # Tenta carregar a imagem
    print("\n=== TESTANDO CARREGAMENTO ===")
    try:
        img = cv2.imread(image_path, cv2.IMREAD_COLOR)
        print(f"cv2.imread retornou: {type(img)}")
        
        if img is None:
            print("❌ Imagem não foi carregada (retornou None)")
            
            # Tenta diferentes métodos
            print("\nTentando métodos alternativos...")
            
            # Método 1: IMREAD_UNCHANGED
            img_unchanged = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
            print(f"IMREAD_UNCHANGED: {type(img_unchanged)}")
            
            # Método 2: Usando PIL e convertendo
            try:
                from PIL import Image
                pil_img = Image.open(image_path)
                img_pil = np.array(pil_img)
                print(f"PIL -> numpy: {img_pil.shape}, {img_pil.dtype}")
                
                # Converte RGB para BGR se necessário
                if len(img_pil.shape) == 3 and img_pil.shape[2] == 3:
                    img_bgr = cv2.cvtColor(img_pil, cv2.COLOR_RGB2BGR)
                    print(f"Conversão RGB->BGR: OK")
                    img = img_bgr
                else:
                    img = img_pil
                    
            except ImportError:
                print("PIL não disponível, instale com: pip install Pillow")
            except Exception as e:
                print(f"Erro ao usar PIL: {e}")
                
        else:
            print(f"✓ Imagem carregada: {img.shape}, {img.dtype}")
            
        # Se conseguiu carregar, testa conversões
        if img is not None:
            print("\n=== TESTANDO CONVERSÕES ===")
            
            # Força o tipo e contiguidade
            img = np.array(img, dtype=np.uint8)
            img = np.ascontiguousarray(img)
            
            print(f"Após ajustes: {img.shape}, {img.dtype}")
            print(f"Contígua: {img.flags['C_CONTIGUOUS']}")
            print(f"C_CONTIGUOUS: {img.flags.c_contiguous}")
            
            # Testa conversão de cor
            try:
                if len(img.shape) == 3:
                    rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                    print("✓ Conversão BGR->RGB: OK")
                else:
                    print("Imagem em grayscale, sem conversão necessária")
                    
                # Testa filtros básicos
                print("\n=== TESTANDO FILTROS BÁSICOS ===")
                
                # Blur simples
                blurred = cv2.GaussianBlur(img, (5, 5), 0)
                print("✓ GaussianBlur: OK")
                
                # Kernel simples
                kernel = np.ones((3, 3), np.float32) / 9
                kernel = np.ascontiguousarray(kernel)
                filtered = cv2.filter2D(img, -1, kernel)
                print("✓ filter2D: OK")
                
                print("\n🎉 Todos os testes básicos passaram!")
                return True
                
            except Exception as e:
                print(f"❌ Erro na conversão: {e}")
                return False
                
    except Exception as e:
        print(f"❌ Erro geral: {e}")
        return False
    
    return False

def create_test_image():
    """Cria uma imagem de teste simples"""
    print("\n=== CRIANDO IMAGEM DE TESTE ===")
    
    # Cria imagem sintética
    img = np.zeros((200, 300, 3), dtype=np.uint8)
    img = np.ascontiguousarray(img)
    
    # Adiciona algumas formas
    cv2.rectangle(img, (50, 50), (150, 150), (0, 255, 0), -1)
    cv2.circle(img, (200, 100), 50, (255, 0, 0), -1)
    
    # Salva como teste
    cv2.imwrite("test_synthetic.png", img)
    print("✓ Imagem sintética criada: test_synthetic.png")
    
    return img

if __name__ == "__main__":
    success = debug_opencv()
    
    if not success:
        print("\n=== CRIANDO IMAGEM ALTERNATIVA ===")
        test_img = create_test_image()
        
        print("\nTente executar o pipeline com 'test_synthetic.png':")
        print("Altere no test_pipeline.py:")
        print("test_image_path = 'test_synthetic.png'")