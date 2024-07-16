from fastapi import FastAPI, HTTPException, status, Depends
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy import create_engine, Column, Integer, String, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
from datetime import datetime

app = FastAPI()

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class UsuarioDB(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String, index=True)
    numero = Column(String, unique=True, index=True)
    saldo = Column(Integer, index=True)
    numeros_contacto = Column(JSON)
    operaciones = relationship("OperacionDB", back_populates="usuario")

class OperacionDB(Base):
    __tablename__ = "operaciones"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    origen = Column(String, index=True)
    destino = Column(String, index=True)
    monto = Column(Integer, index=True)
    fecha = Column(String, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    usuario = relationship("UsuarioDB", back_populates="operaciones")

Base.metadata.create_all(bind=engine)

class Operacion(BaseModel):
    id: Optional[int] = None
    origen: str
    destino: str
    monto: int
    fecha: str
    usuario_id: int

    class Config:
        orm_mode = True

class Usuario(BaseModel):
    id: Optional[int] = None
    nombre: str
    numero: str
    saldo: int
    numeros_contacto: List[str]
    historialOperaciones: List[Operacion] = []

    class Config:
        from_attributes = True

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/usuarios/", response_model=Usuario, status_code=status.HTTP_201_CREATED)
def crear_usuario(usuario: Usuario, db: Session = Depends(get_db)):
    db_usuario = UsuarioDB(
        nombre=usuario.nombre,
        numero=usuario.numero,
        saldo=usuario.saldo,
        numeros_contacto=usuario.numeros_contacto
    )
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

@app.get("/usuarios/", response_model=List[Usuario])
def get_all_users(db: Session = Depends(get_db)):
    return db.query(UsuarioDB).all()

@app.get("/billetera/contactos")
async def contacto(minumero: str, db: Session = Depends(get_db)):
    user = db.query(UsuarioDB).filter(UsuarioDB.numero == minumero).first()
    if user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    numeros_contacto = user.numeros_contacto

    contactos = {}
    for numero in numeros_contacto:
        contacto_usuario = db.query(UsuarioDB).filter(UsuarioDB.numero == numero).first()
        if contacto_usuario:
            contactos[numero] = contacto_usuario.nombre
        else:
            contactos[numero] = "Nombre no encontrado" 

    return contactos

@app.post("/billetera/pagar")
async def pagar(minumero: str, numerodes: str, monto: int, db: Session = Depends(get_db)):
    user = db.query(UsuarioDB).filter(UsuarioDB.numero == minumero).first()
    if user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    userdes = db.query(UsuarioDB).filter(UsuarioDB.numero == numerodes).first()
    if userdes is None:
        raise HTTPException(status_code=404, detail="Usuario destino no encontrado")
    if user.saldo < monto:
        raise HTTPException(status_code=400, detail="Saldo insuficiente")
        
    user.saldo -= monto
    userdes.saldo += monto

    fecha_operacion = str(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))

    operacion = OperacionDB(origen=minumero, destino=numerodes, monto=monto, fecha=fecha_operacion)
    db.add(operacion)
    db.commit()
    return {"message": "Operacion exitosa. Realizado en " + fecha_operacion}

@app.get("/billetera/historial")
async def historial(minumero: str, db: Session = Depends(get_db)):
    user = db.query(UsuarioDB).filter(UsuarioDB.numero == minumero).first()
    if user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    
    operaciones_origen = db.query(OperacionDB).filter(OperacionDB.origen == minumero).all()
    operaciones_destino = db.query(OperacionDB).filter(OperacionDB.destino == minumero).all()
    
    historial_operaciones = []

    for operacion in operaciones_origen:
        usuario_destino = db.query(UsuarioDB).filter(UsuarioDB.numero == operacion.destino).first()
        if usuario_destino:
            historial_operaciones.append(f"Pago realizado de {operacion.monto} a {usuario_destino.numero}")

    for operacion in operaciones_destino:
        usuario_origen = db.query(UsuarioDB).filter(UsuarioDB.numero == operacion.origen).first()
        if usuario_origen:
            historial_operaciones.append(f"Pago recibido de {operacion.monto} de {usuario_origen.numero}")

    response = {
        f"Saldo de {user.nombre}": user.saldo,
        f"Operaciones de {user.nombre}": historial_operaciones
    }

    return response
