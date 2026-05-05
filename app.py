from flask import Flask, render_template, request, redirect, session
import sqlite3
import random

app = Flask(__name__)
app.secret_key = "secret123"

# 🟢 Home Page
@app.route('/')
def index():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()

    conn.close()
    return render_template("index.html", products=products)


# 🟢 Add to Cart
@app.route('/add_to_cart/<int:id>')
def add_to_cart(id):
    if "cart" not in session:
        session["cart"] = []

    session["cart"].append(id)
    return redirect('/cart')


# 🟢 Cart Page
@app.route('/cart')
def cart():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cart_items = []
    if "cart" in session:
        for pid in session["cart"]:
            cursor.execute("SELECT * FROM products WHERE id=?", (pid,))
            cart_items.append(cursor.fetchone())

    conn.close()
    return render_template("cart.html", cart_items=cart_items)


# 🟢 Login Page
@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        number = request.form["number"]
        otp = str(random.randint(1000, 9999))

        session["otp"] = otp
        session["number"] = number

        print("OTP:", otp)  # terminal me dikhega

        return redirect("/verify")

    return render_template("login.html")


# 🟢 Verify OTP
@app.route('/verify', methods=["GET", "POST"])
def verify():
    if request.method == "POST":
        user_otp = request.form["otp"]

        if user_otp == session.get("otp"):
            conn = sqlite3.connect("database.db")
            cursor = conn.cursor()

            cursor.execute(
                "INSERT INTO users (number, otp) VALUES (?, ?)",
                (session.get("number"), session.get("otp"))
            )

            conn.commit()
            conn.close()

            return render_template("result.html", msg="Login Successful")

        else:
            return render_template("result.html", msg="Invalid OTP")

    return render_template("verify.html")


# 🟢 Deals Page
@app.route('/deals')
def deals():
    return render_template("deals.html")


# 💳 🟢 Payment Page (NEW)
@app.route('/payment/<int:id>')
def payment(id):
    return render_template("payment.html", id=id)


# 🎉 🟢 Payment Success (Order confirm)
@app.route('/payment_success/<int:id>')
def payment_success(id):
    return render_template("order_success.html")


# ▶️ Run App
if __name__ == "__main__":
    app.run(debug=True)
    
