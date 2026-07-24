from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

def scrape_page(url, table_selector, click_selector=None, scroll=False, timeout=15000):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)
        page.wait_for_selector(table_selector, timeout=timeout)

        if click_selector:
            page.click(click_selector)
            page.wait_for_timeout(2000)

        if scroll:
            previous_count = 0
            while True:
                page.mouse.wheel(0, 3000)
                page.wait_for_timeout(500)
                current_count = len(page.query_selector_all("tr"))
                if current_count == previous_count:
                    break
                previous_count = current_count

        html = page.content()
        browser.close()

    soup = BeautifulSoup(html, "html.parser")
    table = soup.select_one(table_selector)
    return str(table) if table else None

def get_full_page_html(url, wait_selector, timeout=15000):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)
        page.wait_for_selector(wait_selector, timeout=timeout)
        html = page.content()
        browser.close()

    return html