import allure
from playwright.sync_api import Page


class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.username = page.locator('[data-test="username"]')
        self.password = page.locator('[data-test="password"]')
        self.login_button = page.locator('[data-test="login-button"]')
        self.error = page.locator('[data-test="error"]')

    @allure.step("Открыть страницу логина")
    def open(self):
        self.page.goto("/")
        return self

    @allure.step("Войти как '{username}'")
    def login(self, username: str, password: str):
        self.username.fill(username)
        self.password.fill(password)
        self.login_button.click()
