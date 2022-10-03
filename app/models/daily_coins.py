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
        data = DailyCoins.query.order_by(DailyCoins.id.desc()).limit(10).all()
        data.reverse()
        return data

    def get_week_save(self):
        data = DailyCoins.query.order_by(DailyCoins.id.desc()).limit(70).all()
        data.reverse()
        return data

    def daily_coin_save(self, data=CmcApi().get_all(), date=datetime.date.today()):
        for coin in data:
            coin_save = DailyCoins(name=coin['name'], date_add=date, value=coin['quote']['EUR']['price'],
                                   percent_change_24h=coin['quote']['EUR']['percent_change_24h'],
                                   symbol=coin['symbol'])
            db.session.add(coin_save)
            db.session.commit()
            print('Daily date saved')
        check = DailyCoins.query.all()
        last_coin = DailyCoins.query.order_by(DailyCoins.id.desc()).first()
<<<<<<< HEAD
        if len(check) >= 170:
=======
        if len(check) >= 100:
>>>>>>> 52e7054c0c700fe0c041a2996f991f20cbb2254a
            for i in range((last_coin.id - len(check)), (last_coin.id - len(check)) + 30):
                coin_delete = delete(DailyCoins).where(DailyCoins.id == i)
                db.session.execute(coin_delete)
                db.session.commit()
                print('Daily more then 10 days deleted')

    def __repr__(self):
        return '<daily_saved %r>' % self.name
