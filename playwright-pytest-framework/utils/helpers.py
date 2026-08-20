"""Небольшие хелперы (скриншоты, ожидания, парсинг).

В реальных фреймворках сюда кладут то, что не принадлежит конкретной странице.
"""

from __future__ import annotations

from pathlib import Path

from playwright.sync_api import Page


def take_screenshot(page: Page, name: str, directory: str = "artifacts") -> Path:
    out = Path(directory)
    out.mkdir(parents=True, exist_ok=True)
    path = out / f"{name}.png"
    page.screenshot(path=str(path), full_page=True)
    return path
