from fastapi.testclient import TestClient
from main import app
import pytest

client = TestClient(app)

# Datos de prueba para usuario y ECG
test_user = {"username": "testuser", "password": "testpassword"}
test_ecg = {
    "id": 1,
    "date": "2024-01-01T00:00:00Z",
    "leads": [
        {"name": "I", "signal": [1, -1, 2, -2, 3]},
        {"name": "II", "signal": [-1, 1, -2, 2, -3]}
    ]
}

@pytest.fixture
def get_token():
    # Registro de usuario para pruebas
    client.post("/register/", json=test_user)
    # Generación de token
    response = client.post("/token", data={
        "username": test_user["username"],
        "password": test_user["password"]
    })
    assert response.status_code == 200
    token = response.json().get("access_token")
    return f"Bearer {token}"

def test_register_user():
    response = client.post("/register/", json=test_user)
    assert response.status_code == 200
    assert response.json()["username"] == test_user["username"]

def test_token_generation():
    response = client.post("/token", data={
        "username": test_user["username"],
        "password": test_user["password"]
    })
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_create_ecg(get_token):
    headers = {"Authorization": get_token}
    response = client.post("/ecgs/", json=test_ecg, headers=headers)
    assert response.status_code == 200
    assert response.json()["id"] == test_ecg["id"]

def test_get_ecg_insights(get_token):
    headers = {"Authorization": get_token}
    # Primero, crear el ECG para asegurarse de que exista
    client.post("/ecgs/", json=test_ecg, headers=headers)
    # Luego, obtener insights del ECG
    response = client.get(f"/ecgs/{test_ecg['id']}/insights", headers=headers)
    assert response.status_code == 200
    assert "I" in response.json()  # Verificar que existen insights para lead "I"
    assert "II" in response.json()  # Verificar que existen insights para lead "II"
