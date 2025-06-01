import os
import torch
import torch.nn.functional as F
import cv2
import requests
import base64
import re
import numpy as np
from pathlib import Path
from typing import Dict, List, Union, Optional, Tuple
import albumentations as A
from albumentations.pytorch import ToTensorV2
import sys
from urllib.parse import urlparse



class UnifiedCrackClassifier:
    
    def __init__(self, model_path: str):

        self.model_path = Path(model_path)
        self.model_type = self._detect_model_type()
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
        # Mapear classes (padrão para ambos os modelos)
        self.classes = ["retracao", "termica"]
        self.class_names = {0: "retracao", 1: "termica"}
        
        # Carregar modelo e configurações
        self.model = None
        self.config = None
        self.transform = None
        self._load_model()
        self._setup_transforms()
        
        print(f"Classificador carregado: {self.model_type}")
        print(f"Device: {self.device}")
        print(f"Classes: {self.classes}")
    
    def _detect_model_type(self) -> str:
        """Detecta o tipo de modelo automaticamente baseado no caminho."""
        # Detectar baseado no caminho completo
        path_str = str(self.model_path).lower()
        
        # Verificar se contém "resnet" no caminho
        if "resnet" in path_str:
            return "resnet"
        
        # Verificar se contém "swin" no caminho
        if "swin" in path_str:
            return "swin"
        
        # Verificar diretórios pais na hierarquia
        current_path = self.model_path
        for parent in current_path.parents:
            parent_name = parent.name.lower()
            if "resnet" in parent_name:
                return "resnet"
            elif "swin" in parent_name:
                return "swin"
        
        # Se não detectar, tentar pela estrutura de diretórios
        # Procurar por pastas resnet-18 ou swin-transformer-v2 na hierarquia
        for parent in self.model_path.parents:
            if (parent / "resnet-18").exists():
                return "resnet"
            elif (parent / "swin-transformer-v2").exists():
                return "swin"
        
        # Padrão para ResNet se não conseguir detectar
        print("Aviso: Não foi possível detectar o tipo de modelo automaticamente. Usando SwinTransformer como padrão.")
        return "swin"
    
    def _find_model_directory(self) -> Path:
        """Encontra o diretório do modelo específico (resnet-18 ou swin-transformer-v2)."""
        current_path = self.model_path
        
        # Procurar na hierarquia de diretórios
        for parent in current_path.parents:
            if self.model_type == "resnet":
                resnet_dir = parent / "resnet-18"
                if resnet_dir.exists():
                    return resnet_dir
            elif self.model_type == "swin":
                swin_dir = parent / "swin-transformer-v2"
                if swin_dir.exists():
                    return swin_dir
        
        # Se não encontrar, usar o diretório pai do modelo
        return current_path.parent
    
    def _load_model(self):
        """Carrega o modelo baseado no tipo."""
        if not self.model_path.exists():
            raise FileNotFoundError(f"Modelo não encontrado: {self.model_path}")
        

        checkpoint = torch.load(self.model_path, map_location=self.device, weights_only=False)
        
        if self.model_type == "resnet":
            self._load_resnet_model(checkpoint)
        elif self.model_type == "swin":
            self._load_swin_model(checkpoint)
        else:
            raise ValueError(f"Tipo de modelo não suportado: {self.model_type}")
    
    def _load_resnet_model(self, checkpoint: Dict):
        """Carrega modelo ResNet-18."""
        # Encontrar o diretório do ResNet
        model_dir = self._find_model_directory()
        
        # Adicionar ao sys.path
        sys.path.insert(0, str(model_dir))
        
        try:
            from model import create_model
            from config import Config
            
            self.config = Config()
            
            # Configurações do ResNet
            self.model = create_model(
                num_classes=2,
                model_type="resnet",
                model_name="resnet18",
                pretrained=False,
                freeze_backbone=False,
                dropout_rate=0.5
            )
            
            # Carregar pesos
            if 'model_state_dict' in checkpoint:
                self.model.load_state_dict(checkpoint['model_state_dict'])
            else:
                self.model.load_state_dict(checkpoint)
            
            self.model.to(self.device)
            self.model.eval()
            
            print(f"ResNet-18 carregado da época {checkpoint.get('epoch', 'N/A')}")
            
        except ImportError as e:
            raise ImportError(f"Erro ao importar módulos do ResNet de {model_dir}: {e}")
        finally:
            # Remover do sys.path para evitar conflitos
            if str(model_dir) in sys.path:
                sys.path.remove(str(model_dir))
    
    def _load_swin_model(self, checkpoint: Dict):
        """Carrega modelo Swin Transformer."""
        # Encontrar o diretório do Swin
        model_dir = self._find_model_directory()
        
        # Adicionar ao sys.path
        sys.path.insert(0, str(model_dir))
        
        try:
            from model import create_model
            from config import Config
            
            self.config = Config()
            
            # Criar modelo Swin
            model_config = self.config.get_model_config()
            self.model = create_model(**model_config)
            
            # Carregar pesos
            if 'model_state_dict' in checkpoint:
                self.model.load_state_dict(checkpoint['model_state_dict'])
            else:
                self.model.load_state_dict(checkpoint)
            
            self.model.to(self.device)
            self.model.eval()
            
            print(f"Swin Transformer carregado da época {checkpoint.get('epoch', 'N/A')}")
            if 'metrics' in checkpoint:
                acc = checkpoint['metrics'].get('accuracy', 'N/A')
                print(f"Acurácia de validação: {acc:.2f}%" if isinstance(acc, (int, float)) else f"Acurácia: {acc}")
                
        except ImportError as e:
            raise ImportError(f"Erro ao importar módulos do Swin de {model_dir}: {e}")
        finally:
            # Remover do sys.path para evitar conflitos
            if str(model_dir) in sys.path:
                sys.path.remove(str(model_dir))
    
    def _setup_transforms(self):
        """Configura transformações para inferência."""
        image_size = getattr(self.config, 'IMAGE_SIZE', 224)
        
        transforms = [
            A.Resize(image_size, image_size, interpolation=cv2.INTER_AREA)
        ]
        
        # Aplicar filtros específicos do modelo se configurado
        if hasattr(self.config, 'USE_CLAHE') and getattr(self.config, 'USE_CLAHE', False):
            transforms.append(A.CLAHE(
                clip_limit=getattr(self.config, 'CLAHE_CLIP_LIMIT', 2.0),
                tile_grid_size=getattr(self.config, 'CLAHE_TILE_GRID_SIZE', (8, 8)),
                p=1.0
            ))
        
        if hasattr(self.config, 'USE_EQUALIZE') and getattr(self.config, 'USE_EQUALIZE', False):
            transforms.append(A.Equalize(p=1.0))
        
        # Normalização padrão ImageNet
        transforms.extend([
            A.Normalize(
                mean=getattr(self.config, 'NORMALIZE_MEAN', [0.485, 0.456, 0.406]),
                std=getattr(self.config, 'NORMALIZE_STD', [0.229, 0.224, 0.225]),
                max_pixel_value=255.0
            ),
            ToTensorV2()
        ])
        
        self.transform = A.Compose(transforms)
    
    def _load_image(self, image_path: Union[str, Path]) -> np.ndarray:
        """Carrega e pré-processa uma imagem de um caminho local ou URL."""
        image_path = str(image_path)

        # Se for uma data URL (base64)
        if image_path.startswith("data:image/"):
            try:
                header, base64_data = image_path.split(",", 1)
                image_data = base64.b64decode(base64_data)
                image_array = np.asarray(bytearray(image_data), dtype=np.uint8)
                image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
            except Exception as e:
                raise ValueError(f"Não foi possível carregar a imagem base64.\nErro: {e}")
        # Verifica se é uma URL
        elif urlparse(image_path).scheme in ('http', 'https'):
            try:
                response = requests.get(image_path, timeout=5)
                response.raise_for_status()
                image_array = np.asarray(bytearray(response.content), dtype=np.uint8)
                image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
            except Exception as e:
                raise ValueError(f"Não foi possível carregar a imagem da URL: {image_path}\nErro: {e}")
        else:
            image = cv2.imread(image_path, cv2.IMREAD_COLOR)

        if image is None:
            raise ValueError(f"Não foi possível carregar a imagem: {image_path}")

        # Converter BGR para RGB
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        return image
    
    def predict(self, image_path: Union[str, Path]) -> Dict:

        # Carregar e pré-processar imagem
        image = self._load_image(image_path)
        
        # Aplicar transformações
        transformed = self.transform(image=image)
        tensor = transformed['image'].unsqueeze(0).to(self.device)
        
        # Inferência
        with torch.no_grad():
            outputs = self.model(tensor)
            probabilities = F.softmax(outputs, dim=1)
            confidence, predicted = torch.max(probabilities, 1)
        
        predicted_class = predicted.item()
        confidence_score = confidence.item() * 100
        
        return {
            "predicted_class": self.class_names[predicted_class],
            "predicted_index": predicted_class,
            "confidence": confidence_score,
            "probabilities": {
                self.class_names[i]: prob.item() * 100 
                for i, prob in enumerate(probabilities[0])
            }
        }
    
    def predict_batch_from_objects(self, data: Dict) -> List[Dict]:
        """Recebe JSON com chaves: images ([{id, previewUrl}]), model_path."""
        results = []
        image_entries = data.get("images", [])
    
        for i, entry in enumerate(image_entries):
            try:
                image_id = entry.get("id")
                preview_url = entry.get("previewUrl")
                image_array = self._load_image_from_input(preview_url)
                prediction = self.predict_from_array(image_array)
    
                result = {
                    "id": image_id,
                    "previewUrl": preview_url,
                    "prev": prediction["predicted_class"],
                    "confidence": round(prediction["confidence"], 1),
                    "probabilities": prediction["probabilities"]
                }
                results.append(result)
    
            except Exception as e:
                print(f"Erro ao processar imagem {i}: {e}")
                results.append({
                    "id": entry.get("id", f"img_{i}"),
                    "previewUrl": entry.get("previewUrl", ""),
                    "prev": "erro",
                    "confidence": 0.0,
                    "error": str(e)
                })
    
        return results

    
    def predict_with_confidence(self, 
                               image_paths: List[Union[str, Path]], 
                               image_ids: List,
                               preview_urls: List[str]) -> List[Dict]:

        results = []
        
        for i, image_path in enumerate(image_paths):
            try:
                # Predição individual
                prediction = self.predict(image_path)
                
                # Formato estendido
                result = {
                    "id": image_ids[i],
                    "previewUrl": preview_urls[i],
                    "prev": prediction["predicted_class"],
                    "confidence": round(prediction["confidence"], 1),
                    "probabilities": prediction["probabilities"]
                }
                
                results.append(result)
                
            except Exception as e:
                print(f"Erro ao processar imagem {image_path}: {e}")
                # Adicionar resultado de erro
                results.append({
                    "id": image_ids[i],
                    "previewUrl": preview_urls[i],
                    "prev": "erro",
                    "confidence": 0.0,
                    "error": str(e)
                })
        
        return results

def load_classifier(model_path: str) -> UnifiedCrackClassifier:
    return UnifiedCrackClassifier(model_path)


def classify_for_frontend(images: List[Dict], model_path: str) -> List[Dict]:
    classifier = load_classifier(model_path)

    # Extrair os campos necessários dos dicionários de entrada
    image_paths = [img["previewUrl"] for img in images]
    image_ids = [img["id"] for img in images]
    preview_urls = [img["previewUrl"] for img in images]

    return classifier.predict_with_confidence(image_paths, image_ids, preview_urls)
