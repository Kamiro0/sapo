from fastapi.testclient import TestClient
from app.main import app

def test_token_endpoint_and_invalid(client=None):
    with TestClient(app) as c:
        r = c.post('/token', data={'username':'cliente','password':'1234'})
        assert r.status_code == 200
        data = r.json()
        assert 'access_token' in data

        # invalid user
        r2 = c.post('/token', data={'username':'Camilo','password':'4532'})
        assert r2.status_code == 400
