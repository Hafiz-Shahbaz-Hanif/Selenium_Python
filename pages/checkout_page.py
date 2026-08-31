"""SauceDemo checkout flow (information -> overview -> complete)."""
from __future__ import annotations

from selenium.webdriver.common.by import By

from config.config import CONFIG
from pages.base_page import BasePage


class CheckoutPage(BasePage):
    base_url = CONFIG.saucedemo_url
    path = "/checkout-step-one.html"

    FIRST_NAME = (By.CSS_SELECTOR, '[data-test="firstName"]')
    LAST_NAME = (By.CSS_SELECTOR, '[data-test="lastName"]')
    POSTAL_CODE = (By.CSS_SELECTOR, '[data-test="postalCode"]')
    CONTINUE = (By.CSS_SELECTOR, '[data-test="continue"]')
    FINISH = (By.CSS_SELECTOR, '[data-test="finish"]')
    ERROR = (By.CSS_SELECTOR, '[data-test="error"]')

    SUMMARY_TOTAL = (By.CSS_SELECTOR, '[data-test="total-label"]')
    ITEM_TOTAL = (By.CSS_SELECTOR, '[data-test="subtotal-label"]')
    COMPLETE_HEADER = (By.CSS_SELECTOR, '[data-test="complete-header"]')

    def wait_until_information_step(self) -> "CheckoutPage":
        self.wait_for_url_contains("checkout-step-one")
        self.wait_for_dom_ready()
        self.find(self.FIRST_NAME)
        return self

    def fill_information(self, first: str, last: str, postal: str) -> None:
        self.wait_until_information_step()
        self.type(self.FIRST_NAME, first)
        self.type(self.LAST_NAME, last)
        self.type(self.POSTAL_CODE, postal)
        self.click_and_wait_for_url(self.CONTINUE, "checkout-step-two")
        self.find(self.FINISH)

    def continue_without_details(self) -> None:
        self.click(self.CONTINUE)

    def error_message(self) -> str:
        return self.text_of(self.ERROR)

    def displayed_total(self) -> float:
        raw = self.text_of(self.SUMMARY_TOTAL)  # "Total: $58.29"
        return float(raw.split("$")[1])

    def finish(self) -> None:
        self.click_and_wait_for_url(self.FINISH, "checkout-complete")

    def confirmation_message(self) -> str:
        return self.text_of(self.COMPLETE_HEADER)
