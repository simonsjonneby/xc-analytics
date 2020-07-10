import csv
import os

from flask import Flask, render_template, request
from models import *

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

def main():
    f = open("data/transform/athletes.csv")
    reader = csv.reader(f)
    for row, id, athlete, year_born, nation in reader:
        athletes = Athletes(
        row = row,
        id = id,
        athlete = athlete,
        year_born = year_born,
        nation = nation
        )
        db.session.add(athletes)
        print(f"Added athlete {athlete} with code: {id} from :{nation}")
    db.session.commit()

if __name__ == "__main__":
    with app.app_context():
        main()
