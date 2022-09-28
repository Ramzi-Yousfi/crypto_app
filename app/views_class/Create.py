from flask import url_for
from werkzeug.utils import redirect

from app.models.coin import Coin


class Create():
    def __init__(self, db, current_user, form):
        self.form = form
        self.db = db
        self.current_user = current_user

    def new_coins(self):
        new_coin = Coin(name=self.form.name.data, quantity=self.form.quantity.data, value=self.form.value.data,
                        user_id=self.current_user.id)
        self.db.session.add(new_coin)
        self.db.session.commit()
        return redirect(url_for('coin.list_coins'))
