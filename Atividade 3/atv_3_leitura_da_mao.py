import cv2
import mediapipe as mp

# Inicializando a captura de vídeo
web_cam = cv2.VideoCapture(0)

# Inicializando o módulo de detecção de mãos do MediaPipe
hand = mp.solutions.hands
Hand = hand.Hands(max_num_hands=2)  # detecta até 2 mãos

mpDraw = mp.solutions.drawing_utils

def verificar_sinal_pare(pontos):
    # Sinal de "pare" - Todos os dedos estendidos
    fingers_comparation = [8, 12, 16, 20]
    return all(pontos[x][1] < pontos[x-2][1] for x in fingers_comparation)

def verificar_sinal_joinha(pontos):
    # Joinha - Apenas o polegar levantado (direita: polegar para cima, esquerda: polegar para baixo)
    return (pontos[4][1] < pontos[3][1] and pontos[4][0] > pontos[2][0])

def verificar_sinal_ok(pontos):
    # OK - Polegar e indicador formam um círculo (a distância entre 4 e 8 é pequena)
    return (abs(pontos[4][0] - pontos[8][0]) < 30 and abs(pontos[4][1] - pontos[8][1]) < 30)

while True:
    ret, img = web_cam.read()
     # Espelhar a imagem horizontalmente
    img = cv2.flip(img, 1)
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = Hand.process(imgRGB)
    handPoints = results.multi_hand_landmarks
    h, w, _ = img.shape
    
    if handPoints:
        for i, points in enumerate(handPoints):
            mpDraw.draw_landmarks(img, points, hand.HAND_CONNECTIONS)
            # Obtém a mão direita ou esquerda
            handedness = results.multi_handedness[i].classification[0].label

            pontos = []
            for id, cord in enumerate(points.landmark):
                cx, cy = int(cord.x * w), int(cord.y * h)
                pontos.append((cx, cy))

            # Verifica sinais para a mão direita e esquerda
            if pontos:
                if verificar_sinal_pare(pontos):
                    cv2.putText(img, f"{handedness} PARE!", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 5)
                elif verificar_sinal_joinha(pontos):
                    cv2.putText(img, f"{handedness} Joinha!", (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 5)
                elif verificar_sinal_ok(pontos):
                    cv2.putText(img, f"{handedness} OK!", (50, 300), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 5)
    
    # Mostrar a imagem com as detecções
    cv2.imshow("Detecção de Mãos", img)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

web_cam.release()
cv2.destroyAllWindows()

    