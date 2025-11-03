from fastapi.testclient import TestClient
from backend import main

client = TestClient(main.app)
    
def test_registration():
    dataset = [
    {'login': "mihail", 'age': 12, 'password': "1234567890-="},
    {'login': "alex", 'age': 25, 'password': "password123"},
    {'login': "sara", 'age': 3000, 'password': "qwerty!@#"},
    ]
    
    for data in dataset:
        response = client.post('/reg', json=data)
        assert response.status_code == 200
        assert response.json()


def test_authorisation():
    dataset = [
    {'login': "mihail", 'password': "1234567890-="},
    {'login': "alex", 'password': "password123"},
    {'login': "sara", 'password': "qwerty!@#"},
    ]

    for data in dataset:
        response = client.post('/auth', json=data)
        assert response.status_code == 200
        assert type(response.json()) == str
        