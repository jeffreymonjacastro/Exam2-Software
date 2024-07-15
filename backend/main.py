from fastapi import FastAPI, HTTPException, status, Depends
from pydantic import BaseModel
from typing import List
from sqlalchemy import create_engine, Column, Integer, String, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime


app = FastAPI()

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class UsuarioDB(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    numero = Column(String, index=True)
    saldo = Column(Integer, index=True)
    numeros_contacto = Column(JSON)

class Operacion(Base):
    __tablename__ = "operaciones"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    origen = Column(String, index=True)
    destino = Column(String, index=True)
    monto = Column(Integer, index=True)
    fecha = Column(String, index=True)


Base.metadata.create_all(bind=engine)

class Usuario(BaseModel):
    id: int
    numero: str
    saldo: int
    numeros_contacto: List[str]

class Operacion(BaseModel):
    id: int
    origen: str
    destino: str
    monto: int
    fecha: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

route = "/billetera/"

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/usuarios/", response_model=Usuario, status_code=status.HTTP_201_CREATED)
def crear_usuario(usuario: Usuario, db: Session = Depends(get_db)):
    db_usuario = UsuarioDB(
        numero=usuario.numero,
        saldo=usuario.saldo,
        numeros_contacto=usuario.numeros_contacto
    )
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

#contacto?minumero=123
@app.get(route+"contacto")
async def contacto(minumero: str, db: Session = Depends(get_db)):
    user = db.query(Usuario).filter(Usuario.numero == minumero).first()
    if user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"Numeros de contacto de " + user.name: user.numeros_contacto}

#pagar?minumero=123&numerodes=456&monto=100
@app.post(route+"pagar")
async def pagar(minumero: str, numerodes: str, monto: int, db: Session = Depends(get_db)):
    user = db.query(Usuario).filter(Usuario.numero == minumero).first()
    if user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    userdes = db.query(Usuario).filter(Usuario.numero == numerodes).first()
    if userdes is None:
        raise HTTPException(status_code=404, detail="Usuario destino no encontrado")
    if user.saldo < monto:
        raise HTTPException(status_code=400, detail="Saldo insuficiente")
    user.saldo -= monto
    userdes.saldo += monto
    db.add(Operacion(origen=minumero, destino=numerodes, monto=monto, fecha=str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))))
    db.commit()
    return {"message": "Operacion exitosa"}

#historial?minumero=123
@app.get(route+"historial")
async def historial(minumero: str, db: Session = Depends(get_db)):
    user = db.query(Usuario).filter(Usuario.numero == minumero).first()
    if user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {
        "Saldo de " + user.name: user.saldo,
        "Historial de operaciones de " + user.name: user.historialOperaciones}
