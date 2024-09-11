import cv2
import numpy as np
import glob

# Criando termos de parada da calibração: 
# EPS: diferença entre as interações < 0.001 e MAX_ITER: maior interação 30
stop = (cv2.TERM_CRITERIA_EPS + cv2.TermCriteria_MAX_ITER, 30, 0.001)

# Especificando as dimensões da matriz x,y
boardSize = (16,10)

# Criação da matriz do plano para calibração:
# Essa matriz terá 3 dimensoes.
M_obj = np.zeros((boardSize[0]*boardSize[1],3), np.float32)
M_obj[:,:2] = np.mgrid[0:boardSize[0], 0:boardSize[1]].T.reshape(-1,2)

# Arrays para armazenar os pontos do objeto e os pontos da imagem de todas as imagens
objpoints = []  # Pontos 3d no mundo real
imgpoints = []  # Pontos 2d no plano da imagem

# Carregar as imagens de calibração
images = glob.glob("C:/Users/marco/OneDrive/UFCG/Programacao/GitHub/Visao-Computacional/Atividade 3/Imagens/*.jpg")

for image in images:
    print("X")
    print(image)
    img = cv2.imread(image)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Encontrando os contornos do plano:
    ret, corners = cv2.findChessboardCorners(gray, boardSize, None)
    
    # Caso encontre algum cotorno:
    if ret == True:
        print("y")
        objpoints.append(M_obj)
        imgpoints.append(corners)
        
        # Refinando o contorno encontrado:
        corners = cv2.cornerSubPix(gray, corners, (8,8), (-1,-1), stop)
    
        # Desenhando e exibindo os contornos:
        cv2.drawChessboardCorners(img, boardSize, corners, ret)
        cv2.imshow("Imagem", img)
        cv2.waitKey(1000)
        
# Parametros da calibração:
frame = (1440,1080)
ret, cameraMatrix, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, frame, None, None)

print("Camera Calibrada", ret)
print("\nMatriz:\n",cameraMatrix)
print("\nDistorção:\n",dist)


# Salvar os parâmetros de calibração
np.savez('camera_calib.npz', cameraMatrix=cameraMatriz, dist=dist)