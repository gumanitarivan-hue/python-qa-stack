import allure
import pytest
from playwright.sync_api import Page, expect

from src.pages.cart_page import CartPage
from src.pages.checkout_page import CheckoutPage
from src.pages.inventory_page import InventoryPage
from src.ui_data import BACKPACK

pytestmark = pytest.mark.ui


@pytest.fixture
def checkout(page: Page, inventory: InventoryPage) -> CheckoutPage:
    """Пользователь с товаром в корзине на странице ввода данных."""
    inventory.add_to_cart(BACKPACK)
    inventory.open_cart()
    CartPage(page).checkout()
    return CheckoutPage(page)


@allure.title("Оформление заказа от входа до подтверждения")
def test_checkout_happy_path(checkout: CheckoutPage):
    checkout.fill_info("John", "Doe", "12345")
    checkout.submit_info()
    checkout.finish_order()

    expect(checkout.complete_header).to_have_text("Thank you for your order!")


@allure.title("Незаполненное поле на шаге данных показывает ошибку")
@pytest.mark.parametrize(
    "first_name, last_name, postal_code, message",
    [
        ("", "Doe", "12345", "First Name is required"),
        ("John", "", "12345", "Last Name is required"),
        ("John", "Doe", "", "Postal Code is required"),
    ],
)
def test_checkout_validation(checkout: CheckoutPage, first_name, last_name, postal_code, message):
    checkout.fill_info(first_name, last_name, postal_code)
    checkout.submit_info()

    expect(checkout.error).to_contain_text(message)
