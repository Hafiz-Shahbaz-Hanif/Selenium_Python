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

    BURGER = (By.ID, "react-burger-menu-btn")
    LOGOUT = (By.CSS_SELECTOR, '[data-test="logout-sidebar-link"]')
    RESET = (By.CSS_SELECTOR, '[data-test="reset-sidebar-link"]')

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

    @staticmethod
    def _slug(product_name: str) -> str:
        return product_name.lower().replace(" ", "-")

    def _add_button(self, product_name: str) -> tuple[str, str]:
        return (By.CSS_SELECTOR, f'[data-test="add-to-cart-{self._slug(product_name)}"]')

    def _remove_button(self, product_name: str) -> tuple[str, str]:
        return (By.CSS_SELECTOR, f'[data-test="remove-{self._slug(product_name)}"]')

    def _item_link(self, product_name: str) -> tuple[str, str]:
        return (
            By.XPATH,
            f'//*[@data-test="inventory-item-name"][normalize-space()="{product_name}"]',
        )

    def add_to_cart(self, product_name: str) -> None:
        self.click(self._add_button(product_name))

    def remove_from_cart(self, product_name: str) -> None:
        self.click(self._remove_button(product_name))

    def button_label_for(self, product_name: str) -> str:
        add = self.driver.find_elements(*self._add_button(product_name))
        return "Add to cart" if add else "Remove"

    def price_of(self, product_name: str) -> float:
        row = self.driver.find_element(
            By.XPATH,
            f'//div[@class="inventory_item" and .//*[normalize-space()="{product_name}"]]'
            f'//*[@data-test="inventory-item-price"]',
        )
        return float(row.text.replace("$", "").strip())

    def open_product(self, product_name: str) -> None:
        self.click(self._item_link(product_name))
        self.wait_for_url_contains("inventory-item.html")

    def cart_count(self) -> int:
        if not self.is_visible(self.CART_BADGE, timeout=2):
            return 0
        return int(self.text_of(self.CART_BADGE))

    def go_to_cart(self) -> None:
        self.click_and_wait_for_url(self.CART_LINK, "cart.html")

    def _open_menu(self) -> None:
        self.js_click(self.BURGER)
        self.find(self.LOGOUT)  # menu items are rendered

    def logout(self) -> None:
        self._open_menu()
        self.click_and_wait_for_url(self.LOGOUT, "saucedemo.com")

    def reset_app_state(self) -> None:
        self._open_menu()
        self.js_click(self.RESET)
        # SauceDemo clears the cart on reset but does not repaint the badge until
        # the page reloads.
        self.driver.get(f"{self.base_url.rstrip('/')}/inventory.html")
        self.wait_until_loaded()
