import streamlit as st
import cv2
import numpy as np
from PIL import Image
import io

def load_image(uploaded_file):
    if uploaded_file is not None:
        image_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        image = cv2.imdecode(image_bytes, cv2.IMREAD_COLOR)
        return image
    return None

def apply_filter(image, filter_type, params):
    result = image.copy()
    
    if len(result.shape) == 3 and filter_type not in ['inverter', 'sharpen']:
        gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
    else:
        gray = result.copy() if len(result.shape) == 2 else None
    
    if filter_type == 'inverter':
        result = cv2.bitwise_not(result)
    
    elif filter_type == 'blur':
        kernel_size = params.get('kernel_size', 5)
        if kernel_size % 2 == 0:
            kernel_size += 1
        result = cv2.GaussianBlur(result, (kernel_size, kernel_size), 0)
    
    elif filter_type == 'canny':
        threshold1 = params.get('threshold1', 100)
        threshold2 = params.get('threshold2', 200)
        result = cv2.Canny(gray, threshold1, threshold2)
        # Converter para BGR para exibição consistente
        result = cv2.cvtColor(result, cv2.COLOR_GRAY2BGR)
    
    elif filter_type == 'sobel':
        ksize = params.get('ksize', 3)
        sobel_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=ksize)
        sobel_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=ksize)
        abs_sobel_x = cv2.convertScaleAbs(sobel_x)
        abs_sobel_y = cv2.convertScaleAbs(sobel_y)
        result = cv2.addWeighted(abs_sobel_x, 0.5, abs_sobel_y, 0.5, 0)
        result = cv2.cvtColor(result, cv2.COLOR_GRAY2BGR)
    
    elif filter_type == 'threshold':
        threshold_value = params.get('threshold', 127)
        result = cv2.threshold(gray, threshold_value, 255, cv2.THRESH_BINARY)[1]
        result = cv2.cvtColor(result, cv2.COLOR_GRAY2BGR)
    
    elif filter_type == 'adaptive_threshold':
        block_size = params.get('block_size', 11)
        if block_size % 2 == 0:
            block_size += 1
        c_value = params.get('c_value', 2)
        result = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                      cv2.THRESH_BINARY, block_size, c_value)
        result = cv2.cvtColor(result, cv2.COLOR_GRAY2BGR)
    
    elif filter_type == 'sharpen':
        kernel = np.array([[-1, -1, -1],
                          [-1, 9, -1],
                          [-1, -1, -1]])
        result = cv2.filter2D(result, -1, kernel)
    
    elif filter_type == 'laplacian':
        ksize = params.get('ksize', 3)
        result = cv2.Laplacian(gray, cv2.CV_64F, ksize=ksize)
        result = cv2.convertScaleAbs(result)
        result = cv2.cvtColor(result, cv2.COLOR_GRAY2BGR)
    
    elif filter_type == 'morphology':
        op_type = params.get('op_type', 'dilate')
        kernel_size = params.get('kernel_size', 5)
        iterations = params.get('iterations', 1)
        
        kernel = np.ones((kernel_size, kernel_size), np.uint8)
        
        if op_type == 'erode':
            result = cv2.erode(result, kernel, iterations=iterations)
        elif op_type == 'dilate':
            result = cv2.dilate(result, kernel, iterations=iterations)
        elif op_type == 'open':
            result = cv2.morphologyEx(result, cv2.MORPH_OPEN, kernel, iterations=iterations)
        elif op_type == 'close':
            result = cv2.morphologyEx(result, cv2.MORPH_CLOSE, kernel, iterations=iterations)
    
    elif filter_type == 'frangi':
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        sobel_x = cv2.Sobel(blurred, cv2.CV_64F, 1, 0, ksize=3)
        sobel_y = cv2.Sobel(blurred, cv2.CV_64F, 0, 1, ksize=3)
        magnitude = cv2.magnitude(sobel_x, sobel_y)
        result = cv2.normalize(magnitude, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
        result = cv2.cvtColor(result, cv2.COLOR_GRAY2BGR)
    
    elif filter_type == 'clahe':
        clip_limit = params.get('clip_limit', 2.0)
        clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=(8, 8))
        result = clahe.apply(gray)
        result = cv2.cvtColor(result, cv2.COLOR_GRAY2BGR)
    
    elif filter_type == 'equalize':
        result = cv2.equalizeHist(gray)
        result = cv2.cvtColor(result, cv2.COLOR_GRAY2BGR)
        
    return result

def resize_image(image, max_width=250):
    h, w = image.shape[:2]
    aspect_ratio = w / h
    new_width = min(max_width, w)
    new_height = int(new_width / aspect_ratio)
    return cv2.resize(image, (new_width, new_height))

