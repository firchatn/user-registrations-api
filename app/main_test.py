from fastapi.testclient import TestClient
from .main import app

client = TestClient(app)

def test_create_existing_user():
    response = client.post(
        "/register",
        json={
            "id": "1",
            "email": "firaschaabencss@gmail.com",
            "verified": False,
            "password": "12345678",
            "created_at": "2023-01-23T15:33:23.931+00:00",
            "updated_at": "2023-01-23T15:33:23.931+00:00"
            },
    )
    assert response.status_code == 409
    assert response.json() == {"detail": "User already exists"}