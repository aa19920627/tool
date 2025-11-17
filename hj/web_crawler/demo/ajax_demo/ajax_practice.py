#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : 洪建
# @File : ajax_practice.py
# @Time : 2025/11/17 10:34
import pymongo
import requests
import logging

"""
Ajax数据爬取实例
"""

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s : %(message)s')
INDEX_URL = 'https://spa1.scrape.center/api/movie/?limit={limit}&offset={offset}'
LIMIT = 10
TOTAL_PAGE = 10
DETAIL_URL = 'https://spa1.scrape.center/api/movie/{id}'
MONGO_CONNECTION_STRING = 'mongodb://localhost:27017'
MONGO_DB_NAME = 'movies'
MONGO_COLLECTION_NAME = 'movies'


# 定义通用爬取方法
def scrape_api(url):
    logging.info('scraping %s' % url)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        logging.error('get invalid status code %s while scraping %s', response.status_code, url)
    except requests.RequestException:
        logging.error('error occurred while scraping %s' % url, exc_info=True)


# 定义爬取列表页
def scrape_index(page):
    url = INDEX_URL.format(limit=LIMIT, offset=LIMIT * (page - 1))
    return scrape_api(url)


# 定义详情页爬取逻辑
def scrape_detail(id):
    url = DETAIL_URL.format(id=id)
    return scrape_api(url)


# 将数据存储到MongoDB中
client = pymongo.MongoClient(MONGO_CONNECTION_STRING)
db = client[MONGO_DB_NAME]
collection = db[MONGO_COLLECTION_NAME]


# 定义数据保存的方法
def save_data(data):
    collection.update_one({
        'name': data.get('name'),
    }, {
        '$set': data
    }, upsert=True)


# 定义总的调用方法
def main():
    for page in range(1, TOTAL_PAGE + 1):
        index_data = scrape_index(page)
        for item in index_data.get('results'):
            id = item.get('id')
            detail_data = scrape_detail(id)
            logging.info('detail data %s ', detail_data)
            save_data(detail_data)
            logging.info('data saved sucessfully')


if __name__ == '__main__':
    main()
