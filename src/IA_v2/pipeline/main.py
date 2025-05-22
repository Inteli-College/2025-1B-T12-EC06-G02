# python_pure.py
"""
Sistema de processamento de imagens usando APENAS Python puro
SEM OpenCV, SEM NumPy, SEM dependências externas
Funciona em qualquer Python 3.6+
"""

import random
import math
from typing import List, Tuple


class PureImage:
    """Representa uma imagem usando apenas listas Python"""
    
    def __init__(self, data: List[List[List[int]]], height: int, width: int):
        """
        data: [altura][largura][canal] onde canal = [R, G, B]
        """
        self.data = data
        self.height = height
        self.width = width
        self.channels = 3
    
    @classmethod
    def create_random(cls, height: int, width: int, min_val: int = 0, max_val: int = 255):
        """Cria imagem aleatória"""
        data = []
        for h in range(height):
            row = []
            for w in range(width):
                pixel = [
                    random.randint(min_val, max_val),  # R
                    random.randint(min_val, max_val),  # G
                    random.randint(min_val, max_val)   # B
                ]
                row.append(pixel)
            data.append(row)
        
        return cls(data, height, width)
    
    def get_pixel(self, h: int, w: int) -> List[int]:
        """Obtém pixel em posição específica"""
        if 0 <= h < self.height and 0 <= w < self.width:
            return self.data[h][w][:]
        else:
            return [0, 0, 0]  # Pixel preto para fora dos limites
    
    def set_pixel(self, h: int, w: int, pixel: List[int]):
        """Define pixel em posição específica"""
        if 0 <= h < self.height and 0 <= w < self.width:
            self.data[h][w] = [max(0, min(255, int(p))) for p in pixel]
    
    def to_grayscale(self):
        """Converte para escala de cinza"""
        gray_data = []
        for h in range(self.height):
            row = []
            for w in range(self.width):
                r, g, b = self.data[h][w]
                # Fórmula padrão para escala de cinza
                gray = int(0.299 * r + 0.587 * g + 0.114 * b)
                row.append([gray, gray, gray])
            gray_data.append(row)
        
        return PureImage(gray_data, self.height, self.width)
    
    def copy(self):
        """Cria cópia da imagem"""
        new_data = []
        for h in range(self.height):
            new_row = []
            for w in range(self.width):
                new_row.append(self.data[h][w][:])
            new_data.append(new_row)
        
        return PureImage(new_data, self.height, self.width)
    
    def flatten(self) -> List[int]:
        """Converte imagem em lista plana"""
        flat = []
        for h in range(self.height):
            for w in range(self.width):
                flat.extend(self.data[h][w])
        return flat


class PureFilter:
    """Classe base para filtros em Python puro"""
    
    def apply(self, image: PureImage) -> PureImage:
        """Aplica filtro à imagem"""
        raise NotImplementedError


