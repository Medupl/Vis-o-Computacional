import cv2
import cv2.aruco as aruco
import numpy as np
import glob

# Criando termos de parada da calibração: 
# EPS: diferença entre as interações < 0.001 e MAX_ITER: maior interação 30
stop = (cv2.TERM_CRITERIA_EPS + cv2.TermCriteria_MAX_ITER, 30, 0.001)

# Especificando as dimensões da matriz x,y
boardSize = (11,12)

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
    print(image)
    img = cv2.imread(image)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Encontrando os contornos do plano:
    # ret é tipo bollean, True: caso encontre uma borda.
    ret, corners = cv2.findChessboardCorners(gray, boardSize, None)
    # Caso encontre algum cotorno:
    if ret == True:
        objpoints.append(M_obj)
        imgpoints.append(corners)
        
        # Refinando o contorno encontrado:
        corners_ = cv2.cornerSubPix(gray, corners, (10,10), (-1,-1), stop)
        
        # Desenhando e exibindo os contornos:
        cv2.drawChessboardCorners(img, boardSize, corners, ret)
        cv2.imshow(f"Imagem", img)
        cv2.waitKey(1000)
        
# Parametros da calibração:
frame = (1912,1072)
ret, cameraMatrix, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, frame, None, None)

print("Camera Calibrada", ret)
print("\nMatriz:\n",cameraMatrix)
print("\nDistorção:\n",dist)
print("\nVetor de rotação:\n",rvecs)
print("\nVetor de translação:\n",tvecs)

# Salvar os parâmetros de calibração
np.savez('C:/Users/marco/OneDrive/UFCG/Programacao/GitHub/Visao-Computacional/Atividade 3/Calibracao/camera_calib.npz', 
         cameraMatrix=cameraMatrix, dist=dist)
"""
# Carregar a calibração da câmera
with np.load("C:/Users/marco/OneDrive/UFCG/Programacao/GitHub/Visao-Computacional/Atividade 3/Calibracao/camera_calib.npz") as cal:
    cameraMatrix, dist = [cal[i] for i in ('cameraMatrix', 'dist')]

# Definir o dicionário de marcadores ArUco
aruco_dict = aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)
parameters = aruco.DetectorParameters()  # Correção aqui
parameters.adaptiveThreshConstant = 7
parameters.minMarkerPerimeterRate = 0.03

# Inicializar a captura de vídeo
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    
    if not ret:
        break
    
    # Corrigir distorções da imagem a partir dos paramentros da calibração:
    # roi: retorna a região de interesse, pode ser usado para recortar partes desnecessarias.
    h, w = frame.shape[:2]
    newcameramtx, roi = cv2.getOptimalNewCameraMatrix(cameraMatrix, dist, (w, h), 0, (w, h)) 
    frame = cv2.undistort(frame, cameraMatrix, dist, None, newcameramtx)
    x, y, w, h = roi
    frame = frame[y:y+h, x:x+w]
    cv2.imshow("video",frame)
    # Detectar os marcadores ArUco, usando o dicionario aruco: aruco_dict
    # ids: id dos marcadores ->  rejected: lista dos marcadores que foram rejeitados
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    corners, ids, rejected = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
    print(rejected)
    if np.all(ids is not None): # Verifica todos os ids para encontar algum que não seja nulo.
        # Estimar a pose de cada marcador detectado
        rvecs, tvecs, _ = aruco.estimatePoseSingleMarkers(corners, 0.063, cameraMatrix, dist)
        print("f")
        # Desenhar os marcadores e a pose estimada
        for i in range(len(ids)):

            aruco.drawAxis(frame, cameraMatrix, dist, rvecs[i], tvecs[i], 0.1)
            aruco.drawDetectedMarkers(frame, corners)
            print(f"ID: {ids[i]}, tvec: {tvecs[i].flatten()}, rvec: {rvecs[i].flatten()}")
    # Mostrar a imagem com a pose estimada
    cv2.imshow('Pose Estimation', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

links:
https://github.com/kyle-bersani/opencv-examples
https://www.youtube.com/watch?v=US9p9CL9Ywg
https://www.youtube.com/watch?v=3h7wgR5fYik"""