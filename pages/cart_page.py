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
    ITEM_PRICE = (By.CSS_SELECTOR, '[data-test="inventory-item-price"]')
    CHECKOUT = (By.CSS_SELECTOR, '[data-test="checkout"]')
    CONTINUE_SHOPPING = (By.CSS_SELECTOR, '[data-test="continue-shopping"]')

    def wait_until_loaded(self) -> None:
        self.find(self.CHECKOUT)

    def item_names(self) -> list[str]:
        return [e.text.strip() for e in self.find_all(self.ITEM_NAME)]

    def item_prices(self) -> list[float]:
        return [float(e.text.replace("$", "").strip()) for e in self.find_all(self.ITEM_PRICE)]

    def contains(self, product_name: str) -> bool:
        return product_name in self.item_names()

    def item_count(self) -> int:
        return len(self.driver.find_elements(*self.CART_ITEM))

    def _remove_button(self, product_name: str) -> tuple[str, str]:
        slug = product_name.lower().replace(" ", "-")
        return (By.CSS_SELECTOR, f'[data-test="remove-{slug}"]')

    def remove(self, product_name: str) -> None:
        self.click(self._remove_button(product_name))

    def continue_shopping(self) -> None:
        self.click_and_wait_for_url(self.CONTINUE_SHOPPING, "inventory.html")

    def checkout(self) -> None:
        self.click_and_wait_for_url(self.CHECKOUT, "checkout-step-one")
