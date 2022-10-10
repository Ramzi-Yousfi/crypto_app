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
        """
        The get_saved_coin_names function returns a list of all the names of daily coins that have been saved to the database.
        we will use it in the select field in the add coin form.
        :param self: Reference the class itself
        :return: A list of the names of all saved coins
        """
        saved_coins_names = [saved_coins.name for saved_coins in self.all_data]
        return saved_coins_names

    def unique_coins_names(self):
        """
        The unique_coins_names function returns a list of unique coin names from the user's collection.
        It does this by iterating through each coin in the user's collection and appending its name to a list.
        The function then returns that list, which contains only unique values.
        the total of user coins value * quantity is calculated here
        :param self: Represent the instance of the object itself
        :return: A list of unique coin names : array
        """
        for i in self.coins:
            self.coins_names.append(i.name)
            self.my_price += i.value * i.quantity
        return list(set(self.coins_names))

    def get_user_data(self):
        """
        The get_user_data function takes in the user_data list and returns a new list of coins that are unique to the user's
        collection. This is done by comparing each coin name in all_data with each coin name in unique, if there is a match then
        the data for that coin will be added to the user_data list.
        -> to avoid to have duplicate ex the user have 2 coins of the same name but with different value but the original value
        from the daily coin is one
        :param self: Access variables that belongs to the class
        :return: The user_data it's the user coin with the information of daily coins : array
        """
        unique = self.unique_coins_names()
        for d in self.all_data:
            if d.name in unique:
                self.user_data.append(d)
        return self.user_data

    @login_required
    def user_coins(self):
        """
        The user_coins function returns a list of all the coins in the user's collection, the user_data list and the total
        value of the user's collection.
        we calculate the total price of the coins today in the loop then calculate the total benefit of the user
        :param self: Access variables that belongs to the class
        :return: A list of all the coins in the user's collection : array
                  the user_data :array
                  list and the total value of the user's collection : float
        """
        data = self.get_user_data()
        for i in self.coins:
            for d in data:
                if i.name == d.name:
                    self.today_price += (d.value * i.quantity)
        all_benef = round(self.today_price - self.my_price, 4)
        return self.coins, data, all_benef
