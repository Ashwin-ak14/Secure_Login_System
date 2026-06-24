from flask import Flask, render_template_string, request, redirect, session, url_for
from flask_bcrypt import Bcrypt
import sqlite3
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)
bcrypt = Bcrypt(app)

# Database Initialization
def init_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

init_db()

# HTML Template
BASE_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Secure Login System</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #f4f4f9;
            margin: 50px;
        }
        .container {
            max-width: 400px;
            margin: auto;
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0px 4px 8px rgba(0,0,0,0.1);
        }
        input {
            width: 100%;
            padding: 10px;
            margin: 8px 0;
            box-sizing: border-box;
        }
        button {
            width: 100%;
            padding: 10px;
            background: #28a745;
            color: white;
            border: none;
            cursor: pointer;
        }
        button:hover {
            background: #218838;
        }
        .error {
            color: red;
        }
        .success {
            color: green;
        }
        a {
            text-decoration: none;
        }
    </style>
</head>
<body>
<div class="container">
{{ content|safe }}
</div>
</body>
</html>
"""

# Home Page
@app.route("/")
def home():
    if "username" in session:
        content = f"""
        <h2>Welcome, {session['username']}!</h2>
        <p>You are logged in successfully.</p>
        <a href="/logout">
            <button style="background:#dc3545;">Logout</button>
        </a>
        """
        return render_template_string(BASE_TEMPLATE, content=content)

    return redirect(url_for("login"))

# Registration
@app.route("/register", methods=["GET", "POST"])
def register():
    message = ""
    css_class = "error"

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        if not username or not password:
            message = "All fields are required."

        elif len(password) < 8:
            message = "Password must be at least 8 characters."

        else:
            password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

            try:
                conn = sqlite3.connect("users.db")
                cursor = conn.cursor()

                cursor.execute(
                    "INSERT INTO users(username,password_hash) VALUES (?,?)",
                    (username, password_hash)
                )

                conn.commit()
                conn.close()

                message = "Registration successful. Please login."
                css_class = "success"

            except sqlite3.IntegrityError:
                message = "Username already exists."

    content = f"""
    <h2>Register</h2>
    <p class="{css_class}">{message}</p>

    <form method="POST">
        <input type="text" name="username" placeholder="Username" required>

        <input type="password" name="password"
               placeholder="Password" required>

        <button type="submit">Register</button>
    </form>

    <p>Already have an account?
    <a href="/login">Login</a></p>
    """

    return render_template_string(BASE_TEMPLATE, content=content)

# Login
@app.route("/login", methods=["GET", "POST"])
def login():
    message = ""

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT password_hash FROM users WHERE username=?",
            (username,)
        )

        user = cursor.fetchone()
        conn.close()

        if user and bcrypt.check_password_hash(user[0], password):
            session["username"] = username
            return redirect(url_for("home"))

        else:
            message = "Invalid username or password."

    content = f"""
    <h2>Login</h2>

    <p class="error">{message}</p>

    <form method="POST">
        <input type="text" name="username"
               placeholder="Username" required>

        <input type="password" name="password"
               placeholder="Password" required>

        <button type="submit">Login</button>
    </form>

    <p>Don't have an account?
    <a href="/register">Register</a></p>
    """

    return render_template_string(BASE_TEMPLATE, content=content)

# Logout
@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("login"))

# Run App
if __name__ == "__main__":
    app.run(debug=True)
