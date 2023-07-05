from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)
menu_file = "menu.json"
orders_file = "orders.json"
users_file = "users.json"
wallet_file = "wallet.json"


def load_data(file_name):
    try:
        with open(file_name, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []


def save_data(data, file_name):
    with open(file_name, "w") as file:
        json.dump(data, file)


def load_menu():
    return load_data(menu_file)


def save_menu(menu):
    save_data(menu, menu_file)


def load_orders():
    return load_data(orders_file)


def save_orders(orders):
    save_data(orders, orders_file)


def load_users():
    return load_data(users_file)


def save_users(users):
    save_data(users, users_file)


def load_wallet():
    return load_data(wallet_file)


def save_wallet(wallet):
    save_data(wallet, wallet_file)


def update_user_wallet(username, amount):
    users = load_users()
    for user in users:
        if user["username"] == username:
            user["wallet"] += amount
            break
    save_users(users)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/menu")
def display_menu():
    menu = load_menu()
    return render_template("index.html", menu=menu, content="menu")


@app.route("/add_dish", methods=["GET", "POST"])
def add_dish():
    if request.method == "POST":
        dish_id = int(request.form["dish_id"])
        dish_name = request.form["dish_name"]
        price = float(request.form["price"])
        availability = request.form.get("availability") == "on"

        menu = load_menu()
        new_dish = {
            "dish_id": dish_id,
            "dish_name": dish_name,
            "price": price,
            "availability": availability
        }
        menu.append(new_dish)
        save_menu(menu)
        return redirect(url_for("display_menu"))
    return render_template("index.html", content="add_dish")


@app.route("/update_availability", methods=["GET", "POST"])
def update_dish_availability():
    if request.method == "POST":
        dish_id = int(request.form["dish_id"])
        availability = request.form.get("availability") == "on"

        menu = load_menu()
        for dish in menu:
            if dish["dish_id"] == dish_id:
                dish["availability"] = availability
                break
        save_menu(menu)
        return redirect(url_for("display_menu"))
    return render_template("index.html", content="update_availability")


@app.route("/signup", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        users = load_users()
        for user in users:
            if user["username"] == username:
                return "Username already exists. Please choose a different username."
        new_user = {
            "username": username,
            "password": password,
            "wallet": 0
        }
        users.append(new_user)
        save_users(users)
        return redirect(url_for("home"))
    return render_template("index.html", content="signup")


@app.route("/login", methods=["GET", "POST"])
def log_in():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        users = load_users()
        for user in users:
            if user["username"] == username and user["password"] == password:
                return redirect(url_for("main_menu", username=username))
        return "Invalid username or password. Please try again."
    return render_template("index.html", content="login")


@app.route("/main_menu/<username>", methods=["GET", "POST"])
def main_menu(username):
    if request.method == "POST":
        if "add_funds" in request.form:
            return redirect(url_for("add_funds", username=username))
        elif "display_menu" in request.form:
            return redirect(url_for("display_menu"))
        elif "add_dish" in request.form:
            return redirect(url_for("add_dish"))
        elif "update_availability" in request.form:
            return redirect(url_for("update_dish_availability"))
        elif "place_order" in request.form:
            return redirect(url_for("place_order", username=username))
        elif "exit" in request.form:
            return redirect(url_for("home"))
    return render_template("index.html", content="main_menu", username=username)


@app.route("/add_funds/<username>", methods=["GET", "POST"])
def add_funds(username):
    if request.method == "POST":
        amount = float(request.form["amount"])

        update_user_wallet(username, amount)

        return redirect(url_for("main_menu", username=username))
    return render_template("index.html", content="add_funds", username=username)


@app.route("/place_order/<username>", methods=["GET", "POST"])
def place_order(username):
    if request.method == "POST":
        order_items = request.form.getlist("order_item")

        menu = load_menu()
        order_dishes = []

        for item in order_items:
            dish_id = int(item)
            dish = next((dish for dish in menu if dish["dish_id"] == dish_id and dish["availability"]), None)
            if dish:
                order_dishes.append(dish)

        if order_dishes:
            orders = load_orders()
            order_id = len(orders) + 1
            order = {
                "order_id": order_id,
                "customer_name": username,
                "dishes": order_dishes,
                "status": "received"
            }
            orders.append(order)
            save_orders(orders)
            return redirect(url_for("order_status", order_id=order_id))
        else:
            return "No valid dishes selected. Order not placed."
    else:
        menu = load_menu()
        return render_template("index.html", content="place_order", menu=menu, username=username)


@app.route("/order_status/<int:order_id>")
def order_status(order_id):
    orders = load_orders()
    order = next((order for order in orders if order["order_id"] == order_id), None)
    if order:
        return render_template("index.html", content="order_status", order=order)
    else:
        return "Order not found."


if __name__ == "__main__":
    app.run(debug=True)
