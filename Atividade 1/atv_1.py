import cv2
import numpy as np
from Formularios import * # Fomulario importado, código padrão. Cabecalho e menu pertncem a este código.

def save_image(filename, img, text):
    # Caso o usuario deseje salva a foto da webcam. 
    caminho = "C:/Users/marco/OneDrive/UFCG/Programacao/Ras/Missao/Visao Computacional/Atividade 1"
    cabecalho("Salvar " + text)
    menu(["Sim","Não"])
    save = input("Deseja salvar a " + text + "? ")
    match save:
        case "1":
            # Salvando a foto no caminho especificado.
            cv2.imshow(text, img)
            arquivo = os.path.join(caminho, filename)
            cv2.imwrite(arquivo, img)
            print(f"Imagem salva em: {arquivo}")
        case _:
            # caso nenhuma das funções acima seja digitada.
            print("\033[31mImagem não foi salva.\033[m")

def dimensoes(text,frame):
    # Mostra as dimensões das imagens.
    altura, largura = frame.shape[:2]
    print(f"As dimensões da {text} são:")
    print(f"Altura: {altura} \nLargura: {largura}")
    
def alterar_imagens():
    # Realiza alguns ajustes na imagem.
    try:
        imagem = carregar_imagens(0)
        cv2.imshow("Imagem Original", imagem)
        altura, largura = imagem.shape[:2]
        
        var_a = float(input("Digite o valor de proporção para ampliar: "))
        var_r = float(input("Digite o valor de proporção para redução: "))
        beta = int(input("Digite o valor que irá variar o brilho: "))
        
        ajuste = (int(largura*var_a),int(altura*var_a))
        img_bigger = cv2.resize(imagem,ajuste,interpolation=cv2.INTER_CUBIC)
        cv2.imshow("Imagem Ampliada",img_bigger)
        dimensoes("Imagem Ampliada",img_bigger)
        
        ajuste = (int(largura*var_r),int(altura*var_r))
        img_small = cv2.resize(imagem,ajuste,interpolation=cv2.INTER_CUBIC)
        cv2.imshow("Imagem Reduzida",img_small)
        dimensoes("Imagem Reduzida",img_small)
        
        alpha = 1  # Fator de escala (maior que 1 para aumentar o brilho, menor que 1 para diminuir)
        # Aplicar o ajuste de brilho
        img_brilho = cv2.convertScaleAbs(imagem, alpha=alpha, beta=beta)
        cv2.imshow("Brilho",img_brilho)
        img_escuro = cv2.convertScaleAbs(imagem, alpha=alpha, beta=-beta)
        cv2.imshow("esc",img_escuro)
        
        cv2.waitKey(0)
        cv2.destroyAllWindows() 
        
    except Exception as erro:
    # Evita encerrar o código sempre que aparecer um erro.
        print(erro)

