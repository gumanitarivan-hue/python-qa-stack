import allure
from playwright.sync_api import Page


class InventoryPage:
    def __init__(self, page: Page):
        self.page = page
        self.title = page.locator('[data-test="title"]')
        self.items = page.locator('[data-test="inventory-item"]')
        self.item_names = page.locator('[data-test="inventory-item-name"]')
        self.item_prices = page.locator('[data-test="inventory-item-price"]')
        self.sort_select = page.locator('[data-test="product-sort-container"]')
        self.cart_badge = page.locator('[data-test="shopping-cart-badge"]')
        self.cart_link = page.locator('[data-test="shopping-cart-link"]')
        self.menu_button = page.locator("#react-burger-menu-btn")
        self.logout_link = page.locator('[data-test="logout-sidebar-link"]')

    @allure.step("Добавить товар в корзину: {slug}")
    def add_to_cart(self, slug: str):
        self.page.locator(f'[data-test="add-to-cart-{slug}"]').click()

    @allure.step("Убрать товар из корзины: {slug}")
    def remove_from_cart(self, slug: str):
        self.page.locator(f'[data-test="remove-{slug}"]').click()

    @allure.step("Отсортировать товары: {option}")
    def sort_by(self, option: str):
        self.sort_select.select_option(option)

    @allure.step("Открыть корзину")
    def open_cart(self):
        self.cart_link.click()

    @allure.step("Выйти из аккаунта")
    def logout(self):
        self.menu_button.click()
        self.logout_link.click()
