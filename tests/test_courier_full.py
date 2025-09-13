import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import init_db, engine
from app.core.config import settings
from sqlmodel import SQLModel

@pytest.fixture(autouse=True, scope='module')
def setup_db():
    # recreate schema for tests module
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)
    yield
    SQLModel.metadata.drop_all(engine)

@pytest.fixture(scope='module')
def client():
    with TestClient(app) as c:
        yield c

def get_token(client, username):
    r = client.post('/token', data={'username': username, 'password': 'x'})
    assert r.status_code == 200
    return r.json()['access_token']

def test_crud_flow_and_roles(client):
    token_cliente = get_token(client, 'cliente')
    token_repartidor = get_token(client, 'repartidor')
    token_admin = get_token(client, 'admin')

    headers_cliente = {'Authorization': f'Bearer {token_cliente}'}
    headers_repartidor = {'Authorization': f'Bearer {token_repartidor}'}
    headers_admin = {'Authorization': f'Bearer {token_admin}'}

    # cliente crea un envío
    payload = {
        'remitente':'Camilo',
        'destinatario':'sebastian',
        'direccion_origen':'Calle 16 23-90',
        'direccion_destino':'Calle 22 45-67',
        'peso': 2.2,
        'descripcion':'Documentos importantes'
    }
    r = client.post('/envios/', json=payload, headers=headers_cliente)
    assert r.status_code == 201
    env = r.json()
    assert env['creado_por'] == 'leon_cliente'

    # repartidor puede ver el envío
    r = client.get(f"/envios/{env['id']}", headers=headers_repartidor)
    assert r.status_code == 200

    # cliente no puede actualizar estado
    r = client.patch(f"/envios/{env['id']}/estado", json={'nuevo_estado':'entregado'}, headers=headers_cliente)
    assert r.status_code == 403

    # repartidor actualiza estado
    r = client.patch(f"/envios/{env['id']}/estado", json={'nuevo_estado':'en_transito'}, headers=headers_repartidor)
    assert r.status_code == 200
    assert r.json()['estado'] == 'en_transito'

    # admin elimina
    r = client.delete(f"/envios/{env['id']}", headers=headers_admin)
    assert r.status_code == 204

    # ahora obtener da 404
    r = client.get(f"/envios/{env['id']}", headers=headers_admin)
    assert r.status_code == 404
