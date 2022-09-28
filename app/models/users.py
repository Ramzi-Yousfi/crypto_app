from . import db 
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    coins = db.relationship('Coin', backref='owner', lazy='dynamic')



        
    def __repr__(self):
        return '<User %r>' % self.username

    def __str__(self):
        return self.username
