from unicodedata import decimal
from app.models.coin import Coin
from app.models.daily_coins import DailyCoins
from app.views_class.Read import Read


class Delete():

    def __init__(self, current_user, db, form):
        self.current_user = current_user
        self.all_data = DailyCoins().get_last_save()
        self.daily_coins_names = Read()
        self.coins = Coin.query.filter_by(user_id=current_user.id).all()
        self.db = db
        self.coins_quantity = {}
        self.form = form
        self.errors = ''
        self.redirect = None

    def get_coins_quantity(self):
        for i in self.coins:
            self.coins_quantity[i.id] = i.quantity

    def set_up(self):
        self.get_coins_quantity()
        self.form.name.choices = [(i.id, i.name) for i in self.coins]

    def delete_coins(self):
        new_coin = Coin.query.filter_by(id=self.form.name.data, user_id=self.current_user.id).first()
        self.form.quantity.data = float(self.form.quantity.data)
        if new_coin.quantity > self.form.quantity.data:
            new_coin.quantity -= self.form.quantity.data
            self.db.session.commit()
            self.redirect = True
        elif new_coin.quantity == self.form.quantity.data:
            self.db.session.delete(new_coin)
            self.db.session.commit()
            self.redirect = True
        else:
            self.errors = f'Vous n\'avez pas assez de cette monnaie, ils vous reste {new_coin.quantity} {new_coin.name}'
            self.redirect = False
        return self.errors, self.coins_quantity, self.daily_coins_names, self.redirect

    def view_delete_coins(self):
        return self.daily_coins_names, self.coins_quantity
