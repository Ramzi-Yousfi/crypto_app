from flask_login import current_user

from app.models.daily_coins import DailyCoins


def test_error_response(client):
    resp = client.post('/hello-world')
    assert resp.status_code == 404


def test_redirect_not_authenticated(no_client):
    resp = no_client.get('/coin/add')
    assert current_user.is_authenticated == False
    assert resp.status_code == 302


def test_home(no_client):
    resp = no_client.get('/')
    data = DailyCoins().get_last_save()
    assert resp.status_code == 200
    assert len(data) == 10
    assert data[0].name == 'Bitcoin'

def test_list_coins(client_authenticated):
    resp = client_authenticated.get('/')
    assert resp.status_code == 200
    assert current_user.is_authenticated == True

def test_register(client):
    res = client.post('/register', data={'username': 'test_u_f', 'email': 'hello@live.fr', 'password': 'test123456'})
    assert res.status_code == 302


def test_list_coins(client_authenticated):
    resp = client_authenticated.get('/')
    assert resp.status_code == 200
    assert current_user.is_authenticated == True


def test_get_add_coin(client_authenticated):
    resp = client_authenticated.get('/coin/add')
    assert resp.status_code == 200
    assert current_user.username == "test_u_f"


def test_post_add_coin(client_authenticated):
    resp = client_authenticated.post('/coin/add', data=dict(
        coin='Bitcoin',
        quantity='1',
        value='11110',
        user_id=current_user.id), follow_redirects=True)
    assert current_user.username == "test_u_f"
    assert resp.status_code == 200


def get_delete_coin(client_authenticated):
    resp = client_authenticated.get('/coin-delete-value')
    assert resp.status_code == 200


def test_post_delete_coin(client_authenticated):
    resp = client_authenticated.post('/coin-delete-value', data=dict(
        name=1,
        quantity=2,
        user_id=current_user.id), follow_redirects=True)
    assert resp.status_code == 200


def test_detail_coin(client_authenticated):
    resp = client_authenticated.get('/coin/1/detail')
    assert resp.status_code == 200


def test_logout(client_authenticated):
    resp = client_authenticated.get('/logout')
    assert resp.status_code == 302

    """
        def test_home(client):
            resp = client.get('/')
            data = DailyCoins().get_last_save()
            if not current_user:
                assert resp.status_code == 200
                assert type(data) == list
                assert len(data) == 10
                assert data[0]['name'] == 'Bitcoin'
        
        def test_get_login(client):
            resp = client.get('/login')
            assert resp.status_code == 200
        
        def test_login(client):
            resp = client.post('/login', data=dict(
                email='test_u_f@live.fr',
                password='test123456'
            ), follow_redirects=True)
            pprint(resp.data)
            assert resp.status_code == 200
        
        
        def logout(client):
            return client.get('/logout', follow_redirects=True)
        
        def test_get_register(client):
            resp = client.get('/register')
            assert resp.status_code == 200
        
        def test_register(client):
            resp = client.post('/register', data=dict(
                username='test_u_f',
                email='test_u_f@live.fr',
                password='test123456'
            ), follow_redirects=False)
            assert resp.status_code == 302
        
        
        def test_list_coins(client):
            print(client)
            assert False
        
        
        
        def test_get_add_coin(client_authenticated):
            resp = client_authenticated.get('/coin/add')
            assert resp.status_code == 302
        
        def test_add_coin(client_authenticated):
            resp = client_authenticated.post('/coin/add', data=dict(
                name='Bitcoin',
                value=1000,
                percent_change_24h=10,
                symbol='BTC'
            ), follow_redirects=False)
            assert resp.status_code == 302
        
        
        
        
        def test_get_delete_coin(client_authenticated):
            resp = client_authenticated.get('/coin-delete-value')
            assert resp.status_code == 302
        
        def test_delete_coin(client_authenticated):
            resp = client_authenticated.post('/coin-delete-value', data=dict(
                name='Bitcoin',
                value=3000,
            ), follow_redirects=False)
            assert resp.status_code == 302
        
        
        def test_coin_show(client_authenticated):
            resp = client_authenticated.get('/coin/2/detail')
            assert resp.status_code == 200
        
        
        def test_error_response(client):
            resp = client.post('/hello-world')
            assert resp.status_code == 40       
    """
