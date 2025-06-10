import os
import sys
import cv2
import torch
import numpy as np
from torch.utils.data import Dataset, DataLoader
from typing import List, Tuple, Optional, Callable, Any
import albumentations as A
from albumentations.pytorch import ToTensorV2
import glob

def diagnose_import_issues():
    """Diagnóstica problemas de importação detalhadamente"""
    print("=" * 60)
    print("DIAGNÓSTICO DETALHADO DE IMPORTAÇÃO")
    print("=" * 60)
    
    # 1. Verificar diretório atual e Python path
    current_dir = os.getcwd()
    script_dir = os.path.dirname(os.path.abspath(__file__)) if '__file__' in globals() else current_dir
    
    print(f"Diretório atual: {current_dir}")
    print(f"Diretório do script: {script_dir}")
    print(f"Python path atual: {sys.path[:3]}...")  # Mostrar apenas os primeiros 3
    
    # 2. Procurar arquivos necessários
    required_files = ['image_filters.py', 'square_padding.py']
    found_files = {}
    
    print(f"\nProcurando arquivos necessários...")
    
    # Procurar no diretório atual primeiro
    for file in required_files:
        file_path = os.path.join(current_dir, file)
        if os.path.exists(file_path):
            found_files[file] = file_path
            print(f"{file} encontrado em: {file_path}")
        else:
            print(f"{file} NÃO encontrado no diretório atual")
    
    # Se não encontrou todos, procurar em subdiretórios
    missing_files = [f for f in required_files if f not in found_files]
    if missing_files:
        print(f"\nProcurando arquivos faltantes em subdiretórios...")
        for root, _, files in os.walk(current_dir):
            for file in missing_files:
                if file in files:
                    full_path = os.path.join(root, file)
                    found_files[file] = full_path
                    print(f"{file} encontrado em: {full_path}")
    
    # 3. Verificar se ainda há arquivos faltantes
    still_missing = [f for f in required_files if f not in found_files]
    if still_missing:
        print(f"\nARQUIVOS AINDA FALTANTES: {still_missing}")
        print("\nSOLUÇÕES POSSÍVEIS:")
        print("1. Certifique-se de que os arquivos estão no mesmo diretório do script")
        print("2. Verifique se os nomes dos arquivos estão corretos")
        print("3. Verifique as permissões dos arquivos")
        return False, {}
    
    # 4. Testar importações
    print(f"\nTestando importações...")
    import_results = {}
    
    for file, path in found_files.items():
        module_dir = os.path.dirname(path)
        module_name = os.path.splitext(file)[0]
        
        try:
            # Adicionar diretório ao path se necessário
            if module_dir not in sys.path:
                sys.path.insert(0, module_dir)
                print(f"Adicionado ao Python path: {module_dir}")
            
            # Tentar importar
            if module_name == 'image_filters':
                exec(f"from {module_name} import ImageFilters")
                import_results['ImageFilters'] = True
                print(f"ImageFilters importado com sucesso")
            elif module_name == 'square_padding':
                exec(f"from {module_name} import SquarePadding")
                import_results['SquarePadding'] = True
                print(f"SquarePadding importado com sucesso")
                
        except Exception as e:
            print(f"Erro ao importar {module_name}: {e}")
            import_results[module_name] = False
            
            # Verificar conteúdo do arquivo para diagnóstico adicional
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if 'class ImageFilters' in content:
                        print(f"  → Classe ImageFilters encontrada no arquivo")
                    elif 'class SquarePadding' in content:
                        print(f"  → Classe SquarePadding encontrada no arquivo")
                    else:
                        print(f"  → Classe esperada NÃO encontrada no arquivo")
            except Exception as read_error:
                print(f"  → Erro ao ler arquivo: {read_error}")
    
    success = all(import_results.values())
    print(f"\n{'DIAGNÓSTICO: SUCESSO' if success else 'DIAGNÓSTICO: FALHA'}")
    print("=" * 60)
    
    return success, found_files

# Executar diagnóstico antes de tentar importar
success, found_files = diagnose_import_issues()

if not success:
    print("\nERRO CRÍTICO: Não foi possível importar os módulos necessários!")
    print("Por favor, resolva os problemas indicados acima antes de continuar.")
    sys.exit(1)

# Agora fazer as importações reais
try:
    from image_filters import ImageFilters
    from square_padding import SquarePadding
    CUSTOM_FILTERS_AVAILABLE = True
    print("[SUCCESS] Todos os filtros customizados importados com sucesso!")
except ImportError as e:
    print(f"[ERRO FATAL] Falha na importação após diagnóstico: {e}")
    print("Verifique se as classes estão corretamente definidas nos arquivos.")
    sys.exit(1)

