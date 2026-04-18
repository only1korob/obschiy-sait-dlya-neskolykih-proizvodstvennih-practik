import mysql.connector


def fix():
    try:
        conn = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='',
            database='bakery_and_pastry_shop'
        )
        cursor = conn.cursor()

        cursor.execute("ALTER TABLE system_backup DROP FOREIGN KEY system_backup_ibfk_1")

        conn.commit()
        print("Магия сработала! Ограничение снято. Теперь попробуй зарегистрироваться снова.")

        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Что-то пошло не так: {e}")


if __name__ == '__main__':
    fix()