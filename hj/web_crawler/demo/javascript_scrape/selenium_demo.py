#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : 洪建
# @File : selenium_demo.py
# @Time : 2025/11/18 11:28

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

"""用Selenium爬取JavaScripts动态渲染数据"""

# 设置Chrome选项,禁用自动化控制提示，禁用测试版警告信息显示
# chrome_options = Options()
# chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
# chrome_options.add_argument("--disable-blink-features=AutomationControlled")
# chrome_options.add_argument("--disable-infobars")

browser = webdriver.Chrome()

# # 全屏显示
# browser.maximize_window()
#
# try:
#     browser.get("https://www.baidu.com/")
#     input = browser.find_element(By.ID, "chat-textarea")
#     input.send_keys('Python')
#     input.send_keys(Keys.ENTER)
#     wait = WebDriverWait(browser, 10)
#     wait.until(EC.presence_of_element_located((By.ID, 'content_left')))
#     print(browser.current_url)
#     print(browser.get_cookies())
#     print(browser.page_source)
# finally:
#     browser.close()