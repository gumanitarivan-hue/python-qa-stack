from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def test_open_python_website():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")

    driver = webdriver.Chrome(options=options)

    try:
        driver.get("https://www.python.org/")
        assert "Python" in driver.title
    finally:
        driver.quit()