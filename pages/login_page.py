"""SauceDemo login page."""
from __future__ import annotations

from selenium.webdriver.common.by import By

from config.config import CONFIG
from pages.base_page import BasePage


class LoginPage(BasePage):
    base_url = CONFIG.saucedemo_url
    path = "/"

    USERNAME = (By.ID, "user-name")
    PASSWORD = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR = (By.CSS_SELECTOR, '[data-test="error"]')

    def wait_until_loaded(self) -> None:
        self.find(self.LOGIN_BUTTON)

    def login(self, username: str, password: str) -> None:
        self.type(self.USERNAME, username)
        self.type(self.PASSWORD, password)
        self.click(self.LOGIN_BUTTON)

    def login_as_standard_user(self) -> None:
        self.type(self.USERNAME, CONFIG.saucedemo_user)
        self.type(self.PASSWORD, CONFIG.saucedemo_password)
        self.click_and_wait_for_url(self.LOGIN_BUTTON, "inventory.html")

    def error_message(self) -> str:
        return self.text_of(self.ERROR)
