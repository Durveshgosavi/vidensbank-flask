import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_food_waste_calculator_page(client):
    """Test that the food waste impact page loads and contains calculator elements."""
    response = client.get('/vidensbank/madspild/mit-aftryk')
    assert response.status_code == 200
    content = response.data.decode('utf-8')
    assert 'Beregn Dit Spild' in content
    assert 'wasteInput' in content
    assert 'co2Output' in content

def test_water_calculator_page(client):
    """Test that the water impact page loads and contains calculator elements."""
    response = client.get('/vidensbank/vandforbrug/mit-aftryk')
    assert response.status_code == 200
    content = response.data.decode('utf-8')
    assert 'Beregn Vandaftryk' in content
    assert 'foodSelect' in content
    assert 'waterOutput' in content

def test_products_overview(client):
    """Test that the products overview page loads."""
    response = client.get('/vidensbank/raavarer')
    assert response.status_code == 200
    content = response.data.decode('utf-8')
    assert 'Råvarer &<br>Produkter' in content

def test_product_oksekoed(client):
    """Test that the Oksekød product page loads."""
    response = client.get('/vidensbank/raavarer/oksekoed')
    assert response.status_code == 200
    content = response.data.decode('utf-8')
    assert 'Oksekød' in content
    assert 'Klimaaftryk' in content

def test_product_svinekoed(client):
    """Test that the Svinekød product page loads."""
    response = client.get('/vidensbank/raavarer/svinekoed')
    assert response.status_code == 200
    content = response.data.decode('utf-8')
    assert 'Svinekød' in content
    assert 'Dansk Produktion' in content

def test_product_fjerkreae(client):
    """Test that the Fjerkræ product page loads."""
    response = client.get('/vidensbank/raavarer/fjerkreae')
    assert response.status_code == 200
    content = response.data.decode('utf-8')
    assert 'Fjerkræ' in content
    assert 'Klimaaftryk' in content

def test_product_oksekoed(client):
    """Test that the Oksekød product page loads."""
    response = client.get('/vidensbank/raavarer/oksekoed')
    assert response.status_code == 200
    content = response.data.decode('utf-8')
    assert 'Oksekød' in content
    assert 'Klimaaftryk' in content

def test_product_svinekoed(client):
    """Test that the Svinekød product page loads."""
    response = client.get('/vidensbank/raavarer/svinekoed')
    assert response.status_code == 200
    content = response.data.decode('utf-8')
    assert 'Svinekød' in content
    assert 'Dansk Produktion' in content
