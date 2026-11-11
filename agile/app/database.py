from werkzeug.security import generate_password_hash
import sqlite3
import os

def init_db():
    conn = sqlite3.connect("agile/app/booking.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL
        )
    """)


   
    users = [
        (
            "student01",
            os.environ["STUDENT_PASSWORD"],
            "student"
        ),
        (
            "admin01",
            os.environ["ADMIN_PASSWORD"],
            "admin"
        )
    ]


    for username, password, role in users:
        cursor.execute(
            "SELECT id FROM users WHERE username = ?",
            (username,)
        )

        if cursor.fetchone() is None:
            cursor.execute(
                """INSERT INTO users
                   (username, password_hash, role)
                   VALUES (?, ?, ?)""",
                (username, generate_password_hash(password), role)
            )


    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("資料庫建立成功！")
