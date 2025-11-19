import pytest
import sys
import os

# Add parent directory to path to import app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_biodiversity_landing(client):
    """Test that biodiversity landing page loads"""
    response = client.get('/vidensbank/biodiversitet')
    assert response.status_code == 200
    assert b'Biodiversitet' in response.data

def test_biodiversity_what(client):
    """Test that biodiversity 'what' page loads"""
    response = client.get('/vidensbank/biodiversitet/hvad-er-det')
    assert response.status_code == 200
    assert b'Hvad er' in response.data

def test_biodiversity_why(client):
    """Test that biodiversity 'why' page loads"""
    response = client.get('/vidensbank/biodiversitet/hvorfor-er-det-vigtigt')
    assert response.status_code == 200
    assert b'Vigtigt' in response.data

def test_biodiversity_goal(client):
    """Test that biodiversity 'goal' page loads"""
    response = client.get('/vidensbank/biodiversitet/maal-og-ambition')
    assert response.status_code == 200
    assert b'ambitioner' in response.data.lower()

def test_biodiversity_impact(client):
    """Test that biodiversity 'impact' page loads"""
    response = client.get('/vidensbank/biodiversitet/mit-aftryk')
    assert response.status_code == 200
    assert b'Aftryk' in response.data

def test_biodiversity_tips(client):
    """Test that biodiversity 'tips' page loads"""
    response = client.get('/vidensbank/biodiversitet/tips-og-tricks')
    assert response.status_code == 200
    assert b'Tips' in response.data
