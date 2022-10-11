from app.models.coin import Coin
from app.models.daily_coins import DailyCoins


class Delete():

    def __init__(self, current_user, db, form):
        self.current_user = current_user
        self.all_data = DailyCoins().get_last_save()
        self.coins = Coin.query.filter_by(user_id=current_user.id).all()
        self.db = db
        self.coins_quantity = {}
        self.form = form
        self.errors = ''
        self.redirect = None

    def get_coins_quantity(self):
        """
        The get_coins_quantity function returns a dictionary of user coins quantity with the id  .
        The keys are coin ids and values are their quantity.
        :param self: Access variables that belongs to a class
        :return: set self.coins_quantity
        """
        for i in self.coins:
            self.coins_quantity[i.id] = i.quantity

    def set_up(self):
        """
        The set_up function is called before the form is validated.
        It populates the form with a list of coins and their quantities,
        and sets up a list of coin ids to be used in validation.

        :param self: Access variables that belongs to the class
        :return: set self.form.name.choices

        """
        self.get_coins_quantity()
        self.form.name.choices = [(i.id, i.name) for i in self.coins]

    def delete_coins(self):
        """
        The delete_coins function is used to delete coins from the database. For deferment scenarios.
        case coins quantity is 0, the coin is deleted from the database.
        case coins quantity is not 0, the coin quantity is updated in the database.
        It is called in POST method.
        :param self: Access variables that belongs to the class
        :return: The redirect to the list_coins function or the errors
                  the quantity and the name of the coin
        """
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
        return self.errors, self.coins_quantity, self.redirect

    def view_delete_coins(self):
        """
        The view_delete_coins function is used to return data to the form in GET method.
        :param self: Access variables that belongs to the class
        :return:  coins_quantity attributes that we will use in the form
        """
        return self.coins_quantity
