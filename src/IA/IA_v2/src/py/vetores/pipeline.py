"""
Pipeline de pré-processamento de imagens
Orquestra os módulos de filtros e square padding
Este é o ÚNICO arquivo que importa os outros módulos customizados
"""

import cv2
import numpy as np
from typing import List, Union, Tuple, Dict, Any

# Importa os módulos separados e independentes
from image_filters import ImageFilters
from square_padding import SquarePadding


class ImageProcessingPipeline:
    """Pipeline principal que orquestra todos os módulos de processamento"""
    
    def __init__(self):
        """Inicializa a pipeline com os módulos disponíveis"""
        self.filters = ImageFilters()
        self.padding = SquarePadding()
        
        # Mapeamento de filtros disponíveis
        self.available_filters = {
            'equalize': self.filters.equalize,
            'clahe': self.filters.clahe,
            'sharpen': self.filters.sharpen,
            'square_padding': self.padding.apply_padding
        }
    
    def apply_sequence(self, image: np.ndarray, 
                      sequence: List[Union[str, Tuple[str, Dict[str, Any]]]]) -> np.ndarray:
        """
        Aplica uma sequência de filtros na imagem
        
        Args:
            image: Imagem de entrada
            sequence: Lista de filtros a serem aplicados
                     Pode ser strings (nome do filtro) ou tuplas (nome, parâmetros)
                     
        Returns:
            Imagem processada com todos os filtros aplicados
            
        Example:
            sequence = [
                'equalize',
                ('clahe', {'clip_limit': 3.0}),
                ('square_padding', {'target_size': (224, 224)})
            ]
        """
        processed_image = image.copy()
        
        for step in sequence:
            if isinstance(step, str):
                # Apenas nome do filtro, usa parâmetros padrão
                filter_name = step
                kwargs = {}
            elif isinstance(step, tuple) and len(step) == 2:
                # Nome do filtro e parâmetros
                filter_name, kwargs = step
            else:
                raise ValueError("Cada etapa deve ser uma string ou tupla (nome, kwargs)")
            
            # Verifica se o filtro existe
            if filter_name not in self.available_filters:
                available = ', '.join(self.available_filters.keys())
                raise ValueError(f"Filtro '{filter_name}' não reconhecido. Disponíveis: {available}")
            
            # Aplica o filtro
            filter_function = self.available_filters[filter_name]
            processed_image = filter_function(processed_image, **kwargs)
        
        return processed_image
    
    def create_ml_pipeline(self, model_type: str = 'efficientnet') -> List:
        """
        Cria pipelines pré-configuradas para diferentes modelos de ML
        
        Args:
            model_type: Tipo do modelo ('efficientnet', 'resnet', 'vit', 'mobilenet')
            
        Returns:
            Lista de filtros configurada para o modelo
        """
        pipelines = {
            'efficientnet': [
                ('clahe', {'clip_limit': 2.5, 'tile_grid_size': (8, 8)}),
                'equalize',
                ('sharpen', {'strength': 0.8, 'kernel_type': 'laplacian'}),
                ('square_padding', {'target_size': (300, 300), 'padding_color': (0, 0, 0)})
            ],
            'resnet': [
                ('clahe', {'clip_limit': 2.0}),
                ('sharpen', {'strength': 1.0}),
                ('square_padding', {'target_size': (224, 224), 'padding_color': (0, 0, 0)})
            ],
            'vit': [
                'equalize',
                ('clahe', {'clip_limit': 3.0}),
                ('square_padding', {'target_size': (384, 384), 'padding_color': (0, 0, 0)})
            ],
            'mobilenet': [
                ('clahe', {'clip_limit': 1.5}),
                ('square_padding', {'target_size': (224, 224), 'padding_color': (0, 0, 0)})
            ]
        }
        
        if model_type not in pipelines:
            available = ', '.join(pipelines.keys())
            raise ValueError(f"Modelo '{model_type}' não suportado. Disponíveis: {available}")
        
        return pipelines[model_type]
    
    def process_image_file(self, image_path: str, 
                          sequence: List, 
                          output_path: str = None,
                          normalize: bool = False) -> Union[np.ndarray, Tuple[np.ndarray, np.ndarray]]:
        """
        Processa um arquivo de imagem com a pipeline
        
        Args:
            image_path: Caminho para a imagem
            sequence: Sequência de filtros a aplicar
            output_path: Caminho para salvar (opcional)
            normalize: Se True, retorna também versão normalizada (0-1)
            
        Returns:
            Imagem processada (e normalizada se solicitado)
        """
        # Carrega a imagem
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Não foi possível carregar a imagem: {image_path}")
        
        # Aplica a pipeline
        processed = self.apply_sequence(image, sequence)
        
        # Salva se especificado
        if output_path:
            cv2.imwrite(output_path, processed)
            print(f"✓ Imagem processada salva em: {output_path}")
        
        if normalize:
            normalized = processed.astype(np.float32) / 255.0
            return processed, normalized
        
        return processed
    
    def get_filter_info(self) -> Dict[str, str]:
        """Retorna informações sobre os filtros disponíveis"""
        return {
            'equalize': 'Equalização de histograma para melhorar contraste',
            'clahe': 'CLAHE (Contrast Limited Adaptive Histogram Equalization)',
            'sharpen': 'Filtro de nitidez (laplacian ou unsharp masking)',
            'square_padding': 'Transforma imagem em quadrada com padding preto'
        }
    
    def benchmark_pipeline(self, image: np.ndarray, sequence: List, iterations: int = 10) -> Dict:
        """
        Faz benchmark de performance da pipeline
        
        Args:
            image: Imagem para teste
            sequence: Sequência de filtros
            iterations: Número de iterações para o benchmark
            
        Returns:
            Estatísticas de performance
        """
        import time
        
        times = []
        
        for _ in range(iterations):
            start_time = time.time()
            _ = self.apply_sequence(image, sequence)
            end_time = time.time()
            times.append(end_time - start_time)
        
        return {
            'mean_time': np.mean(times),
            'std_time': np.std(times),
            'min_time': np.min(times),
            'max_time': np.max(times),
            'total_time': np.sum(times),
            'iterations': iterations
        }


