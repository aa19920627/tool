import re
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.firefox.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.baidu.com/")
    page.get_by_role("textbox", name="合肥市委副书记路军被查").click()
    with page.expect_popup() as page1_info:
        page.get_by_role("link", name="高市早苗或于12月26日参拜靖国神社").click()
    page1 = page1_info.value
    with page1.expect_popup() as page2_info:
        page1.locator("#content_left").get_by_role("link", name="高市早苗或于12月26日参拜靖国神社", exact=True).click()
    page2 = page2_info.value
    page2.close()
    page1.close()
    page.get_by_role("textbox", name="合肥市委副书记路军被查").click()
    page.get_by_role("textbox", name="合肥市委副书记路军被查").fill("haha")
    page.get_by_role("link", name="图片").click()
    page.close()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
