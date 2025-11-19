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

def test_saeson_landing(client):
    """Test that saeson landing page loads"""
    response = client.get('/vidensbank/saeson')
    assert response.status_code == 200
    assert b'S' in response.data

def test_saeson_what(client):
    """Test that saeson 'what' page loads"""
    response = client.get('/vidensbank/saeson/hvad-er-det')
    assert response.status_code == 200

def test_saeson_why(client):
    """Test that saeson 'why' page loads"""
    response = client.get('/vidensbank/saeson/hvorfor-vigtigt')
    assert response.status_code == 200

def test_saeson_goal(client):
    """Test that saeson 'goal' page loads"""
    response = client.get('/vidensbank/saeson/maal-og-ambition')
    assert response.status_code == 200

def test_saeson_impact(client):
    """Test that saeson 'impact' page loads"""
    response = client.get('/vidensbank/saeson/mit-aftryk')
    assert response.status_code == 200

def test_saeson_tips(client):
    """Test that saeson 'tips' page loads"""
    response = client.get('/vidensbank/saeson/tips-og-tricks')
    assert response.status_code == 200
