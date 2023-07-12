# app.py
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)


class Dish(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price
        }

# Routes for CRUD operations
@app.route('/dishes', methods=['GET'])
def get_all_dishes():
    dishes = Dish.query.all()
    return jsonify([dish.serialize() for dish in dishes])

@app.route('/dishes/<int:dish_id>', methods=['GET'])
def get_dish(dish_id):
    dish = Dish.query.get(dish_id)
    if not dish:
        return jsonify({'error': 'Dish not found'}), 404
    return jsonify(dish.serialize())

@app.route('/dishes', methods=['POST'])
def create_dish():
    name = request.json.get('name')
    price = request.json.get('price')
    if not name or not price:
        return jsonify({'error': 'Name and price are required'}), 400
    dish = Dish(name=name, price=price)
    db.session.add(dish)
    db.session.commit()
    return jsonify({'message': 'Dish created successfully', 'dish_id': dish.id})

@app.route('/dishes/<int:dish_id>', methods=['PUT'])
def update_dish(dish_id):
    dish = Dish.query.get(dish_id)
    if not dish:
        return jsonify({'error': 'Dish not found'}), 404
    name = request.json.get('name')
    price = request.json.get('price')
    if not name or not price:
        return jsonify({'error': 'Name and price are required'}), 400
    dish.name = name
    dish.price = price
    db.session.commit()
    return jsonify({'message': 'Dish updated successfully'})

@app.route('/dishes/<int:dish_id>', methods=['DELETE'])
def delete_dish(dish_id):
    dish = Dish.query.get(dish_id)
    if not dish:
        return jsonify({'error': 'Dish not found'}), 404
    db.session.delete(dish)
    db.session.commit()
    return jsonify({'message': 'Dish deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True)
