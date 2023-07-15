from flask import Flask, request, jsonify

app = Flask(__name__)

# Sample data for menu and orders
menu = [
    {"id": 1, "name": "Pizza", "price": 10, "availability": True},
    {"id": 2, "name": "Burger", "price": 5, "availability": True},
    {"id": 3, "name": "Pasta", "price": 8, "availability": False}
]

orders = []

# Get menu
@app.route('/api/menu', methods=['GET'])
def get_menu():
    return jsonify(menu)

# Add a new dish to the menu
@app.route('/api/menu', methods=['POST'])
def add_dish():
    data = request.get_json()
    dish = {
        "id": len(menu) + 1,
        "name": data["name"],
        "price": data["price"],
        "availability": True
    }
    menu.append(dish)
    return jsonify({"message": "Dish added successfully"})

# Remove a dish from the menu
@app.route('/api/menu/<int:dish_id>', methods=['DELETE'])
def remove_dish(dish_id):
    dish = next((item for item in menu if item["id"] == dish_id), None)
    if dish:
        menu.remove(dish)
        return jsonify({"message": "Dish removed successfully"})
    else:
        return jsonify({"error": "Dish not found"})

# Update the availability of a dish
@app.route('/api/menu/<int:dish_id>/availability', methods=['PUT'])
def update_availability(dish_id):
    data = request.get_json()
    availability = data["availability"]
    dish = next((item for item in menu if item["id"] == dish_id), None)
    if dish:
        dish["availability"] = availability
        return jsonify({"message": "Availability updated successfully"})
    else:
        return jsonify({"error": "Dish not found"})

# Take a new order from a customer
@app.route('/api/orders', methods=['POST'])
def take_order():
    data = request.get_json()
    dish_id = data["dish_id"]
    customer_name = data["customer_name"]
    dish = next((item for item in menu if item["id"] == dish_id), None)
    if dish and dish["availability"]:
        order = {
            "customer_name": customer_name,
            "dish_id": dish_id,
            "status": "pending"
        }
        orders.append(order)
        return jsonify({"message": "Order placed successfully"})
    else:
        return jsonify({"error": "Dish not available"})

# Update the status of an order
@app.route('/api/orders/<int:order_id>/status', methods=['PUT'])
def update_order_status(order_id):
    data = request.get_json()
    status = data["status"]
    order = next((item for item in orders if item["id"] == order_id), None)
    if order:
        order["status"] = status
        return jsonify({"message": "Order status updated successfully"})
    else:
        return jsonify({"error": "Order not found"})

# Review all orders
@app.route('/api/orders', methods=['GET'])
def get_all_orders():
    return jsonify(orders)

if __name__ == '__main__':
    app.run()
