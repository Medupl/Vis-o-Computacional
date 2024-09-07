import cv2
import numpy as np 

webcam = cv2.VideoCapture(0)

def nothing(x):
    return

def ajuste_cor():
    # Armazenando cor por dicionarios.
    Hue={}
    Hue["min"]=cv2.getTrackbarPos("min Hue",ajuste)
    Hue["max"]=cv2.getTrackbarPos("max Hue",ajuste)
    if Hue["max"]<Hue["min"]:
        cv2.setTrackbarPos("max Hue",ajuste,Hue["min"])
        Hue["max"]=cv2.getTrackbarPos("max Hue",ajuste)
        
    Sat={}
    Sat["min"]=cv2.getTrackbarPos("min Sat.",ajuste)
    Sat["max"]=cv2.getTrackbarPos("max Sat.",ajuste)
    if Sat["max"]<Sat["min"]:
        cv2.setTrackbarPos("max Sat.",ajuste,Sat["min"])
        Sat["max"]=cv2.getTrackbarPos("max Sat.",ajuste)
        
    Value={}
    Value["min"]=cv2.getTrackbarPos("min Value",ajuste)
    Value["max"]=cv2.getTrackbarPos("max Value",ajuste)
    if Value["max"]<Value["min"]:
        cv2.setTrackbarPos("max Value",ajuste,Value["min"])
        Value["max"]=cv2.getTrackbarPos("max Value",ajuste)
        
    return Hue,Sat,Value

def manipular_imagem(frame,hue,sat,value):
    # Transformando a imagem de RGB para HSV.
    img_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # Define os intervalores que irao aparecer na imagem final.
    lowerColor = np.array([hue["min"],sat["min"],value["min"]])
    upperColor = np.array([hue["max"],sat["max"],value["max"]])
    # marcador para saber se pertence ao intervalo
    mascara = cv2.inRange(img_hsv,lowerColor,upperColor)
    resultado = cv2.bitwise_and(frame, frame, mask = mascara)
    # aplicando limiarização.
    cinza = cv2.cvtColor(resultado,cv2.COLOR_BGR2GRAY)
    _,cinza = cv2.threshold(cinza,0,255,cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
    # encontra pontos que circundam regioes conexas.
    contours, hierarchy = cv2.findContours(cinza, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    
    if contours:
        max_area = cv2.contourArea(contours[0])
        id_area = 0
        i = 0
        
        # Procurando o grupo de maior area.
        for cnt in contours:
            if max_area < cv2.contourArea(cnt):
                max_area = cv2.contourArea(cnt)
                id_area = i
            i = i + 1
        cnt_max_area = contours[id_area]
        
        x,y,w,h = cv2.boundingRect(cnt_max_area)
        cv2.rectangle(frame, (x,y), (x+w,y+h), (0,0,255),2)        
    
    return frame, cinza

ajuste = "Controlador de HSV"
cv2.namedWindow(ajuste,cv2.WINDOW_NORMAL)
cv2.createTrackbar("min Hue",ajuste,0,255,nothing)
cv2.createTrackbar("max Hue",ajuste,255,255,nothing)
cv2.createTrackbar("min Sat.",ajuste,0,255,nothing)
cv2.createTrackbar("max Sat.",ajuste,255,255,nothing)
cv2.createTrackbar("min Value",ajuste,0,255,nothing)
cv2.createTrackbar("max Value",ajuste,255,255,nothing)

while(1):
    sucess, frame = webcam.read()
    
    hue,sat,value=ajuste_cor()
    
    frame,cinza=manipular_imagem(frame,hue,sat,value)
    
    cv2.imshow("Webcam",frame)
    cv2.imshow("Webcam Alterada",cinza)
    
    if cv2.waitKey(1) & 0xFF == 27:
        break
    
webcam.release()
cv2.destroyAllWindows()