class BaseImageDataset(Dataset):
    """Dataset base para classificação de imagens."""
    
    def __init__(self, 
                 image_paths: List[str],
                 labels: List[int],
                 transform: Optional[Callable] = None,
                 config: Any = None,
                 cache_processed: bool = False):
        
        if len(image_paths) != len(labels):
            raise ValueError(f"Número de imagens ({len(image_paths)}) deve ser igual ao número de labels ({len(labels)})")
        
        self.image_paths = image_paths
        self.labels = labels
        self.transform = transform
        self.config = config
        self.cache_processed = cache_processed
        
        # Inicializar filtros customizados
        print("[DEBUG] Inicializando ImageFilters e SquarePadding em BaseImageDataset.")
        self.image_filters = ImageFilters()
        self.square_padding = SquarePadding()
        print("[DEBUG] Filtros customizados inicializados com sucesso.")
        
        self._image_cache = {} if cache_processed else None
        self.num_classes = len(set(labels))
        self.class_counts = {i: labels.count(i) for i in range(self.num_classes)}
        
    def __len__(self) -> int:
        return len(self.image_paths)
    
    def __getitem__(self, idx: int) -> Tuple[torch.Tensor, int]:
        if self._image_cache is not None and idx in self._image_cache:
            return self._image_cache[idx]
        
        image_path = self.image_paths[idx]
        label = self.labels[idx]
        
        try:
            image = self._load_image(image_path)
            
            # Aplicar filtros customizados se config estiver presente
            if self.config:
                print(f"[DEBUG] Aplicando filtros customizados em {os.path.basename(image_path)}")
                image = self._apply_custom_filters(image)
            else:
                print(f"[DEBUG] Config não fornecido - pulando filtros customizados para {os.path.basename(image_path)}")
            
            if self.transform:
                transformed = self.transform(image=image)
                image = transformed['image']
            
            if self._image_cache is not None:
                self._image_cache[idx] = (image, label)
            
            return image, label
            
        except Exception as e:
            print(f"[ERRO] Falha ao processar imagem {image_path}: {e}")
            raise  # Re-raise para não mascarar erros
    
    def _load_image(self, image_path: str) -> np.ndarray:
        """Carrega uma imagem de forma robusta."""
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Arquivo não encontrado: {image_path}")
        
        image = cv2.imread(image_path, cv2.IMREAD_COLOR)
        
        if image is None:
            image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
            
            if image is None:
                raise ValueError(f"Não foi possível carregar a imagem: {image_path}")
            
            if len(image.shape) == 2:
                image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
            elif len(image.shape) == 3 and image.shape[2] == 4:
                image = cv2.cvtColor(image, cv2.COLOR_BGRA2RGB)
            elif len(image.shape) == 3 and image.shape[2] == 3:
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        else:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        image = np.ascontiguousarray(image, dtype=np.uint8)
        return image
    
    def _apply_custom_filters(self, image: np.ndarray) -> np.ndarray:
        """Aplica filtros customizados baseado na configuração."""
        original_image = image.copy()  # Backup em caso de erro
        
        try:
            # 1. CLAHE (se habilitado)
            if hasattr(self.config, 'USE_CLAHE') and self.config.USE_CLAHE:
                print("[DEBUG] Aplicando CLAHE")
                image = self.image_filters.clahe(
                    image,
                    clip_limit=getattr(self.config, 'CLAHE_CLIP_LIMIT', 3.0),
                    tile_grid_size=getattr(self.config, 'CLAHE_TILE_GRID_SIZE', (8, 8))
                )
                print("[DEBUG] CLAHE aplicado com sucesso")
            
            # 2. Equalização (se habilitado)
            if hasattr(self.config, 'USE_EQUALIZE') and self.config.USE_EQUALIZE:
                print("[DEBUG] Aplicando Equalização")
                image = self.image_filters.equalize(image)
                print("[DEBUG] Equalização aplicada com sucesso")
            
            # 3. Sharpening (se habilitado)
            if hasattr(self.config, 'USE_SHARPEN') and self.config.USE_SHARPEN:
                print("[DEBUG] Aplicando Sharpen")
                image = self.image_filters.sharpen(
                    image,
                    strength=getattr(self.config, 'SHARPEN_STRENGTH', 1.2),
                    kernel_type=getattr(self.config, 'SHARPEN_KERNEL_TYPE', 'laplacian')
                )
                print("[DEBUG] Sharpen aplicado com sucesso")
            
            # 4. Square Padding (se habilitado)
            if hasattr(self.config, 'USE_SQUARE_PADDING') and self.config.USE_SQUARE_PADDING:
                print("[DEBUG] Aplicando Square Padding")
                image_size = getattr(self.config, 'IMAGE_SIZE', 224)
                padding_color = getattr(self.config, 'SQUARE_PADDING_COLOR', (0, 0, 0))
                image = self.square_padding.apply_padding(
                    image,
                    target_size=(image_size, image_size),
                    padding_color=padding_color
                )
                print("[DEBUG] Square Padding aplicado com sucesso")
                
            # 5. Sato Filter (se habilitado)
            if hasattr(self.config, 'USE_SATO_FILTER') and self.config.USE_SATO_FILTER:
                print("[DEBUG] Aplicando Sato Filter")
                sato_result = self.image_filters.sato_filter(image)
                # Normaliza para 0-255 e converte para uint8
                sato_norm = cv2.normalize(sato_result, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
                # Inverte para fundo branco e fissura preta
                sato_inv = cv2.bitwise_not(sato_norm)
                # Se for imagem 2D, converte para 3 canais
                if len(sato_inv.shape) == 2:
                    sato_inv = cv2.cvtColor(sato_inv, cv2.COLOR_GRAY2RGB)
                image = sato_inv
                print("[DEBUG] Sato Filter aplicado e cores invertidas com sucesso")


        except Exception as e:
            print(f"[ERRO] Falha ao aplicar filtros customizados: {e}")
            print("[DEBUG] Retornando imagem original devido ao erro")
            return original_image
        
        return image
    
    def _create_fallback_image(self) -> np.ndarray:
        """Cria uma imagem de fallback quando há erro no carregamento."""
        image_size = getattr(self.config, 'IMAGE_SIZE', 224) if self.config else 224
        return np.zeros((image_size, image_size, 3), dtype=np.uint8)
    
    def get_class_weights(self) -> torch.Tensor:
        """Calcula pesos das classes para lidar com desbalanceamento."""
        total_samples = len(self.labels)
        weights = []
        
        for class_idx in range(self.num_classes):
            class_count = self.class_counts[class_idx]
            weight = total_samples / (self.num_classes * class_count)
            weights.append(weight)
        
        return torch.tensor(weights, dtype=torch.float32)


def create_basic_transforms(image_size: int = 224) -> A.Compose:
    """Cria transformações básicas que funcionam para qualquer modelo."""
    transforms = [
        A.Resize(image_size, image_size),
        A.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225],
            max_pixel_value=255.0
        ),
        ToTensorV2()
    ]
    
    return A.Compose(transforms)


