import sqlite3

DB_NAME = "auth/users.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def create_users_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def add_user(username, password):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, password)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()


def get_user(username):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT username, password FROM users WHERE username = ?",
        (username,)
    )

    user = cursor.fetchone()
    conn.close()
    return user
