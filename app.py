from flask import Flask, render_template , request

import marks as m
import materials as ma

app = Flask(__name__)


@app.route("/predict",methods=["GET","POST"])
def marks():
    marks_pred=0
    if request.method=="POST":
        hrs = request.form["hrs"]
        marks_pred= m.marks_prediction(hrs)
    return render_template("index.html",my_marks = marks_pred)

@app.route("/materials", methods = ["GET", "POST"])
def materials():
    material={}
    if request.method=="POST":
        subject = request.form["subject"]
        material= ma.scrape_youtube_videos(subject)
    links_list = [{'title': title, 'url': url} for title, url in material.items()]
    return render_template('index.html', links=links_list)

  
  
if __name__ == "__main__":
    app.run(debug=True)