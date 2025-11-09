from fastapi.testclient import TestClient
from backend import main
from backend.security.jwt_handler import create_token

client = TestClient(main.app)

def test_get_posts():
    response = client.get('/items')
    assert response.status_code == 200


def test_add_post():
    test_data = {'age' : 20, 'login' : 'michael1337', 'password' : 'superpassword123'}
    test_token = create_token(test_data)
    response = client.post(url='/postCreate',json={'content' : 'testcontent'}, headers={'Authorization' : f'Bearer {test_token}'})
    
    assert response.status_code == 200