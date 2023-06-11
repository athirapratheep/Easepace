from flask import Flask, render_template , request

import marks as m
import materials as ma

import datetime
import pickle

app = Flask(__name__)


@app.route("/",methods=["GET","POST"])
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