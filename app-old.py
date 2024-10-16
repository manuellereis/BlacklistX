import cv2
import numpy as np
import face_recognition

# Carregar a imagem de referência
known_image = face_recognition.load_image_file("sua_imagem2.jpg")
known_encoding = face_recognition.face_encodings(known_image)[0]

# Iniciar a captura de vídeo
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Erro ao acessar a câmera")
    exit()

print("Pressione 'q' para sair")

# Defina um limite de distância para a comparação (quanto menor, mais estrita a correspondência)
threshold = 0.6

while True:
    ret, frame = cap.read()
    if not ret:
        print("Não foi possível ler o frame")
        break

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(frame_rgb)
    face_encodings = face_recognition.face_encodings(frame_rgb, face_locations)

    for (face_encoding, face_location) in zip(face_encodings, face_locations):
        # Calcular a distância entre o rosto detectado e o rosto conhecido
        face_distance = face_recognition.face_distance([known_encoding], face_encoding)
        is_match = face_distance < threshold

        if is_match[0]:  # Se a distância for menor que o threshold, reconhecido
            name = "Reconhecido"
            color = (0, 255, 0)  # Verde
        else:
            name = "Desconhecido"
            color = (0, 0, 255)  # Vermelho

        (top, right, bottom, left) = face_location
        cv2.rectangle(frame, (left, top), (right, bottom), color, 2)  # Corrigido aqui
        cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, color, 2)

    cv2.imshow("Detecção de Faces em Tempo Real", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
