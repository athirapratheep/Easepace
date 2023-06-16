from flask import Flask, render_template , request , redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import current_user, LoginManager, UserMixin, login_required,login_user
from flask_migrate import Migrate
from flask import flash
import marks as m
import materials as ma

import datetime
import pickle

app = Flask(__name__)
app.secret_key = "afaafaefaagaegeg"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///auth.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

login_manager.init_app(app)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    student_data = db.relationship('StudentData', backref='user', lazy=True)

class StudentData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    study_hours = db.Column(db.Float, nullable=False)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("marks"))

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)  # Perform the login
            return redirect(url_for("marks"))

        flash("Invalid email or password. Please try again.")
        return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        email = request.form.get("email")

        user = User.query.filter_by(username=username).first()
        if user:
            flash("Username already exists", "error")
            return redirect(url_for("signup"))

        new_user = User(username=username, password=generate_password_hash(password), email=email)
        db.session.add(new_user)
        db.session.commit()

        flash("Sign up successful! Please login.", "success")
        return redirect(url_for("login"))

    return render_template("signup.html")

@app.route("/logout", methods=["GET","POST"])
def logout():

    if request.method == "POST":
        session.pop("user_id", None)
        session.clear()
        return redirect(url_for("home"))

@app.route("/index", methods=["GET", "POST"])
@login_required
def marks():
    marks_pred = 0
    study_hour_list = []
    avghrs = 0
    goalto_be = 0

    if request.method == "POST":
        hrs = request.form["hrs"]
        goals = request.form["goalto"]

        if hrs and goals:
            marks_pred, goaltobe = m.marks_prediction(hrs, goals)
        else:
            marks_pred = 0
            goaltobe = None

        study_hours = request.form["hrs"]

        current_date = datetime.date.today()

        user_id = current_user.id

       # Check if an entry already exists for the current user and date
        existing_entry = StudentData.query.filter_by(user_id=user_id, date=current_date).first()
        if existing_entry:
            existing_entry.study_hours = study_hours  # Update the study_hours value
            db.session.commit()
        else:
            # Delete the oldest entry if the user already has 7 records
            user_data_count = db.session.query(func.count(StudentData.id)).filter_by(user_id=user_id).scalar()
            if user_data_count >= 7:
                oldest_entry = StudentData.query.filter_by(user_id=user_id).order_by(StudentData.date).first()
                db.session.delete(oldest_entry)
                db.session.commit()

            student_data = StudentData(user_id=user_id, date=current_date, study_hours=study_hours)
            db.session.add(student_data)
            db.session.commit()


        # Retrieve all student data for the user
        user_data = StudentData.query.filter_by(user_id=user_id).all()

        for data in user_data:
            avghrs += float(data.study_hours)

        avghrs = avghrs / len(user_data)
        goaltobe = (float(goaltobe) - float(avghrs)) * len(user_data)
        goalto_be = round(goaltobe, 2)
        avghrs = round(avghrs, 2)

        # Convert StudentData objects to a list of dictionaries
        study_hour_list = [
            {
                "date": data.date.strftime("%Y-%m-%d"),
                "study_hours": data.study_hours
            }
            for data in user_data
        ]

    return render_template("index.html", my_marks=avghrs, goal_tobe=goalto_be, study_hour_data=study_hour_list)

@app.route("/materials", methods=["GET", "POST"])
@login_required
def materials():
    material = {}
    notes = {}
    if request.method == "POST":
        subject = request.form["subject"]
        material, notes = ma.scrape_youtube_videos(subject)
    links_list = [{'title': title, 'url': url} for title, url in material.items()]
    notes_list = [{'title': title, 'url': url} for title, url in notes.items()]
    return render_template('sub.html', links=links_list, note_links=notes_list)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
