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
    
    if result is None:
        print(f"Image with ID {face_id} not found")
        return None
    
    image_data = result[0]
    cursor.close()
    conn.close()
    
    return image_data

def load_known_faces_from_db():
    known_encodings = []
    known_names = []
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor.execute("SELECT id_face, name FROM faces")
    rows = cursor.fetchall()
    
    for row in rows:
        face_id = row[0]
        name = row[1]
        image_data = get_image_from_db(face_id)
        if image_data is None:
            continue
        
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

known_encodings, known_names = load_known_faces_from_db()

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Erro ao acessar a câmera")
    exit()

print("Pressione 'q' para sair")

face_recognition_timestamps = {}

while True:
    ret, frame = cap.read()
    if not ret:
        print("Não foi possível ler o frame")
        break

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(frame_rgb)
    face_encodings = face_recognition.face_encodings(frame_rgb, face_locations)

    for (face_encoding, face_location) in zip(face_encodings, face_locations):
        matches = face_recognition.compare_faces(known_encodings, face_encoding)
        name = "Rosto Desconhecido"

        if True in matches:
            first_match_index = matches.index(True)
            name = known_names[first_match_index]
            color = (0, 255, 0)

            # Verificar se o rosto foi reconhecido e manter o tempo
            if name not in face_recognition_timestamps:
                face_recognition_timestamps[name] = time.time()

            # Verificar se passou 2 segundos desde o último reconhecimento
            if time.time() - face_recognition_timestamps[name] >= 2:
                print(f"Rosto reconhecido: {name}")
                ip_camera = "192.168.0.1"  # Substitua com o IP da sua câmera
                register_face_in_db(face_id=first_match_index + 1, ip_camera=ip_camera)
                face_recognition_timestamps[name] = time.time()  # Resetando o timer

        else:
            color = (0, 0, 255)

        (top, right, bottom, left) = face_location
        cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
        cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 255), 2)

    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
