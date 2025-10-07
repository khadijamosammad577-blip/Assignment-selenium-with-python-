import time
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from helpers.utils import login, add_to_cart, go_to_cart, checkout


@pytest.fixture(scope="module")
def driver():
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()
    yield driver
    driver.quit()


@pytest.mark.order(1)
def test_order_confirmation(driver):
    """ Test successful order placement."""
    login(driver)
    add_to_cart(driver)
    go_to_cart(driver)
    checkout(driver)
    driver.find_element(By.ID, "finish").click()
    time.sleep(2)
    message = driver.find_element(By.CLASS_NAME, "complete-header").text
    assert "THANK YOU" in message.upper()
    print(" Order Confirmation successful.")


@pytest.mark.order(2)
def test_order_cancellation(driver):
    """ Test cancelling an order before confirmation."""
    login(driver)
    add_to_cart(driver, "Sauce Labs Bike Light")
    go_to_cart(driver)
    checkout(driver)
    driver.find_element(By.ID, "cancel").click()
    time.sleep(1)
    assert "inventory" in driver.current_url
    print(" Order Cancellation verified.")


@pytest.mark.order(3)
def test_checkout_details_verification(driver):
    """ Test validation of checkout details."""
    login(driver)
    add_to_cart(driver)
    go_to_cart(driver)
    driver.find_element(By.ID, "checkout").click()
    time.sleep(1)

    # Check all input fields exist
    assert driver.find_element(By.ID, "first-name").is_displayed()
    assert driver.find_element(By.ID, "last-name").is_displayed()
    assert driver.find_element(By.ID, "postal-code").is_displayed()

    print(" Checkout details fields are visible.")
