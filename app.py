from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)


def get_db_connection():
    return mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        password='',
        database='bakery_and_pastry_shop'
    )


@app.route('/')
def index():
    return render_template('login.html', title="Вход")


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        full_name = request.form.get('full_name')
        phone = request.form.get('phone')
        email = request.form.get('email')

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            sql = """INSERT INTO user (login, password, full_name, phone, email) 
                     VALUES (%s, %s, %s, %s, %s)"""
            values = (username, password, full_name, phone, email)

            cursor.execute(sql, values)
            conn.commit()

            cursor.close()
            conn.close()

            return "<h1>Ритуал завершен! Ты в базе. Теперь можешь войти.</h1><a href='/'>Назад</a>"

        except Exception as e:
            return f"<h1>Тьма не приняла тебя... Ошибка: {e}</h1>"

    return render_template('register.html')


@app.route('/admin')
def admin_panel():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT integration_id, intedration_type, service_name, is_active FROM integration")
        integrations = cursor.fetchall()

        cursor.execute("SELECT * FROM system_backup ORDER BY backup_date DESC")
        backups = cursor.fetchall()

        cursor.close()
        conn.close()

        return render_template('admin.html', integrations=integrations, backups=backups)
    except Exception as e:
        return f"<h1>Ошибка: {e}</h1>"

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user WHERE login = %s AND password = %s", (username, password))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    if user:
        return f"<h1>Добро пожаловать, мастер {user[3]}! Вход разрешен.</h1>"
    else:
        return "<h1>Неверный логин или пароль. Доступ закрыт.</h1>"

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route('/reports')
def reports():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        sql = "SELECT order_id, customer_id, status, created_at, total_amount FROM bakery_and_pastry_shop.order"

        cursor.execute(sql)
        orders = cursor.fetchall()

        cursor.close()
        conn.close()

        return render_template('reports.html', orders=orders)
    except Exception as e:
        return f"<h1>Ошибка в чертогах отчетности: {e}</h1>"

if __name__ == '__main__':
    app.run(debug=True)