class PureMedianFilter(PureFilter):
    """Filtro mediano em Python puro"""
    
    def __init__(self, kernel_size: int = 3):
        self.kernel_size = kernel_size
        self.offset = kernel_size // 2
    
    def apply(self, image: PureImage) -> PureImage:
        """Aplica filtro mediano"""
        result = image.copy()
        
        for h in range(image.height):
            for w in range(image.width):
                # Coletar pixels da vizinhança
                neighborhood = []
                
                for kh in range(-self.offset, self.offset + 1):
                    for kw in range(-self.offset, self.offset + 1):
                        nh, nw = h + kh, w + kw
                        pixel = image.get_pixel(nh, nw)
                        neighborhood.append(pixel)
                
                # Calcular mediana para cada canal
                median_pixel = []
                for channel in range(3):
                    channel_values = [p[channel] for p in neighborhood]
                    channel_values.sort()
                    median = channel_values[len(channel_values) // 2]
                    median_pixel.append(median)
                
                result.set_pixel(h, w, median_pixel)
        
        return result


class PureContrastFilter(PureFilter):
    """Ajuste de contraste em Python puro"""
    
    def __init__(self, factor: float = 1.2):
        self.factor = factor
    
    def apply(self, image: PureImage) -> PureImage:
        """Aplica ajuste de contraste"""
        result = image.copy()
        
        for h in range(image.height):
            for w in range(image.width):
                pixel = image.get_pixel(h, w)
                new_pixel = []
                
                for channel_value in pixel:
                    # Contraste: (valor - 128) * fator + 128
                    new_value = (channel_value - 128) * self.factor + 128
                    new_value = max(0, min(255, int(new_value)))
                    new_pixel.append(new_value)
                
                result.set_pixel(h, w, new_pixel)
        
        return result


class PureSharpenFilter(PureFilter):
    """Filtro de nitidez em Python puro"""
    
    def __init__(self, strength: float = 0.5):
        self.strength = strength
    
    def apply(self, image: PureImage) -> PureImage:
        """Aplica filtro de nitidez usando kernel simples"""
        result = image.copy()
        
        # Kernel de sharpening simples
        kernel = [
            [-1, -1, -1],
            [-1,  9, -1],
            [-1, -1, -1]
        ]
        
        for h in range(1, image.height - 1):
            for w in range(1, image.width - 1):
                new_pixel = [0, 0, 0]
                
                # Aplicar kernel
                for kh in range(-1, 2):
                    for kw in range(-1, 2):
                        nh, nw = h + kh, w + kw
                        pixel = image.get_pixel(nh, nw)
                        kernel_value = kernel[kh + 1][kw + 1]
                        
                        for channel in range(3):
                            new_pixel[channel] += pixel[channel] * kernel_value
                
                # Aplicar força do filtro
                original_pixel = image.get_pixel(h, w)
                final_pixel = []
                
                for channel in range(3):
                    enhanced = new_pixel[channel] * self.strength / 8
                    final_value = original_pixel[channel] + enhanced
                    final_value = max(0, min(255, int(final_value)))
                    final_pixel.append(final_value)
                
                result.set_pixel(h, w, final_pixel)
        
        return result


class PureHistogramEqualizer(PureFilter):
    """Equalização de histograma em Python puro"""
    
    def apply(self, image: PureImage) -> PureImage:
        """Aplica equalização de histograma"""
        # Converter para escala de cinza primeiro
        gray_image = image.to_grayscale()
        
        # Calcular histograma
        histogram = [0] * 256
        total_pixels = gray_image.height * gray_image.width
        
        for h in range(gray_image.height):
            for w in range(gray_image.width):
                gray_value = gray_image.get_pixel(h, w)[0]  # Todos os canais são iguais
                histogram[gray_value] += 1
        
        # Calcular CDF (Cumulative Distribution Function)
        cdf = [0] * 256
        cdf[0] = histogram[0]
        for i in range(1, 256):
            cdf[i] = cdf[i-1] + histogram[i]
        
        # Normalizar CDF
        cdf_min = min(cdf[i] for i in range(256) if cdf[i] > 0)
        lookup_table = []
        
        for i in range(256):
            equalized_value = int(((cdf[i] - cdf_min) / (total_pixels - cdf_min)) * 255)
            lookup_table.append(max(0, min(255, equalized_value)))
        
        # Aplicar equalização
        result = image.copy()
        for h in range(image.height):
            for w in range(image.width):
                original_pixel = image.get_pixel(h, w)
                
                # Calcular luminância
                luminance = int(0.299 * original_pixel[0] + 
                              0.587 * original_pixel[1] + 
                              0.114 * original_pixel[2])
                
                # Equalizar luminância
                new_luminance = lookup_table[luminance]
                
                # Ajustar todos os canais proporcionalmente
                if luminance > 0:
                    factor = new_luminance / luminance
                    new_pixel = [
                        max(0, min(255, int(original_pixel[0] * factor))),
                        max(0, min(255, int(original_pixel[1] * factor))),
                        max(0, min(255, int(original_pixel[2] * factor)))
                    ]
                else:
                    new_pixel = [new_luminance, new_luminance, new_luminance]
                
                result.set_pixel(h, w, new_pixel)
        
        return result


class PureClassifier:
    """Classificador simples em Python puro"""
    
    def __init__(self):
        self.class_centers = {}
        self.classes = []
    
    def fit(self, X: List[List[int]], y: List[int]):
        """Treina o classificador"""
        print(f"Treinando com {len(X)} amostras...")
        
        # Encontrar classes únicas
        self.classes = list(set(y))
        print(f"Classes encontradas: {self.classes}")
        
        # Calcular centro de cada classe
        for class_label in self.classes:
            class_samples = [X[i] for i in range(len(X)) if y[i] == class_label]
            
            if class_samples:
                # Calcular média (centro)
                feature_size = len(class_samples[0])
                center = []
                
                for feature_idx in range(feature_size):
                    feature_sum = sum(sample[feature_idx] for sample in class_samples)
                    feature_avg = feature_sum / len(class_samples)
                    center.append(feature_avg)
                
                self.class_centers[class_label] = center
                print(f"Classe {class_label}: {len(class_samples)} amostras")
        
        print("Treinamento concluído!")
    
    def predict(self, X: List[List[int]]) -> List[int]:
        """Faz predições"""
        predictions = []
        
        for sample in X:
            best_class = self.classes[0]
            best_distance = float('inf')
            
            # Calcular distância para cada centro
            for class_label, center in self.class_centers.items():
                distance = 0
                for i in range(len(sample)):
                    diff = sample[i] - center[i]
                    distance += diff * diff
                distance = math.sqrt(distance)
                
                if distance < best_distance:
                    best_distance = distance
                    best_class = class_label
            
            predictions.append(best_class)
        
        return predictions
    
    def score(self, X: List[List[int]], y: List[int]) -> float:
        """Calcula accuracy"""
        predictions = self.predict(X)
        correct = sum(1 for i in range(len(y)) if predictions[i] == y[i])
        return correct / len(y)


class PurePipeline:
    """Pipeline completa em Python puro"""
    
    def __init__(self, target_size: Tuple[int, int] = (16, 16)):
        self.filters = []
        self.target_size = target_size
        self.classifier = PureClassifier()
    
    def add_filter(self, filter_obj: PureFilter):
        """Adiciona filtro à pipeline"""
        self.filters.append(filter_obj)
        return self
    
    def resize_image(self, image: PureImage, new_height: int, new_width: int) -> PureImage:
        """Redimensiona imagem usando interpolação simples"""
        if image.height == new_height and image.width == new_width:
            return image.copy()
        
        result_data = []
        
        for h in range(new_height):
            row = []
            for w in range(new_width):
                # Interpolação nearest neighbor simples
                orig_h = int(h * image.height / new_height)
                orig_w = int(w * image.width / new_width)
                
                orig_h = max(0, min(image.height - 1, orig_h))
                orig_w = max(0, min(image.width - 1, orig_w))
                
                pixel = image.get_pixel(orig_h, orig_w)
                row.append(pixel)
            result_data.append(row)
        
        return PureImage(result_data, new_height, new_width)
    
    def preprocess(self, images: List[PureImage]) -> List[List[int]]:
        """Pré-processa lista de imagens"""
        print(f"Pré-processando {len(images)} imagens...")
        
        processed_features = []
        
        for i, image in enumerate(images):
            if (i + 1) % 5 == 0:
                print(f"  Processando imagem {i + 1}/{len(images)}")
            
            # Aplicar filtros
            processed_image = image
            for filter_obj in self.filters:
                processed_image = filter_obj.apply(processed_image)
            
            # Redimensionar
            if (processed_image.height, processed_image.width) != self.target_size:
                processed_image = self.resize_image(
                    processed_image, 
                    self.target_size[0], 
                    self.target_size[1]
                )
            
            # Achatar
            features = processed_image.flatten()
            processed_features.append(features)
        
        print("Pré-processamento concluído!")
        return processed_features
    
    def fit(self, images: List[PureImage], labels: List[int]):
        """Treina a pipeline"""
        print("=== INICIANDO TREINAMENTO ===")
        features = self.preprocess(images)
        self.classifier.fit(features, labels)
        print("=== TREINAMENTO CONCLUÍDO ===")
    
    def predict(self, images: List[PureImage]) -> List[int]:
        """Faz predições"""
        features = self.preprocess(images)
        return self.classifier.predict(features)
    
    def score(self, images: List[PureImage], labels: List[int]) -> float:
        """Calcula accuracy"""
        features = self.preprocess(images)
        return self.classifier.score(features, labels)


def create_pure_dataset() -> Tuple[List[PureImage], List[int]]:
    """Cria dataset de teste em Python puro"""
    print("Criando dataset de teste...")
    
    random.seed(42)
    
    images = []
    labels = []
    
    # 20 imagens pequenas para ser rápido
    for i in range(20):
        if i % 2 == 0:
            # Classe 0 - imagens mais escuras
            img = PureImage.create_random(12, 12, min_val=0, max_val=120)
            label = 0
        else:
            # Classe 1 - imagens mais claras
            img = PureImage.create_random(12, 12, min_val=130, max_val=255)
            label = 1
        
        images.append(img)
        labels.append(label)
    
    print(f"Dataset criado: {len(images)} imagens")
    return images, labels


def test_pure_system():
    """Teste completo do sistema em Python puro"""
    print("🐍 SISTEMA EM PYTHON PURO")
    print("SEM dependências externas")
    print("=" * 35)
    
    try:
        # 1. Criar dados
        print("\n1. Criando dados...")
        images, labels = create_pure_dataset()
        print(f"   ✅ {len(images)} imagens criadas")
        print(f"   ✅ Tamanho: {images[0].height}x{images[0].width}")
        print(f"   ✅ Classes: {list(set(labels))}")
        
        # 2. Dividir dados
        print("\n2. Dividindo dados...")
        split_idx = int(len(images) * 0.7)
        
        train_images = images[:split_idx]
        train_labels = labels[:split_idx]
        test_images = images[split_idx:]
        test_labels = labels[split_idx:]
        
        print(f"   ✅ Train: {len(train_images)}, Test: {len(test_images)}")
        
        # 3. Criar pipeline
        print("\n3. Criando pipeline...")
        pipeline = PurePipeline(target_size=(10, 10))
        pipeline.add_filter(PureContrastFilter(factor=1.3))
        pipeline.add_filter(PureMedianFilter(kernel_size=3))
        
        print(f"   ✅ Pipeline com {len(pipeline.filters)} filtros")
        
        # 4. Treinar
        print("\n4. Treinando...")
        pipeline.fit(train_images, train_labels)
        
        # 5. Avaliar
        print("\n5. Avaliando...")
        train_score = pipeline.score(train_images, train_labels)
        test_score = pipeline.score(test_images, test_labels)
        
        print(f"   ✅ Score treino: {train_score:.3f}")
        print(f"   ✅ Score teste: {test_score:.3f}")
        
        # 6. Teste de predição
        print("\n6. Testando predições...")
        if test_images:
            predictions = pipeline.predict(test_images[:3])
            real = test_labels[:3]
            print(f"   Predições: {predictions}")
            print(f"   Real:      {real}")
        
        print("\n🎉 SUCESSO ABSOLUTO!")
        print("Sistema funcionando 100% em Python puro!")
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERRO: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("🐍 SISTEMA DE PROCESSAMENTO DE IMAGENS")
    print("100% Python Puro - Zero Dependências")
    print("=" * 50)
    
    success = test_pure_system()
    
    if success:
        print(f"\n🌟 PERFEITO!")
        print(f"Agora você pode:")
        print(f"1. Adaptar create_pure_dataset() para seus dados")
        print(f"2. Adicionar mais filtros")
        print(f"3. Ajustar parâmetros")
        print(f"4. Funciona em QUALQUER Python!")
    else:
        print(f"\nSe ainda deu erro, é algo muito específico")
        print(f"Me mande a mensagem de erro completa")