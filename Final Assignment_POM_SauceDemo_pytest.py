import pytest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


@pytest.fixture(scope="session")
def browser():
    options = Options()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    yield driver
    driver.quit()


@pytest.fixture
def base_url():
    return "https://www.saucedemo.com/"


@pytest.fixture
def login_helper(browser, base_url):
    from helpers import AuthHelpers
    return AuthHelpers(browser, base_url)

from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage


class AuthHelpers:
    def __init__(self, driver, base_url):
        self.driver = driver
        self.base_url = base_url

    def login(self, username="standard_user", password="secret_sauce"):
        self.driver.get(self.base_url)
        login_page = LoginPage(self.driver)
        login_page.login(username, password)

    def logout(self):
        inv = InventoryPage(self.driver)
        inv.open_menu()
        inv.logout()

    def add_item_to_cart(self, item_name):
        inv = InventoryPage(self.driver)
        inv.add_item_to_cart(item_name)

    def go_to_cart(self):
        inv = InventoryPage(self.driver)
        inv.go_to_cart()

    def checkout(self, first="John", last="Doe", postal="12345"):
        cart = CartPage(self.driver)
        cart.click_checkout()
        checkout = CheckoutPage(self.driver)
        checkout.fill_info(first, last, postal)
        checkout.continue_checkout()

from selenium.webdriver.common.by import By


class LoginPage:
    USERNAME = (By.ID, "user-name")
    PASSWORD = (By.ID, "password")
    LOGIN_BTN = (By.ID, "login-button")

    def __init__(self, driver):
        self.driver = driver

    def login(self, username, password):
        self.driver.find_element(*self.USERNAME).send_keys(username)
        self.driver.find_element(*self.PASSWORD).send_keys(password)
        self.driver.find_element(*self.LOGIN_BTN).click()

from selenium.webdriver.common.by import By


class InventoryPage:
    BURGER_MENU = (By.ID, "react-burger-menu-btn")
    LOGOUT = (By.ID, "logout_sidebar_link")
    CART_ICON = (By.CLASS_NAME, "shopping_cart_link")
    ITEMS = (By.CLASS_NAME, "inventory_item")

    def __init__(self, driver):
        self.driver = driver

    def open_menu(self):
        self.driver.find_element(*self.BURGER_MENU).click()

    def logout(self):
        self.driver.find_element(*self.LOGOUT).click()

    def add_item_to_cart(self, item_name):
        items = self.driver.find_elements(*self.ITEMS)
        for item in items:
            name = item.find_element(By.CLASS_NAME, "inventory_item_name").text
            if name.strip() == item_name:
                item.find_element(By.TAG_NAME, "button").click()
                break

    def go_to_cart(self):
        self.driver.find_element(*self.CART_ICON).click()

from selenium.webdriver.common.by import By


class CartPage:
    CHECKOUT_BTN = (By.ID, "checkout")

    def __init__(self, driver):
        self.driver = driver

    def click_checkout(self):
        self.driver.find_element(*self.CHECKOUT_BTN).click()

from selenium.webdriver.common.by import By


class CheckoutPage:
    FIRST_NAME = (By.ID, "first-name")
    LAST_NAME = (By.ID, "last-name")
    POSTAL = (By.ID, "postal-code")
    CONTINUE = (By.ID, "continue")
    FINISH = (By.ID, "finish")
    CANCEL = (By.ID, "cancel")

    def __init__(self, driver):
        self.driver = driver

    def fill_info(self, first, last, postal):
        self.driver.find_element(*self.FIRST_NAME).send_keys(first)
        self.driver.find_element(*self.LAST_NAME).send_keys(last)
        self.driver.find_element(*self.POSTAL).send_keys(postal)

    def continue_checkout(self):
        self.driver.find_element(*self.CONTINUE).click()

    def finish(self):
        self.driver.find_element(*self.FINISH).click()

    def cancel(self):
        self.driver.find_element(*self.CANCEL).click()

import pytest
from pages.checkout_page import CheckoutPage


@pytest.mark.dependency()
@pytest.mark.order(1)
def test_order_confirmation(login_helper):
    login_helper.login()
    login_helper.add_item_to_cart("Sauce Labs Backpack")
    login_helper.go_to_cart()
    login_helper.checkout(first="Alice", last="Smith", postal="10001")

    checkout = CheckoutPage(login_helper.driver)
    checkout.finish()

    assert "THANK YOU" in login_helper.driver.page_source.upper()


@pytest.mark.dependency(depends=["test_order_confirmation"])
@pytest.mark.order(2)
@pytest.mark.flaky(reruns=2, reruns_delay=1)
def test_order_cancellation(login_helper):
    login_helper.login()
    login_helper.add_item_to_cart("Sauce Labs Bike Light")
    login_helper.go_to_cart()
    login_helper.checkout(first="Bob", last="Gray", postal="20002")

    checkout = CheckoutPage(login_helper.driver)
    checkout.cancel()

    assert "cart" in login_helper.driver.current_url


@pytest.mark.parametrize("first,last,postal", [
    ("John", "Doe", "11111"),
    ("Jane", "Roe", "22222")
])
@pytest.mark.order(3)
@pytest.mark.skipif(False, reason="Skipping demo")
@pytest.mark.xfail(reason="Known bug for postal validation")
def test_checkout_details_verification(login_helper, first, last, postal):
    login_helper.login()
    login_helper.add_item_to_cart("Sauce Labs Bolt T-Shirt")
    login_helper.go_to_cart()
    login_helper.checkout(first, last, postal)

    assert first in login_helper.driver.page_source
