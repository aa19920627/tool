#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : 洪建
# @File : getter.py
# @Time : 2026/1/13 15:46
from loguru import logger
from web_crawler.build_proxy_pool.proxypool.crawlers import BaseCrawler
from web_crawler.build_proxy_pool.proxypool.setting import *
from web_crawler.build_proxy_pool.proxypool.storages.redis_client import RedisClient
from web_crawler.build_proxy_pool.proxypool.testers import __all__ as testers_cls


class Getter:
    """
    代理池的获取器类，用于从各种网站爬取代理IP
    """

    def __init__(self):
        """
        初始化Redis连接和爬虫列表
        """
        self.redis = RedisClient()
        # self.crawlers_cls = crawlers_cls  # 获取所有可用的爬虫类列表
        # self.crawlers = [crawler_cls() for crawler_cls in self.crawlers_cls]  # 实例化所有爬虫类型
        self.crawler_cls = BaseCrawler()
        self.testers_cls = testers_cls  # 获取所有可用的测试器类列表
        self.testers = [tester_cls() for tester_cls in self.testers_cls]

    def is_full(self):
        """
        检查代理池是否已满
        return: bool - 如果代理池中的代理数量达到最大值返回True，否则返回False
        """
        return self.redis.count() >= PROXY_NUMBER_MAX

    @logger.catch
    def run(self):
        """
        运行爬虫获取代理
        :return: None
        """
        # 如果代理池已满，则停止获取新代理
        if self.is_full():
            return
        # 遍历所有爬虫实例
        for proxy in self.crawler_cls.crawl():
            self.redis.add(proxy)  # 将代理添加到主代理池
            # 将代理也添加到各个测试器的队列中，用于后续验证
            [self.redis.add(proxy, redis_key=tester.key) for tester in self.testers_cls]


if __name__ == '__main__':
    getter = Getter()
    getter.run()
