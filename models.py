import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Users(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String, nullable=False)
    lastname = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)

class Athletes(db.Model):
    __tablename__ = "athletes_orm"
    row = db.Column(db.Integer, nullable = True)
    id = db.Column(db.Integer, primary_key = True)
    athlete = db.Column(db.String, nullable = True)
    year_born = db.Column(db.String, nullable = True)
    nation = db.Column(db.String, nullable = True)

class Results(db.Model):
    __tablename__ = "results_orm"
    row = db.Column(db.Integer, primary_key=True)
    rank = db.Column(db.Integer, nullable=False)
    bib = db.Column(db.String, nullable=True)
    athlete_id = db.Column(db.Integer, nullable=True)
    athlete_name = db.Column(db.String, nullable=True)
    athlete_year_born = db.Column(db.String, nullable=True)
    athlete_nation = db.Column(db.String, nullable=True)
    time = db.Column(db.String, nullable=True)
    diff_time = db.Column(db.String, nullable=True)
    fis_points = db.Column(db.String, nullable=True)
    event = db.Column(db.String, nullable=True)
    event_id = db.Column(db.Integer, nullable=True)
    place = db.Column(db.String, nullable=True)
    date = db.Column(db.Date, nullable=True)
    result_type = db.Column(db.String, nullable=True)
    season = db.Column(db.Integer, nullable=True)
    technique = db.Column(db.String, nullable=True)
    gender = db.Column(db.String, nullable=True)
    individual_team = db.Column(db.String, nullable=True)
    sprint_distance = db.Column(db.String, nullable=True)
    distance = db.Column(db.String, nullable=True)
    points = db.Column(db.String, nullable=True)
