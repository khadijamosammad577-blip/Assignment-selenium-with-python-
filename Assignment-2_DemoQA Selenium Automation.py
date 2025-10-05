import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


def setup_driver():
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()
    return driver


def take_screenshot(driver, name="error_screenshot.png"):
    driver.save_screenshot(name)
    print(f"Screenshot saved as {name}")


def input_field_test(driver):
    driver.get("https://demoqa.com/text-box")
    driver.find_element(By.ID, "userName").send_keys("Khadija QA")
    driver.find_element(By.ID, "userEmail").send_keys("khadijamosammad577@gmail.com")
    driver.find_element(By.ID, "currentAddress").send_keys("Dhaka, Bangladesh")
    driver.find_element(By.ID, "permanentAddress").send_keys("Same as above")
    driver.find_element(By.ID, "submit").click()
    time.sleep(2)


def radio_button_test(driver):
    driver.get("https://demoqa.com/radio-button")
    driver.find_element(By.XPATH, "//label[@for='yesRadio']").click()
    time.sleep(2)


def checkbox_test(driver):
    driver.get("https://demoqa.com/checkbox")
    driver.find_element(By.CLASS_NAME, "rct-icon-expand-close").click()
    driver.find_element(By.CLASS_NAME, "rct-checkbox").click()
    time.sleep(2)


def buttons_test(driver):
    driver.get("https://demoqa.com/buttons")
    actions = ActionChains(driver)
    double_btn = driver.find_element(By.ID, "doubleClickBtn")
    right_btn = driver.find_element(By.ID, "rightClickBtn")
    click_btn = driver.find_element(By.XPATH, "//button[text()='Click Me']")

    actions.double_click(double_btn).perform()
    actions.context_click(right_btn).perform()
    click_btn.click()
    time.sleep(2)


def hover_test(driver):
    driver.get("https://demoqa.com/menu")
    actions = ActionChains(driver)
    menu_item = driver.find_element(By.XPATH, "//a[text()='Main Item 2']")
    actions.move_to_element(menu_item).perform()
    time.sleep(2)


def file_upload_test(driver):
    driver.get("https://demoqa.com/upload-download")
    upload = driver.find_element(By.ID, "uploadFile")
    upload.send_keys("C:\\Users\\User\\Downloads\\testfile.txt")  # change path
    time.sleep(2)


def alert_test(driver):
    driver.get("https://demoqa.com/alerts")
    driver.find_element(By.ID, "alertButton").click()
    driver.switch_to.alert.accept()
    time.sleep(1)

    driver.find_element(By.ID, "confirmButton").click()
    driver.switch_to.alert.dismiss()
    time.sleep(1)

    driver.find_element(By.ID, "promtButton").click()
    alert = driver.switch_to.alert
    alert.send_keys("Khadija")
    alert.accept()
    time.sleep(2)


def alert_wait_test(driver):
    driver.get("https://demoqa.com/alerts")
    driver.find_element(By.ID, "timerAlertButton").click()
    WebDriverWait(driver, 10).until(EC.alert_is_present())
    driver.switch_to.alert.accept()
    time.sleep(2)


def dynamic_button_test(driver):
    driver.get("https://demoqa.com/dynamic-properties")
    btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "enableAfter"))
    )
    print("Button is enabled:", btn.is_enabled())
    time.sleep(2)


def navigation_test(driver):
    driver.get("https://demoqa.com/links")
    link = driver.find_element(By.ID, "simpleLink")
    link.click()
    time.sleep(2)
    driver.switch_to.window(driver.window_handles[1])
    print("New tab title:", driver.title)
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    time.sleep(2)


def modal_test(driver):
    driver.get("https://demoqa.com/modal-dialogs")
    driver.find_element(By.ID, "showSmallModal").click()
    time.sleep(2)
    driver.find_element(By.ID, "closeSmallModal").click()
    time.sleep(2)


# MAIN
if __name__ == "__main__":
    driver = setup_driver()
    try:
        input_field_test(driver)
        radio_button_test(driver)
        checkbox_test(driver)
        buttons_test(driver)
        hover_test(driver)
        file_upload_test(driver)
        alert_test(driver)
        alert_wait_test(driver)
        dynamic_button_test(driver)
        navigation_test(driver)
        modal_test(driver)
        print("All tests completed successfully.")
    except Exception as e:
        print("Test failed:", e)
        take_screenshot(driver)
    finally:
        driver.quit()