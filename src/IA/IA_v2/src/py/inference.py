import torch
import torch.nn.functional as F
from PIL import Image
import numpy as np
import cv2
from typing import Dict, List, Tuple, Union
from pathlib import Path
import albumentations as A
from albumentations.pytorch import ToTensorV2
import matplotlib.pyplot as plt
import seaborn as sns

from model import create_model
from config import Config


class CrackClassifier:
    """
    Classificador de fissuras para inferência em novas imagens.
    
    Carrega modelo treinado e realiza classificação entre fissuras de retração e térmicas.
    """
    
    def __init__(self, model_path: str, config: Config = None):
        self.config = config or Config()
        self.device = torch.device(self.config.DEVICE)
        self.class_names = self.config.CLASSES
        
        # Carregar modelo
        self.model = self._load_model(model_path)
        
        # Transformações para pré-processamento
        self.transform = self._create_transform()
        
        print(f"Classificador carregado!")
        print(f"Device: {self.device}")
        print(f"Classes: {self.class_names}")
    
    def _load_model(self, model_path: str):
        """Carrega modelo treinado."""
        print(f"Carregando modelo de: {model_path}")
        
        # Carregar checkpoint
        checkpoint = torch.load(model_path, map_location=self.device)
        
        # Criar modelo
        model = create_model(**self.config.get_model_config())
        
        # Carregar pesos
        model.load_state_dict(checkpoint['model_state_dict'])
        model.to(self.device)
        model.eval()
        
        print(f"Modelo carregado da época {checkpoint.get('epoch', 'N/A')}")
        print(f"Acurácia de validação: {checkpoint.get('metrics', {}).get('accuracy', 'N/A'):.2f}%")
        
        return model
    
    def _create_transform(self):
        """Cria transformações para pré-processamento."""
        transforms = []
        
        # Redimensionar para o tamanho esperado
        transforms.append(A.Resize(self.config.IMAGE_SIZE, self.config.IMAGE_SIZE))
        
        # Aplicar filtros se configurado
        if self.config.USE_SQUARE_PADDING:
            transforms.append(A.PadIfNeeded(
                min_height=self.config.IMAGE_SIZE,
                min_width=self.config.IMAGE_SIZE,
                border_mode=cv2.BORDER_CONSTANT,
                value=self.config.SQUARE_PADDING_COLOR
            ))
        
        if self.config.USE_CLAHE:
            transforms.append(A.CLAHE(
                clip_limit=self.config.CLAHE_CLIP_LIMIT,
                tile_grid_size=self.config.CLAHE_TILE_GRID_SIZE,
                p=1.0
            ))
        
        if self.config.USE_EQUALIZE:
            transforms.append(A.Equalize(p=1.0))
        
        if self.config.USE_SHARPEN:
            if self.config.SHARPEN_KERNEL_TYPE.lower() == "laplacian":
                transforms.append(A.Sharpen(
                    alpha=(0.2, 0.5),
                    lightness=(0.5, 1.0),
                    p=1.0
                ))
        
        # Normalização ImageNet
        transforms.extend([
            A.Normalize(
                mean=self.config.NORMALIZE_MEAN,
                std=self.config.NORMALIZE_STD
            ),
            ToTensorV2()
        ])
        
        return A.Compose(transforms)
    
    def preprocess_image(self, image: Union[str, np.ndarray, Image.Image]) -> torch.Tensor:
        """Pré-processa imagem para inferência."""
        
        # Converter para numpy array se necessário
        if isinstance(image, str):
            image = cv2.imread(image)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        elif isinstance(image, Image.Image):
            image = np.array(image)
            if len(image.shape) == 3 and image.shape[2] == 4:  # RGBA
                image = image[:, :, :3]  # Remove alpha channel
        
        # Aplicar transformações
        transformed = self.transform(image=image)
        tensor = transformed['image'].unsqueeze(0)  # Add batch dimension
        
        return tensor.to(self.device)
    
    def predict(self, image: Union[str, np.ndarray, Image.Image], 
                return_probabilities: bool = True) -> Dict[str, Union[str, float, Dict]]:
        """
        Prediz a classe de uma imagem.
        
        Args:
            image: Caminho da imagem, array numpy ou PIL Image
            return_probabilities: Se deve retornar probabilidades
            
        Returns:
            Dicionário com predição e informações
        """
        
        # Pré-processar imagem
        tensor = self.preprocess_image(image)
        
        # Inferência
        with torch.no_grad():
            outputs = self.model(tensor)
            probabilities = F.softmax(outputs, dim=1)
            predicted_class = torch.argmax(probabilities, dim=1).item()
            confidence = probabilities[0][predicted_class].item()
        
        result = {
            'predicted_class': self.class_names[predicted_class],
            'confidence': confidence * 100,
            'predicted_index': predicted_class
        }
        
        if return_probabilities:
            probs = {self.class_names[i]: prob.item() * 100 
                    for i, prob in enumerate(probabilities[0])}
            result['probabilities'] = probs
        
        return result
    
    def predict_batch(self, images: List[Union[str, np.ndarray, Image.Image]]) -> List[Dict]:
        """Prediz classe para múltiplas imagens."""
        results = []
        
        print(f"Processando {len(images)} imagens...")
        
        for i, image in enumerate(images):
            try:
                result = self.predict(image)
                result['image_index'] = i
                results.append(result)
                
                if (i + 1) % 10 == 0:
                    print(f"Processadas {i + 1}/{len(images)} imagens")
                    
            except Exception as e:
                print(f"Erro ao processar imagem {i}: {str(e)}")
                results.append({
                    'image_index': i,
                    'error': str(e),
                    'predicted_class': None,
                    'confidence': 0.0
                })
        
        return results
    
    def predict_folder(self, folder_path: str, extensions: List[str] = None) -> Dict[str, List]:
        """
        Prediz classe para todas as imagens em uma pasta.
        
        Args:
            folder_path: Caminho da pasta
            extensions: Extensões de arquivo permitidas
            
        Returns:
            Dicionário com resultados organizados por classe
        """
        if extensions is None:
            extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']
        
        folder = Path(folder_path)
        image_files = []
        
        for ext in extensions:
            image_files.extend(folder.glob(f"*{ext}"))
            image_files.extend(folder.glob(f"*{ext.upper()}"))
        
        print(f"Encontradas {len(image_files)} imagens em {folder_path}")
        
        if not image_files:
            print("Nenhuma imagem encontrada!")
            return {}
        
        # Processar todas as imagens
        results = self.predict_batch([str(f) for f in image_files])
        
        # Organizar resultados por classe
        organized_results = {class_name: [] for class_name in self.class_names}
        organized_results['errors'] = []
        
        for result, image_file in zip(results, image_files):
            result['file_path'] = str(image_file)
            result['file_name'] = image_file.name
            
            if 'error' in result:
                organized_results['errors'].append(result)
            else:
                organized_results[result['predicted_class']].append(result)
        
        # Estatísticas
        total_processed = len([r for r in results if 'error' not in r])
        print(f"\nResultados:")
        for class_name in self.class_names:
            count = len(organized_results[class_name])
            percentage = (count / total_processed * 100) if total_processed > 0 else 0
            print(f"   {class_name}: {count} imagens ({percentage:.1f}%)")
        
        if organized_results['errors']:
            print(f"   Erros: {len(organized_results['errors'])} imagens")
        
        return organized_results
    
    def visualize_prediction(self, image: Union[str, np.ndarray, Image.Image], 
                           save_path: str = None, figsize: Tuple[int, int] = (10, 6)):
        """Visualiza predição com imagem e probabilidades."""
        
        # Fazer predição
        result = self.predict(image, return_probabilities=True)
        
        # Carregar imagem original
        if isinstance(image, str):
            img = cv2.imread(image)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        elif isinstance(image, Image.Image):
            img = np.array(image)
        else:
            img = image
        
        # Criar visualização
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize)
        
        # Mostrar imagem
        ax1.imshow(img)
        ax1.set_title(f'Predição: {result["predicted_class"]}\n'
                     f'Confiança: {result["confidence"]:.1f}%')
        ax1.axis('off')
        
        # Gráfico de probabilidades
        classes = list(result['probabilities'].keys())
        probs = list(result['probabilities'].values())
        colors = ['red' if p == max(probs) else 'lightblue' for p in probs]
        
        bars = ax2.bar(classes, probs, color=colors)
        ax2.set_title('Probabilidades por Classe')
        ax2.set_ylabel('Probabilidade (%)')
        ax2.set_ylim(0, 100)
        
        # Adicionar valores nas barras
        for bar, prob in zip(bars, probs):
            ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                    f'{prob:.1f}%', ha='center', va='bottom')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Visualização salva em: {save_path}")
        
        plt.show()
        
        return result


