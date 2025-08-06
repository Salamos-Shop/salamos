from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

# إنشاء قاعدة البيانات والجداول
def init_db():
    conn = sqlite3.connect('store.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        phone TEXT
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        phone TEXT,
        address TEXT,
        product TEXT NOT NULL,
        color TEXT,
        quantity INTEGER,
        price REAL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    conn.commit()
    conn.close()

init_db()

# تسجيل دخول المستخدم
@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    phone = data.get('phone')
    if not all([name, email, phone]):
        return jsonify({'message': 'بيانات غير مكتملة'}), 400
    conn = sqlite3.connect('store.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE email = ?', (email,))
    user = c.fetchone()
    if not user:
        c.execute('INSERT INTO users (name, email, phone) VALUES (?, ?, ?)', (name, email, phone))
        conn.commit()
    conn.close()
    return jsonify({'message': 'تم تسجيل الدخول بنجاح'})

# استقبال الطلب
@app.route('/api/order', methods=['POST'])
def add_order():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    phone = data.get('phone')
    address = data.get('address')
    product = data.get('product')
    color = data.get('color')
    quantity = data.get('quantity')
    price = data.get('price')
    if not all([name, email, phone, address, product, price]):
        return jsonify({'message': 'بيانات غير مكتملة'}), 400
    conn = sqlite3.connect('store.db')
    c = conn.cursor()
    c.execute('''INSERT INTO orders (name, email, phone, address, product, color, quantity, price)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
              (name, email, phone, address, product, color, quantity, price))
    conn.commit()
    conn.close()
    return jsonify({'message': 'تم تسجيل الطلب بنجاح'})

# عرض جميع الطلبات (اختياري)
@app.route('/api/orders', methods=['GET'])
def get_orders():
    conn = sqlite3.connect('store.db')
    c = conn.cursor()
    c.execute('''SELECT id, name, email, phone, address, product, quantity, price, created_at FROM orders ORDER BY created_at DESC''')
    orders = [
        {
            'id': row[0],
            'name': row[1],
            'email': row[2],
            'phone': row[3],
            'address': row[4],
            'product': row[5],
            'quantity': row[6],
            'price': row[7],
            'created_at': row[8]
        }
        for row in c.fetchall()
    ]
    conn.close()
    return jsonify(orders)

@app.route('/api/users', methods=['GET'])
def get_users():
    conn = sqlite3.connect('store.db')
    c = conn.cursor()
    c.execute('SELECT id, name, email, phone FROM users ORDER BY id DESC')
    users = [
        {'id': row[0], 'name': row[1], 'email': row[2], 'phone': row[3]}
        for row in c.fetchall()
    ]
    conn.close()
    return jsonify(users)

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('../Salamos-Shop1-main', filename)

if __name__ == '__main__':
    app.run(debug=True)