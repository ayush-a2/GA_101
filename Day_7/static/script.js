// Handle add funds form submission
document.getElementById('add-funds-form').addEventListener('submit', function(event) {
    event.preventDefault();
    
    // Get the amount input value
    var amountInput = document.getElementById('amount-input');
    var amount = parseFloat(amountInput.value);
    
    // Validate the amount
    if (isNaN(amount) || amount <= 0) {
        alert('Please enter a valid amount.');
        amountInput.value = '';
        amountInput.focus();
        return;
    }
    
    // Perform any necessary processing with the amount
    // ...
    
    // Display a success message
    alert('Funds added successfully!');
    
    // Clear the amount input field
    amountInput.value = '';
});

// Handle place order form submission
document.getElementById('place-order-form').addEventListener('submit', function(event) {
    event.preventDefault();
    
    // Get the selected order items
    var orderItems = Array.from(document.querySelectorAll('input[name="order-item"]:checked'))
                        .map(function(checkbox) {
                            return parseInt(checkbox.value);
                        });
    
    // Validate the order items
    if (orderItems.length === 0) {
        alert('Please select at least one dish.');
        return;
    }
    
    // Perform any necessary processing with the order items
    // ...
    
    // Display a success message
    alert('Order placed successfully!');
    
    // Clear the checked order items
    document.querySelectorAll('input[name="order-item"]:checked').forEach(function(checkbox) {
        checkbox.checked = false;
    });
});
