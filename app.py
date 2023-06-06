from flask import Flask, render_template , request

import marks as m

app = Flask(__name__)


@app.route("/",methods=["GET","POST"])
def marks():
    marks_pred=0
    if request.method=="POST":
        hrs = request.form["hrs"]
        marks_pred= m.marks_prediction(hrs)
    return render_template("index.html",my_marks = marks_pred)

"""
@app.route("/sub", methods = ['POST'])
def submit():
    if request.method == "POST":
        name = request.form["username"]

    return render_template("sub.html",n=name)  

"""    
  
if __name__ == "__main__":
    app.run(debug=True)