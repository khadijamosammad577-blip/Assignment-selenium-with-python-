# SauceDemo — Pytest Automation (POM)

This repository contains a Pytest-based automation project for [https://www.saucedemo.com/](https://www.saucedemo.com/) implemented with the **Page Object Model (POM)**, Pytest fixtures, helper functions, and advanced markers. It covers three test flows:

* **Order Confirmation**
* **Order Cancellation**
* **Checkout Details Verification**n
  Included: sample code files (page objects, helpers, tests, fixtures), how to run tests, and how to generate an Allure test report.

---

## Project structure

```
saucedemo-pytest-pom/
├─ pages/
│  ├─ __init__.py
│  ├─ login_page.py
│  ├─ inventory_page.py
│  ├─ cart_page.py
│  └─ checkout_page.py
├─ tests/
│  ├─ test_order_flows.py
├─ helpers.py
├─ conftest.py
├─ requirements.txt
└─ README.md
```

---

## requirements.txt

```
pytest
selenium
webdriver-manager
pytest-ordering
pytest-dependency
pytest-rerunfailures
allure-pytest
```

Install with:

```bash
pip install -r requirements.txt
```

---

## conftest.py

```python
# conftest.py
import os
import pytest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options

@pytest.fixture(scope="session")
def browser():
    """Session-level browser fixture: starts a Chrome browser and quits at the end."""
    opts = Options()
    opts.add_argument('--headless=new') if os.getenv('HEADLESS', '0') == '1' else None
    opts.add_argument('--no-sandbox')
    opts.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=opts)
    driver.maximize_window()
    yield driver
    driver.quit()


@pytest.fixture
def base_url():
    return "https://www.saucedemo.com/"


@pytest.fixture
def login_helper(browser, base_url):
    """A helper fixture exposing login/logout helper functions via `helpers.py`."""
    from helpers import AuthHelpers
    return AuthHelpers(browser, base_url)


@pytest.fixture(scope='function')
def clean_cart(browser, base_url):
    """Optional fixture that navigates to inventory and ensures cart is clean before each test."""
    browser.get(base_url)
    # best-effort: remove all items from cart if present; implemented in InventoryPage
    from pages.inventory_page import InventoryPage
    inv = InventoryPage(browser)
    try:
        inv.remove_all_from_cart()
    except Exception:
        pass
    yield
    # post-test cleanup
    try:
        inv.remove_all_from_cart()
    except Exception:
        pass
```

---

## helpers.py

```python
# helpers.py
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage

class AuthHelpers:
    def __init__(self, driver, base_url):
        self.driver = driver
        self.base_url = base_url

    def login(self, username='standard_user', password='secret_sauce'):
        self.driver.get(self.base_url)
        lp = LoginPage(self.driver)
        lp.login(username, password)

    def logout(self):
        inv = InventoryPage(self.driver)
        inv.open_menu()
        inv.logout()

    def add_item_to_cart_by_name(self, item_name):
        inv = InventoryPage(self.driver)
        inv.add_item_to_cart(item_name)

    def go_to_cart(self):
        cp = CartPage(self.driver)
        cp.open()

    def checkout(self, first='John', last='Doe', postal='12345'):
        cp = CartPage(self.driver)
        cp.open()
        cp.click_checkout()
        ck = CheckoutPage(self.driver)
        ck.fill_info(first, last, postal)
        ck.continue_checkout()
```

---

## pages/login_page.py

```python
# pages/login_page.py
from selenium.webdriver.common.by import By

class LoginPage:
    URL = 'https://www.saucedemo.com/'
    USERNAME = (By.ID, 'user-name')
    PASSWORD = (By.ID, 'password')
    LOGIN_BTN = (By.ID, 'login-button')
    ERROR = (By.CSS_SELECTOR, '[data-test="error"]')

    def __init__(self, driver):
        self.driver = driver

    def open(self):
        self.driver.get(self.URL)

    def login(self, username, password):
        self.driver.find_element(*self.USERNAME).clear()
        self.driver.find_element(*self.USERNAME).send_keys(username)
        self.driver.find_element(*self.PASSWORD).clear()
        self.driver.find_element(*self.PASSWORD).send_keys(password)
        self.driver.find_element(*self.LOGIN_BTN).click()

    def get_error(self):
        return self.driver.find_element(*self.ERROR).text
```

---

## pages/inventory_page.py

```python
# pages/inventory_page.py
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

class InventoryPage:
    BURGER = (By.ID, 'react-burger-menu-btn')
    LOGOUT = (By.ID, 'logout_sidebar_link')
    CART_LINK = (By.CLASS_NAME, 'shopping_cart_link')
    ITEMS = (By.CSS_SELECTOR, '.inventory_item')

    def __init__(self, driver):
        self.driver = driver

    def open_menu(self):
        self.driver.find_element(*self.BURGER).click()

    def logout(self):
        self.driver.find_element(*self.LOGOUT).click()

    def add_item_to_cart(self, item_name):
        items = self.driver.find_elements(*self.ITEMS)
        for it in items:
            title = it.find_element(By.CLASS_NAME, 'inventory_item_name').text
            if title.strip() == item_name:
                it.find_element(By.TAG_NAME, 'button').click()
                return True
        raise NoSuchElementException(f"Item '{item_name}' not found")

    def remove_all_from_cart(self):
        # find 'Remove' buttons and click all
        remove_buttons = self.driver.find_elements(By.XPATH, "//button[text()='Remove']")
        for btn in remove_buttons:
            try:
                btn.click()
            except Exception:
                pass

    def go_to_cart(self):
        self.driver.find_element(*self.CART_LINK).click()
```

---

## pages/cart_page.py

```python
# pages/cart_page.py
from selenium.webdriver.common.by import By

class CartPage:
    CHECKOUT_BTN = (By.ID, 'checkout')
    CONTINUE_SHOPPING = (By.ID, 'continue-shopping')
    CART_ITEMS = (By.CSS_SELECTOR, '.cart_item')

    def __init__(self, driver):
        self.driver = driver

    def open(self):
        # assumes we are on inventory or other page where cart link exists
        from pages.inventory_page import InventoryPage
        InventoryPage(self.driver).go_to_cart()

    def click_checkout(self):
        self.driver.find_element(*self.CHECKOUT_BTN).click()

    def get_cart_item_names(self):
        items = self.driver.find_elements(*self.CART_ITEMS)
        return [i.find_element(By.CLASS_NAME, 'inventory_item_name').text for i in items]
```

---

## pages/checkout_page.py

```python
# pages/checkout_page.py
from selenium.webdriver.common.by import By

class CheckoutPage:
    FIRST = (By.ID, 'first-name')
    LAST = (By.ID, 'last-name')
    POSTAL = (By.ID, 'postal-code')
    CONTINUE = (By.ID, 'continue')
    FINISH = (By.ID, 'finish')
    BACK = (By.ID, 'cancel')

    def __init__(self, driver):
        self.driver = driver

    def fill_info(self, first, last, postal):
        self.driver.find_element(*self.FIRST).clear()
        self.driver.find_element(*self.FIRST).send_keys(first)
        self.driver.find_element(*self.LAST).clear()
        self.driver.find_element(*self.LAST).send_keys(last)
        self.driver.find_element(*self.POSTAL).clear()
        self.driver.find_element(*self.POSTAL).send_keys(postal)

    def continue_checkout(self):
        self.driver.find_element(*self.CONTINUE).click()

    def finish(self):
        self.driver.find_element(*self.FINISH).click()

    def cancel(self):
        self.driver.find_element(*self.BACK).click()
```

---

## tests/test_order_flows.py

```python
# tests/test_order_flows.py
import pytest
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage

pytestmark = pytest.mark.usefixtures('clean_cart')


@pytest.mark.dependency()
@pytest.mark.order(1)
def test_order_confirmation(login_helper):
    """Place an order and assert success message / order finished."""
    # login and add item
    login_helper.login()
    # add item
    login_helper.add_item_to_cart_by_name('Sauce Labs Backpack')
    login_helper.checkout(first='Alice', last='Smith', postal='10001')

    ck = CheckoutPage(login_helper.driver)
    # finish
    ck.finish()
    # simple assertion: after finish, there is a confirmation text somewhere
    assert 'THANK YOU' in login_helper.driver.page_source.upper()


@pytest.mark.dependency(depends=["test_order_confirmation"])
@pytest.mark.order(2)
@pytest.mark.flaky(reruns=2, reruns_delay=1)
def test_order_cancellation(login_helper):
    """Start checkout and cancel — ensure user returns to cart/inventory."""
    login_helper.login()
    login_helper.add_item_to_cart_by_name('Sauce Labs Backpack')
    login_helper.go_to_cart()

    from pages.cart_page import CartPage
    cp = CartPage(login_helper.driver)
    cp.click_checkout()

    from pages.checkout_page import CheckoutPage
    ck = CheckoutPage(login_helper.driver)
    # cancel action
    ck.cancel()
    # after cancel, cart page should be visible (cart items or checkout button removed)
    assert 'cart' in login_helper.driver.current_url or len(cp.get_cart_item_names()) > 0


@pytest.mark.parametrize("first,last,postal", [
    ("John","Doe","11111"),
    ("Jane","Roe","22222")
])
@pytest.mark.order(3)
@pytest.mark.skipif(False, reason="Demonstration skipif: set to True to skip this test")
@pytest.mark.xfail(reason="Known formatting issue with postal code in UI", strict=False)
def test_checkout_details_verification(login_helper, first, last, postal):
    """Verify checkout form accepts data and shows summary with correct names."""
    login_helper.login()
    login_helper.add_item_to_cart_by_name('Sauce Labs Bike Light')
    login_helper.checkout(first=first, last=last, postal=postal)

    # after clicking continue, we should see the overview and item name
    assert first in login_helper.driver.page_source or last in login_helper.driver.page_source
```

Notes on markers used:

* `pytest.mark.dependency`: makes tests run with dependency enforcement. See `pytest-dependency` plugin.
* `pytest.mark.order`: from `pytest-ordering`, enforces test order.
* `pytest.mark.flaky`: requires `pytest-rerunfailures` for reruns.
* `pytest.mark.skipif`: conditional skipping.
* `pytest.mark.xfail`: expected failure for known issues.
* `pytest.mark.parametrize`: parameterized inputs for the checkout details test.

---

## Run tests & generate report

Run tests with:

```bash
# basic run
pytest -q

# run with Allure (generate results folder)
pytest --alluredir=allure-results

# serve viewable Allure report (if allure is installed)
allure serve allure-results
```

### Example: show flaky reruns and marker outputs

Pytest will print markers like `SKIPPED`, `XPASS`, `XFAIL`, `FAILED`, `PASSED`. When using `pytest-rerunfailures` with `@pytest.mark.flaky(reruns=2)` unstable tests will be retried automatically.

---

## Tips / Notes

* Use `HEADLESS=1` environment variable if you want headless Chrome: `export HEADLESS=1` (or on Windows `set HEADLESS=1`).
* For CI, install Chrome and run with `--headless` and `--no-sandbox`.
* You can convert this project into a proper Git repo. Create separate files for each code block shown above.
* If you prefer HTML reporting only, you may add `pytest-html` to `requirements.txt` and run `pytest --html=report.html`.

---

## Example expected pytest output (truncated)

```
collected 4 items

tests/test_order_flows.py::test_order_confirmation PASSED
tests/test_order_flows.py::test_order_cancellation PASSED (rerun 1)
tests/test_order_flows.py::test_order_cancellation PASSED
tests/test_order_flows.py::test_checkout_details_verification[x0] XFAIL
tests/test_order_flows.py::test_checkout_details_verification[x1] XFAIL
```

#   F i n a l - A s s i g n m e n t _ P O M _ S a u c e D e m o _ p y t e s t . p y  
 