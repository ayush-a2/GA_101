from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'ayush'
app.config['MYSQL_DB'] = 'python'

mysql = MySQL(app)


# Route for displaying dishes
@app.route('/dishes')
def display_dishes():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM dishes')
    dishes = cur.fetchall()
    cur.close()
    return render_template('menu.html', dishes=dishes)

# Route for adding a new dish
@app.route('/add_dish', methods=['GET', 'POST'])
def add_dish():
    if request.method == 'POST':
        dish_name = request.form['dish_name']
        price = request.form['price']
        availability = request.form['availability']
        cur = mysql.connection.cursor()
        cur.execute(
            'INSERT INTO dishes (dish_name, price, availability) VALUES (%s, %s, %s)',
            (dish_name, price, availability)
        )
        mysql.connection.commit()
        cur.close()
        return redirect('/dishes')
    return render_template('menu.html')

# Route for updating dish details
@app.route('/update_dish/<int:dish_id>', methods=['GET', 'POST'])
def update_dish(dish_id):
    if request.method == 'POST':
        dish_name = request.form['dish_name']
        price = request.form['price']
        availability = request.form['availability']
        cur = mysql.connection.cursor()
        cur.execute(
            'UPDATE dishes SET dish_name=%s, price=%s, availability=%s WHERE dish_id=%s',
            (dish_name, price, availability, dish_id)
        )
        mysql.connection.commit()
        cur.close()
        return redirect('/dishes')
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM dishes WHERE dish_id = %s', (dish_id,))
    dish = cur.fetchone()
    cur.close()
    return render_template('menu.html', dish=dish)

# Route for removing a dish
@app.route('/remove_dish/<int:dish_id>')
def remove_dish(dish_id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM dishes WHERE dish_id = %s', (dish_id,))
    mysql.connection.commit()
    cur.close()
    return redirect('/dishes')

if __name__ == '__main__':
    app.run(debug=True)
