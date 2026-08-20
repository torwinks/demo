"""Базовый Page Object: общие действия для всех страниц."""

from __future__ import annotations

from playwright.sync_api import Locator, Page, expect


class BasePage:
    def __init__(self, page: Page, base_url: str) -> None:
        self.page = page
        self.base_url = base_url.rstrip("/")

    def open(self, path: str = "/") -> None:
        url = path if path.startswith("http") else f"{self.base_url}{path}"
        self.page.goto(url)

    def click(self, locator: Locator) -> None:
        locator.click()

    def fill(self, locator: Locator, value: str) -> None:
        locator.fill(value)

    def expect_visible(self, locator: Locator) -> None:
        expect(locator).to_be_visible()

    def expect_text(self, locator: Locator, text: str) -> None:
        expect(locator).to_contain_text(text)
