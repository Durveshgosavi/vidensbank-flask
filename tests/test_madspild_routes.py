import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_madspild_landing(client):
    response = client.get('/vidensbank/madspild')
    assert response.status_code == 200

def test_madspild_what(client):
    response = client.get('/vidensbank/madspild/hvad-er-det')
    assert response.status_code == 200

def test_madspild_why(client):
    response = client.get('/vidensbank/madspild/hvorfor-vigtigt')
    assert response.status_code == 200

def test_madspild_goal(client):
    response = client.get('/vidensbank/madspild/maal-og-ambition')
    assert response.status_code == 200

def test_madspild_tips(client):
    response = client.get('/vidensbank/madspild/tips-og-tricks')
    assert response.status_code == 200

def test_madspild_impact(client):
    response = client.get('/vidensbank/madspild/mit-aftryk')
    assert response.status_code == 200
