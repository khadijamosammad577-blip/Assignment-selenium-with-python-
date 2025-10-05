import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


def setup_driver():
    """Initialize Chrome WebDriver"""
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()
    return driver


def login_with_id(driver):
    driver.get("https://www.saucedemo.com/")
    wait = WebDriverWait(driver, 10)

    wait.until(EC.presence_of_element_located((By.ID, "user-name"))).send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()

    time.sleep(2)
    print("Login with ID successful:", "inventory" in driver.current_url)


def login_with_name(driver):
    driver.get("https://www.saucedemo.com/")
    wait = WebDriverWait(driver, 10)

    wait.until(EC.presence_of_element_located((By.NAME, "user-name"))).send_keys("standard_user")
    driver.find_element(By.NAME, "password").send_keys("secret_sauce")
    driver.find_element(By.NAME, "login-button").click()

    time.sleep(2)
    print("Login with NAME successful:", "inventory" in driver.current_url)


def login_with_xpath(driver):
    driver.get("https://www.saucedemo.com/")
    wait = WebDriverWait(driver, 10)

    wait.until(EC.presence_of_element_located((By.XPATH, '//input[@data-test="username"]'))).send_keys("standard_user")
    driver.find_element(By.XPATH, '//input[@data-test="password"]').send_keys("secret_sauce")
    driver.find_element(By.XPATH, '//input[@data-test="login-button"]').click()

    time.sleep(2)
    print("Login with XPATH successful:", "inventory" in driver.current_url)


# -------- MAIN EXECUTION --------
if __name__ == "__main__":
    driver = setup_driver()

    try:
        login_with_id(driver)
        login_with_name(driver)
        login_with_xpath(driver)
    finally:
        driver.quit()
