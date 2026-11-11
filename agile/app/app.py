
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        return f"收到帳號：{username}"

    return render_template("login.html")

if __name__ == "__main__":
    app.run(debug=True)
