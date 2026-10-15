
from selenium import webdriver
from selenium.webdriver.common.by import By


def test_open_python_website():
    driver = webdriver.Chrome()

    try:
        driver.get("https://www.python.org/")
        heading = driver.find_element(By.ID, "id-search-field")
        assert heading.is_displayed()
    finally:
        driver.quit()
