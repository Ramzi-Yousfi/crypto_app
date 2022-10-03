from datetime import datetime

from flask import Flask
from flask_apscheduler import APScheduler
from app import DailyCoins

app = Flask(__name__)

scheduler = APScheduler()
scheduler.init_app(app)


# =====================Inisialise the recusive of api call evry days  ========

@scheduler.task('interval', id='do_job_1', days=1, misfire_grace_time=3000)
def users_coins_save():
    with app.app_context():
        DailyCoins().daily_coin_save(date=datetime.now().strftime("%Y-%m-%d"))


scheduler.start()
