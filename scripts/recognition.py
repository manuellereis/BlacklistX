import os
from dotenv import load_dotenv
import cv2
import face_recognition
import psycopg2
from io import BytesIO
from PIL import Image
import time

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

def get_image_from_db(face_id: int):
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor.execute("SELECT image FROM faces WHERE id_face = %s", (face_id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result[0] if result else None

def load_known_faces_from_db():
    known_encodings = []
    known_names = []
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor.execute("SELECT id_face, name FROM faces")
    rows = cursor.fetchall()
    for row in rows:
        face_id, name = row
        image_data = get_image_from_db(face_id)
        if image_data:
            known_image = face_recognition.load_image_file(BytesIO(image_data))
            known_encoding = face_recognition.face_encodings(known_image)
            if known_encoding:
                known_encodings.append(known_encoding[0])
                known_names.append(name)
    cursor.close()
    conn.close()
    return known_encodings, known_names

def register_face_in_db(face_id: int, ip_camera: str):
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO registers (id_face, ip_camera) VALUES (%s, %s)", (face_id, ip_camera))
    conn.commit()
    cursor.close()
    conn.close()

print("Carregando faces conhecidas do banco de dados...")
known_encodings, known_names = load_known_faces_from_db()

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Erro ao acessar a câmera")
    exit()

print("Pressione 'q' para sair")
face_recognition_timestamps = {}
frame_skip = 5  # Processar 1 em cada 5 frames
frame_count = 0

while True:
    ret, frame = cap.read()
    if not ret:
        print("Não foi possível ler o frame")
        break

    # Incrementa o contador de frames
    frame_count += 1
    if frame_count % frame_skip != 0:
        cv2.imshow('Reconhecimento Facial', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        continue

    # Reduz o tamanho do frame para melhorar a performance
    small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
    frame_rgb = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

    # Detecta e reconhece faces
    face_locations = face_recognition.face_locations(frame_rgb)
    face_encodings = face_recognition.face_encodings(frame_rgb, face_locations)

    for (face_encoding, face_location) in zip(face_encodings, face_locations):
        matches = face_recognition.compare_faces(known_encodings, face_encoding)
        name = "Rosto Desconhecido"
        color = (0, 0, 255)  

        if True in matches:
            first_match_index = matches.index(True)
            name = known_names[first_match_index]
            color = (0, 255, 0) 

            # Reconhecimento temporal
            current_time = time.time()
            if name not in face_recognition_timestamps or current_time - face_recognition_timestamps[name] >= 2:
                print(f"Rosto reconhecido: {name}")
                ip_camera = "192.168.0.1"
                register_face_in_db(face_id=first_match_index + 1, ip_camera=ip_camera)
                face_recognition_timestamps[name] = current_time

        (top, right, bottom, left) = [int(coord * 2) for coord in face_location]
        cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
        cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 255), 2)

    cv2.imshow('Reconhecimento Facial', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
