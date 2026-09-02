"""OrangeHRM (open-source demo) login page.

Included as a second application to show the framework is not coupled to one
site: different locator strategies (name/XPath), a slower Angular app and a
post-login landmark assertion.
"""
from __future__ import annotations

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config.config import CONFIG
from pages.base_page import BasePage

ORANGEHRM_WAIT_S = 40


class OrangeHrmLoginPage(BasePage):
    base_url = CONFIG.orangehrm_url
    path = "/web/index.php/auth/login"

    USERNAME = (By.NAME, "username")
    PASSWORD = (By.NAME, "password")
    SUBMIT = (By.CSS_SELECTOR, "button[type='submit']")
    ERROR_ALERT = (By.CSS_SELECTOR, ".oxd-alert-content-text")
    DASHBOARD_HEADER = (By.XPATH, "//h6[normalize-space()='Dashboard']")

    def __init__(self, driver) -> None:
        super().__init__(driver)
        self.wait = WebDriverWait(driver, ORANGEHRM_WAIT_S)

    def wait_until_loaded(self) -> None:
        self.find(self.SUBMIT)

    def login(self, username: str, password: str) -> None:
        self.type(self.USERNAME, username)
        self.type(self.PASSWORD, password)
        # Recent headless Chrome does not fire the Angular submit handler on a
        # native WebDriver click; a synthetic click does.
        self.js_click(self.SUBMIT)

    def login_as_admin(self) -> None:
        self.login(CONFIG.orangehrm_user, CONFIG.orangehrm_password)
        self.wait.until(EC.url_contains("dashboard"))

    def is_dashboard_displayed(self) -> bool:
        return self.is_visible(self.DASHBOARD_HEADER, timeout=ORANGEHRM_WAIT_S)

    def error_message(self) -> str:
        return self.wait.until(
            EC.visibility_of_element_located(self.ERROR_ALERT)
        ).text.strip()
