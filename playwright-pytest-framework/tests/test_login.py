"""UI-тесты логина.

Паттерн AAA: Arrange → Act → Assert.
Тест описывает бизнес-сценарий, детали UI — в Page Object.
"""

import pytest


@pytest.mark.smoke
@pytest.mark.login
def test_successful_login(login_page, valid_user):
    # Arrange
    login_page.open_login()

    # Act
    login_page.login(valid_user["username"], valid_user["password"])

    # Assert
    login_page.expect_success()


@pytest.mark.regression
@pytest.mark.login
def test_login_with_invalid_username(login_page, valid_user):
    login_page.open_login()
    login_page.login("wrong-user", valid_user["password"])
    login_page.expect_failure()
