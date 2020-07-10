import os
import psycopg2
from flask import Flask, session, render_template, request, jsonify, redirect, url_for
from flask_session import Session
from sqlalchemy import create_engine, and_
from sqlalchemy.orm import scoped_session, sessionmaker
from models import *
from flask_table import Table, Col, LinkCol



app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)
engine = create_engine(app.config["SQLALCHEMY_DATABASE_URI"])
db = scoped_session(sessionmaker(bind=engine))

# Session variables
user_id = []

@app.route("/")
def index():
    if session.get("user_id") is None or session.get("user_id")==[]:
        session["user_id"] = []
        return render_template("index.html")
    else:
        return redirect(url_for('welcome'))

@app.route("/logout")
def logout():
    session["user_id"] = []
    return render_template("index.html")


@app.route("/register"  )
def register():
    return render_template("register.html")

@app.route("/registered", methods=["POST"])
def registered():
    username=request.form.get("username")
    user = Users(
    firstname=request.form.get("firstname"),
    lastname=request.form.get("lastname"),
    email=request.form.get("email"),
    username=request.form.get("username"),
    password=request.form.get("password")
    )
    db.add(user)
    db.commit()
    return render_template("registered.html", username=username)

@app.route("/login",methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    users = Users.query.filter(and_(Users.username == username, Users.password == password)).first()

    if users == None:
        return render_template("error.html")
    session["user_id"] = users.id
    return redirect(url_for('welcome'))

@app.route("/welcome", methods=["POST","GET"])
def welcome():
    if session.get("user_id") is None or session.get("user_id")==[]:
        session["user_id"] = []
        return redirect(url_for('index'))

    """Show latest results in a table"""
    class ItemTable(Table):
        rank = Col('Rank')
        athlete_id = LinkCol("Athlete", "athlete", url_kwargs=dict(athlete_id='athlete_id'))
        athlete_name = Col('Name')
        event = Col('Event')
        date = Col('Date')
        diff_time = Col('Diff time')
    # Or, more likely, load items from your database with something like
    results_women = Results.query.filter_by(gender='Women')
    results_men = Results.query.filter_by(gender='Men')

    # Populate the table
    table_women = ItemTable(results_women, classes=["table table-bordered table-striped"])
    table_men = ItemTable(results_men, classes=["table table-bordered table-striped"])
    return render_template("welcome.html", table_women = table_women, table_men = table_men)


@app.route("/athlete/<athlete_id>", methods=["GET","POST"])
def athlete(athlete_id):
    if session.get("user_id") is None or session.get("user_id")==[]:
        session["user_id"] = []
        return redirect(url_for('index'))

    """Lists details about a single athlete."""

    wins = Results.query.filter(Results.rank == 1 , Results.athlete_id == athlete_id, Results.points == '1').count()
    podiums = Results.query.filter(Results.rank <= 3 , Results.athlete_id == athlete_id, Results.points == '1').count()
    athletes = Athletes.query.filter_by(id = athlete_id).first()
    if athletes is None:
        return render_template("error.html")


    return render_template("athlete.html", athletes=athletes, wins=wins, podiums=podiums)
