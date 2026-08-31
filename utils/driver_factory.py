"""WebDriver creation.

Selenium 4.6+ ships **Selenium Manager**, which resolves and downloads the
correct driver binary automatically - so there are no chromedriver/geckodriver
files to manage or commit.
"""
from __future__ import annotations

from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver

from config.config import Config


def _chrome_options(config: Config) -> webdriver.ChromeOptions:
    options = webdriver.ChromeOptions()
    if config.headless:
        options.add_argument("--headless=new")
    width, height = config.window_dimensions
    options.add_argument(f"--window-size={width},{height}")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    return options


def _firefox_options(config: Config) -> webdriver.FirefoxOptions:
    options = webdriver.FirefoxOptions()
    if config.headless:
        options.add_argument("--headless")
    width, height = config.window_dimensions
    options.add_argument(f"--width={width}")
    options.add_argument(f"--height={height}")
    return options


def create_driver(config: Config) -> WebDriver:
    browser = config.browser.lower()

    if browser in {"chrome", "chromium"}:
        options = _chrome_options(config)
    elif browser in {"firefox", "ff"}:
        options = _firefox_options(config)
    else:  # pragma: no cover - guard
        raise ValueError(f"Unsupported browser: {config.browser!r}")

    if config.remote_url:
        driver = webdriver.Remote(command_executor=config.remote_url, options=options)
    elif browser in {"chrome", "chromium"}:
        driver = webdriver.Chrome(options=options)
    else:
        driver = webdriver.Firefox(options=options)

    if config.implicit_wait:
        driver.implicitly_wait(config.implicit_wait)
    driver.set_page_load_timeout(config.page_load_timeout)
    return driver
