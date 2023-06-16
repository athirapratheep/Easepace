from flask import Flask, render_template , request , redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
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
migrate = Migrate(app,db)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            session["user_id"] = user.id
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

@app.route("/logout")
def logout():
    session.pop("user_id", None)
    return redirect(url_for("home"))

@app.route("/index",methods=["GET","POST"])
def marks():
    marks_pred=0
    study_hour_list={}
    data={}
    avghrs=0
    goalto_be=0
    if request.method=="POST":
        hrs = request.form["hrs"]
        goals=request.form["goalto"]
        if hrs and goals:
            marks_pred, goaltobe = m.marks_prediction(hrs, goals)
        else:
            marks_pred = 0
            goaltobe = None

        study_hours = request.form["hrs"]
        data={}
        try:
            with open("student_data.txt", "rb") as file:
                data = pickle.load(file)
        except FileNotFoundError:
            data = {}
        except EOFError:
            data = {}     

        # Check if there are already 5 entries in the data
        if len(data) == 7:
            oldest_date = min(data.keys())
            data.pop(oldest_date)

        # Prompt the user for study hours
        current_date = datetime.date.today().strftime("%Y-%m-%d")

        # Add new entry to data
        data[current_date] = study_hours

        # Save data to file
        with open("student_data.txt", "wb") as file:
            pickle.dump(data, file)

        for value in data.values():
            avghrs=avghrs+float(value)

        avghrs=avghrs/len(data)
        

        goaltobe[0]=(float(goaltobe[0])-float(avghrs))* len(data)    
        goalto_be=round(goaltobe[0],2)
        avghrs=round(avghrs,2)    
        
        # Pass study hour data as a list to the template
        study_hour_list = data
    return render_template("index.html",my_marks = avghrs ,goal_tobe = goalto_be,study_hour_data=study_hour_list)

@app.route("/materials", methods = ["GET", "POST"])
def materials():
    material={}
    notes={}
    if request.method=="POST":
        subject = request.form["subject"]
        material,notes= ma.scrape_youtube_videos(subject)
    links_list = [{'title': title, 'url': url} for title, url in material.items()]
    notes_list = [{'title': title, 'url': url} for title, url in notes.items()]
    return render_template('sub.html', links=links_list,note_links=notes_list)

  
  
if __name__ == "__main__":
    app.run(debug=True)
