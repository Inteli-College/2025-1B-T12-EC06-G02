from ultralytics import YOLO
from pathlib import Path
from PIL import Image
import requests
import uuid
from modules.inference import classify_for_frontend, classify_grupos

def train(model_path='yolov8n.pt', data_path='data-v1/data.yaml', epochs=50, imgsz=640, batch=16):
    model = YOLO(model_path)
    model.train(data=data_path, epochs=epochs, imgsz=imgsz, batch=batch)
    print("Treinamento concluído!")

def detect_and_crop(peso_modelo, pasta_imagens, pasta_saida='crops', conf_thresh=0.3, iou_thresh=0.0, exibir=False):
    model = YOLO(peso_modelo)
    test_images_dir = Path(pasta_imagens)
    output_crops_dir = Path(pasta_saida)
    output_crops_dir.mkdir(parents=True, exist_ok=True)

    cropped_files = []

    for image_file in test_images_dir.glob('*.jpg'):
        print(f'Processando {image_file.name}...')

        results = model.predict(source=str(image_file), save=True, conf=conf_thresh, iou=iou_thresh)

        if exibir:
            results[0].show()

        boxes = results[0].boxes
        print(f'Detectado {len(boxes)} objeto(s)')

        image = Image.open(image_file).convert("RGB")

        if boxes is not None:
            for i, box in enumerate(boxes.xyxy):
                x1, y1, x2, y2 = map(int, box.tolist())
                print(f'Objeto {i+1}: x1={x1}, y1={y1}, x2={x2}, y2={y2}')
                cropped = image.crop((x1, y1, x2, y2))
                crop_filename = output_crops_dir / f"{image_file.stem}_obj{i+1}.jpg"
                cropped.save(crop_filename)
                cropped_files.append(str(crop_filename))
                print(f'Recorte salvo em: {crop_filename}')

    return cropped_files

def send_to_classifier(crops):
    # Monta a estrutura esperada com ID e previewUrl
    input_data = [{"id": str(uuid.uuid4()), "previewUrl": path} for path in crops]
    
    # Classifica com a função correta
    results = classify_for_frontend(input_data)

    # Exibe os resultados
    for result in results:
        print(f"Imagem: {result['previewUrl']} - Classe: {result['prev']} - Confiança: {result['confidence']:.2f}%")

# ------------------------------------------
# Execução principal
# ------------------------------------------

# Etapa 1: Treinar o modelo (caso necessário)
train(
    model_path='yolov8n.pt',
    data_path='yolo/data-v1/data.yaml',  # Corrija este caminho conforme a localização real do seu data.yaml
    epochs=50,
    imgsz=640,
    batch=16
)

# Etapa 2: Detectar e recortar objetos em imagens de teste
recortes = detect_and_crop(
    peso_modelo='../../../../runs/detect/train/weights/best.pt',
    pasta_imagens='data-v1/test/images',
    pasta_saida='crops',
    conf_thresh=0.3,
    iou_thresh=0.0,
    exibir=False
)

# Etapa 3: Enviar recortes para classificador
send_to_classifier(recortes)