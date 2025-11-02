import time
from selenium.webdriver.common.by import By


def login(driver, username="standard_user", password="secret_sauce"):
    driver.get("https://www.saucedemo.com/")
    driver.find_element(By.ID, "user-name").send_keys(username)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.ID, "login-button").click()
    time.sleep(2)


def add_to_cart(driver, item_name="Sauce Labs Backpack"):
    driver.find_element(By.XPATH, f"//div[text()='{item_name}']/ancestor::div[@class='inventory_item']//button").click()
    time.sleep(1)


def go_to_cart(driver):
    driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
    time.sleep(1)


def checkout(driver, first="Khadija", last="QA", postal="1207"):
    driver.find_element(By.ID, "checkout").click()
    driver.find_element(By.ID, "first-name").send_keys(first)
    driver.find_element(By.ID, "last-name").send_keys(last)
    driver.find_element(By.ID, "postal-code").send_keys(postal)
    driver.find_element(By.ID, "continue").click()
    time.sleep(1)
