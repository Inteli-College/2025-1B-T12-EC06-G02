import cv2
import numpy as np
from typing import Tuple, Union
import os


class SquarePadding:
    """Classe para aplicar square padding em imagens"""
    
    @staticmethod
    def apply_padding(image: np.ndarray, 
                     target_size: Tuple[int, int] = (300, 300), 
                     padding_color: Tuple[int, int, int] = (0, 0, 0)) -> np.ndarray:
        """
        Aplica square padding em uma imagem
        
        Args:
            image: Imagem de entrada (numpy array)
            target_size: Tamanho final desejado (largura, altura)
            padding_color: Cor do padding em RGB/BGR (sempre preto por padrão)
            
        Returns:
            Imagem com padding aplicado e redimensionada
        """
        # Garante que a imagem seja um array numpy válido
        image = np.array(image, dtype=np.uint8)
        image = np.ascontiguousarray(image)
        
        # Obtém dimensões da imagem
        height, width = image.shape[:2]
        
        # Determina o lado maior para criar o quadrado
        max_side = max(height, width)
        
        # Cria uma imagem quadrada com o tamanho do lado maior
        if len(image.shape) == 3:
            # Imagem colorida (BGR/RGB)
            square_img = np.full((max_side, max_side, 3), 
                               padding_color, dtype=np.uint8)
        else:
            # Imagem em grayscale
            square_img = np.full((max_side, max_side), 
                               padding_color[0], dtype=np.uint8)
        
        # Calcula os offsets para centralizar a imagem original
        y_offset = (max_side - height) // 2
        x_offset = (max_side - width) // 2
        
        # Insere a imagem original no centro da imagem quadrada
        if len(image.shape) == 3:
            square_img[y_offset:y_offset+height, x_offset:x_offset+width] = image
        else:
            square_img[y_offset:y_offset+height, x_offset:x_offset+width] = image
        
        # Redimensiona a imagem quadrada para o tamanho alvo
        resized_img = cv2.resize(square_img, target_size, interpolation=cv2.INTER_AREA)
        
        return resized_img
    
    @staticmethod
    def process_image_file(image_path: str, 
                          target_size: Tuple[int, int] = (300, 300),
                          output_path: str = None,
                          show_comparison: bool = True) -> np.ndarray:
        """
        Processa um arquivo de imagem aplicando square padding
        
        Args:
            image_path: Caminho para o arquivo de imagem
            target_size: Tamanho final desejado
            output_path: Caminho para salvar a imagem processada (opcional)
            show_comparison: Se True, mostra comparação antes/depois
            
        Returns:
            Imagem processada
        """
        # Carrega a imagem
        original_image = cv2.imread(image_path)
        
        if original_image is None:
            raise ValueError(f"Não foi possível carregar a imagem: {image_path}")
        
        # Converte para RGB se necessário para exibição
        if show_comparison:
            original_rgb = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)
        
        # Aplica o padding
        processed_image = SquarePadding.apply_padding(
            original_image, target_size=target_size
        )
        
        # Salva se especificado
        if output_path:
            cv2.imwrite(output_path, processed_image)
            print(f"✓ Imagem salva em: {output_path}")
        
        # Mostra comparação se solicitado
        if show_comparison:
            import matplotlib.pyplot as plt
            
            processed_rgb = cv2.cvtColor(processed_image, cv2.COLOR_BGR2RGB)
            
            fig, axes = plt.subplots(1, 2, figsize=(12, 6))
            
            # Original
            axes[0].imshow(original_rgb)
            axes[0].set_title(f"Original\n{original_image.shape[1]}x{original_image.shape[0]}")
            axes[0].axis('off')
            
            # Processada
            axes[1].imshow(processed_rgb)
            axes[1].set_title(f"Square Padded\n{processed_image.shape[1]}x{processed_image.shape[0]}")
            axes[1].axis('off')
            
            plt.suptitle('Square Padding - Antes e Depois')
            plt.tight_layout()
            plt.show()
        
        return processed_image
    
    @staticmethod
    def batch_process(input_folder: str, 
                     output_folder: str = None,
                     target_size: Tuple[int, int] = (300, 300),
                     supported_formats: Tuple[str, ...] = ('.jpg', '.jpeg', '.png', '.bmp', '.tiff')):
        """
        Processa múltiplas imagens em lote
        
        Args:
            input_folder: Pasta com imagens de entrada
            output_folder: Pasta para salvar imagens processadas
            target_size: Tamanho final desejado
            supported_formats: Formatos de arquivo suportados
        """
        if not os.path.exists(input_folder):
            raise ValueError(f"Pasta de entrada não encontrada: {input_folder}")
        
        # Cria pasta de saída se não especificada
        if output_folder is None:
            output_folder = os.path.join(input_folder, "padded_images")
        
        os.makedirs(output_folder, exist_ok=True)
        
        # Processa cada imagem
        processed_count = 0
        for filename in os.listdir(input_folder):
            if filename.lower().endswith(supported_formats):
                input_path = os.path.join(input_folder, filename)
                
                # Nome do arquivo de saída
                name, ext = os.path.splitext(filename)
                output_filename = f"{name}_padded{ext}"
                output_path = os.path.join(output_folder, output_filename)
                
                try:
                    # Processa a imagem
                    SquarePadding.process_image_file(
                        input_path, 
                        target_size=target_size,
                        output_path=output_path,
                        show_comparison=False
                    )
                    processed_count += 1
                    print(f"✓ Processado: {filename}")
                    
                except Exception as e:
                    print(f"❌ Erro ao processar {filename}: {e}")
        
        print(f"\n🎉 Processamento em lote concluído!")
        print(f"   {processed_count} imagens processadas")
        print(f"   Salvas em: {output_folder}")


