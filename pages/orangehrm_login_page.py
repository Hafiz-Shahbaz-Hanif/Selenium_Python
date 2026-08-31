"""OrangeHRM (open-source demo) login page.

Included as a second application to show the framework is not coupled to one
site: different locator strategies (name/XPath), a slower Angular-style app and
a post-login landmark assertion.
"""
from __future__ import annotations

from selenium.webdriver.common.by import By

from config.config import CONFIG
from pages.base_page import BasePage


class OrangeHrmLoginPage(BasePage):
    base_url = CONFIG.orangehrm_url
    path = "/web/index.php/auth/login"

    USERNAME = (By.NAME, "username")
    PASSWORD = (By.NAME, "password")
    SUBMIT = (By.CSS_SELECTOR, "button[type='submit']")
    ERROR_ALERT = (By.CSS_SELECTOR, ".oxd-alert-content-text")
    DASHBOARD_HEADER = (By.XPATH, "//h6[normalize-space()='Dashboard']")

    def wait_until_loaded(self) -> None:
        self.find(self.SUBMIT)

    def login(self, username: str, password: str) -> None:
        self.type(self.USERNAME, username)
        self.type(self.PASSWORD, password)
        self.click(self.SUBMIT)

    def login_as_admin(self) -> None:
        self.login(CONFIG.orangehrm_user, CONFIG.orangehrm_password)

    def is_dashboard_displayed(self) -> bool:
        return self.is_visible(self.DASHBOARD_HEADER)

    def error_message(self) -> str:
        return self.text_of(self.ERROR_ALERT)
