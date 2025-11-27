import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_ernaering_landing(client):
    response = client.get('/vidensbank/ernaering')
    assert response.status_code == 200

def test_ernaering_what(client):
    response = client.get('/vidensbank/ernaering/hvad-er-det')
    assert response.status_code == 200

def test_ernaering_why(client):
    response = client.get('/vidensbank/ernaering/hvorfor-vigtigt')
    assert response.status_code == 200

def test_ernaering_goal(client):
    response = client.get('/vidensbank/ernaering/maal-og-ambition')
    assert response.status_code == 200

def test_ernaering_tips(client):
    response = client.get('/vidensbank/ernaering/tips-og-tricks')
    assert response.status_code == 200

def test_ernaering_impact(client):
    response = client.get('/vidensbank/ernaering/mit-aftryk')
    assert response.status_code == 200
