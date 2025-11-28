#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : 洪建
# @File : selenium_example.py
# @Time : 2025/11/27 16:06


"""selenium实例"""
import logging
from urllib.parse import urljoin

from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s: %(message)s')

INDEX_URL = "https://spa2.scrape.center/page/{page}"
TIME_OUT = 10
TOTAL_PAGE = 10

browser = webdriver.Chrome()
wait = WebDriverWait(browser, TIME_OUT)


# 爬取页面，隐式等待页面加载出指定资源
def scrape_page(url, condition, locator):
    logging.info('scraping %s', url)
    try:
        browser.get(url)
        wait.until(condition(locator))
    except TimeoutException:
        logging.error('timed out for %s', url)


def scrape_index(page):
    url = INDEX_URL.format(page=page)
    scrape_page(url, condition=EC.visibility_of_element_located, locator=(By.CSS_SELECTOR, '#index .item'))


# 解析列表页的方法
def parse_index():
    elements = browser.find_elements_by_css_selector('#index .item .name')
    for element in elements:
        href = element.get_attribute('href')
        yield urljoin(INDEX_URL, href)


def main():
    try:
        for page in range(1, TOTAL_PAGE + 1):
            scrape_index(page)
            detail_urls = parse_index()
            logging.info('details urls %s', list(detail_urls))
    finally:
        browser.close()

if __name__ == '__main__':
    scrape_index(1)