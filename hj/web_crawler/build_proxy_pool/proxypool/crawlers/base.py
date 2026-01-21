#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : 洪建
# @File : base.py
# @Time : 2026/1/15 17:00
import time

import requests
from loguru import logger
from web_crawler.build_proxy_pool.proxypool.schemas.proxy import Proxy

# APIs
# 定义两个API端点列表，分别从不同的来源获取代理数据
JSON_ENDPOINTS1 = [
    # 从proxy-daily.com获取代理数据，使用分页参数获取不同范围的数据
    {"url": "https://proxy-daily.com/api/serverside/proxies?draw=1&start=0&length=100"},  # 获取前100个代理
    {"url": "https://proxy-daily.com/api/serverside/proxies?draw=2&start=100&length=100"},  # 获取100-200个代理
    {"url": "https://proxy-daily.com/api/serverside/proxies?draw=3&start=200&length=100"},  # 获取200-300个代理
    {"url": "https://proxy-daily.com/api/serverside/proxies?draw=4&start=300&length=100"},  # 获取300-400个代理
    {"url": "https://proxy-daily.com/api/serverside/proxies?draw=5&start=400&length=100"},  # 获取400-500个代理
]
JSON_ENDPOINTS2 = [
    # 从GitHub上的开源项目获取代理数据
    {"url": "https://cdn.jsdelivr.net/gh/proxifly/free-proxy-list@main/proxies/all/data.json"},  # 获取所有国家的代理数据
    {"url": "https://cdn.jsdelivr.net/gh/proxifly/free-proxy-list@main/proxies/countries/us/data.json"},  # 获取美国的代理数据
]
# 设置默认请求头，模拟Chrome浏览器访问
DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"}


class BaseCrawler(object):

    def fetch_jsonendpoint1(self, ep):
        """
        从proxy-daily.com获取代理数据
        """
        url = ep["url"]  # 提取url
        try:
            resp = requests.get(url, timeout=25, headers=DEFAULT_HEADERS)
            resp.raise_for_status()  # 检查HTTP状态码，如果不是200会抛出异常
            data = resp.json()  # 解析响应为JSON格式
        except Exception as e:
            logger.error(f"获取代理失败 {url}: {e}")
            return []
        rows = data.get("data", []) or []  # 获取data字段中的数据，如果没有则为空列表

        for row in rows:
            ip = row.get("ip")  # 获取IP地址
            port = row.get("port")
            if not ip or not port:
                continue
            yield Proxy(host=ip, port=port)

    def fetch_jsonendpoint2(self, ep):
        """
        从GitHub上的开源项目获取代理数据
        """
        url = ep["url"]
        try:
            resp = requests.get(url, timeout=25, headers=DEFAULT_HEADERS)
            resp.raise_for_status()     # 检查HTTP状态码，如果不是200会抛出异常
            data = resp.json()      # 解析响应为JSON格式
        except Exception as e:
            logger.error(f"获取代理失败 {url}: {e}")
            return []
        rows = data or []
        for row in rows:
            ip = row.get("ip")
            port = row.get("port")
            if not ip or not port:
                continue
            yield Proxy(host=ip, port=port)

    def crawl(self):

        # 遍历第一组API端点获取代理数据
        for ep in JSON_ENDPOINTS1:
            try:
                for proxy in self.fetch_jsonendpoint1(ep):
                    print(f'获取代理成功，代理为{proxy}')
                    yield proxy
            except Exception as e:
                logger.error(f"获取代理失败 {ep['url']}: {e}")

        # 遍历第二组API端点获取代理数据
        for ep in JSON_ENDPOINTS2:
            try:
                for proxy in self.fetch_jsonendpoint2(ep):
                    print(f'获取代理成功，代理为{proxy}')
                    yield proxy
            except Exception as e:
                logger.error(f"获取代理失败 {ep['url']}: {e}")


if __name__ == '__main__':
    basecrawler = BaseCrawler()
    for proxy in basecrawler.crawl():
        print(type(proxy))
