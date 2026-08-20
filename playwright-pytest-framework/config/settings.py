"""Центральные настройки стенда.

На собеседовании часто спрашивают: «где берётся URL и креды?»
Ответ: из env / .env, а не захардкожены в тестах.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

# Корень фреймворка: .../playwright-pytest-framework
ROOT_DIR = Path(__file__).resolve().parent.parent
load_dotenv(ROOT_DIR / ".env")


@dataclass(frozen=True)
class Settings:
    base_url: str
    username: str
    password: str
    browser: str
    headless: bool
    timeout_ms: int


def get_settings() -> Settings:
    return Settings(
        base_url=os.getenv("BASE_URL", "https://the-internet.herokuapp.com"),
        username=os.getenv("USERNAME", "tomsmith"),
        password=os.getenv("PASSWORD", "SuperSecretPassword!"),
        browser=os.getenv("BROWSER", "chromium"),
        headless=os.getenv("HEADLESS", "true").lower() == "true",
        timeout_ms=int(os.getenv("TIMEOUT_MS", "10000")),
    )
