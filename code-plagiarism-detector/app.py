from flask import Flask, render_template, request, redirect, url_for, session, flash, g
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from plagiarism.preprocess import preprocess
from plagiarism.similarity import calculate_similarity, highlight_code
from plagiarism.ast_logic import calculate_ast_similarity
import os

app = Flask(__name__)
app.secret_key = 'super_secret_key_for_demo_only' # Change this in production
DATABASE = 'database.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    with app.app_context():
        db = get_db()
        db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        db.commit()

init_db()

@app.route("/")
def index():
    return render_template("landing.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        
        hashed_password = generate_password_hash(password)
        
        try:
            db = get_db()
            db.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                       (username, email, hashed_password))
            db.commit()
            flash("Account created! Please log in.", "success")
            return redirect(url_for("login"))
        except sqlite3.IntegrityError:
            flash("Username or email already exists.", "error")
            
    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email_or_username = request.form.get("email") # Using 'email' field for both/email
        password = request.form["password"]
        
        db = get_db()
        # Allow login by username OR email
        user = db.execute("SELECT * FROM users WHERE email = ? OR username = ?", 
                          (email_or_username, email_or_username)).fetchone()
        
        if user and check_password_hash(user["password"], password):
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            return redirect(url_for("detector"))
        else:
            flash("Invalid credentials. Please try again.", "error")
            
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

@app.route("/detector", methods=["GET", "POST"])
def detector():
    if "user_id" not in session:
        flash("Please log in to use the detector.", "error")
        return redirect(url_for("login"))

    results = []
    codes = []

    if request.method == "POST":
        codes = request.form.getlist("codes[]")
        use_ast = request.form.get("use_ast") # Checkbox value

        for i in range(len(codes)):
            for j in range(i + 1, len(codes)):
                clean1 = preprocess(codes[i])
                clean2 = preprocess(codes[j])

                if use_ast:
                    # Try AST similarity
                    ast_score = calculate_ast_similarity(clean1, clean2)
                    
                    # Check for syntax error (-1.0)
                    if ast_score >= 0:
                         score = ast_score
                         status = "AST Analysis: " + similarity_label(score)
                    else:
                         # Fallback if syntax error
                         score = calculate_similarity(clean1, clean2)
                         status = "Syntax Error (Fallback): " + similarity_label(score)
                else:
                    score = calculate_similarity(clean1, clean2)
                    status = similarity_label(score)
                    
                h1, h2 = highlight_code(clean1, clean2)
                
                results.append({
                    "pair_name": f"Code {i+1} vs Code {j+1}",
                    "index1": i + 1,
                    "index2": j + 1,
                    "score": score,
                    "status": status,
                    "h1": h1,
                    "h2": h2
                })

    return render_template(
        "detector.html",
        results=results,
        codes=codes if request.method == "POST" else []
    )



def similarity_label(score):
    if score >= 85:
        return "High Plagiarism"
    elif score >= 50:
        return "Moderate Plagiarism"
    else:
        return "Low Plagiarism"


if __name__ == "__main__":
    app.run(debug=True)
