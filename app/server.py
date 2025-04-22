#!/home/ubuntu/webapp/venv/bin/python3
from flask import Flask, request, render_template, render_template_string, redirect, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "supersecretkey")  # Use environment variable for secret key

def get_db_connection():
    conn = sqlite3.connect("/app/database.db")  # Use /tmp for AWS Lambda compatibility
    conn.row_factory = sqlite3.Row
    return conn

# Initialize a simple table
with get_db_connection() as conn:
    conn.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT, email TEXT)")

    # Insert user if it doesn't already exist
    conn.execute("""
        INSERT OR IGNORE INTO users (username, password, email)
        VALUES ('admin', 'superman', 'maintenance.info.1234@gmail.com');
    """)

    conn.commit()

@app.route("/")
def home():
    return redirect("/login")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        email = request.form["email"]
        conn = get_db_connection()
        query = f"INSERT INTO users (username, password, email) VALUES ('{username}', '{password}', '{email}')"  # SQL Injection vulnerability
        conn.execute(query)
        conn.commit()
        conn.close()
        return "Signup successful! <a href='/login'>Login here</a>"
    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        conn = get_db_connection()
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"  # SQL Injection vulnerability
        user = conn.execute(query).fetchone()
        conn.close()
        if user:
            session["user"] = username
            return redirect("/dashboard")
        return "Invalid credentials!"  # No rate limiting (brute-force vulnerability)
    return render_template("login.html")

@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if "user" not in session:
        return redirect("/login")

    user = session["user"]
    message = ""

    # Get email from the database
    conn = get_db_connection()
    query = "SELECT email FROM users WHERE username = ?"
    email = conn.execute(query, (user,)).fetchone()
    conn.close()


    # If the user exists in the database, get their email, otherwise set to None
    email = email["email"] if email else None

    if request.method == "POST" and user == "admin":
        if "file" in request.files:
            uploaded_file = request.files["file"]
            if uploaded_file.filename:
                upload_dir = os.path.join(os.getcwd(), "uploads")
                os.makedirs(upload_dir, exist_ok=True)
                uploaded_file.save(os.path.join(upload_dir, uploaded_file.filename))
                message = "File uploaded successfully!"
            else:
                message = "No file selected."
        else:
            message = "No file part found in request."
    
    return render_template("dashboard.html", user=user, message=message, email=email)



@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.getenv("PORT", 80)), debug=True)  # Run on all interfaces for AWS

