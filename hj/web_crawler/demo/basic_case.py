#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : 洪建
# @File : basic_case.py
# @Time : 2025/11/6 13:43
import requests
import logging
import re
from urllib.parse import urljoin
import json
from os import makedirs
from os.path import exists
import multiprocessing

'''爬虫基础案例'''

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
BASE_URL = 'https://ssr1.scrape.center'
TOTAL_PAGE = 10
RESULTS_DIR = 'results'
exists(RESULTS_DIR) or makedirs(RESULTS_DIR)


# 爬取页面通用方法
def scrape_page(url):
    logging.info('scraping %s' % url)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        logging.error('get invalid status %s while scraping %s' % (response.status_code, url))
    except requests.RequestException:
        logging.error('error occurred while scraping %s', url, exc_info=True)


# 定义列表爬取方法
def scrape_index(page):
    index_url = f'{BASE_URL}/page/{page}'
    return scrape_page(index_url)


# 解析列表页
def parse_index(html):
    pattern = re.compile('<a.*?href="(.*?)".*?class="name"')
    items = re.findall(pattern, html)
    if not items:
        return []
    for item in items:
        detail_url = urljoin(BASE_URL, item)
        logging.info('get detail url %s', detail_url)
        yield detail_url


# 详情页爬取
def scrape_detail(url):
    return scrape_page(url)


# 详情页解析
def parse_detail(html):
    # 封面正则匹配
    cover_pattern = re.compile('class="item.*?<img.*?src="(.*?)".*?class="cover">', re.S)
    # 影片名正则匹配
    name_pattern = re.compile('<h2.*?>(.*?)</h2>', re.S)
    # 影片类别正则匹配
    categories_pattern = re.compile('<button.*?category.*?<span>(.*?)</span>.*?</button>', re.S)
    # 上映时间正则匹配
    published_at_pattern = re.compile('(\d{4}-\d{2}-\d{2})\s?上映')
    # 剧情简介正则匹配
    drama_pattern = re.compile('<div.*?drama.*?>.*?<p.*?>(.*?)</p>', re.S)
    # 剧情评分正则匹配
    score_pattern = re.compile('<p.*?score.*?>(.*?)</p>', re.S)

    cover = re.search(cover_pattern, html).group(1).strip() if re.search(cover_pattern, html) else None
    name = re.search(name_pattern, html).group(1).strip() if re.search(name_pattern, html) else None
    categories = re.findall(categories_pattern, html) if re.findall(categories_pattern, html) else []
    published_at = re.search(published_at_pattern, html).group(1) if re.search(published_at_pattern, html) else None
    drama = re.search(drama_pattern, html).group(1).strip() if re.search(drama_pattern, html) else None
    score = float(re.search(score_pattern, html).group(1).strip()) if re.search(score_pattern, html) else None

    # 去除影片中的中英文冒号
    name = re.sub(r"[:：]", "", name) if isinstance(name, str) else name
    return {
        'cover': cover,
        'name': name,
        'categories': categories,
        'published_at': published_at,
        'drama': drama,
        'score': score,
    }


# 影片列表获取
# def main():
#     for page in range(1, TOTAL_PAGE + 1):
#         index_html = scrape_index(page)
#         detail_urls = parse_index(index_html)
#         logging.info('detail urls %s', list(detail_urls))

# 保存获取的数据
def save_data(data):
    name = data.get('name')
    data_path = f'{RESULTS_DIR}/{name}.json'
    json.dump(data, open(data_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)


# 影片详情获取
def main(page):
    index_html = scrape_index(page)
    detail_urls = parse_index(index_html)
    for detail_url in detail_urls:
        detail_html = scrape_detail(detail_url)
        data = parse_detail(detail_html)
        logging.info('get detail data %s', data)
        logging.info('save data to json file')
        save_data(data)
        logging.info('data saved successfully')


if __name__ == '__main__':
    pool = multiprocessing.Pool()
    pages = range(1, TOTAL_PAGE + 1)
    pool.map(main, pages)
    pool.close()
    pool.join()