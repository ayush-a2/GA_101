# test_app.py
import json
import pytest
from app import app, db, Dish

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()

def test_create_dish(client):
    with app.app_context():
        response = client.post('/dishes', json={'name': 'Pizza', 'price': 9.99})
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'message' in data
        assert 'dish_id' in data
        dish_id = data['dish_id']
        dish = Dish.query.get(dish_id)
        assert dish is not None
        assert dish.name == 'Pizza'
        assert dish.price == 9.99

def test_get_all_dishes(client):
    with app.app_context():
        dish1 = Dish(name='Pizza', price=9.99)
        dish2 = Dish(name='Burger', price=5.99)
        db.session.add(dish1)
        db.session.add(dish2)
        db.session.commit()

        response = client.get('/dishes')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert isinstance(data, list)
        assert len(data) == 2
        assert data[0]['name'] == 'Pizza'
        assert data[1]['name'] == 'Burger'

# Similarly, update_dish and delete_dish can be modified to use app.app_context()

if __name__ == '__main__':
    pytest.main()
