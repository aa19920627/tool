#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : 洪建
# @File : asyn_demo.py
# @Time : 2025/11/17 16:13

import asyncio
import json
import aiohttp
import logging

import pymongo

"""异步爬虫案例"""

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s : %(message)s')
INDEX_URL = 'https://spa5.scrape.center/api/book/?limit=18&offset={offset}'
DETAIL_URL = 'https://spa5.scrape.center/api/book/{id}'

PAGE_SIZE = 18
PAGE_NUMBER = 100
CONCURRENCY = 5
MONGO_CONNECTION_STRING = 'mongodb://localhost:27017'
MONGO_DB_NAME = 'books'
MONGO_COLLECTION_NAME = 'books'

# 爬取列表页
# 定义并发量
semaphore = asyncio.Semaphore(CONCURRENCY)
session = None


# 定义通用爬取方法
async def scrape_api(url):
    async with semaphore:
        try:
            logging.info('scraping %s', url)
            async with session.get(url) as response:
                return await response.json()
        except aiohttp.ClientError:
            logging.error('error occured while scraping %s', url, exc_info=True)


# 爬取列表页面
async def scrape_index(page):
    url = INDEX_URL.format(offset=PAGE_SIZE * (page - 1))
    return await scrape_api(url)


# 定义异步存储数据到MongoDB
client = pymongo.MongoClient(MONGO_CONNECTION_STRING)
db = client[MONGO_DB_NAME]
collection = db[MONGO_COLLECTION_NAME]


async def save_data(data):
    logging.info('saving data %s', data)
    if data:
        return await collection.update_one({
            'id': data.get('id')
        }, {
            '$set': data
        }, upsert=True)


# 定义爬取详情页的方法
async def scrape_detail(id):
    url = DETAIL_URL.format(id=id)
    data = await scrape_api(url)
    await save_data(data)


# 定义main方法
async def main():
    # 声明全局可用的session对象
    global session
    session = aiohttp.ClientSession()
    # 定义爬取列表页的所有task组成的列表
    scrape_index_tasks = [asyncio.ensure_future(scrape_index(page)) for page in range(1, PAGE_NUMBER + 1)]
    # 调用asyncio的gather方法，并将task列表出入其参数，将结果赋值给results
    results = await asyncio.gather(*scrape_index_tasks)
    # logging.info('results  %s', json.dumps(results, ensure_ascii=False, indent=2))
    ids = []
    for index_data in results:
        if not index_data: continue
        for item in index_data.get('results'):
            ids.append(item.get('id'))
    # 定义爬取详情页的所有task组成的列表
    scrape_detail_tasks = [asyncio.ensure_future(scrape_detail(id)) for id in ids]
    await asyncio.wait(scrape_detail_tasks)
    await session.close()


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
