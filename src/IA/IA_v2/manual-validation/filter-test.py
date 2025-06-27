import cv2

def processar_imagem_safe(nome_imagem):
    
    print(f"Carregando: {nome_imagem}")
    
    # Carregar imagem
    img = cv2.imread(nome_imagem)
    if img is None:
        print("Erro ao carregar imagem")
        return
    
    print(f"arregada com sucesso!")
    
    # Converter para cinza
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    print("Convertida para cinza")
    
    # FILTRO 1: Sobel usando método direto do OpenCV
    print("Aplicando Sobel...")
    
    # Usar Sobel direto sem magnitude (evita NumPy)
    sobel_x = cv2.Sobel(gray, cv2.CV_8U, 1, 0, ksize=3)
    sobel_y = cv2.Sobel(gray, cv2.CV_8U, 0, 1, ksize=3)
    
    # Combinar de forma simples
    sobel_result = cv2.addWeighted(sobel_x, 0.5, sobel_y, 0.5, 0)
    
    # Salvar Sobel
    cv2.imwrite("sobel_final.jpg", sobel_result)
    print("Sobel salvo: sobel_final.jpg")
    
    # FILTRO 2: Canny
    print("Aplicando Canny...")
    canny_result = cv2.Canny(gray, 100, 200)
    
    # Salvar Canny
    cv2.imwrite("canny_final.jpg", canny_result)
    print("Canny salvo: canny_final.jpg")
    
    # FILTRO 3: ANN Simulado
    print("Aplicando ANN simulado...")
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, ann_result = cv2.threshold(blur, 127, 255, cv2.THRESH_BINARY)
    
    # Salvar ANN
    cv2.imwrite("ann_final.jpg", ann_result)
    print("ANN salvo: ann_final.jpg")
    
    # Criar comparação simples
    print("Criando comparação...")
    
    # Redimensionar todas para 350x350
    h, w = 350, 350
    orig_small = cv2.resize(gray, (w, h))
    sobel_small = cv2.resize(sobel_result, (w, h))
    canny_small = cv2.resize(canny_result, (w, h))
    ann_small = cv2.resize(ann_result, (w, h))
    
    # Criar linhas horizontais (em vez de grid)
    linha1 = cv2.hconcat([orig_small, sobel_small])
    linha2 = cv2.hconcat([canny_small, ann_small])
    comparison = cv2.vconcat([linha1, linha2])
    
    # Salvar comparação
    cv2.imwrite("comparacao_final.jpg", comparison)
    print("Comparação salva: comparacao_final.jpg")
    
    print("\n🎉 SUCESSO TOTAL! Arquivos criados:")
    print("sobel_final.jpg")
    print("canny_final.jpg") 
    print("ann_final.jpg")
    print("comparacao_final.jpg (4 em 1)")

# Executar
if __name__ == "__main__":
    
    nome = input("Nome da imagem: ").strip()
    
    if nome:
        try:
            processar_imagem_safe(nome)
        except Exception as e:
            print(f"Erro: {e}")
    else:
        print("Nome da imagem não pode estar vazio")
    
    input("\nPressione Enter para sair...")