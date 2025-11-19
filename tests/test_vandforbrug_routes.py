import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_vandforbrug_landing(client):
    response = client.get('/vidensbank/vandforbrug')
    assert response.status_code == 200

def test_vandforbrug_what(client):
    response = client.get('/vidensbank/vandforbrug/hvad-er-det')
    assert response.status_code == 200

def test_vandforbrug_why(client):
    response = client.get('/vidensbank/vandforbrug/hvorfor-vigtigt')
    assert response.status_code == 200

def test_vandforbrug_goal(client):
    response = client.get('/vidensbank/vandforbrug/maal-og-ambition')
    assert response.status_code == 200

def test_vandforbrug_tips(client):
    response = client.get('/vidensbank/vandforbrug/tips-og-tricks')
    assert response.status_code == 200

def test_vandforbrug_impact(client):
    response = client.get('/vidensbank/vandforbrug/mit-aftryk')
    assert response.status_code == 200
