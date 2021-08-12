from os import environ
from flask import Flask, render_template, request, session, redirect
from flask_sqlalchemy import SQLAlchemy
import sys
import logging

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SECRET_KEY"] = "mkciufn49infceii499923@(N#"
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URL') or 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
app.config["SESSION_TYPE"] = "filesystem"


db = SQLAlchemy(app)

app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)

#Declares the tasks model
class Tasks(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), index = True, unique = False)
    task = db.Column(db.String(100), index = True, unique = False)
    start = db.Column(db.String(100), index = True, unique = False)
    end = db.Column(db.String(100), index = True, unique = False)

@app.route("/")
def login_page():
    """Renders login page"""
    return render_template("login.html") 

@app.route("/main")
def main():
    """Renders main page, by selecting all tasks a user needs to complete."""

    tasks = Tasks.query.all()

    final_results = []
    
    for task in tasks:
        if task.name == session["name"]:
            final_results.append((task.task, task.start, task.end))

    return render_template("main.html", final_results = final_results)

@app.route("/login")
def main_page(): 
    """"Sends user to the main page, with the list of all their tasks to be completed, 
    if the user provides their name. Otherwise, send users back to login page."""

    name = request.args.get("name")
    session["name"] = name
    if name != "": 
        return redirect("/main")
    else: 
        return redirect("/")

@app.route("/input")
def input():
    """Allows user to input new task into their table. Does not allow users to input an empty string as the task name.
    If this fails, render error.html."""

    if request.args.get("inputname") != "":
        name = session["name"]
        task = request.args.get("inputname")
        start = request.args.get("inputstart")
        end = request.args.get("inputend")

        db.session.add(Tasks(name = name, task = task, start = start, end = end))
         
        try:
            db.session.commit()
            return redirect("/main") 

        except:
            db.session.rollback()
            return render_template("error.html")

    else: 
        return redirect("/main")            


@app.route("/delete")
def delete():
    """Deletes task from a user's table, given the name of the task a user wants to delete. If this fails, 
    render error.html."""

    tasks = Tasks.query.filter(Tasks.name == session["name"], Tasks.task == request.args.get("taskname")).all()

    for task in tasks:
        db.session.delete(task)

        try:
            db.session.commit()
            
        except:
            db.session.rollback()
            return render_template("error.html")
    
    return redirect("/main")

@app.route("/logout")
def logout():
    """Logs out user, then sends user to log out page"""

    session["name"] = None 
    return render_template("logout.html")

if __name__ == '__main__':
    app.run(port=8000)
