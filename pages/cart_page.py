"""SauceDemo cart page."""
from __future__ import annotations

from selenium.webdriver.common.by import By

from config.config import CONFIG
from pages.base_page import BasePage


class CartPage(BasePage):
    base_url = CONFIG.saucedemo_url
    path = "/cart.html"

    CART_ITEM = (By.CSS_SELECTOR, ".cart_item")
    ITEM_NAME = (By.CSS_SELECTOR, '[data-test="inventory-item-name"]')
    CHECKOUT = (By.CSS_SELECTOR, '[data-test="checkout"]')
    CONTINUE_SHOPPING = (By.CSS_SELECTOR, '[data-test="continue-shopping"]')

    def wait_until_loaded(self) -> None:
        self.find(self.CHECKOUT)

    def item_names(self) -> list[str]:
        return [e.text.strip() for e in self.find_all(self.ITEM_NAME)]

    def contains(self, product_name: str) -> bool:
        return product_name in self.item_names()

    def item_count(self) -> int:
        return len(self.driver.find_elements(*self.CART_ITEM))

    def checkout(self) -> None:
        self.click_and_wait_for_url(self.CHECKOUT, "checkout-step-one")
