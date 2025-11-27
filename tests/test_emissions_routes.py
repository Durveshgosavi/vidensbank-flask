import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_emissions_landing(client):
    response = client.get('/vidensbank/emissioner')
    assert response.status_code == 200

def test_emissions_what(client):
    response = client.get('/vidensbank/emissioner/hvad-er-det')
    assert response.status_code == 200

def test_emissions_why(client):
    response = client.get('/vidensbank/emissioner/hvorfor-vigtigt')
    assert response.status_code == 200

def test_emissions_goal(client):
    response = client.get('/vidensbank/emissioner/maal-og-ambition')
    assert response.status_code == 200

def test_emissions_tips(client):
    response = client.get('/vidensbank/emissioner/tips-og-tricks')
    assert response.status_code == 200

def test_emissions_impact(client):
    response = client.get('/vidensbank/emissioner/mit-aftryk')
    assert response.status_code == 200
