from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host='127.0.0.1', user='root', password='', database='bakery_and_pastry_shop'
    )

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Логика входа
        return redirect(url_for('admin_panel'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Логика сохранения в базу (как делали раньше)
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/admin')
def admin_panel():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM integration")
    ints = cursor.fetchall()
    cursor.execute("SELECT * FROM system_backup")
    backs = cursor.fetchall()
    conn.close()
    return render_template('admin.html', integrations=ints, backups=backs)

@app.route('/reports')
def reports():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM bakery_and_pastry_shop.order")
    ords = cursor.fetchall()
    conn.close()
    return render_template('reports.html', orders=ords)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)