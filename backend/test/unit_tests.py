import pytest
import requests
from datetime import datetime

BASE_URL = "http://127.0.0.1:8000"

def create_user(numero, saldo, numeros_contacto):
    return requests.post(
        f"{BASE_URL}/usuarios/",
        json={
            "numero": numero,
            "saldo": saldo,
            "numeros_contacto": numeros_contacto
        }
    )

# Helper function to perform a payment
def realizar_pago(minumero, numerodestino, monto):
    return requests.post(
        f"{BASE_URL}/billetera/pagar",
        params={
            "minumero": minumero,
            "numerodestino": numerodestino,
            "monto": monto
        }
    )

@pytest.fixture(scope="module")
def setup_users():
    # Create two users for testing
    create_user("123456789", 500, ["987654321"])
    create_user("987654321", 300, ["123456789"])

def test_crear_usuario(setup_users):
    response = create_user("111111111", 100, ["222222222"])
    assert response.status_code == 201
    data = response.json()
    assert data["numero"] == "111111111"
    assert data["saldo"] == 100
    assert data["numeros_contacto"] == ["222222222"]

def test_realizar_pago_exitoso():
    response = realizar_pago("123456789", "987654321", 100)
    assert response.status_code == 200
    data = response.json()
    assert "Realizado en la fecha" in data["message"]

def test_saldo_insuficiente():
    response = realizar_pago("123456789", "987654321", 1000)
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Saldo insuficiente"

def test_usuario_no_encontrado():
    response = realizar_pago("000000000", "987654321", 100)
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Usuario no encontrado"

def test_usuario_destino_no_encontrado():
    response = realizar_pago("123456789", "000000000", 100)
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Usuario destino no encontrado"
