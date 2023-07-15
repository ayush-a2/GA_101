import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [menu, setMenu] = useState([]);
  const [orders, setOrders] = useState([]);
  const [dishId, setDishId] = useState(null); // Updated initial state to null
  const [customerName, setCustomerName] = useState('');

  // Fetch menu data from the backend
  useEffect(() => {
    fetch('/api/menu')
      .then(response => response.json())
      .then(data => setMenu(data))
      .catch(error => console.log(error));
  }, []);

  // Fetch orders data from the backend
  useEffect(() => {
    fetch('/api/orders')
      .then(response => response.json())
      .then(data => setOrders(data))
      .catch(error => console.log(error));
  }, []);

  // Function to handle placing an order
  const handlePlaceOrder = (e) => {
    e.preventDefault();
    if (!dishId || !customerName) {
      console.log('Please fill in all fields');
      return;
    }

    fetch('/api/orders', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ dish_id: dishId, customer_name: customerName }),
    })
      .then(response => response.json())
      .then(data => {
        if (data.message) {
          // Order placed successfully, fetch updated orders data
          fetch('/api/orders')
            .then(response => response.json())
            .then(data => setOrders(data))
            .catch(error => console.log(error));
        } else {
          console.log(data.error);
        }
      })
      .catch(error => console.log(error));

    // Clear form inputs
    setDishId(null);
    setCustomerName('');
  };

  // Function to handle updating the order status
  const handleUpdateOrderStatus = (orderId, newStatus) => {
    fetch(`/api/orders/${orderId}/status`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ status: newStatus }),
    })
      .then(response => response.json())
      .then(data => {
        if (data.message) {
          // Order status updated successfully, fetch updated orders data
          fetch('/api/orders')
            .then(response => response.json())
            .then(data => setOrders(data))
            .catch(error => console.log(error));
        } else {
          console.log(data.error);
        }
      })
      .catch(error => console.log(error));
  };

  return (
    <div className="App">
      <h1 className="title">Zesty Zomato</h1>
      <div className="menu">
        <h2>Menu</h2>
        {menu.map(dish => (
          <div key={dish.id} className="dish">
            <p className="dish-name">{dish.name}</p>
            <p className="dish-price">Price: ${dish.price}</p>
            <p className="dish-availability">
              Availability: {dish.availability ? 'Available' : 'Not Available'}
            </p>
          </div>
        ))}
      </div>
      <div className="order-form">
        <h2>Place an Order</h2>
        <form onSubmit={handlePlaceOrder}>
          <div className="form-group">
            <label htmlFor="dishId">Dish:</label>
            <select
              id="dishId"
              value={dishId || ''} // Set value to an empty string when dishId is null
              onChange={e => setDishId(parseInt(e.target.value))} // Parse selected value as an integer
            >
              <option value="">Select a dish</option>
              {menu.map(dish => (
                <option key={dish.id} value={dish.id}>
                  {dish.name}
                </option>
              ))}
            </select>
          </div>
          <div className="form-group">
            <label htmlFor="customerName">Customer Name:</label>
            <input
              type="text"
              id="customerName"
              value={customerName}
              onChange={e => setCustomerName(e.target.value)}
            />
          </div>
          <button type="submit" className="submit-btn">
            Place Order
          </button>
        </form>
      </div>
      <div className="order-status-update">
        <h2>Update Order Status</h2>
        {orders.map(order => (
          <div key={order.id} className="order">
            <p className="order-id">Order ID: {order.id}</p>
            <p className="customer">Customer: {order.customer_name}</p>
            <p className="status">Status: {order.status}</p>
            <button
              className="status-btn"
              onClick={() => handleUpdateOrderStatus(order.id, 'In Progress')}
            >
              Set In Progress
            </button>
            <button
              className="status-btn"
              onClick={() => handleUpdateOrderStatus(order.id, 'Delivered')}
            >
              Set Delivered
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;
