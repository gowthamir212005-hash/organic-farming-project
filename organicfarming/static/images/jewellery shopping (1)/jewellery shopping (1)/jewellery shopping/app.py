dccdimport sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash
import base64

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Initialize DB
with sqlite3.connect("users.db") as conn:
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,j;
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            name TEXT NOT NULL,
            price TEXT NOT NULL,
            image TEXT NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            name TEXT NOT NULL,
            price TEXT NOT NULL,
            image TEXT NOT NULL
        )
    """)

@app.route('/')
def home():
    return redirect(url_for('signin'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        with sqlite3.connect("users.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
            if cursor.fetchone():
                return render_template('signup.html', msg="Email already exists!")
            cursor.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", (name, email, password))
            conn.commit()

        return render_template('signin.html', msg="Signup successful")

    return render_template('signup.html')

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        with sqlite3.connect("users.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
            user = cursor.fetchone()

        if user:
            with sqlite3.connect("users.db") as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT id, title, name, price, image FROM books")
                books = [{"id": row[0], "title": row[1], "name": row[2], "price": row[3], "image": row[4]} for row in cursor.fetchall()]
            return render_template('books.html', books=books)
        else:
            return render_template('signin.html', msg="Invalid email or password! Try again.")

    return render_template('signin.html')

@app.route("/books")
def books():
    with sqlite3.connect("users.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, title, name, price, image FROM books")
        books = [{"id": row[0], "title": row[1], "name": row[2], "price": row[3], "image": row[4]} for row in cursor.fetchall()]
    return render_template('books.html', books=books)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if email == 'admin@gmail.com' and password == 'admin123':
            return render_template('upload.html')
        else:
            return render_template('admin.html', msg="Invalid email or password! Try again.")
    return render_template('admin.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['name']
        price = request.form['price']
        file = request.files['image']

        file_content = file.read()
        image_b64 = base64.b64encode(file_content).decode('utf-8')

        with sqlite3.connect("users.db") as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO books (title, name, price, image) VALUES (?, ?, ?, ?)", (title, author, price, image_b64))
            conn.commit()

        return render_template('upload.html', msg="Upload successful")

    return render_template('upload.html')

@app.route('/buy/<Id>')
def buy(Id):
    with sqlite3.connect("users.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT title, name, price, image FROM books WHERE id = ?", (Id,))
        data = cursor.fetchone()
        if data:
            cursor.execute("INSERT INTO orders (title, name, price, image) VALUES (?, ?, ?, ?)", data)
            conn.commit()
        cursor.execute("SELECT id, title, name, price, image FROM orders")
        books = [{"id": row[0], "title": row[1], "name": row[2], "price": row[3], "image": row[4]} for row in cursor.fetchall()]
    return render_template('orders.html', books=books)

@app.route('/orders')
def orders():
    with sqlite3.connect("users.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, title, name, price, image FROM orders")
        books = [{"id": row[0], "title": row[1], "name": row[2], "price": row[3], "image": row[4]} for row in cursor.fetchall()]
    return render_template('orders.html', books=books)

@app.route('/cancel/<Id>')
def cancel(Id):
    with sqlite3.connect("users.db") as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM orders WHERE id = ?", (Id,))
        conn.commit()
        cursor.execute("SELECT id, title, name, price, image FROM orders")
        books = [{"id": row[0], "title": row[1], "name": row[2], "price": row[3], "image": row[4]} for row in cursor.fetchall()]
    return render_template('orders.html', books=books)

@app.route("/booklist")
def booklist():
    with sqlite3.connect("users.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, title, name, price, image FROM books")
        books = [{"id": row[0], "title": row[1], "name": row[2], "price": row[3], "image": row[4]} for row in cursor.fetchall()]
    return render_template('booklist.html', books=books)

@app.route('/delete/<Id>')
def delete(Id):
    with sqlite3.connect("users.db") as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM books WHERE id = ?", (Id,))
        conn.commit()
        cursor.execute("SELECT id, title, name, price, image FROM books")
        books = [{"id": row[0], "title": row[1], "name": row[2], "price": row[3], "image": row[4]} for row in cursor.fetchall()]
    return render_template('booklist.html', books=books)

if __name__ == '__main__':
    app.run(debug=True)
     