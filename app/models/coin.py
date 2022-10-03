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
        """
        The get_user_coin function is used to retrieve all the coins that belong to a specific user.
        It takes in the user_id as an argument and returns a list of coins.
        :param self: Access variables that belongs to the class
        :param user_id: Filter the query and only return the coins that belong to a specific user
        :return: The coin object for the user_id passed in
        """
        return Coin.query.filter_by(user_id=user_id).all()

    def __repr__(self):
        return '<Coin %r>' % self.name
