"""SauceDemo single product page (/inventory-item.html?id=N)."""
from __future__ import annotations

from selenium.webdriver.common.by import By

from config.config import CONFIG
from pages.base_page import BasePage


class ProductPage(BasePage):
    base_url = CONFIG.saucedemo_url
    path = "/inventory-item.html"

    NAME = (By.CSS_SELECTOR, '[data-test="inventory-item-name"]')
    PRICE = (By.CSS_SELECTOR, '[data-test="inventory-item-price"]')
    DESCRIPTION = (By.CSS_SELECTOR, '[data-test="inventory-item-desc"]')
    ADD_TO_CART = (By.CSS_SELECTOR, '[data-test="add-to-cart"]')
    REMOVE = (By.CSS_SELECTOR, '[data-test="remove"]')
    BACK = (By.CSS_SELECTOR, '[data-test="back-to-products"]')
    CART_BADGE = (By.CSS_SELECTOR, '[data-test="shopping-cart-badge"]')

    def wait_until_loaded(self) -> None:
        self.find(self.NAME)

    def name(self) -> str:
        return self.text_of(self.NAME)

    def price(self) -> float:
        return float(self.text_of(self.PRICE).replace("$", "").strip())

    def description(self) -> str:
        return self.text_of(self.DESCRIPTION)

    def add_to_cart(self) -> None:
        self.click(self.ADD_TO_CART)

    def remove_from_cart(self) -> None:
        self.click(self.REMOVE)

    def button_label(self) -> str:
        return "Add to cart" if self.driver.find_elements(*self.ADD_TO_CART) else "Remove"

    def cart_count(self) -> int:
        if not self.is_visible(self.CART_BADGE, timeout=2):
            return 0
        return int(self.text_of(self.CART_BADGE))

    def back_to_products(self) -> None:
        self.click_and_wait_for_url(self.BACK, "inventory.html")
