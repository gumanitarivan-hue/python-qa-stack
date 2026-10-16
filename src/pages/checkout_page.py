import allure
from playwright.sync_api import Page


class CheckoutPage:
    def __init__(self, page: Page):
        self.page = page
        self.first_name = page.locator('[data-test="firstName"]')
        self.last_name = page.locator('[data-test="lastName"]')
        self.postal_code = page.locator('[data-test="postalCode"]')
        self.continue_button = page.locator('[data-test="continue"]')
        self.finish_button = page.locator('[data-test="finish"]')
        self.error = page.locator('[data-test="error"]')
        self.complete_header = page.locator('[data-test="complete-header"]')

    @allure.step("Заполнить данные покупателя")
    def fill_info(self, first_name: str, last_name: str, postal_code: str):
        self.first_name.fill(first_name)
        self.last_name.fill(last_name)
        self.postal_code.fill(postal_code)

    @allure.step("Продолжить оформление")
    def submit_info(self):
        self.continue_button.click()

    @allure.step("Завершить заказ")
    def finish_order(self):
        self.finish_button.click()
