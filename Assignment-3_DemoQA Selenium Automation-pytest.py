import time
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture(scope="module")
def driver():
    """Setup and teardown for WebDriver."""
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()
    yield driver
    driver.quit()


def take_screenshot(driver, name="error_screenshot.png"):
    """Capture screenshot on failure."""
    driver.save_screenshot(name)
    print(f"Screenshot saved as {name}")


def test_input_field(driver):
    driver.get("https://demoqa.com/text-box")
    driver.find_element(By.ID, "userName").send_keys("Khadija QA")
    driver.find_element(By.ID, "userEmail").send_keys("khadijamosammad577@gmail.com")
    driver.find_element(By.ID, "currentAddress").send_keys("Dhaka, Bangladesh")
    driver.find_element(By.ID, "permanentAddress").send_keys("Same as above")
    driver.find_element(By.ID, "submit").click()
    time.sleep(2)
    assert "test@example.com" in driver.page_source


def test_radio_button(driver):
    driver.get("https://demoqa.com/radio-button")
    driver.find_element(By.XPATH, "//label[@for='yesRadio']").click()
    time.sleep(2)
    assert "Yes" in driver.page_source


def test_checkbox(driver):
    driver.get("https://demoqa.com/checkbox")
    driver.find_element(By.CLASS_NAME, "rct-icon-expand-close").click()
    driver.find_element(By.CLASS_NAME, "rct-checkbox").click()
    time.sleep(2)
    assert "home" in driver.page_source.lower()


def test_buttons(driver):
    driver.get("https://demoqa.com/buttons")
    actions = ActionChains(driver)
    double_btn = driver.find_element(By.ID, "doubleClickBtn")
    right_btn = driver.find_element(By.ID, "rightClickBtn")
    click_btn = driver.find_element(By.XPATH, "//button[text()='Click Me']")

    actions.double_click(double_btn).perform()
    actions.context_click(right_btn).perform()
    click_btn.click()
    time.sleep(2)
    assert "You have done a double click" in driver.page_source


def test_hover_menu(driver):
    driver.get("https://demoqa.com/menu")
    actions = ActionChains(driver)
    menu_item = driver.find_element(By.XPATH, "//a[text()='Main Item 2']")
    actions.move_to_element(menu_item).perform()
    time.sleep(2)
    assert "Main Item 2" in driver.page_source


def test_file_upload(driver):
    driver.get("https://demoqa.com/upload-download")
    upload = driver.find_element(By.ID, "uploadFile")
    upload.send_keys("C:\\Users\\User\\Downloads\\testfile.txt")  # update your path
    time.sleep(2)
    assert "testfile.txt" in driver.page_source


def test_alerts(driver):
    driver.get("https://demoqa.com/alerts")

    # Normal alert
    driver.find_element(By.ID, "alertButton").click()
    driver.switch_to.alert.accept()
    time.sleep(1)

    # Confirm alert
    driver.find_element(By.ID, "confirmButton").click()
    driver.switch_to.alert.dismiss()
    time.sleep(1)

    # Prompt alert
    driver.find_element(By.ID, "promtButton").click()
    alert = driver.switch_to.alert
    alert.send_keys("Khadija")
    alert.accept()
    time.sleep(2)
    assert "Khadija" in driver.page_source


def test_alert_wait(driver):
    driver.get("https://demoqa.com/alerts")
    driver.find_element(By.ID, "timerAlertButton").click()
    WebDriverWait(driver, 10).until(EC.alert_is_present())
    driver.switch_to.alert.accept()
    time.sleep(2)


def test_dynamic_button(driver):
    driver.get("https://demoqa.com/dynamic-properties")
    btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "enableAfter"))
    )
    assert btn.is_enabled()


def test_navigation(driver):
    driver.get("https://demoqa.com/links")
    link = driver.find_element(By.ID, "simpleLink")
    link.click()
    time.sleep(2)
    driver.switch_to.window(driver.window_handles[1])
    assert "ToolsQA" in driver.title
    driver.close()
    driver.switch_to.window(driver.window_handles[0])


def test_modal_dialog(driver):
    driver.get("https://demoqa.com/modal-dialogs")
    driver.find_element(By.ID, "showSmallModal").click()
    time.sleep(2)
    driver.find_element(By.ID, "closeSmallModal").click()
    time.sleep(2)
    assert "Small Modal" in driver.page_source