# Funções de conveniência para uso direto
def create_pipeline() -> ImageProcessingPipeline:
    """Cria uma nova instância da pipeline"""
    return ImageProcessingPipeline()


def apply_filter_sequence(image: np.ndarray, sequence: List) -> np.ndarray:
    """
    Função de conveniência para aplicar sequência de filtros
    
    Args:
        image: Imagem de entrada
        sequence: Lista de filtros
        
    Returns:
        Imagem processada
    """
    pipeline = create_pipeline()
    return pipeline.apply_sequence(image, sequence)


def process_for_ml(image_path: str, model_type: str = 'efficientnet') -> Tuple[np.ndarray, np.ndarray]:
    """
    Função de conveniência para processar imagem para ML
    
    Args:
        image_path: Caminho da imagem
        model_type: Tipo do modelo ('efficientnet', 'resnet', 'vit', 'mobilenet')
        
    Returns:
        Tupla (imagem_processada, imagem_normalizada)
    """
    pipeline = create_pipeline()
    sequence = pipeline.create_ml_pipeline(model_type)
    return pipeline.process_image_file(image_path, sequence, normalize=True)


def quick_preprocess(image: np.ndarray, target_size: Tuple[int, int] = (300, 300)) -> np.ndarray:
    """
    Função de conveniência para pré-processamento rápido
    
    Args:
        image: Imagem de entrada
        target_size: Tamanho final desejado
        
    Returns:
        Imagem pré-processada rapidamente
    """
    quick_sequence = [
        ('clahe', {'clip_limit': 2.0}),
        ('square_padding', {'target_size': target_size})
    ]
    return apply_filter_sequence(image, quick_sequence)


