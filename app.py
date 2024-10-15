# from database import ENGINE

# print(ENGINE)



# Carregue uma imagem e aprenda a reconhecê-la.
imagem_conhecida = face_recognition.load_image_file("sua_imagem.jpg")
face_encoding_conhecida = face_recognition.face_encodings(imagem_conhecida)[0]

# Crie um array para armazenar os dados conhecidos
conhecidos = [face_encoding_conhecida]
nomes_conhecidos = ["Seu Nome"]

# Inicie a captura de vídeo
video_capture = cv2.VideoCapture(0)

while True:
    # Capture um frame do vídeo
    ret, frame = video_capture.read()

    # Converta a imagem de BGR (OpenCV) para RGB (face_recognition)
    rgb_frame = frame[:, :, ::-1]

    # Encontre todas as faces e as codificações no frame atual
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        # Veja se a face corresponde a alguma das faces conhecidas
        matches = face_recognition.compare_faces(conhecidos, face_encoding)
        name = "Desconhecido"

        # Se houver uma correspondência, use o nome correspondente
        if True in matches:
            first_match_index = matches.index(True)
            name = nomes_conhecidos[first_match_index]

        # Desenhe um retângulo em volta da face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Coloque o nome abaixo da face
        cv2.putText(frame, name, (left, bottom + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 255), 2)

    # Mostre o resultado
    cv2.imshow('Reconhecimento Facial', frame)

    # Pressione 'q' para sair
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libere a captura e feche as janelas
video_capture.release()
cv2.destroyAllWindows()
