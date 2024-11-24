import cv2
import face_recognition
import os

# Função para carregar todas as imagens de uma pasta e calcular suas codificações
def load_known_faces(known_faces_dir):
    known_encodings = []
    known_names = []

    for filename in os.listdir(known_faces_dir):
        if filename.endswith(('.jpg', '.jpeg', '.png')):  # Suporte a formatos de imagem
            image_path = os.path.join(known_faces_dir, filename)
            known_image = face_recognition.load_image_file(image_path)
            known_encoding = face_recognition.face_encodings(known_image)
            
            if known_encoding:  # Verifica se a codificação foi encontrada
                known_encodings.append(known_encoding[0])
                known_names.append(os.path.splitext(filename)[0])  # Nome sem extensão

    return known_encodings, known_names

# Diretório com as imagens conhecidas
known_faces_dir = "faces/"  # Substitua pelo caminho da sua pasta
known_encodings, known_names = load_known_faces(known_faces_dir)

# Iniciar a captura de vídeo
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Erro ao acessar a câmera")
    exit()

print("Pressione 'q' para sair")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Não foi possível ler o frame")
        break

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(frame_rgb)
    face_encodings = face_recognition.face_encodings(frame_rgb, face_locations)

    for (face_encoding, face_location) in zip(face_encodings, face_locations):
        # Comparar com todos os rostos conhecidos
        matches = face_recognition.compare_faces(known_encodings, face_encoding)
        name = "Rosto Desconhecido"  # Nome padrão

        # Se houver uma correspondência
        if True in matches:
            first_match_index = matches.index(True)
            name = known_names[first_match_index]
            color = (0, 255, 0)  # Verde para reconhecido
        else:
            color = (0, 0, 255)  # Vermelho para não reconhecido

        (top, right, bottom, left) = face_location
        cv2.rectangle(frame, (left, top), (right, bottom), color, 2)  # Cor do retângulo
        cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 255), 2)

    # Mostrar o frame na janela
    cv2.imshow('frame', frame)

    # Verificar se a tecla 'q' foi pressionada
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar a captura e fechar as janelas
cap.release()
cv2.destroyAllWindows()
