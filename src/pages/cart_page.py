import allure
from playwright.sync_api import Locator, Page


class CartPage:
    def __init__(self, page: Page):
        self.page = page
        self.items = page.locator('[data-test="inventory-item"]')
        self.item_names = page.locator('[data-test="inventory-item-name"]')
        self.checkout_button = page.locator('[data-test="checkout"]')

    def item(self, name: str) -> Locator:
        return self.item_names.filter(has_text=name)

    @allure.step("Перейти к оформлению заказа")
    def checkout(self):
        self.checkout_button.click()
