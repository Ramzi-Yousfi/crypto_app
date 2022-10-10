from datetime import datetime

from flask import Flask, render_template
import os
from dotenv import load_dotenv
from flask_login import LoginManager
from whitenoise import WhiteNoise
from app.helpers.CmcApi import CmcApi
from app.models import db, migrate
from apscheduler.schedulers.background import BackgroundScheduler
# ======================================Database models ====================================
from app.models.users import User
from app.models.coin import Coin
from app.models.daily_coins import DailyCoins



# Global variables
login_manager = LoginManager()


def create_app():
    app = Flask(__name__)

    # ===========================Load environment variables from .env file=====================
    APP_ROOT = os.path.join(os.path.dirname(__file__), '..')
    dotenv_path = os.path.join(APP_ROOT, '.env')
    load_dotenv(dotenv_path)
    app.config.from_object('config.settings.' + os.environ.get('FLASK_ENV'))
    app.config.get('SQLALCHEMY_DATABASE_URI')
    # ========================Initialize the extentions (app factory===========================

    migrate.init_app(app, db)
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    # =====================Inisialise the recusive of api call evry days  ========



    with app.app_context():
        db.init_app(app)
        db.create_all()
        db.session.commit()
        # =====================Inisialise the recusive of api call evry days  ========
        scheduler = BackgroundScheduler(daemon=True)

        @scheduler.scheduled_job("interval", seconds=250)
        def users_coins_save():
            with app.app_context():
                DailyCoins().daily_coin_save(date=datetime.now().strftime("%Y-%m-%d"))
                # DailyCoins().daily_coin_save(date='2021-05-01')

        scheduler.start()
        # =====================================Small HTTP Errors Handling========================
        @app.errorhandler(404)
        def page_not_found(e):
            status = "404"
            return render_template('errors/404.html', status=status), 404

        @app.errorhandler(500)
        def internal_server_error(e):
            status = "500"
            return render_template('errors/404.html', status=status), 500

        @login_manager.user_loader
        def load_user(user_id):
            return User.query.get(int(user_id))

        # ========================================Blueprints========================================
        from app.views.auth import auth as auth_blueprint
        app.register_blueprint(auth_blueprint)
        from app.views.coin import coins as coin_blueprint
        app.register_blueprint(coin_blueprint)

        # add whitenoise to serve static files in heroku
        app.wsgi_app = WhiteNoise(app.wsgi_app, root="app/static/")

        return app
