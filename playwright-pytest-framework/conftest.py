"""Точка сборки рантайма тестов.

Читай этот файл первым после pytest.ini / requirements.txt.
Здесь живут фикстуры: браузер, контекст, page, page objects, данные.
"""

from __future__ import annotations

import pytest
from playwright.sync_api import Browser, BrowserContext, Page, Playwright, sync_playwright

from config.settings import Settings, get_settings
from pages.login_page import LoginPage


@pytest.fixture(scope="session")
def settings() -> Settings:
    """Один раз на всю сессию: URL, креды, таймауты."""
    return get_settings()


@pytest.fixture(scope="session")
def playwright_instance() -> Playwright:
    """Собственный lifecycle Playwright — чтобы было видно «как устроен движок»."""
    with sync_playwright() as p:
        yield p


@pytest.fixture(scope="session")
def browser(playwright_instance: Playwright, settings: Settings) -> Browser:
    browser_type = getattr(playwright_instance, settings.browser)
    browser = browser_type.launch(headless=settings.headless)
    yield browser
    browser.close()


@pytest.fixture
def context(browser: Browser, settings: Settings) -> BrowserContext:
    """Новый контекст = чистая сессия (cookies/storage) на каждый тест."""
    ctx = browser.new_context(base_url=settings.base_url)
    ctx.set_default_timeout(settings.timeout_ms)
    yield ctx
    ctx.close()


@pytest.fixture
def page(context: BrowserContext) -> Page:
    page = context.new_page()
    yield page
    page.close()


@pytest.fixture
def login_page(page: Page, settings: Settings) -> LoginPage:
    """Готовый Page Object — тест получает уже собранную страницу."""
    return LoginPage(page, settings.base_url)


@pytest.fixture
def valid_user(settings: Settings) -> dict[str, str]:
    return {"username": settings.username, "password": settings.password}
