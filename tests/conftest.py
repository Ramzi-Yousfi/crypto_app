import pytest
from werkzeug.security import generate_password_hash
from app import create_app, db
from app.models.users import User

app = create_app()
@pytest.fixture(scope='session')
def client():
    with app.test_client() as client:
        with app.app_context():
            db.drop_all()
            db.create_all()
            yield client
@pytest.fixture(scope='session')
def client_authenticated(client):
    user = User(username='test_u_f', email='test_u_f@live.fr', password=generate_password_hash('test123456', method='sha256'))
    db.session.add(user)
    db.session.commit()
    client.post('/login', data=dict(
        email='test_u_f@live.fr',
        password='test123456'), follow_redirects=True)
    yield client
@pytest.fixture(scope='function')
def no_client():
    with app.test_client() as client:
        with app.app_context():
            yield client

