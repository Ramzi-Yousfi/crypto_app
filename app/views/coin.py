from flask import render_template, redirect, url_for, Blueprint
from flask_login import current_user, login_required
from app.forms.coins import AddForm, DeleteForm
from app.models import db
from app.models.coin import Coin
from app.models.daily_coins import DailyCoins
from app.views_class.Create import Create
from app.views_class.Delete import Delete
from app.views_class.Read import Read
from app.views_class.Show import Show

coins = Blueprint('coin', __name__)


@coins.route('/')
def list_coins():
    """
    The list_coins function is used to display the list of coins that are available for
    the user to choose from. It also displays the amount of money that is currently in their account if he is authenticated.
    :return: The list of coins that the user has saved in his account if he is authenticated or a liste of the coins save in the last dy if he is not
    """
    if current_user.is_authenticated:
        coins, data, all_benef = Read(current_user).user_coins()
        return render_template('coins/list_coins.html', data=data, coins=coins, all_benef=all_benef)
    else:
        data = DailyCoins().get_last_save()
        return render_template('home/index.html', data=data)


@coins.route('/coin/add', methods=['GET', 'POST'])
@login_required
def add_coin():
    """
    The add_coin function allows the user to add a new coin in the database.
    It uses an AddForm object which is defined in forms.py and contains all fields needed for adding a new coin.
    :return: A render_template object that contains the html page add_coins
    """
    form = AddForm()
    if form.validate_on_submit():
        return Create(db, current_user, form).new_coins()
    return render_template('coins/add_coins.html', form=form, title='Ajouter une monnaie')


@coins.route('/coin-delete-value', methods=['GET', 'POST'])
@login_required
def delete_value_coin():
    """
    The delete_value_coin function is used to delete a coin from the database.
    It takes no parameters
    :return: The template delete_coin_value or a redirect if the form is valid and submited
    """
    form = DeleteForm()
    delete = Delete(current_user, db, form)
    delete.set_up()
    if form.validate_on_submit():
        errors, coins_quantity, success_redirect = delete.delete_coins()
        if success_redirect == True:
            return redirect(url_for('coin.list_coins'))
        elif success_redirect == False:
            return render_template('coins/delete_coin_value.html', coins_quantity=coins_quantity,
                                   title='Mes monnaies', form=form, errors=errors)
    coins_quantity = delete.view_delete_coins()
    return render_template('coins/delete_coin_value.html', coins_quantity=coins_quantity,
                           title='Mes monnaies', form=form)


@coins.route('/coin/<int:coin_id>/detail', methods=['GET'])
@login_required
def detail_coin(coin_id):
    """
    The detail_coin function is used to display the details of a coin.
    It takes as input the id of a coin and returns its graph with the help of matplotlip Figure .
    :param coin_id: Get the coin_id of the coin selected in the list_coins
    :return: The template coins/detail_coins
    """
    coin = Coin.query.get_or_404(coin_id)
    daily = DailyCoins().get_week_save()
    if coin.user_id == current_user.id:
        show = Show(coin, daily)
        dataurl = show.figure_gain_value()
        return render_template('coins/detail_coins.html', coin=coin, title='Détails de la monnaie', img=dataurl)
    else:
        return redirect(url_for('coin.list_coins'))
