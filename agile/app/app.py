
import sqlite3
from pathlib import Path
from werkzeug.security import check_password_hash
from flask import Flask, render_template, request, session, redirect, url_for
import os

app = Flask(__name__)
app.secret_key = os.environ["SECRET_KEY"]

# 資料庫位置
DB_PATH = Path(__file__).resolve().parent / "booking.db"


# 登入頁面
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # 連接資料庫
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row

        # 查詢帳號
        user = conn.execute(
            "SELECT * FROM users WHERE username = ?",
            (username,)
        ).fetchone()

        conn.close()

        # 驗證密碼
        if user and check_password_hash(
            user["password_hash"], password
        ):
            session.clear()
            session["username"] = user["username"]
            session["role"] = user["role"]

            return redirect(url_for("dashboard"))

        return "帳號或密碼錯誤！"

    return render_template("login.html")


# 學生與管理員首頁
@app.route("/dashboard")
def dashboard():
    if "username" not in session:
        return redirect(url_for("home"))

    if session["role"] == "admin":
        return render_template("admin.html")

    return render_template("student.html")


# 登出功能
@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for("home"))


# 啟動 Flask
if __name__ == "__main__":
    app.run(debug=True)
