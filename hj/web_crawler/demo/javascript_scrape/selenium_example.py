#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : 洪建
# @File : selenium_example.py
# @Time : 2025/11/27 16:06


"""selenium实例"""
import json
import logging
import re
from os import makedirs
from os.path import exists
from urllib.parse import urljoin
from selenium.webdriver.chrome.options import Options
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
RESULTS_DIR = "results"  # 数据存储路径
# 判断数据存储路径是否存在，不存在创建
exists(RESULTS_DIR) or makedirs(RESULTS_DIR)

# 设置Chrome选项,禁用自动化控制提示，禁用测试版警告信息显示
chrome_options = Options()
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--headless")   # 设置无头模式

browser = webdriver.Chrome(options=chrome_options)
# 全屏显示
browser.maximize_window()

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
    elements = browser.find_elements(By.CSS_SELECTOR, '#index .item .name')
    for element in elements:
        href = element.get_attribute('href')
        yield urljoin(INDEX_URL, href)


# 爬取详情页
def scrape_detail(url):
    # 爬取页面，等待h2节点出现
    scrape_page(url, condition=EC.visibility_of_element_located, locator=(By.TAG_NAME, 'h2'))


# 解析详情页
def parse_detail():
    url = browser.current_url
    name = browser.find_element(By.TAG_NAME, 'h2').text
    categories = [element.text for element in browser.find_elements(By.CSS_SELECTOR, '.categories button span')]
    cover = browser.find_element(By.CSS_SELECTOR, '.cover').get_attribute('src')
    score = browser.find_element(By.CLASS_NAME, 'score').text
    drama = browser.find_element(By.CSS_SELECTOR, '.drama p').text

    name = re.sub(r"[:：]", "", name) if isinstance(name, str) else name

    return {
        'url': url,
        'name': name,
        'categories': categories,
        'cover': cover,
        'score': score,
        'drama': drama,
    }


# 数据存储
def save_data(data):
    name = data.get('name')
    data_path = f'{RESULTS_DIR}/{name}.json'
    json.dump(data, open(data_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)


def main():
    try:
        for page in range(1, TOTAL_PAGE + 1):
            scrape_index(page)
            detail_urls = parse_index()
            for detail_url in list(detail_urls):
                logging.info('get detail url %s', detail_url)
                scrape_detail(detail_url)
                detail_data = parse_detail()
                logging.info('detail data %s', detail_data)
                save_data(detail_data)  # 存储数据
    finally:
        browser.close()


if __name__ == '__main__':
    main()
