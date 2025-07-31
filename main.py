import os
from dotenv import load_dotenv
from flask import Flask, flash, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from werkzeug.security import generate_password_hash, check_password_hash

load_dotenv()

user = os.environ.get("DB_USER")
password = os.environ.get("DB_PASSWORD")
host = os.environ.get("DB_HOST")
port = os.environ.get("DB_PORT")
database = os.environ.get("DB_NAME")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{user}:{password}@{host}:{port}/{database}?sslmode=require"
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique = True, nullable = False)
    password = db.Column(db.String(512), nullable = False)


@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/")
@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        user = User.query.filter_by(email=email).first()

        if user:
            
            if check_password_hash(user.password, password):
                return redirect('/home')

            else:
                flash("Incorrect Password")
        else:
            flash("User Not Found")

    return render_template('login.html')


@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        new_user = User(email=email, password=generate_password_hash(password))
        
        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect('/login')
        
        except Exception as e:
            return f"Error: {e}"

    else:
        return render_template('register.html')

@app.route("/db-test")
def db_test():
    try:
        db.session.execute(text('SELECT 1')).scalar()
        return "Database connected sucessfully"
    except Exception as e:
        return f"Database connection failed: {e}"

with app.app_context():
    db.create_all()