if __name__ == "__main__":
    """Exemplo de uso da pipeline"""
    print("=== PIPELINE DE PROCESSAMENTO DE IMAGENS ===")
    print("Este arquivo orquestra os módulos independentes:")
    print("- image_filters.py (equalize, clahe, sharpen)")
    print("- square_padding.py (square padding)")
    
    # Cria pipeline
    pipeline = create_pipeline()
    
    # Mostra filtros disponíveis
    print("\nFiltros disponíveis:")
    for name, description in pipeline.get_filter_info().items():
        print(f"  {name}: {description}")
    
    # Exemplo de sequência customizada
    custom_sequence = [
        ('clahe', {'clip_limit': 3.0}),
        ('sharpen', {'strength': 1.2}),
        'equalize',
        ('square_padding', {'target_size': (300, 300)})
    ]
    
    print(f"\nSequência de exemplo: {len(custom_sequence)} filtros")
    for i, step in enumerate(custom_sequence, 1):
        if isinstance(step, tuple):
            name, params = step
            print(f"  {i}. {name}: {params}")
        else:
            print(f"  {i}. {step}: parâmetros padrão")
    
    # Mostra pipelines pré-configuradas
    print("\nPipelines pré-configuradas para ML:")
    models = ['efficientnet', 'resnet', 'vit', 'mobilenet']
    for model in models:
        ml_pipeline = pipeline.create_ml_pipeline(model)
        print(f"  {model}: {len(ml_pipeline)} etapas")
    
    # Testa com imagem se disponível
    import os
    test_image = "FR98.PNG"
    
    if os.path.exists(test_image):
        print(f"\n✓ Testando com imagem: {test_image}")
        
        try:
            # Carrega imagem para testes
            original = cv2.imread(test_image)
            original = np.ascontiguousarray(original, dtype=np.uint8)
            
            print(f"  Dimensões originais: {original.shape[1]}x{original.shape[0]}")
            
            # Processa com pipeline customizada
            result = pipeline.process_image_file(
                test_image, 
                custom_sequence,
                output_path="pipeline_result.png"
            )
            
            print(f"✓ Pipeline customizada aplicada!")
            print(f"  Shape final: {result.shape}")
            
            # Mostra comparação visual
            print("\n✓ Mostrando comparação visual...")
            import matplotlib.pyplot as plt
            
            # Converte para RGB para matplotlib
            original_rgb = cv2.cvtColor(original, cv2.COLOR_BGR2RGB)
            result_rgb = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)
            
            plt.figure(figsize=(12, 6))
            
            plt.subplot(1, 2, 1)
            plt.imshow(original_rgb)
            plt.title(f'Original\n{original.shape[1]}x{original.shape[0]}')
            plt.axis('off')
            
            plt.subplot(1, 2, 2)
            plt.imshow(result_rgb)
            plt.title(f'Pipeline Aplicada\n{result.shape[1]}x{result.shape[0]}')
            plt.axis('off')
            
            plt.suptitle('Pipeline Customizada - Antes e Depois')
            plt.tight_layout()
            plt.show()
            
            # Teste pipeline para EfficientNet
            print("\n✓ Testando pipeline para EfficientNet...")
            processed, normalized = process_for_ml(test_image, 'efficientnet')
            
            print(f"✓ Pipeline EfficientNet aplicada!")
            print(f"  Shape: {processed.shape}")
            print(f"  Range normalizado: {normalized.min():.3f} - {normalized.max():.3f}")
            
            # Mostra resultado EfficientNet
            print("\n✓ Comparando diferentes pipelines ML...")
            
            # Testa diferentes modelos
            models_to_test = ['resnet', 'vit']
            ml_results = {}
            
            for model in models_to_test:
                ml_processed, _ = process_for_ml(test_image, model)
                ml_results[model] = ml_processed
            
            # Visualização comparativa
            plt.figure(figsize=(16, 8))
            
            # Original
            plt.subplot(2, 3, 1)
            plt.imshow(original_rgb)
            plt.title(f'Original\n{original.shape[1]}x{original.shape[0]}')
            plt.axis('off')
            
            # Pipeline customizada
            plt.subplot(2, 3, 2)
            plt.imshow(result_rgb)
            plt.title(f'Pipeline Customizada\n{result.shape[1]}x{result.shape[0]}')
            plt.axis('off')
            
            # EfficientNet
            plt.subplot(2, 3, 3)
            plt.imshow(cv2.cvtColor(processed, cv2.COLOR_BGR2RGB))
            plt.title(f'EfficientNet Pipeline\n{processed.shape[1]}x{processed.shape[0]}')
            plt.axis('off')
            
            # ResNet
            plt.subplot(2, 3, 4)
            plt.imshow(cv2.cvtColor(ml_results['resnet'], cv2.COLOR_BGR2RGB))
            plt.title(f'ResNet Pipeline\n{ml_results["resnet"].shape[1]}x{ml_results["resnet"].shape[0]}')
            plt.axis('off')
            
            # ViT
            plt.subplot(2, 3, 5)
            plt.imshow(cv2.cvtColor(ml_results['vit'], cv2.COLOR_BGR2RGB))
            plt.title(f'ViT Pipeline\n{ml_results["vit"].shape[1]}x{ml_results["vit"].shape[0]}')
            plt.axis('off')
            
            # Quick preprocess
            quick_result = quick_preprocess(original, target_size=(224, 224))
            plt.subplot(2, 3, 6)
            plt.imshow(cv2.cvtColor(quick_result, cv2.COLOR_BGR2RGB))
            plt.title(f'Quick Preprocess\n{quick_result.shape[1]}x{quick_result.shape[0]}')
            plt.axis('off')
            
            plt.suptitle('Comparação de Diferentes Pipelines para ML', fontsize=16)
            plt.tight_layout()
            plt.show()
            
            # Benchmark de performance
            print("\n✓ Fazendo benchmark de performance...")
            benchmark_sequence = ['clahe', 'sharpen', 'square_padding']
            stats = pipeline.benchmark_pipeline(original, benchmark_sequence, iterations=5)
            
            print(f"  Tempo médio: {stats['mean_time']:.4f}s")
            print(f"  Tempo mín/máx: {stats['min_time']:.4f}s / {stats['max_time']:.4f}s")
            
            # Teste função rápida
            print("\n✓ Testando pré-processamento rápido...")
            # quick_result já foi criado acima na visualização
            print(f"  Resultado rápido: {quick_result.shape}")
            
            print("\n✓ Visualizações exibidas! Verifique as janelas do matplotlib.")
            
        except Exception as e:
            print(f"❌ Erro: {e}")
    
    else:
        print(f"\n⚠️  Imagem {test_image} não encontrada.")
        print("Coloque uma imagem de teste no diretório para testar a pipeline.")
        
        # Cria e testa com imagem sintética
        print("\n✓ Criando imagem sintética para teste...")
        synthetic = np.zeros((200, 350, 3), dtype=np.uint8)
        cv2.rectangle(synthetic, (50, 50), (300, 150), (100, 150, 200), -1)
        cv2.putText(synthetic, 'PIPELINE TEST', (80, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        
        # Testa pipeline básica
        basic_sequence = ['clahe', ('square_padding', {'target_size': (256, 256)})]
        result_synthetic = apply_filter_sequence(synthetic, basic_sequence)
        
        print(f"✓ Teste com imagem sintética concluído!")
        print(f"  Original: {synthetic.shape}")
        print(f"  Processada: {result_synthetic.shape}")
    
    print("\n🎉 Demonstração da pipeline finalizada!")
    print("\nResumo da arquitetura:")
    print("✓ image_filters.py - Módulo independente de filtros")
    print("✓ square_padding.py - Módulo independente de padding")
    print("✓ pipeline.py - Orquestração dos módulos (este arquivo)")
    print("✓ Cada módulo pode ser usado separadamente")
    print("✓ Pipeline oferece interface unificada e configurações para ML")