from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    blood_group = db.Column(db.String(3))
    user_type = db.Column(db.String(100))
    query_class = db.Query

    def __repr__(self):
        return '<User %r>' % self.name
