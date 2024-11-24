import os
from dotenv import load_dotenv
from fastapi import FastAPI, File, Form, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import create_engine, Column, Integer, String, LargeBinary
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")  # Usando variável de ambiente
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class Face(Base):
    __tablename__ = "faces"
    id_face = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    image = Column(LargeBinary)

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_index():
    try:
        with open("2static/index.html", "r") as f:
            html_content = f.read()
        return HTMLResponse(content=html_content)
    except FileNotFoundError:
        return HTMLResponse(content="<h1>Index file not found!</h1>", status_code=404)

@app.post("/upload")
async def upload_image(
    name: str = Form(...),
    image: UploadFile = File(...),
):
    image_content = await image.read()

    db = SessionLocal()
    try:
        new_face = Face(name=name, image=image_content)
        db.add(new_face)
        db.commit()
        db.refresh(new_face)
        return {"message": "Image uploaded successfully", "face_id": new_face.id_face}
    finally:
        db.close()
