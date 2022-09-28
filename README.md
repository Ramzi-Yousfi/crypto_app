# crypto_app


python -m venv env

pip install -r requirements.txt

add a text file and name it .env where you will put the env variables

FLASK_ENV = development
FLASK_APP= run.py

SECRET_KEY = "***************"

_____on local machine ____<br/>
SQLALCHEMY_DATABASE_URI = "postgresql://user:password@host/db-name"

_____on cloud database ____<br/>
SQLALCHEMY_DATABASE_URL ="postgresql://user:password@host/db-name"

folow the documentation to get your API key => https://coinmarketcap.com/api/documentation/v1/
CMC_API_KEY='*******************************'


flask db init

flask db migrate 

flask db upgrade

flask run <br/>
enjoy
