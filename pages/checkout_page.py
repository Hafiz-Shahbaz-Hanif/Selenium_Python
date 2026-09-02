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
    CANCEL = (By.CSS_SELECTOR, '[data-test="cancel"]')
    ERROR = (By.CSS_SELECTOR, '[data-test="error"]')

    SUBTOTAL = (By.CSS_SELECTOR, '[data-test="subtotal-label"]')
    TAX = (By.CSS_SELECTOR, '[data-test="tax-label"]')
    SUMMARY_TOTAL = (By.CSS_SELECTOR, '[data-test="total-label"]')
    ITEM_NAME = (By.CSS_SELECTOR, '[data-test="inventory-item-name"]')
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
        self.js_click(self.CONTINUE)

    def error_message(self) -> str:
        return self.text_of(self.ERROR)

    @staticmethod
    def _money(text: str) -> float:
        return float(text.split("$")[1])

    def subtotal(self) -> float:
        return self._money(self.text_of(self.SUBTOTAL))  # "Item total: $58.29"

    def tax(self) -> float:
        return self._money(self.text_of(self.TAX))  # "Tax: $4.66"

    def displayed_total(self) -> float:
        return self._money(self.text_of(self.SUMMARY_TOTAL))  # "Total: $62.95"

    def overview_item_names(self) -> list[str]:
        return [e.text.strip() for e in self.find_all(self.ITEM_NAME)]

    def cancel_information_step(self) -> None:
        self.click_and_wait_for_url(self.CANCEL, "cart.html")

    def cancel_overview_step(self) -> None:
        self.click_and_wait_for_url(self.CANCEL, "inventory.html")

    def finish(self) -> None:
        self.click_and_wait_for_url(self.FINISH, "checkout-complete")

    def confirmation_message(self) -> str:
        return self.text_of(self.COMPLETE_HEADER)
