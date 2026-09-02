"""OrangeHRM dashboard - left menu navigation and top bar."""
from __future__ import annotations

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config.config import CONFIG
from pages.base_page import BasePage
from pages.orangehrm_login_page import OrangeHrmLoginPage

# The public OrangeHRM demo is noticeably slower than SauceDemo.
ORANGEHRM_WAIT_S = 40


class OrangeHrmDashboardPage(BasePage):
    base_url = CONFIG.orangehrm_url
    path = "/web/index.php/dashboard/index"

    MENU_SEARCH = (By.CSS_SELECTOR, ".oxd-main-menu-search input")
    PAGE_TITLE = (By.CSS_SELECTOR, ".oxd-topbar-header-breadcrumb h6")
    USER_DROPDOWN = (By.CSS_SELECTOR, ".oxd-userdropdown-tab")
    LOGOUT_LINK = (By.XPATH, "//a[normalize-space()='Logout']")

    def __init__(self, driver) -> None:
        super().__init__(driver)
        self.wait = WebDriverWait(driver, ORANGEHRM_WAIT_S)

    def wait_until_loaded(self) -> None:
        self.wait.until(EC.visibility_of_element_located(self.PAGE_TITLE))

    def _menu_item(self, name: str) -> tuple[str, str]:
        return (By.XPATH, f"//aside//a[.//span[normalize-space()='{name}']]")

    def open_menu(self, name: str) -> None:
        self.js_click(self._menu_item(name))

    def current_page_title(self) -> str:
        return self.wait.until(
            EC.visibility_of_element_located(self.PAGE_TITLE)
        ).text.strip()

    def is_menu_present(self, name: str) -> bool:
        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "aside .oxd-main-menu")))
        return len(self.driver.find_elements(*self._menu_item(name))) > 0

    def logout(self) -> OrangeHrmLoginPage:
        self.js_click(self.USER_DROPDOWN)
        self.wait.until(EC.visibility_of_element_located(self.LOGOUT_LINK))
        self.js_click(self.LOGOUT_LINK)
        self.wait.until(EC.url_contains("auth/login"))
        return OrangeHrmLoginPage(self.driver)
