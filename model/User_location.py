from flask_sqlalchemy import SQLAlchemy
from User import Users
db = SQLAlchemy()

class User_location(db.Model):
    id = db.Column(db.Integer, db.ForeignKey('Users.id'))
    location = db.Column(db.String(100))
    city = db.Column(db.String(100))
    state = db.Column(db.String(100))





