import os
import psycopg2
from flask import Flask, session, render_template, request, jsonify, redirect, url_for
from flask_session import Session
from sqlalchemy import create_engine, and_, func, select
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
    #results_women = Results.query.filter_by(gender='Women')
    results_women = db.execute("select * from results_orm where date = (select max(date) from results_orm where gender='Women') and points='1' and gender='Women';")
    results_men = db.execute("select * from results_orm where date = (select max(date) from results_orm where gender='Men') and points='1' and gender='Men';")

    # Populate the table
    table_women = ItemTable(results_women, classes=["table table-bordered table-striped"])
    table_men = ItemTable(results_men, classes=["table table-bordered table-striped"])
    return render_template("welcome.html", table_women = table_women, table_men = table_men)


@app.route("/athlete/<athlete_id>", methods=["GET","POST"])
def athlete(athlete_id):
    if session.get("user_id") is None or session.get("user_id")==[]:
        session["user_id"] = []
        return redirect(url_for('index'))

    """Table with latest results of athlete"""

    class ItemTable(Table):
        event = Col('Event')
        rank = Col('Rank')
        date = Col('Date')
        place = Col('Place')

    results_athlete = Results.query.filter_by(athlete_id=athlete_id)
        # Populate the table
    table_athlete = ItemTable(results_athlete, classes=["table table-bordered table-striped"])



    """Lists details and KPI:s about a single athlete."""

    wins = Results.query.filter(Results.rank == 1 , Results.athlete_id == athlete_id, Results.points == '1').count()
    podiums = Results.query.filter(Results.rank <= 3 , Results.athlete_id == athlete_id, Results.points == '1').count()
    starts = Results.query.filter(Results.athlete_id == athlete_id, Results.points == '1').count()
    avg_pos = db.execute("SELECT CAST(avg(rank) AS DECIMAL (3,1)) FROM results_orm WHERE athlete_id = :athlete_id and points = '1'", {"athlete_id": athlete_id}).fetchone()
    avg_pos_sprint = db.execute("SELECT CAST(avg(rank) AS DECIMAL (3,1)) FROM results_orm WHERE athlete_id = :athlete_id and points = '1' and sprint_distance='Sprint'", {"athlete_id": athlete_id}).fetchone()
    avg_pos_distance = db.execute("SELECT CAST(avg(rank) AS DECIMAL (3,1)) FROM results_orm WHERE athlete_id = :athlete_id and points = '1' and sprint_distance='Distance'", {"athlete_id": athlete_id}).fetchone()
    table_avg_pos_place = db.execute("select place, CAST(avg(rank) AS DECIMAL (12,2))  as avg_pos from results_orm where points='1' and athlete_id= :athlete_id group by place, athlete_id order by avg_pos", {"athlete_id": athlete_id}).fetchall()
    athletes = Athletes.query.filter_by(id = athlete_id).first()


    class PlaceTable(Table):
        place = Col('Place')
        avg_pos = Col('Average rank')

    table_place = PlaceTable(table_avg_pos_place, classes=["table table-bordered table-striped"])


    if athletes is None:
        return render_template("error.html")

    return render_template("athlete.html",
        table_athlete = table_athlete,
        table_place = table_place,
        athletes=athletes,
        starts = starts,
        wins=wins,
        podiums=podiums,
        avg_pos=avg_pos[0],
        avg_pos_sprint = avg_pos_sprint[0],
        avg_pos_distance = avg_pos_distance[0],
        favourite_place = table_avg_pos_place[0][0]
        )
