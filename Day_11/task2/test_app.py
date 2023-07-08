import json
import pytest

from app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_get_weather(client):
    response = client.get('/weather/San Francisco')
    data = json.loads(response.data.decode('utf-8'))

    assert response.status_code == 200
    assert data['city'] == 'San Francisco'
    assert 'temperature' in data
    assert 'weather' in data


def test_get_weather_invalid_city(client):
    response = client.get('/weather/Invalid City')

    assert response.status_code == 404


def test_add_weather(client):
    data = {
        'city': 'Chicago',
        'temperature': 18,
        'weather': 'Cloudy'
    }
    response = client.post('/weather', json=data)
    data = json.loads(response.data.decode('utf-8'))

    assert response.status_code == 201
    assert data['city'] == 'Chicago'
    assert data['temperature'] == 18
    assert data['weather'] == 'Cloudy'


def test_update_weather(client):
    data = {
        'temperature': 25,
        'weather': 'Sunny'
    }
    response = client.put('/weather/San Francisco', json=data)
    data = json.loads(response.data.decode('utf-8'))

    assert response.status_code == 200
    assert data['city'] == 'San Francisco'
    assert data['temperature'] == 25
    assert data['weather'] == 'Sunny'


def test_update_weather_invalid_city(client):
    data = {
        'temperature': 25,
        'weather': 'Sunny'
    }
    response = client.put('/weather/Invalid City', json=data)

    assert response.status_code == 404


def test_delete_weather(client):
    response = client.delete('/weather/Seattle')

    assert response.status_code == 204


def test_delete_weather_invalid_city(client):
    response = client.delete('/weather/Invalid City')

    assert response.status_code == 404