from fastapi.testclient import TestClient
from backend import main

client = TestClient(main.app)
    
def test_weather():
    cities = ['Moscow', 'Pekin', 'New York', 'Dubai', 'London']
    for city in cities:
        response = client.get(f'/weather/{city}')
        assert response.status_code == 200
        data = response.json()
        assert type(data['temp']) == float
        assert type(data['description']) == str
        assert type(data['wind']) == float
