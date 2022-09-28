from . import db
import datetime


class Coin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), nullable=False)
    quantity = db.Column(db.FLOAT, nullable=False)
    value = db.Column(db.FLOAT, nullable=False)
    date_added = db.Column(db.DateTime, nullable=False, default=datetime.date.today())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, name, quantity, value, user_id):
        self.name = name
        self.quantity = quantity
        self.value = value
        self.user_id = user_id

    def get_user_coin(self, user_id):
        return Coin.query.filter_by(user_id=user_id).all()

    def __repr__(self):
        return '<Coin %r>' % self.name
