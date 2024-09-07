import cv2
import numpy as np
from Formularios import *

def carregar_imagem(text):
    try:
        # Função para carregar imagens.
        pasta = os.path.expanduser(f"C:/Users/marco/OneDrive/UFCG/Programacao/Ras/Missao/Visao Computacional/Atividade 2/Imagens/{text}")
        nome1 = input("Digite o nome da primeira imagem, ex: imagem.(png,jpg...): ")
        nome2 = input("Digite o nome da segunda imagem, ex: imagem.(png,jpg...): ")
        caminho1 = os.path.join(pasta,nome1)
        caminho2 = os.path.join(pasta,nome2)
        imagem1 = cv2.imread(caminho1)
        imagem2 = cv2.imread(caminho2)
        return(imagem1,imagem2)
    except Exception as erro:
        # Evita encerrar o código sempre que aparecer um erro.
        print(erro)

def contorno(thresh,img,op):
    try:
        # procurando contornos
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours_img = []
        # Fazendo um laço para imprimir separado cada contorno.
        for i, cont in enumerate(contours):
            if cv2.contourArea(contours[i]) > 100:
                img_copy = np.zeros_like(img)
                cv2.drawContours(img_copy,contours, i, (255,255,255),2)
                contours_img.append(img_copy)
                #cv2.imshow(f"Contorno{i}",img_copy)
        if op == 0:    
            # Fazendo o retangulo na figura    
            for cont in contours:
                # Pegando a área maior
                if cv2.contourArea(cont) > 13000:
                    x, y, w, h = cv2.boundingRect(cont)
                    cv2.rectangle(img, (x, y), (w-80+x, h-20+y), (0, 255, 0), 2)
                # Pegando a região menor.
                elif cv2.contourArea(cont) > 400 and cv2.contourArea(cont)  < 500:
                    x, y, w, h = cv2.boundingRect(cont)
                    cv2.rectangle(img, (x-60, y-20), (w+70+x, h+10+y), (0, 255, 0), 2)
            cv2.imshow('Carros Detectados', img)
            
        else:
            # Fazendo o retangulo na figura 
            for cont in contours:
                if cv2.contourArea(cont) > 1000:
                    x, y, w, h = cv2.boundingRect(cont)
                    cv2.rectangle(img, (x,y), (w+x , h+y), (0,255,0), 2)
            cv2.imshow(f"Invasor Detectado {op}", img)
        
    except Exception as erro:
        # Evita encerrar o código sempre que aparecer um erro.
        print(erro)
    
def detectar_carro():
    try:
        # Carregando imagem.
        imagem1,img2 = carregar_imagem("Tarefa-01")
        cv2.imshow("Rua normal",imagem1)
        cv2.imshow("Rua movimentada",img2)
        # Aplicando um grayscale.
        imagem1 = cv2.cvtColor(imagem1, cv2.COLOR_BGR2GRAY)
        imagem2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
        # Aplicando o GaussianBlur para mehorar a imagem.
        imagem1 = cv2.GaussianBlur(imagem1, (9, 9),0)
        imagem2 = cv2.GaussianBlur(imagem2, (9, 9),0)
        # Calcular a diferença e Aplicar o threshold.
        diff = cv2.absdiff(imagem1, imagem2)
        ret, thresh = cv2.threshold(diff, 30,255,cv2.THRESH_BINARY)
        # Exibir a diferença
        #cv2.imshow('Diferença', thresh)
        contorno(thresh,img2,0)
        
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
    except Exception as erro:
        # Evita encerrar o código sempre que aparecer um erro.
        print(erro)

def detectar_invasor():
    try:
        # Carregando a imagem.
        imagem = cv2.imread("C:/Users/marco/OneDrive/UFCG/Programacao/Ras/Missao/Visao Computacional/Atividade 2/Imagens/Tarefa-02/porta.jpg")
        img1, img2 = carregar_imagem("Tarefa-02")
        cv2.imshow("Imagem Original",imagem)
        cv2.imshow("Primeiro Invasor",img1)
        cv2.imshow("Segundo Invasor", img2)
        # Aplicando Grayscale.
        imagem = cv2.cvtColor(imagem,cv2.COLOR_BGR2GRAY)
        imagem1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        imagem2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
        # Aplicando o GaussianBlur para melhor a manipulação.
        imagem = cv2.GaussianBlur(imagem, (9,9),0)
        imagem1 = cv2.GaussianBlur(imagem1, (9,9),0)
        imagem2 = cv2.GaussianBlur(imagem2, (9,9),0)
        # Calcular a diferença e Aplicar o threshold.
        diff1 = cv2.absdiff(imagem,imagem1)
        diff2 = cv2.absdiff(imagem,imagem2)
        ret, thresh1 = cv2.threshold(diff1, 23, 255, cv2.THRESH_BINARY)
        ret, thresh2 = cv2.threshold(diff2, 23, 255, cv2.THRESH_BINARY)
        # Aplicando os contornos.
        contorno(thresh1,img1,1)
        contorno(thresh2,img2,2)
                
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
    except Exception as erro:
        # Evita encerrar o código sempre que aparecer um erro.
        print(erro)
        cv2.waitKey(10000)

while True:
    limpar_tela()
    cv2.waitKey(100)
    cabecalho("Missão 2 - Atividade 2")
    menu(["Detectar carro.","Detecta invasor.","Sair"])
    funcao = input("Digite a opção desejada: ")
    limpar_tela()
    match funcao:
        # Utilizando a função case, para acessar o menu.
        case "1":
            cabecalho("Detectar carro.")
            detectar_carro()
        case "2":
            cabecalho("Detectar invasor.")
            detectar_invasor()
        case "3":
            cabecalho("Finlizando programa ...")
            break
        case _:
            # caso nenhuma das funções acima seja digitada.
            print("\033[31mOpção invalida tente novamente.\033[m")
            
cv2.destroyAllWindows()