def create_square_padding(image: np.ndarray, 
                         target_size: Tuple[int, int] = (300, 300)) -> np.ndarray:
    """
    Função de conveniência para aplicar square padding
    
    Args:
        image: Imagem de entrada
        target_size: Tamanho final desejado
        
    Returns:
        Imagem com padding aplicado
    """
    return SquarePadding.apply_padding(image, target_size, padding_color=(0, 0, 0))


def normalize_for_ml(image: np.ndarray) -> np.ndarray:
    """
    Normaliza imagem para uso em machine learning (0-1)
    
    Args:
        image: Imagem de entrada (0-255)
        
    Returns:
        Imagem normalizada (0-1)
    """
    return image.astype(np.float32) / 255.0


def preprocess_for_efficientnet(image_path: str) -> Tuple[np.ndarray, np.ndarray]:
    """
    Pré-processa imagem especificamente para EfficientNet
    
    Args:
        image_path: Caminho para a imagem
        
    Returns:
        Tupla (imagem_processada_uint8, imagem_normalizada_float32)
    """
    # Carrega imagem
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Não foi possível carregar: {image_path}")
    
    # Aplica square padding para 300x300 (padrão EfficientNet B3)
    padded = SquarePadding.apply_padding(image, target_size=(300, 300))
    
    # Normaliza para ML
    normalized = normalize_for_ml(padded)
    
    return padded, normalized


if __name__ == "__main__":
    """Exemplo de uso do módulo"""
    import sys
    
    print("=== SQUARE PADDING - MÓDULO INDEPENDENTE ===")
    
    # Exemplo 1: Imagem única
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
    else:
        image_path = input("Digite o caminho da imagem (ou Enter para usar exemplo): ").strip()
        if not image_path:
            image_path = "FR98.PNG"  # Padrão
    
    if os.path.exists(image_path):
        print(f"\n1. Processando imagem única: {image_path}")
        
        try:
            # Processa com visualização
            result = SquarePadding.process_image_file(
                image_path, 
                target_size=(300, 300),
                output_path=f"padded_{os.path.basename(image_path)}",
                show_comparison=True
            )
            
            print(f"✓ Processamento concluído!")
            print(f"  Dimensões finais: {result.shape[1]}x{result.shape[0]}")
            
            # Versão para ML
            print("\n2. Criando versão para Machine Learning...")
            padded, normalized = preprocess_for_efficientnet(image_path)
            print(f"✓ Versão ML criada:")
            print(f"  Shape: {padded.shape}")
            print(f"  Range normalizado: {normalized.min():.3f} - {normalized.max():.3f}")
            
        except Exception as e:
            print(f"❌ Erro: {e}")
    
    else:
        print(f"❌ Arquivo não encontrado: {image_path}")
        print("\n3. Criando exemplo sintético...")
        
        # Cria exemplo sintético
        example_img = np.zeros((180, 320, 3), dtype=np.uint8)
        cv2.rectangle(example_img, (40, 40), (280, 140), (100, 150, 200), -1)
        cv2.putText(example_img, 'EXEMPLO', (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        
        # Aplica padding
        padded_example = create_square_padding(example_img, target_size=(224, 224))
        
        # Mostra resultado
        import matplotlib.pyplot as plt
        
        fig, axes = plt.subplots(1, 2, figsize=(10, 4))
        
        axes[0].imshow(cv2.cvtColor(example_img, cv2.COLOR_BGR2RGB))
        axes[0].set_title(f"Original: {example_img.shape[1]}x{example_img.shape[0]}")
        axes[0].axis('off')
        
        axes[1].imshow(cv2.cvtColor(padded_example, cv2.COLOR_BGR2RGB))
        axes[1].set_title(f"Padded: {padded_example.shape[1]}x{padded_example.shape[0]}")
        axes[1].axis('off')
        
        plt.suptitle('Exemplo Sintético - Square Padding')
        plt.tight_layout()
        plt.show()
        
        print("✓ Exemplo sintético criado e exibido!")
    
    print("\n🎉 Demonstração do módulo Square Padding concluída!")
    print("Este módulo é completamente independente e pode ser usado sozinho.")
    print("Importações: apenas cv2, numpy, typing e os")