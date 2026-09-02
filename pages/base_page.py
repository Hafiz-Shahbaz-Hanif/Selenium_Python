"""Shared behaviour for every Page Object."""
from __future__ import annotations

from typing import Sequence

from selenium.common.exceptions import (
    ElementClickInterceptedException,
    TimeoutException,
)
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config.config import CONFIG

Locator = tuple[str, str]


class BasePage:
    """Base class: navigation, waits and thin element helpers.

    Page Objects expose intent-revealing methods; step definitions never touch
    locators or the raw driver.
    """

    #: Path relative to the application base URL, e.g. ``"/inventory.html"``.
    path: str = ""
    #: Absolute base URL for the page's application.
    base_url: str = ""

    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver
        self.wait = WebDriverWait(driver, CONFIG.explicit_wait)

    # --- navigation ---------------------------------------------------------
    def open(self) -> "BasePage":
        self.driver.get(f"{self.base_url.rstrip('/')}/{self.path.lstrip('/')}")
        self.wait_until_loaded()
        return self

    def wait_until_loaded(self) -> None:
        """Override to assert the page's landmark element is present."""

    # --- element helpers --------------------------------------------------
    def find(self, locator: Locator) -> WebElement:
        return self.wait.until(EC.presence_of_element_located(locator))

    def find_all(self, locator: Locator) -> Sequence[WebElement]:
        self.wait.until(EC.presence_of_element_located(locator))
        return self.driver.find_elements(*locator)

    def click(self, locator: Locator) -> None:
        element = self.wait.until(EC.element_to_be_clickable(locator))
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", element
        )
        try:
            element.click()
        except ElementClickInterceptedException:
            # A sticky footer/overlay is in the way - fall back to a JS click.
            self.driver.execute_script("arguments[0].click();", element)

    def js_click(self, locator: Locator) -> None:
        """Synthetic in-page click. Needed for React routing/submit buttons that
        recent headless Chrome does not activate with a native WebDriver click."""
        element = self.wait.until(EC.element_to_be_clickable(locator))
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", element)
        self.driver.execute_script("arguments[0].click();", element)

    def click_and_wait_for_url(
        self, locator: Locator, url_fragment: str, attempts: int = 4
    ) -> None:
        """Click, then confirm navigation happened.

        SauceDemo is a React app and, on recent headless Chrome, the native
        WebDriver click on some routing buttons does not fire the React handler.
        The first attempt uses a native click; retries fall back to a synthetic
        ``element.click()`` in the page, which does trigger the handler.
        """
        for attempt in range(attempts):
            element = self.wait.until(EC.element_to_be_clickable(locator))
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center'});", element
            )
            if attempt == 0:
                try:
                    element.click()
                except ElementClickInterceptedException:
                    self.driver.execute_script("arguments[0].click();", element)
            else:
                self.driver.execute_script("arguments[0].click();", element)
            try:
                WebDriverWait(self.driver, 8).until(EC.url_contains(url_fragment))
                return
            except TimeoutException:
                if attempt == attempts - 1:
                    raise

    def type(self, locator: Locator, text: str) -> None:
        element = self.wait.until(EC.visibility_of_element_located(locator))
        element.clear()
        element.send_keys(text)

    def text_of(self, locator: Locator) -> str:
        return self.wait.until(EC.visibility_of_element_located(locator)).text.strip()

    def is_visible(self, locator: Locator, timeout: float | None = None) -> bool:
        try:
            WebDriverWait(self.driver, timeout or CONFIG.explicit_wait).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except Exception:  # noqa: BLE001 - visibility probe
            return False

    def wait_for_url_contains(self, fragment: str) -> None:
        self.wait.until(EC.url_contains(fragment))

    def wait_for_dom_ready(self) -> None:
        self.wait.until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )

    def current_url(self) -> str:
        return self.driver.current_url
