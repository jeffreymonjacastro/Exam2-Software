from usuario import Usuario

class Operacion:
    def __init__(self, origen:Usuario, destino:Usuario, monto:float, fecha:str):
        self.origen = origen
        self.destino = destino
        self.monto = monto
        self.fecha = fecha
    
    def __str__(self):
        return f"Origen: {self.origen}, Destino: {self.destino}, Monto: {self.monto}, Fecha: {self.fecha}"
    
    def __repr__(self):
        return f"Origen: {self.origen}, Destino: {self.destino}, Monto: {self.monto}, Fecha: {self.fecha}"