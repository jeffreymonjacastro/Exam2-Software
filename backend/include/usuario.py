from operacion import Operacion
from datetime import datetime

class Usuario:
    def __init__(self, numero:str, saldo:float, NumerosContacto: list[str]):
        self.numero = numero
        self.saldo = saldo
        self.NumerosContacto = NumerosContacto
        self.historialOperaciones = []
    
    def __str__(self):
        return f"Numero: {self.numero}, Saldo: {self.saldo}, Numeros de Contacto: {self.NumerosContacto}"
    
    def __repr__(self):
        return f"Numero: {self.numero}, Saldo: {self.saldo}, Numeros de Contacto: {self.NumerosContacto}"
    
    def historialOperaciones(self):
        return self.historialOperaciones

    def transferir(self, numero:str, monto:float):
        if numero not in self.NumerosContacto:
            return False
        if self.saldo < monto:
            return False
        self.saldo -= monto

        op = Operacion(self.numero, numero, monto, str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        self.historialOperaciones.append(op)

        return True