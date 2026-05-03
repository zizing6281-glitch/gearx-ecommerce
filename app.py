from flask import Flask, render_template, request, session, redirect
import sqlite3
import random

app = Flask(__name__)
app.secret_key = "secret123"


# ---------------- DATABASE INIT ----------------
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        price INTEGER,
        image TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_name TEXT,
        price INTEGER
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        phone TEXT,
        otp TEXT
    )
    """)

    cursor.execute("SELECT COUNT(*) FROM products")
    if cursor.fetchone()[0] == 0:
        products = [
            ('iPhone', 79999, 'iphone.jpg'),
            ('Samsung', 69999, 'samsung.jpg'),
            ('Laptop', 55000, 'laptop.jpg'),
            ('Smart Watch', 2999, 'watch.jpg'),
            ('Earbuds', 1999, 'earbuds.jpg')
        ]

        cursor.executemany(
            "INSERT INTO products (name, price, image) VALUES (?, ?, ?)",
            products
        )

    conn.commit()
    conn.close()


# ---------------- 🔥 DATABASE HELPER (EASY DEMO) ----------------
def get_users():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users")
    data = cursor.fetchall()

    conn.close()
    return data


# ---------------- HOME ----------------
@app.route('/')
def home():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()

    conn.close()

    return render_template("index.html", products=products)


# ---------------- USERS VIEW (TEACHER DEMO) ----------------
@app.route('/users')
def users():
    data = get_users()
    return str(data)


# ---------------- DEALS ----------------
@app.route('/deals')
def deals():
    return render_template("deals.html")


# ---------------- CART ----------------
@app.route('/add_to_cart/<int:id>')
def add_to_cart(id):
    if 'cart' not in session:
        session['cart'] = []

    session['cart'].append(id)
    session.modified = True
    return redirect('/')


@app.route('/cart')
def cart():
    cart_items = session.get('cart', [])

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    products = []
    total = 0

    for pid in cart_items:
        cursor.execute("SELECT * FROM products WHERE id=?", (pid,))
        item = cursor.fetchone()
        if item:
            products.append(item)
            total += item[2]

    conn.close()

    return render_template("cart.html", products=products, total=total)


@app.route('/remove/<int:id>')
def remove(id):
    cart = session.get('cart', [])

    if id in cart:
        cart.remove(id)

    session['cart'] = cart
    return redirect('/cart')


# ---------------- BUY ----------------
@app.route('/buy/<int:id>')
def buy(id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("SELECT name, price FROM products WHERE id=?", (id,))
    product = cursor.fetchone()

    if product:
        cursor.execute(
            "INSERT INTO orders (product_name, price) VALUES (?, ?)",
            (product[0], product[1])
        )
        conn.commit()

    conn.close()

    return render_template("order_success.html", product=product)


# ---------------- LOGIN ----------------
@app.route('/login')
def login():
    return render_template("login.html")


# ---------------- OTP SEND + STORE ----------------
@app.route('/send_otp', methods=['POST'])
def send_otp():
    phone = request.form['phone']
    otp = str(random.randint(1000, 9999))

    session['otp'] = otp

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO users (phone, otp) VALUES (?, ?)",
        (phone, otp)
    )

    conn.commit()
    conn.close()

    return render_template("verify.html", otp=otp)


# ---------------- VERIFY ----------------
@app.route('/verify', methods=['POST'])
def verify():
    if request.form['otp'] == session.get('otp'):
        return render_template("result.html", message="Login Successful ✅", status="success")
    else:
        return render_template("result.html", message="Wrong OTP ❌", status="error")


# ---------------- RUN ----------------
if __name__ == '__main__':
    init_db()
    app.run(debug=True)
    
# update 1
# update 2
# update 3
# update 4
# update 5
# update 6
# update 7
# update 8
# update 9
# update 10
# update 11
# update 12
# update 13
# update 14
# update 15
