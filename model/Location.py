from flask_sqlalchemy import SQLAlchemy
from User import Users
db = SQLAlchemy()

class Location(db.Model):
    id = db.Column(db.Integer, db.ForeignKey('User.id'))
    location = db.Column(db.String(100))
    city = db.Column(db.String(100))
    state = db.Column(db.String(100))





