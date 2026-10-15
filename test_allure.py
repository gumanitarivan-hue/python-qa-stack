
import allure


@allure.title("Проверка сложения")
@allure.feature("Калькулятор")
@allure.story("Базовые операции")
def test_addition():
    assert 2 + 2 == 4
