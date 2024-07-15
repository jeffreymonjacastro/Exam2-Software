from fastapi import FastAPI, HTTPException, status, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime


app = FastAPI()

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class UsuarioDB(Base):
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    numero = Column(String, index=True)
    saldo = Column(Integer, index=True)
    numeros_contacto = Column(String)


Base.metadata.create_all(bind=engine)

class Usuario(BaseModel):
    id: int
    numero: str
    saldo: int
    numeros_contacto: str


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

#contacto?minumero=123
@app.get(route+"contacto")
async def get_contactos(minumero: str, db: Session = Depends(get_db)):
    return {"contactos": db.query(Usuario).filter(Usuario.numero == minumero).first().NumerosContacto}

#pagar?minumero=123&numerodes=456&monto=100
@app.post(route+"pagar")
async def pagar(minumero: str, numerodes: str, monto: float, db: Session = Depends(get_db)):
    origen = db.query(Usuario).filter(Usuario.numero == minumero).first()
    destino = db.query(Usuario).filter(Usuario.numero == numerodes).first()
    if origen is None or destino is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    if origen.saldo < monto:
        raise HTTPException(status_code=400, detail="Saldo insuficiente")
    origen.saldo -= monto
    destino.saldo += monto
    db.commit()
    return {"message": "Transacción exitosa", "fecha": str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))}

