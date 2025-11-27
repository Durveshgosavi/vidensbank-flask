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

def test_organic_landing(client):
    """Test that organic landing page loads"""
    response = client.get('/vidensbank/okologi')
    assert response.status_code == 200
    assert b'okologi' in response.data.lower() or b'organic' in response.data.lower()

def test_organic_what(client):
    """Test that organic 'what' page loads"""
    response = client.get('/vidensbank/okologi/hvad-er-det')
    assert response.status_code == 200

def test_organic_why(client):
    """Test that organic 'why' page loads"""
    response = client.get('/vidensbank/okologi/hvorfor-er-det-vigtigt')
    assert response.status_code == 200

def test_organic_goal(client):
    """Test that organic 'goal' page loads"""
    response = client.get('/vidensbank/okologi/maal-og-ambition')
    assert response.status_code == 200

def test_organic_impact(client):
    """Test that organic 'impact' page loads"""
    response = client.get('/vidensbank/okologi/mit-aftryk')
    assert response.status_code == 200

def test_organic_tips(client):
    """Test that organic 'tips' page loads"""
    response = client.get('/vidensbank/okologi/tips-og-tricks')
    assert response.status_code == 200
