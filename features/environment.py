"""Behave lifecycle hooks: WebDriver setup/teardown, failure screenshots and
Allure attachments.

A fresh browser session is created per scenario for isolation. On failure the
page screenshot, current URL and page source are attached to the Allure report.
"""
from __future__ import annotations

import os

import allure

from config.config import CONFIG  # noqa: F401 - re-exported default config
from utils.driver_factory import create_driver


def before_all(context) -> None:
    context.config.setup_logging()
    context.app_config = CONFIG.with_userdata(context.config.userdata)
    os.makedirs(context.app_config.artifacts_dir, exist_ok=True)


def before_scenario(context, scenario) -> None:
    context.driver = create_driver(context.app_config)


def after_step(context, step) -> None:
    if step.status == "failed" and getattr(context, "driver", None):
        _attach_failure_artifacts(context, step.name)


def after_scenario(context, scenario) -> None:
    driver = getattr(context, "driver", None)
    if driver is None:
        return
    service_pid = _service_pid(driver)
    try:
        driver.quit()
    except Exception:  # noqa: BLE001 - teardown must not fail the run
        pass
    finally:
        context.driver = None
        # Headless Chrome on Windows occasionally survives driver.quit(); across a
        # 100+ scenario run those orphans exhaust the machine. Reap the tree.
        _reap(service_pid)


def _service_pid(driver):
    try:
        return driver.service.process.pid
    except Exception:  # noqa: BLE001
        return None


def _reap(pid) -> None:
    if not pid:
        return
    try:
        import psutil  # optional; present via selenium's deps on most setups

        proc = psutil.Process(pid)
        for child in proc.children(recursive=True):
            child.kill()
        proc.kill()
    except Exception:  # noqa: BLE001
        if os.name == "nt":
            os.system(f"taskkill /F /T /PID {pid} >NUL 2>&1")


def _attach_failure_artifacts(context, label: str) -> None:
    driver = context.driver
    try:
        allure.attach(
            driver.get_screenshot_as_png(),
            name=f"screenshot - {label}",
            attachment_type=allure.attachment_type.PNG,
        )
        allure.attach(driver.current_url, name="url", attachment_type=allure.attachment_type.TEXT)
        allure.attach(
            driver.page_source,
            name="page source",
            attachment_type=allure.attachment_type.HTML,
        )
    except Exception:  # noqa: BLE001 - never mask the real failure
        pass
