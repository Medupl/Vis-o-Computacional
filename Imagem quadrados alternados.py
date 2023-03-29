import cv2
imagem = cv2.imread('ponte.png')
imagem[30:50, :]=(255,0,0) # cria um quadrado da linha 31 a 50, na coluna 0 até o final na cor desejada.
imagem[110:165, 75:130]=(0,0,255)   # cria um quadrado da linha 111 a 165, na coluna 76 a 130 na cor desejada.
imagem[:, 200:220]=(0,255,255)
imagem[300:365,75:150]=(255,255,0)
imagem[60:80,300:450]=(0,0,0)
imagem[150:300,250:350]=(0,255,0)
imagem[250:350,300:400]=(255,255,255)
cv2.line(imagem,(600,360),(400,150),(0,0,255),3)
cv2.rectangle(imagem,(620,300),(580,180),(0,255,0),3)
cv2.rectangle(imagem,(620,170),(580,80),(0,0,255),-1)
for raio in range(0,90,15):
    cv2.circle(imagem,(400,150),raio,(0,0,0))
cv2.imshow("Imagem alterada",imagem)
cv2.imwrite("Imagem saida.jpg",imagem)
cv2.waitKey(0)