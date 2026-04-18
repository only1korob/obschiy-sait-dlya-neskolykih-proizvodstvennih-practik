import mysql.connector
from datetime import datetime


def get_connection():
    return mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        password='',
        database='bakery_and_pastry_shop'
    )


def add_all_data():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT user_id FROM user LIMIT 1")
        user = cursor.fetchone()

        if not user:
            print("Ошибка: В таблице user нет пользователей. Сначала зарегистрируйся на сайте!")
            return

        user_id = user[0]

        sql_int = "INSERT INTO integration (intedration_type, service_name, is_active) VALUES (%s, %s, %s)"
        cursor.execute(sql_int, ("payment", "GothicPay", 1))

        sql_back = "INSERT INTO system_backup (backup_date, backup_file_path, initiated_by) VALUES (%s, %s, %s)"
        cursor.execute(sql_back, (datetime.now(), "/backups/save_001.sql", "Admin"))

        sql_order = "INSERT INTO order (customer_id, status, total_amount) VALUES (%s, %s, %s)"
        cursor.execute(sql_order, (user_id, "Выполнен", 1250.50))

        conn.commit()
        print(f"Великолепно! Данные добавлены для пользователя с ID: {user_id}")

    except Exception as e:
        print(f"Ошибка в ритуале: {e}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()