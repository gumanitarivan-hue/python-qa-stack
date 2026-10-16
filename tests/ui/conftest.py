import pytest
from playwright.sync_api import Page, expect

from src.pages.inventory_page import InventoryPage
from src.pages.login_page import LoginPage
from src.ui_data import PASSWORD, STANDARD_USER


@pytest.fixture
def login_page(page: Page) -> LoginPage:
    """Открытая страница логина."""
    return LoginPage(page).open()


@pytest.fixture
def inventory(page: Page, login_page: LoginPage) -> InventoryPage:
    """Авторизованный пользователь на странице каталога."""
    login_page.login(STANDARD_USER, PASSWORD)
    inventory_page = InventoryPage(page)
    expect(inventory_page.title).to_have_text("Products")
    return inventory_page
