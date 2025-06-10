import os
import cv2

def draw_and_save_masks(
    input_dir,
    output_dir,
    mask_color=(0, 255, 0),
    thickness=2,
    fissure_threshold=30
):
    """
    Aplica máscaras nas imagens das subpastas de input_dir e salva em output_dir, mantendo a estrutura.
    Preenche as fissuras detectadas.
    """
    for subfolder in ["retracao", "termicas"]:
        sub_input = os.path.join(input_dir, subfolder)
        sub_output = os.path.join(output_dir, subfolder)
        os.makedirs(sub_output, exist_ok=True)
        for fname in os.listdir(sub_input):
            if fname.lower().endswith(('.png', '.jpg', '.jpeg')):
                img_path = os.path.join(sub_input, fname)
                img = cv2.imread(img_path)
                if img is None:
                    print(f"Warning: Unable to read image {img_path}. Skipping.")
                    continue
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                _, mask = cv2.threshold(gray, fissure_threshold, 255, cv2.THRESH_BINARY)
                contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                img_masked = img.copy()
                # Preenche os contornos das fissuras
                cv2.drawContours(img_masked, contours, -1, mask_color, thickness=cv2.FILLED)
                out_path = os.path.join(sub_output, fname)
                cv2.imwrite(out_path, img_masked)

if __name__ == "__main__":
    input_dir = "../data/results_with_sato"
    output_dir = "../data/masked_images"
    draw_and_save_masks(input_dir, output_dir)
