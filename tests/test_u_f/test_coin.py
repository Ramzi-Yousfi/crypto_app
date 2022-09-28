'''
 besause the Coin Market Cap API have limited call
 to avoid an error in the test_u_f, we will use a json file (coin.json) to get 10 coins
'''
import json
from datetime import datetime

from flask_login import current_user
from wtforms import Form

from app import db
from app.forms.coins import AddForm, DeleteForm
from app.models.coin import Coin
from app.models.daily_coins import DailyCoins
from app.views_class.Create import Create
from app.views_class.Delete import Delete
from app.views_class.Show import Show


def test_list_coins(client):
    with open("tests/test_u_f/coins.json") as json_file:
        data = json.load(json_file)
        assert len(data) == 10
        assert data[0]['name'] == 'Bitcoin'


def test_daily(client):
    with open("tests/test_u_f/coins.json", 'r', encoding='utf-8') as f:
        data = json.load(f)
    rec = DailyCoins()
    rec.daily_coin_save(data)
    assert len(DailyCoins.query.all()) == 10
    assert DailyCoins.query.all()[0].name == 'Bitcoin'


def test_new_coins(client_authenticated):
    form = AddForm()
    form.name.data = 'Ethereum'
    form.quantity.data = 25
    form.value.data = 11110
    Create(db, current_user, form).new_coins()
    assert len(Coin.query.all()) == 1
    assert Coin.query.all()[0].name == 'Ethereum'
    assert Coin.query.all()[0].quantity == 25


def test_delete_coin(client_authenticated):
    form = DeleteForm()
    '''the form return the id of the coin in the database in place of the name beacause the set_up method return the id from a dict with the name of the coin
        choosen in the form'''
    form.name.choices = [(1, 'Ethereum')]
    form.name.data = 1
    form.quantity.data = 5
    form.validate()
    form.is_submitted()
    Delete(current_user, db, form).delete_coins()
    assert len(Coin.query.all()) == 1
    assert Coin.query.all()[0].name == 'Ethereum'
    assert Coin.query.all()[0].quantity == 20


def test_detail_coin(client_authenticated):
    coin = Coin.query.get_or_404(1)
    daily = DailyCoins().get_week_save()
    show = Show(coin, daily)
    dataurl = show.figure_gain_value()
    assert coin.name == 'Ethereum'
    assert dataurl != None
    assert show.figure_gain_value() != None
    assert type(show.bins[0]) == str
    assert type(show.values[0]) == float
    assert len(show.coin_saved_week) == 2
    assert show.coin_saved_week[1].name == 'Ethereum'