def manipulacao():
    # Realiza alguns ajustes na imagem.
    try:
        imagem = carregar_imagens(0)
        cv2.imshow("Imagem Original", imagem)
        matriz_k = (9,9)
        kernel = np.ones(matriz_k,np.float32)/81
        
        # Blurring por convolução
        convolucao = cv2.filter2D(imagem, -1, kernel)
        cv2.imshow('Blurring por Convolução', convolucao)
        
        # Blurring Regular (Média)
        regular = cv2.blur(imagem, matriz_k)
        cv2.imshow('Blurring Regular', regular)
        
        # Blurring Gaussiano
        gaussiano = cv2.GaussianBlur(imagem, matriz_k, 0)
        cv2.imshow('Blurring Gaussiano', gaussiano)
        
        gray_img = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
        cv2.imshow('Imagem em Grayscale', gray_img)
        # Usando o Regular Thresholding.
        ret,thresh_reg = cv2.threshold(gray_img,127,255,cv2.THRESH_BINARY)
        cv2.imshow('Thresholding Regular', thresh_reg)
        # Usando o Adaptativo Thresholding.
        thresh_adp = cv2.adaptiveThreshold(gray_img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
        cv2.imshow('Thresholding Adaptativo', thresh_adp)
        
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
    except Exception as erro:
    # Evita encerrar o código sempre que aparecer um erro.
        print(erro)
        
def converter_imagens(frame, save):
    # Convertendo imagem em Grayscale.
    gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imshow("Imagem em Grayscale", gray_image)  

    # Convertendo imagem em HSV.
    hsv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    cv2.imshow("Imagem em HSV", hsv_image)  
    
    if save == True:
        dimensoes("Imagem em Grayscale", gray_image)
        dimensoes("Imagem em HSV", hsv_image)
        cv2.waitKey(0)
        save_image("foto_Grayscale.png", gray_image, "Imagem em Grayscale")
        save_image("foto_HSV.png", hsv_image, "Imagem em HSV")
        cv2.destroyAllWindows()
    
def carregar_imagens(op):
    try:
        # Carregando uma imagem na pasta pre-definida.
        pasta = os.path.expanduser("C:/Users/marco/OneDrive/UFCG/Programacao/Ras/Missao/Visao Computacional/Atividade 1")
        nome = input("Digite o nome da imagem, ex: imagem.(png,jpg...): ")
        caminho = os.path.join(pasta,nome)
        imagem = cv2.imread(caminho)
        cv2.imshow("Imagem", imagem)
        dimensoes("Imagem carregada",imagem)
        if op == 1:
            # True é para salvar:
            converter_imagens(imagem, True)
        cv2.waitKey(0)
        cv2.destroyWindow("Imagem")
        return imagem
        
    except Exception as erro:
    # Evita encerrar o código sempre que aparecer um erro.
        print(erro)
        
def carregar_webcam(op):
    # Carrega a imagem da webcam.
    try:
        webcam = cv2.VideoCapture(1)  # Conectar a câmera no python
        
        if webcam.isOpened():  
            sucess, frame = webcam.read() 

        while sucess:
            sucess, frame = webcam.read()
            cv2.imshow("Video", frame) 
            key = cv2.waitKey(5)    
            if key == 27:  # Quando apertar a tecla ESC, ele fecha a janela
                break
            elif op == 1:
                # Enquanto False Imagem da camera normal.
                converter_imagens(frame, False)
                
        dimensoes("imagem da Webcam",frame)
        filename = "foto.png"
        save_image(filename, frame, "imagem da Webcam")
        if op == 1:
            converter_imagens(frame, True)
        
    except Exception as erro:
    # Evita encerrar o código sempre que aparecer um erro.
        print(erro)
    webcam.release()
    cv2.destroyAllWindows()
    
while True:
    limpar_tela()
    cv2.waitKey(100)
    cabecalho("Missão 2 - Atividade 1")
    menu(["Carregar imagens do computador.","Carregar imagenm via webcam.",
          "Converter imagens do computador","Converter imagem da webcam","Realizar Alterações",
          "Manipulação Imagens","Sair"])
    funcao = input("Digite a opção desejada: ")
    limpar_tela()
    match funcao:
        # Utilizando a função case, para acessar o menu.
        case "1":
            cabecalho("Carregar imagens do computador.")
            carregar_imagens(0)     # 0 = Imagem não será convertida.
        case "2":
            cabecalho("Carregar imagens via webcam.")
            carregar_webcam(0)      # 0 = Imagem não será convertida.
        case "3":
            cabecalho("Converter imagens do computador.")
            carregar_imagens(1)     # 1 = Imagem será convertida
        case "4":
            cabecalho("Converter imagens via webcam.")
            carregar_webcam(1)      # 1 = Imagem será convertida
        case "5":
            cabecalho("Realizar alterações.")
            alterar_imagens() 
        case "6":
            cabecalho("Manipulação imagens.")
            manipulacao()
        case "7":
            break
        case _:
            # caso nenhuma das funções acima seja digitada.
            print("\033[31mOpção invalida tente novamente.\033[m")
            
cv2.destroyAllWindows()