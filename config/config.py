"""Central, environment-driven configuration.

Every value has a working default so the suite runs out of the box against the
public demo applications. Override with an environment variable (optionally via
a local ``.env`` file) or with Behave userdata (``-D headless=false``).
"""
from __future__ import annotations

import os
from dataclasses import dataclass, replace
from typing import Any, Mapping

from dotenv import load_dotenv

load_dotenv()


def _bool(value: Any, default: bool = False) -> bool:
    if value is None:
        return default
    return str(value).strip().lower() in {"1", "true", "yes", "on"}


@dataclass(frozen=True)
class Config:
    # --- browser ---
    browser: str = os.getenv("BROWSER", "chrome")
    headless: bool = _bool(os.getenv("HEADLESS"), True)
    window_size: str = os.getenv("WINDOW_SIZE", "1920,1080")
    remote_url: str | None = os.getenv("SELENIUM_REMOTE_URL") or None

    # --- timeouts (seconds) ---
    implicit_wait: float = float(os.getenv("IMPLICIT_WAIT", "0"))
    explicit_wait: float = float(os.getenv("EXPLICIT_WAIT", "15"))
    page_load_timeout: float = float(os.getenv("PAGE_LOAD_TIMEOUT", "40"))

    # --- applications under test ---
    saucedemo_url: str = os.getenv("SAUCEDEMO_URL", "https://www.saucedemo.com")
    orangehrm_url: str = os.getenv(
        "ORANGEHRM_URL", "https://opensource-demo.orangehrmlive.com"
    )

    # --- credentials (public demo creds) ---
    saucedemo_user: str = os.getenv("SAUCEDEMO_USER", "standard_user")
    saucedemo_password: str = os.getenv("SAUCEDEMO_PASSWORD", "secret_sauce")
    orangehrm_user: str = os.getenv("ORANGEHRM_USER", "Admin")
    orangehrm_password: str = os.getenv("ORANGEHRM_PASSWORD", "admin123")

    # --- artifacts ---
    artifacts_dir: str = os.getenv("ARTIFACTS_DIR", "reports")
    screenshot_on_failure: bool = _bool(os.getenv("SCREENSHOT_ON_FAILURE"), True)

    @property
    def window_dimensions(self) -> tuple[int, int]:
        width, _, height = self.window_size.partition(",")
        return int(width), int(height)

    def with_userdata(self, userdata: Mapping[str, Any]) -> "Config":
        """Return a copy with Behave ``-D`` overrides applied."""
        overrides: dict[str, Any] = {}
        if "browser" in userdata:
            overrides["browser"] = str(userdata["browser"])
        if "headless" in userdata:
            overrides["headless"] = _bool(userdata["headless"], self.headless)
        return replace(self, **overrides) if overrides else self


CONFIG = Config()
