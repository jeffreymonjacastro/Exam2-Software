from operacion import Operacion

class Usuario:
    def __init__(self, numero:str, saldo:float, NumerosContacto: list):
        self.numero = numero
        self.saldo = saldo
        self.NumerosContacto = NumerosContacto
        self.historialOperaciones: list[Operacion] = []
    
    def __str__(self):
        return f"Numero: {self.numero}, Saldo: {self.saldo}, Numeros de Contacto: {self.NumerosContacto}"
    
    def __repr__(self):
        return f"Numero: {self.numero}, Saldo: {self.saldo}, Numeros de Contacto: {self.NumerosContacto}"
    
    def historialOperaciones(self):
        pass

    def transferir(self, numero:str, monto:float):
        pass