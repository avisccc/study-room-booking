
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        
        
        if username == "student01" and password == "1234":
            return "學生首頁"

        elif username == "admin01" and password == "5678":
            return "管理員首頁"

        else:
            return "帳號或密碼錯誤！"


    return render_template("login.html")

if __name__ == "__main__":
    app.run(debug=True)
