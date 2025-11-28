#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : 洪建
# @File : playwright_demo.py
# @Time : 2025/11/18 16:35


"""playwright库的示例"""
import asyncio
import re

from playwright.async_api import async_playwright
from playwright.sync_api import sync_playwright


# # 同步模式示例
# with sync_playwright() as p:
#     for browser_type in [p.chromium, p.firefox, p.webkit]:
#         browser = browser_type.launch(headless=False)
#         page = browser.new_page()
#         page.goto("https://www.baidu.com/")
#         page.screenshot(path = f'screenshot - {browser_type.name}.png')
#         print(page.title())
#         browser.close()

# # 异步模式示例
# async def main():
#     async with async_playwright() as p:
#         for browser_type in [p.chromium, p.firefox, p.webkit]:
#             browser = await browser_type.launch()
#             page = await browser.new_page()
#             await page.goto('https://www.baidu.com/')
#             await page.screenshot(path=f'screenshot - {browser_type.name}.png')
#             print(await page.title())
#             await browser.close()
#
# asyncio.run(main())

# # 模拟手机浏览器
# with sync_playwright() as p:
#     iphone_12_pro_max = p.devices['iPhone 12 Pro Max']
#     browser = p.webkit.launch(headless=False)
#     context = browser.new_context(
#         **iphone_12_pro_max,
#         locale='zh-CN'
#     )
#     page = context.new_page()
#     page.goto('https://www.whatismybrowser.com/')
#     page.wait_for_load_state(state='networkidle')
#     page.screenshot(path='browser-iphone.png')
#     browser.close()


# 事件监听
# def on_response(response):
#     if '/api/movie/' in response.url and response.status == 200:
#         print(response.json())
#
#
# with sync_playwright() as p:
#     browser = p.chromium.launch(headless=False)
#     page = browser.new_page()
#     page.on('response', on_response)
#     page.goto('https://spa6.scrape.center/')
#     page.wait_for_load_state('networkidle')
#     browser.close()


#网络劫持
with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    def cancel_request(route,request):
        route.abort()

    page.route(re.compile(r"(\.png)|(\.jpg)"),cancel_request)
    page.goto("https://spa6.scrape.center/")
    page.wait_for_load_state("networkidle")
    page.screenshot(path = "no_picture.png")
    browser.close()