from flask import render_template
from flask_login import login_required
import pprint
from app.models.coin import Coin
from app.models.daily_coins import DailyCoins


class Read():

    def __init__(self, current_user=None):
        self.current_user = current_user
        self.all_data = DailyCoins().get_last_save()
        self.user_data = []
        self.coins_names = []
        self.today_price = 0
        self.my_price = 0
        if self.current_user != None:
            self.coins = Coin.query.filter_by(user_id=current_user.id).all()

    def get_saved_coin_names(self):
        saved_coins_names = [saved_coins.name for saved_coins in self.all_data]
        return saved_coins_names

    def unique_coins_names(self):
        for i in self.coins:
            self.coins_names.append(i.name)
            self.my_price += i.value * i.quantity
        return list(set(self.coins_names))

    def get_user_data(self):
        unique = self.unique_coins_names()
        for d in self.all_data:
            if d.name in unique:
                self.user_data.append(d)
        return self.user_data

    @login_required
    def user_coins(self):
        data = self.get_user_data()
        for i in self.coins:
            for d in data:
                if i.name == d.name:
                    self.today_price += (d.value * i.quantity)
        all_benef = round(self.today_price - self.my_price, 4)
        return self.coins, data, all_benef