def get_filter_params(filter_type):
    params = {}
    
    if filter_type == 'blur':
        params['kernel_size'] = st.slider("Tamanho do Kernel (Blur)", 1, 31, 5, 2)
    
    elif filter_type == 'canny':
        params['threshold1'] = st.slider("Limiar Inferior (Canny)", 0, 255, 100)
        params['threshold2'] = st.slider("Limiar Superior (Canny)", 0, 255, 200)
    
    elif filter_type == 'sobel':
        params['ksize'] = st.select_slider("Tamanho do Kernel (Sobel)", options=[1, 3, 5, 7])
    
    elif filter_type == 'threshold':
        params['threshold'] = st.slider("Valor do Limiar", 0, 255, 127)
    
    elif filter_type == 'adaptive_threshold':
        params['block_size'] = st.slider("Tamanho do Bloco", 3, 51, 11, 2)
        params['c_value'] = st.slider("Valor C", 0, 20, 2)
    
    elif filter_type == 'laplacian':
        params['ksize'] = st.select_slider("Tamanho do Kernel (Laplacian)", options=[1, 3, 5, 7, 9, 11, 13, 15])
    
    elif filter_type == 'morphology':
        params['op_type'] = st.selectbox("Operação", ['erode', 'dilate', 'open', 'close'])
        params['kernel_size'] = st.slider("Tamanho do Kernel", 1, 15, 5, 2)
        params['iterations'] = st.slider("Iterações", 1, 10, 1)
    
    elif filter_type == 'clahe':
        params['clip_limit'] = st.slider("Limite de Contraste", 0.1, 10.0, 2.0, 0.1)
    
    return params

def main():
    st.set_page_config(page_title="Detector de Fissuras", layout="wide")
    
    st.title("Detector de Fissuras - Aplicação de Filtros Sequenciais")
    
    st.sidebar.header("Carregar Imagem")
    uploaded_file = st.sidebar.file_uploader("Escolha uma imagem", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        original_image = load_image(uploaded_file)
        
        if 'filtered_images' not in st.session_state:
            st.session_state.filtered_images = [original_image]
        
        if 'applied_filters' not in st.session_state:
            st.session_state.applied_filters = ["Original"]
        
        filter_types = [
            "inverter", "blur", "canny", "sobel", "threshold", 
            "adaptive_threshold", "sharpen", "laplacian", 
            "morphology", "frangi", "clahe", "equalize"
        ]
        
        st.sidebar.header("Configuração de Filtros")
        
        selected_filter = st.sidebar.selectbox(
            "Selecione o próximo filtro a aplicar", filter_types
        )
        
        filter_params = get_filter_params(selected_filter)
        
        col1, col2, col3 = st.sidebar.columns(3)
        
        if col1.button("Aplicar Filtro"):
            last_image = st.session_state.filtered_images[-1]
            filtered_image = apply_filter(last_image, selected_filter, filter_params)
            
            if len(st.session_state.filtered_images) >= 8:
                st.warning("Limite de 8 filtros atingido. Remova um filtro ou reinicie.")
            else:
                st.session_state.filtered_images.append(filtered_image)
                st.session_state.applied_filters.append(selected_filter)
        
        if col2.button("Desfazer"):
            if len(st.session_state.filtered_images) > 1:  
                st.session_state.filtered_images.pop()
                st.session_state.applied_filters.pop()
                st.success("Último filtro removido!")
            else:
                st.warning("Não é possível remover a imagem original.")
        
        if col3.button("Reiniciar"):
            st.session_state.filtered_images = [original_image]
            st.session_state.applied_filters = ["Original"]
            st.success("Processamento reiniciado!")
        
        if len(st.session_state.filtered_images) > 0:
            row1_cols = st.columns(4)
            row2_cols = st.columns(4)
            
            columns = row1_cols + row2_cols
            
            for i, (img, filter_name) in enumerate(zip(st.session_state.filtered_images, 
                                                  st.session_state.applied_filters)):
                if i < 8: 

                    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                    img_rgb_resized = resize_image(img_rgb, max_width=250)
                    
                    columns[i].image(
                        img_rgb_resized, 
                        caption=f"Filtro {i+1}: {filter_name}", 
                        width=250  
                    )
                    
                    img_pil = Image.fromarray(img_rgb)
                    buf = io.BytesIO()
                    img_pil.save(buf, format="PNG")
                    columns[i].download_button(
                        label=f"Baixar {i+1}",
                        data=buf.getvalue(),
                        file_name=f"filtro_{i+1}_{filter_name}.png",
                        mime="image/png"
                    )
    else:
        st.info("Por favor, carregue uma imagem para começar.")

if __name__ == "__main__":
    main()