from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

class Tour(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    waypoints = db.relationship('Waypoint', backref='tour', lazy='dynamic')

class Waypoint(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    script = db.Column(db.Text())
    content = db.Column(db.Text())
    tour_id = db.Column(db.Integer, db.ForeignKey('tour.id'))