def create_basic_dataloaders(train_dataset: Dataset, 
                            val_dataset: Dataset, 
                            test_dataset: Dataset,
                            batch_size: int = 16,
                            num_workers: int = 4) -> Tuple[DataLoader, DataLoader, DataLoader]:
    """Cria DataLoaders básicos."""
    train_loader = DataLoader(
        train_dataset,
        batch_size=batch_size,
        shuffle=True,
        num_workers=num_workers,
        pin_memory=True,
        drop_last=True
    )
    
    val_loader = DataLoader(
        val_dataset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=num_workers,
        pin_memory=True,
        drop_last=False
    )
    
    test_loader = DataLoader(
        test_dataset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=num_workers,
        pin_memory=True,
        drop_last=False
    )
    
    return train_loader, val_loader, test_loader


def process_and_save_images(
    input_root: str,
    output_root: str,
    config: Any,
    image_size: int = 224,
    allowed_subfolders: List[str] = None
):
    """Processa e salva imagens com filtros aplicados"""
    if allowed_subfolders is None:
        allowed_subfolders = ['retracao', 'termicas']
    
    # Inicializar filtros customizados
    print("[DEBUG] Inicializando filtros para processamento em lote...")
    filters = ImageFilters()
    padding = SquarePadding()
    print("[DEBUG] Filtros inicializados para processamento em lote")
    
    for subfolder in allowed_subfolders:
        input_folder = os.path.join(input_root, subfolder)
        output_folder = os.path.join(output_root, subfolder)
        
        if not os.path.isdir(input_folder):
            print(f"Pasta não encontrada: {input_folder}")
            continue
            
        print(f"\nProcessando pasta: {subfolder}")
        print(f"   Input: {input_folder}")
        print(f"   Output: {output_folder}")
        
        os.makedirs(output_folder, exist_ok=True)
        
        # Remover arquivos existentes na pasta de saída
        existing_files = glob.glob(os.path.join(output_folder, '*'))
        if existing_files:
            print(f"Removendo {len(existing_files)} arquivos existentes...")
            for file in existing_files:
                try:
                    os.remove(file)
                except Exception as e:
                    print(f"   Erro ao remover {file}: {e}")
        
        # Encontrar todas as imagens
        image_extensions = ['*.jpg', '*.jpeg', '*.png', '*.bmp', '*.tiff', '*.tif']
        image_paths = []
        for ext in image_extensions:
            image_paths.extend(glob.glob(os.path.join(input_folder, ext)))
            image_paths.extend(glob.glob(os.path.join(input_folder, ext.upper())))
        
        if not image_paths:
            print(f"   Nenhuma imagem encontrada em {input_folder}")
            continue
            
        print(f"   Encontradas {len(image_paths)} imagens para processar")
        
        # Processar cada imagem
        processed_count = 0
        error_count = 0
        
        for i, img_path in enumerate(image_paths, 1):
            try:
                print(f"   [{i}/{len(image_paths)}] Processando: {os.path.basename(img_path)}")
                
                # Carregar imagem
                image = cv2.imread(img_path, cv2.IMREAD_COLOR)
                if image is None:
                    print(f"      Não foi possível carregar a imagem")
                    error_count += 1
                    continue
                    
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                
                # Aplicar filtros customizados baseado na configuração
                print(f"      Aplicando filtros customizados...")
                
                # CLAHE
                if hasattr(config, 'USE_CLAHE') and config.USE_CLAHE:
                    print(f"         CLAHE")
                    image = filters.clahe(
                        image,
                        clip_limit=getattr(config, 'CLAHE_CLIP_LIMIT', 3.0),
                        tile_grid_size=getattr(config, 'CLAHE_TILE_GRID_SIZE', (8, 8))
                    )
                
                # Equalização
                if hasattr(config, 'USE_EQUALIZE') and config.USE_EQUALIZE:
                    print(f"         Equalização")
                    image = filters.equalize(image)
                
                # Sharpen
                if hasattr(config, 'USE_SHARPEN') and config.USE_SHARPEN:
                    print(f"         Sharpen")
                    image = filters.sharpen(
                        image,
                        strength=getattr(config, 'SHARPEN_STRENGTH', 1.2),
                        kernel_type=getattr(config, 'SHARPEN_KERNEL_TYPE', 'laplacian')
                    )
                
                # Square Padding
                if hasattr(config, 'USE_SQUARE_PADDING') and config.USE_SQUARE_PADDING:
                    print(f"         Square Padding")
                    padding_color = getattr(config, 'SQUARE_PADDING_COLOR', (0, 0, 0))
                # Sato Filter
                if hasattr(config, 'USE_SATO_FILTER') and config.USE_SATO_FILTER:
                    print(f"         Sato Filter")
                    sato_result = filters.sato_filter(image)
                    sato_norm = cv2.normalize(sato_result, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
                    sato_inv = cv2.bitwise_not(sato_norm)
                    if len(sato_inv.shape) == 2:
                        sato_inv = cv2.cvtColor(sato_inv, cv2.COLOR_GRAY2RGB)
                    image = sato_inv
                
                
                # Salvar imagem processada
                image = cv2.bitwise_not(image)
                filename = os.path.basename(img_path)
                output_path = os.path.join(output_folder, filename)
                
                success = cv2.imwrite(output_path, image)
                if success:
                    print(f"      Salva em: {output_path}")
                    processed_count += 1
                else:
                    print(f"      Erro ao salvar: {output_path}")
                    error_count += 1
                    
            except Exception as e:
                print(f"      Erro ao processar: {e}")
                error_count += 1
        
        print(f"   Resumo da pasta {subfolder}:")
        print(f"      Processadas com sucesso: {processed_count}")
        print(f"      Erros: {error_count}")


# Exemplo de uso e teste
if __name__ == "__main__":
    class TestConfig:
        USE_CLAHE = True
        CLAHE_CLIP_LIMIT = 3.0
        CLAHE_TILE_GRID_SIZE = (8, 8)
        USE_EQUALIZE = False
        USE_SHARPEN = True
        SHARPEN_STRENGTH = 1.2
        SHARPEN_KERNEL_TYPE = 'laplacian'
        USE_SQUARE_PADDING = True
        IMAGE_SIZE = 224
        SQUARE_PADDING_COLOR = (0, 0, 0)
        USE_SATO_FILTER = True
    
    config = TestConfig()
    input_root = "../data/raw"
    output_root = "../data/results_with_sato"
    
    print("\nINICIANDO PROCESSAMENTO DE IMAGENS")
    print("=" * 60)
    
    # Executar processamento
    process_and_save_images(
        input_root=input_root,
        output_root=output_root,
        config=config,
        image_size=config.IMAGE_SIZE
    )
    
    print(f"\nPROCESSAMENTO CONCLUÍDO!")
    print("=" * 60)