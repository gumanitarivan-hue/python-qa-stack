import allure
import pytest
from playwright.sync_api import Page, expect

from src.pages.cart_page import CartPage
from src.pages.inventory_page import InventoryPage
from src.ui_data import BACKPACK, BIKE_LIGHT, PRODUCT_NAMES

pytestmark = pytest.mark.ui


@allure.title("Добавление товара увеличивает счётчик корзины")
def test_add_one_item(inventory: InventoryPage):
    inventory.add_to_cart(BACKPACK)

    expect(inventory.cart_badge).to_have_text("1")


@allure.title("Добавленные товары отображаются в корзине")
def test_added_items_are_in_cart(page: Page, inventory: InventoryPage):
    inventory.add_to_cart(BACKPACK)
    inventory.add_to_cart(BIKE_LIGHT)
    expect(inventory.cart_badge).to_have_text("2")

    inventory.open_cart()

    cart = CartPage(page)
    expect(cart.items).to_have_count(2)
    expect(cart.item(PRODUCT_NAMES[BACKPACK])).to_have_count(1)
    expect(cart.item(PRODUCT_NAMES[BIKE_LIGHT])).to_have_count(1)


@allure.title("Удаление товара убирает счётчик корзины")
def test_remove_item(inventory: InventoryPage):
    inventory.add_to_cart(BACKPACK)

    inventory.remove_from_cart(BACKPACK)

    expect(inventory.cart_badge).to_have_count(0)
