from Models.db import db


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Names = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    UserId = db.Column(db.String(100), unique=True)
    present=db.Column(db.String(100),default="false")
    date=db.Column(db.String(100), default="now")
    def __init__(self, names, email,userId):
        self.email = email
        self.Names = names
        self.UserId = userId



