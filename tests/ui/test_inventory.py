import allure
import pytest
from playwright.sync_api import expect

from src.pages.inventory_page import InventoryPage

pytestmark = pytest.mark.ui


@allure.title("В каталоге 6 товаров")
def test_products_count(inventory: InventoryPage):
    expect(inventory.items).to_have_count(6)


@allure.title("Сортировка по названию: {option}")
@pytest.mark.parametrize("option, reverse", [("az", False), ("za", True)])
def test_sort_by_name(inventory: InventoryPage, option, reverse):
    expect(inventory.items).to_have_count(6)
    names = inventory.item_names.all_inner_texts()

    inventory.sort_by(option)

    expect(inventory.item_names).to_have_text(sorted(names, reverse=reverse))


@allure.title("Сортировка по цене: {option}")
@pytest.mark.parametrize("option, reverse", [("lohi", False), ("hilo", True)])
def test_sort_by_price(inventory: InventoryPage, option, reverse):
    expect(inventory.items).to_have_count(6)
    texts = inventory.item_prices.all_inner_texts()
    prices = [float(text.removeprefix("$")) for text in texts]

    inventory.sort_by(option)

    expected = [f"${price:.2f}" for price in sorted(prices, reverse=reverse)]
    expect(inventory.item_prices).to_have_text(expected)
