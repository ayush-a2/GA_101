import json
import pytest
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_get_weather_existing_city(client):
    response = client.get('/weather/San Francisco')
    data = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    assert data == {'temperature': 14
                    , 'weather': 'Cloudy'}

def test_get_weather_non_existing_city(client):
    response = client.get('/weather/Nonexistent City')
    data = json.loads(response.get_data(as_text=True))
    assert response.status_code == 404
    assert data == {'error': 'City not found'}
