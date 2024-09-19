import os  # Biblioteca para operações de sistema, como listar arquivos de diretórios
import cv2  # Biblioteca OpenCV para manipulação de imagens e visão computacional
import numpy as np  # Biblioteca para operações matemáticas, especialmente com arrays
import matplotlib.pyplot as plt  # Biblioteca para plotar gráficos e exibir imagens

# Caminho para a pasta onde as imagens estão armazenadas
image_folder_path = 'C:/Users/marco/OneDrive/UFCG/Programacao/GitHub/Visao-Computacional/Atividade 3'

# Lista todos os arquivos no diretório que terminam com '.jpg' (imagens)
image_files = [f for f in os.listdir(image_folder_path) if f.lower().endswith('.jpg')]

# Ordena os arquivos de imagem alfabeticamente
image_files.sort()

# Índice inicial para a primeira imagem a ser mostrada
current_index = 0

# Função para exibir a imagem com indexação baseada no índice passado
def show_image(index):
    # Constrói o caminho completo da imagem usando o diretório e o nome do arquivo
    image_path = os.path.join(image_folder_path, image_files[index])
    
    # Carrega a imagem usando o OpenCV
    image = cv2.imread(image_path)
    
    # Converte a imagem para escala de cinza
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Aplica um filtro de desfoque Gaussiano para suavizar a imagem
    blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0)
    
    # Detecta as bordas usando o algoritmo Canny
    edges = cv2.Canny(blurred_image, 50, 150)
    
    # Encontra os contornos na imagem de bordas
    contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    # Converte a imagem em escala de cinza para BGR (para desenhar contornos coloridos)
    output_image = cv2.cvtColor(gray_image, cv2.COLOR_GRAY2BGR)
    
    # Desenha os contornos encontrados na imagem (cor verde)
    cv2.drawContours(output_image, contours, -1, (0, 255, 0), 1)

    # Mostra a imagem original no lado esquerdo da tela
    plt.subplot(1, 2, 1)
    plt.title('Original')  # Título para a imagem original
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))  # Converte BGR para RGB para exibir corretamente
    plt.axis('off')  # Desativa os eixos da imagem

    # Mostra a imagem com os contornos detectados no lado direito da tela
    plt.subplot(1, 2, 2)
    plt.title('Detectadas')  # Título para a imagem processada
    plt.imshow(cv2.cvtColor(output_image, cv2.COLOR_BGR2RGB))  # Converte BGR para RGB para exibir corretamente
    plt.axis('off')  # Desativa os eixos da imagem

    # Título geral com o número da imagem e o total de imagens
    plt.suptitle(f'Imagem {index + 1} de {len(image_files)}')
    
    # Atualiza o gráfico
    plt.draw()

def on_key(event):
    global current_index
    # Se a tecla 'm' for pressionada, muda para a próxima imagem na lista
    if event.key == 'm':
        current_index = (current_index + 1) % len(image_files)  # Incrementa o índice ciclicamente
        plt.clf()  # Limpa a tela para mostrar a próxima imagem
        show_image(current_index)  # Mostra a próxima imagem

# Cria uma nova figura para exibir as imagens
plt.figure(figsize=(8, 4))

# Exibe a primeira imagem (índice inicial)
show_image(current_index)

# Conecta o evento de teclado à função 'on_key'
plt.gcf().canvas.mpl_connect('key_press_event', on_key)

# Exibe o gráfico e aguarda por eventos de teclado
plt.show()
