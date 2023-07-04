import json

menu_file = "menu.json"
orders_file = "orders.json"

def load_menu():
    try:
        with open(menu_file, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def add_menu(menu):
    with open(menu_file, "w") as file:
        json.dump(menu, file)

def load_orders():
    try:
        with open(orders_file, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_orders(orders):
    with open(orders_file, "w") as file:
        json.dump(orders, file)

def display_menu(menu):
    print("*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*")
    print("Here is your Delecious Zesty Zomato Menu :D")
    print("*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*")
    for dish in menu:
        print(f"Dish ID: {dish['dish_id']}")
        print(f"Dish Name: {dish['dish_name']}")
        print(f"Price: ${dish['price']}")
        availability = "Available" if dish['availability'] else "Not Available"
        print(f"Availability: {availability}")
        print("*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*")

def add_dish():
    dish_id = int(input("Enter the dish ID: "))
    dish_name = input("Enter the dish name: ")
    price = float(input("Enter the price: "))
    availability = input("Is the dish available? (yes/no): ").lower() == "yes"

    new_dish = {
        "dish_id": dish_id,
        "dish_name": dish_name,
        "price": price,
        "availability": availability
    }

    menu.append(new_dish)
    add_menu(menu)
    print("*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*")
    print("New dish added successfully!")
    print("*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*")
    print()

def update_dish_availability():
    dish_id = int(input("Enter the dish ID: "))
    dish = next((dish for dish in menu if dish["dish_id"] == dish_id), None)
    if dish:
        new_availability = input("Set availability (yes/no): ").lower() == "yes"
        dish["availability"] = new_availability
        add_menu(menu)
        print("*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*")
        print(f"Dish ID {dish_id} availability updated successfully!")
        print("*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*")
        print()
    else:
        print("*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*")
        print(f"Dish with ID {dish_id} not found.")
        print("*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*")
        print()

def take_order():
    customer_name = input("Enter customer name: ")
    order_items = input("Enter dish IDs (comma-separated): ").split(",")
    order_dishes = []

    for item in order_items:
        item = int(item.strip())
        dish = next((dish for dish in menu if dish["dish_id"] == item and dish["availability"]), None)
        if dish:
            order_dishes.append(dish)
        else:
            print(f"Dish with ID {item} is not available.")
            print()

    if order_dishes:
        order_id = len(orders) + 1
        order = {
            "order_id": order_id,
            "customer_name": customer_name,
            "dishes": order_dishes,
            "status": "received"
        }
        orders.append(order)
        save_orders(orders)
        print("*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*")
        print(f"Order ID {order_id} placed successfully!")
        print("*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*")
        print()
    else:
        print("*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*")
        print("No valid dishes selected. Order not placed :( )")
        print("*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*")
        print()

def update_order_status():
    order_id = int(input("Enter the order ID: "))
    order = next((order for order in orders if order["order_id"] == order_id), None)
    if order:
        new_status = input("Enter the new status: ")
        order["status"] = new_status
        save_orders(orders)
        print("*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*")
        print(f"Order ID {order_id} status updated successfully!")
        print("*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*")
        print()
    else:
        print("*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*")
        print(f"Order with ID {order_id} not found.")
        print("*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*")
        print()

def review_orders():
    print("*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*")
    print("Zesty Zomato Orders:")
    print("*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*")
    print()
    for order in orders:
        print(f"Order ID: {order['order_id']}")
        print(f"Customer Name: {order['customer_name']}")
        print("Dishes:")
        for dish in order["dishes"]:
            print(f"- {dish['dish_name']}")
        print(f"Status: {order['status']}")
        print("*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*")
        print()


menu = load_menu()
orders = load_orders()

while True:
    print("*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*")
    print("Welcome to Zesty Zomato")
    print("*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*")
    print("1. Want to see the Delicious Menu!!?")
    print("2. Add Dish to Menu")
    print("3. Update the Dish availability")
    print("4. Take Order")
    print("5. Update Order Status")
    print("6. Review Orders")
    print("0. Exit")
    choice = input("Enter your choice: ")

    if choice == "1":
        display_menu(menu)
    elif choice == "2":
        add_dish()
    elif choice == "3":
        update_dish_availability()    
    elif choice == "4":
        take_order()
    elif choice == "5":
        update_order_status()
    elif choice == "6":
        review_orders()
    elif choice == "0":
        print("Exiting...")
        break
    else:
        print("Invalid choice. Please try again.")

print("Thank you, Visit again!")
print()