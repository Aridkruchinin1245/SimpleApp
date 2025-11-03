from fastapi.testclient import TestClient
from backend import main

client = TestClient(main.app)

def test_get_posts():
    response = client.get('/items')
    assert response.status_code == 200