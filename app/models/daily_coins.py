import datetime

from sqlalchemy import delete

from . import db
from .. import CmcApi


class DailyCoins(db.Model):
    __tablename__ = 'daily_coins'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), nullable=False)
    date_add = db.Column(db.DateTime, default=datetime.date.today(), nullable=False)
    value = db.Column(db.FLOAT, nullable=False)
    percent_change_24h = db.Column(db.FLOAT, nullable=False)
    symbol = db.Column(db.String(25), nullable=False)

    def get_last_save(self):
        """
        The get_last_save function returns the last 10 coins that have been saved to the database.
        The data is returned in reverse order so that the most recent coin is first.we will use it in home template and to create
        and compare user coins
        :param self: Access variables that belongs to the class
        :return: The last 10 rows of the dailycoins table
        """

        data = DailyCoins.query.order_by(DailyCoins.id.desc()).limit(10).all()
        data.reverse()
        return data

    def get_week_save(self):
        """
        The get_week_save function returns the last 70 coins saved in the database.
        The data is returned in reverse order so that it can be displayed on a graph.
        :param self: Access variables that belongs to the class
        :return: The last 70 rows of data from the dailycoins table
        """

        data = DailyCoins.query.order_by(DailyCoins.id.desc()).limit(70).all()
        data.reverse()
        return data

    def daily_coin_save(self, data=CmcApi().get_all(), date=datetime.date.today()):
        """
        The daily_coin_save function saves the daily coins data to the database.
        It takes two arguments, data and date. Data is a list of dictionaries containing all coin information from CMC API.
        Date is a datetime object that contains today's date.
        and it deletes the rows if the length of the table is more than 140 row how matches 2 weeks of auto save
        :param self: Allow the function to reference attributes or methods of the class
        :param data=CmcApi().get_all(): Get all the data from cmcapi()
        :param date=datetime.date.today(): Set the date of the coin
        :return: A string with the date of the last saved coin
        """
        for coin in data:
            coin_save = DailyCoins(name=coin['name'], date_add=date, value=coin['quote']['EUR']['price'],
                                   percent_change_24h=coin['quote']['EUR']['percent_change_24h'],
                                   symbol=coin['symbol'])
            db.session.add(coin_save)
            db.session.commit()
            print('Daily date saved')
        check = DailyCoins.query.all()
        last_coin = DailyCoins.query.order_by(DailyCoins.id.desc()).first()
        if len(check) >= 170:
            for i in range((last_coin.id - len(check)), (last_coin.id - len(check)) + 30):
                coin_delete = delete(DailyCoins).where(DailyCoins.id == i)
                db.session.execute(coin_delete)
                db.session.commit()
                print('Daily more then 20 days deleted')

    def __repr__(self):
        return '<daily_saved %r>' % self.name
