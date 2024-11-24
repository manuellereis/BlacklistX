from fastapi import FastAPI, File, Form, UploadFile
from fastapi.responses import HTMLResponse  # Importando HTMLResponse para servir HTML
from fastapi.staticfiles import StaticFiles
from sqlalchemy import create_engine, Column, Integer, String, LargeBinary
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Configuração do banco de dados
DATABASE_URL = "postgresql://postgres:root@localhost:5432/black_listix"
engine = create_engine(DATABASE_URL, echo=True)  # echo=True para mostrar logs de SQL
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# Modelo do banco de dados
class Face(Base):
    __tablename__ = "faces"
    id_face = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    image = Column(LargeBinary)

Base.metadata.create_all(bind=engine)

# Configuração do FastAPI
app = FastAPI()

# Monta o diretório "static" para servir arquivos estáticos (CSS, JS, etc.)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Rota para carregar o index.html como página principal
@app.get("/", response_class=HTMLResponse)
async def read_index():
    try:
        with open("static/index.html", "r") as f:  # Certifique-se que o index.html esteja no diretório correto
            html_content = f.read()
        return HTMLResponse(content=html_content)
    except FileNotFoundError:
        return HTMLResponse(content="<h1>Index file not found!</h1>", status_code=404)

@app.post("/upload")
async def upload_image(
    name: str = Form(...),  # Recebe o nome como dado de formulário
    image: UploadFile = File(...),  # Recebe a imagem como arquivo
):
    # Lê o conteúdo da imagem
    image_content = await image.read()

    # Conexão com o banco de dados
    db = SessionLocal()
    try:
        # Cria uma nova entrada na tabela faces
        new_face = Face(name=name, image=image_content)
        db.add(new_face)
        db.commit()
        db.refresh(new_face)
        return {"message": "Image uploaded successfully", "face_id": new_face.id_face}
    finally:
        db.close()
