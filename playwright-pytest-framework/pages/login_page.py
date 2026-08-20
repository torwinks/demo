"""Page Object страницы логина (the-internet.herokuapp.com/login)."""

from __future__ import annotations

from playwright.sync_api import Page

from pages.base_page import BasePage


class LoginPage(BasePage):
    PATH = "/login"

    def __init__(self, page: Page, base_url: str) -> None:
        super().__init__(page, base_url)
        # Локаторы — «карта» UI. Тест не знает CSS, знает только методы страницы.
        self.username_input = page.locator("#username")
        self.password_input = page.locator("#password")
        self.login_button = page.locator("button[type='submit']")
        self.flash_message = page.locator("#flash")

    def open_login(self) -> "LoginPage":
        self.open(self.PATH)
        return self

    def login(self, username: str, password: str) -> None:
        self.fill(self.username_input, username)
        self.fill(self.password_input, password)
        self.click(self.login_button)

    def expect_success(self) -> None:
        self.expect_text(self.flash_message, "You logged into a secure area!")

    def expect_failure(self) -> None:
        self.expect_text(self.flash_message, "Your username is invalid!")
