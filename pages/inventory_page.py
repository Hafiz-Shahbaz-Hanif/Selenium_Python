"""SauceDemo product listing (inventory) page."""
from __future__ import annotations

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from config.config import CONFIG
from pages.base_page import BasePage


class InventoryPage(BasePage):
    base_url = CONFIG.saucedemo_url
    path = "/inventory.html"

    ITEM = (By.CSS_SELECTOR, ".inventory_item")
    ITEM_NAME = (By.CSS_SELECTOR, '[data-test="inventory-item-name"]')
    ITEM_PRICE = (By.CSS_SELECTOR, '[data-test="inventory-item-price"]')
    SORT_SELECT = (By.CSS_SELECTOR, '[data-test="product-sort-container"]')
    CART_BADGE = (By.CSS_SELECTOR, '[data-test="shopping-cart-badge"]')
    CART_LINK = (By.CSS_SELECTOR, '[data-test="shopping-cart-link"]')

    SORT_OPTIONS = {
        "name (a to z)": "az",
        "name (z to a)": "za",
        "price (low to high)": "lohi",
        "price (high to low)": "hilo",
    }

    def wait_until_loaded(self) -> None:
        self.find(self.SORT_SELECT)

    def product_names(self) -> list[str]:
        return [e.text.strip() for e in self.find_all(self.ITEM_NAME)]

    def product_prices(self) -> list[float]:
        return [float(e.text.replace("$", "").strip()) for e in self.find_all(self.ITEM_PRICE)]

    def item_count(self) -> int:
        return len(self.find_all(self.ITEM))

    def sort_by(self, label: str) -> None:
        value = self.SORT_OPTIONS[label.strip().lower()]
        Select(self.find(self.SORT_SELECT)).select_by_value(value)

    def _add_button(self, product_name: str) -> tuple[str, str]:
        slug = product_name.lower().replace(" ", "-")
        return (By.CSS_SELECTOR, f'[data-test="add-to-cart-{slug}"]')

    def add_to_cart(self, product_name: str) -> None:
        self.click(self._add_button(product_name))

    def cart_count(self) -> int:
        if not self.is_visible(self.CART_BADGE, timeout=2):
            return 0
        return int(self.text_of(self.CART_BADGE))

    def go_to_cart(self) -> None:
        self.click_and_wait_for_url(self.CART_LINK, "cart.html")
