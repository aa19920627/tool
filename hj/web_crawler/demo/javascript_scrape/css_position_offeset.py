#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : 洪建
# @File : css_position_offeset.py
# @Time : 2025/11/28 16:07


"""CSS位置偏移反爬案例"""
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyquery import PyQuery


def parse_name(name_html):
    has_whole = name_html('.whole')
    if has_whole:
        return name_html.text()
    else:
        chars = name_html('.char')
        items = []
        for char in chars.items():
            items.append({
                'text': char.text().strip(),
                'left': int(re.search('(\d+)px', char.attr('style')).group(1)),
            })
        items = sorted(items, key=lambda x: x['left'], reverse=False)
        return ''.join([item.get('text') for item in items])


browser = webdriver.Chrome()
browser.get('https://antispider3.scrape.center/')
WebDriverWait(browser, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.item')))
html = browser.page_source
doc = PyQuery(html)
names = doc('.item .name')
for name_html in names.items():
    name = parse_name(name_html)
    print(name)
browser.close()
