import json
from datetime import date

from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait as wait

from app import db
from app.models.daily_coins import DailyCoins
from tests.conftest import app


class TestUserProcess:
    driver = webdriver.Chrome("C:/Program Files/chromedriver_win32/chromedriver.exe")
    driver.get("http://localhost:5000/")
    with app.app_context():
        db.drop_all()
        db.create_all()
        db.session.commit()
        with open("tests/test_u_f/coins.json", 'r', encoding='utf-8') as f:
            data = json.load(f)
        daily = DailyCoins()
        for i in range(20, 27):
            daily.daily_coin_save(data, date=date(2022, 9, i))


    def test_register(self):
        self.driver.implicitly_wait(5000)
        btn_auth = self.driver.find_element("id", "btn-auth")
        btn_auth.click()
        self.driver.implicitly_wait(50)
        link_to_register = self.driver.find_element("id", "link-to-register")
        link_to_register.click()
        self.driver.implicitly_wait(50)
        email = self.driver.find_element("id", "email")
        email.send_keys("hello@autotest.fr")
        self.driver.implicitly_wait(50)
        username = self.driver.find_element("id", "username")
        username.send_keys("autotest")
        self.driver.implicitly_wait(50)
        password = self.driver.find_element("id", "password")
        password.send_keys("test123456")
        self.driver.implicitly_wait(50)
        confirm_password = self.driver.find_element("id", "confirm_password")
        confirm_password.send_keys("test123456")
        self.driver.implicitly_wait(50)
        submit = self.driver.find_element("id", "submit")
        submit.click()
        self.driver.implicitly_wait(500)

    def test_login(self):
        self.driver.implicitly_wait(5000)
        email = self.driver.find_element("id", "email")
        email.send_keys("hello@autotest.fr")
        password = self.driver.find_element("id", "password")
        password.send_keys("test123456")
        submit = self.driver.find_element("id", "submit")
        submit.click()
        self.driver.implicitly_wait(2000)

    def test_add_coin(self):
        self.driver.implicitly_wait(5000)
        btn_add = self.driver.find_element("id", "btn-add")
        btn_add.click()
        self.driver.implicitly_wait(5000)
        coin_name = Select(self.driver.find_element("id", "name"))
        coin_name.select_by_visible_text("Bitcoin")
        coin_quantity = self.driver.find_element("id", "quantity")
        coin_quantity.send_keys("10")
        coin_price = self.driver.find_element("id", "value")
        coin_price.send_keys("50000")
        submit = self.driver.find_element("id", "submit")
        submit.click()
        self.driver.implicitly_wait(5000)

    def test_delete_coin(self):
        self.driver.implicitly_wait(5000)
        btn_delete = self.driver.find_element("id", "btn-delete")
        btn_delete.click()
        self.driver.implicitly_wait(5000)
        coin_name = Select(self.driver.find_element("id", "name"))
        coin_name.select_by_visible_text("Bitcoin")
        quantity = self.driver.find_element("id", "quantity")
        quantity.clear()
        quantity.send_keys("5.4")
        btn_delete = self.driver.find_element("id", "delete")
        btn_delete.click()
        self.driver.implicitly_wait(5000)

    def test_show_coin(self):
        btn_show = self.driver.find_element("id", "coin-1")
        btn_show.click()
        self.driver.implicitly_wait(500000)
        btn_return = self.driver.find_element("id", "return-home")
        btn_return.click()
        self.driver.implicitly_wait(5000)

    def test_logout(self):
        wait(self.driver, 2000)
        btn_logout = self.driver.find_element("id", "logout")
        btn_logout.click()
        self.driver.implicitly_wait(20)
        self.driver.close()