def load_classifier(model_path: str, config_path: str = None) -> CrackClassifier:
    """
    Função utilitária para carregar classificador.
    
    Args:
        model_path: Caminho do modelo treinado
        config_path: Caminho da configuração (opcional)
        
    Returns:
        Instância do classificador
    """
    config = Config()
    if config_path:
        # Carregar config customizado se fornecido
        pass
    
    return CrackClassifier(model_path, config)


# Exemplo de uso
if __name__ == "__main__":
    # Exemplo de como usar o classificador
    model_path = "models/best_model_epoch_50.pt"  # Ajustar caminho
    
    try:
        # Carregar classificador
        classifier = load_classifier(model_path)
        
        # Exemplo 1: Predizer uma imagem
        image_path = "data/raw/retracao/example.jpg"  # Ajustar caminho
        if Path(image_path).exists():
            result = classifier.predict(image_path)
            print(f"Resultado: {result}")
            
            # Visualizar predição
            classifier.visualize_prediction(image_path, save_path="prediction_result.png")
        
        # Exemplo 2: Processar pasta inteira
        folder_path = "data/raw/termicas"  # Ajustar caminho
        if Path(folder_path).exists():
            results = classifier.predict_folder(folder_path)
            print(f"Resultados da pasta: {results}")
    
    except Exception as e:
        print(f"Erro: {e}")
        print("Certifique-se de que o modelo foi treinado e os caminhos estão corretos.") 