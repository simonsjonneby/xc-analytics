import csv
import os

from flask import Flask, render_template, request
from models import *

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

def main():
    f = open("data/transform/results.csv")
    reader = csv.reader(f)
    for row, rank, bib, athlete_id, athlete_name, athlete_year_born, athlete_nation, time, diff_time, fis_points, event, event_id, place, date, result_type, season, technique, gender, individual_team, sprint_distance, distance, points in reader:
        result = Results(
        row=row,
        rank=rank,
        bib=bib,
        athlete_id=athlete_id,
        athlete_name = athlete_name,
        athlete_year_born = athlete_year_born,
        athlete_nation = athlete_nation,
        time=time,
        diff_time=diff_time,
        fis_points=fis_points,
        event = event,
        event_id = event_id,
        place = place,
        date = date,
        result_type = result_type,
        season = season,
        technique = technique,
        gender = gender,
        individual_team = individual_team,
        sprint_distance = sprint_distance,
        distance = distance,
        points = points
        )
        db.session.add(result)
        print(f"Added result {rank} with bib: {bib} athlete :{athlete_id}, time: {time}")
    db.session.commit()

if __name__ == "__main__":
    with app.app_context():
        main()
