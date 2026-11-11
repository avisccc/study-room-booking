from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = "dev-only-change-this-key"

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        
        
        
        if username == "student01" and password == "1234":
            session["username"] = username
            session["role"] = "student"
            return redirect(url_for("dashboard"))

        elif username == "admin01" and password == "5678":
            session["username"] = username
            session["role"] = "admin"
            return redirect(url_for("dashboard"))

        else:
            return "帳號或密碼錯誤！"



    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    if "username" not in session:
        return redirect(url_for("home"))

    if session["role"] == "admin":
        return render_template("admin.html")

    return render_template("student.html")



@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
