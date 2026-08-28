from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200


def test_rota_principal():
    response = client.get("/")
    assert response.status_code == 200


def test_login_sem_credenciais():
    response = client.post("/login", json={})
    assert response.status_code == 422


def test_listar_usuarios_sem_token():
    response = client.get("/usuarios")
    assert response.status_code in [401, 403]


def test_consultar_perfil_sem_token():
    response = client.get("/me")
    assert response.status_code in [401, 403]


def test_usuario_inexistente_sem_token():
    response = client.get("/usuarios/999")
    assert response.status_code in [401, 403]
