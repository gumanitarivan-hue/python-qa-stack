from playwright.sync_api import sync_playwright


def test_open_python_website():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        page = browser.new_page()

        try:
            page.goto("https://www.python.org/")
            assert "Python" in page.title()
        finally:
            browser.close()
