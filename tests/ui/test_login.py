import re

import allure
import pytest
from playwright.sync_api import Page, expect

from src.pages.inventory_page import InventoryPage
from src.pages.login_page import LoginPage
from src.ui_data import LOCKED_USER, PASSWORD, STANDARD_USER

pytestmark = pytest.mark.ui


@allure.title("Успешный вход стандартным пользователем")
def test_login_success(page: Page, login_page: LoginPage):
    login_page.login(STANDARD_USER, PASSWORD)

    expect(page).to_have_url(re.compile(r".*/inventory\.html"))
    expect(InventoryPage(page).title).to_have_text("Products")


@allure.title("Вход с неверными данными показывает ошибку")
@pytest.mark.parametrize(
    "username, password, message",
    [
        (LOCKED_USER, PASSWORD, "this user has been locked out"),
        (STANDARD_USER, "wrong_password", "do not match any user"),
        ("", PASSWORD, "Username is required"),
        (STANDARD_USER, "", "Password is required"),
    ],
)
def test_login_invalid(login_page: LoginPage, username, password, message):
    login_page.login(username, password)

    expect(login_page.error).to_contain_text(message)


@allure.title("Выход из аккаунта возвращает на страницу логина")
def test_logout(inventory: InventoryPage, login_page: LoginPage):
    inventory.logout()

    expect(login_page.login_button).to_be_visible()


@allure.title("Каталог недоступен без авторизации")
def test_inventory_requires_login(page: Page):
    page.goto("/inventory.html")

    expect(LoginPage(page).error).to_contain_text("You can only access")
