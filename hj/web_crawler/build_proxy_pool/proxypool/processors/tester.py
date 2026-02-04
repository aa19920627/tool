#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : 洪建
# @File : tester.py
# @Time : 2026/1/9 13:50
import asyncio
import platform

import aiohttp
from aiohttp import ClientProxyConnectionError, ServerDisconnectedError, ClientOSError, ClientHttpProxyError
from loguru import logger
from web_crawler.build_proxy_pool.proxypool.schemas.proxy import Proxy
from web_crawler.build_proxy_pool.proxypool.setting import *
from web_crawler.build_proxy_pool.proxypool.storages.redis_client import RedisClient
from web_crawler.build_proxy_pool.proxypool.testers import __all__ as testers_cls

# 定义需要捕获的异常类型
EXCEPTIONS = (
    ClientProxyConnectionError,  # 代理连接错误
    ConnectionRefusedError,  # 连接被拒绝错误
    TimeoutError,  # 超时错误
    ServerDisconnectedError,  # 服务器断开连接错误
    ClientOSError,  # 客户端操作系统错误
    ClientHttpProxyError,  # HTTP代理错误
    AssertionError  # 断言错误
)
if platform.system() == 'Windows':
    # Windows 上使用 Selector 事件循环
    logger.debug('运行平台为Windows，使用selector事件循环')
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


class Proxy_Tester(object):
    """
    代理测试器类，用于测试队列中的代理是否可用
    """

    def __init__(self):
        """
        初始化Redis客户端、事件循环和独立测试器
        """
        self.redis = RedisClient()  # 创建Redis客户端实例

        try:
            self.loop = asyncio.get_running_loop()  # 获取当前事件循环
        except RuntimeError:  # 如果没有创建新事件
            self.loop = asyncio.new_event_loop()


        self.testers_cls = testers_cls  # 获取所有独立测试器的类
        # 创建独立测试器的实例列表
        self.testers = [tester_cls() for tester_cls in self.testers_cls]

    async def proxy_test(self, proxy):
        """
        测试单个代理
        参数:
            proxy: Proxy对象，包含代理的host和port
        返回: None
        """
        # 创建aiohttp会话
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
            try:
                logger.debug(f'正在测试代理 {proxy.string()}')  # 记录调试日志

                # 如果配置了匿名性测试，确保代理具有隐藏真实IP的效果
                if TEST_ANONYMOUS == "1":
                    # 测试匿名性：首先获取真实IP
                    url = 'https://httpbin.org/ip'
                    async with session.get(url, timeout=TEST_TIMEOUT) as response:
                        resp_json = await response.json()
                        origin_ip = resp_json['origin']  # 获取真实ip

                    # 通过代理获取IP
                    async with session.get(url, proxy=f'http://{proxy.string()}', timeout=TEST_TIMEOUT) as response:
                        resp_json = await response.json()
                        anonymous_ip = resp_json['origin']  # 通过代理获取的
                        logger.debug(f'匿名IP是 {anonymous_ip}')

                    # 断言：真实IP和代理IP不同，且代理IP等于代理的host
                    assert origin_ip != anonymous_ip
                    assert proxy.host == anonymous_ip

                # 使用代理访问测试URL
                async with session.get(TEST_URL, proxy=f'http://{proxy.string()}/', timeout=TEST_TIMEOUT,
                                       allow_redirects=False) as response:
                    # 检查响应状态码是否在有效状态码列表中
                    if response.status in TEST_VALID_STATUS:
                        if TEST_DONT_SET_MAX_SCORE:
                            # 如果不设置最大分数，则保留当前分数
                            logger.debug(f'代理 {proxy.string()} 有效，保留当前分数')
                        else:
                            # 设置代理分数为最大值
                            self.redis.max(proxy)
                            logger.debug(f'代理 {proxy.string()} 有效，设置为最大分数')
                    else:
                        # 响应状态码无效，降低代理分数
                        self.redis.decease(proxy)
                        logger.debug(f'代理 {proxy.string()} 无效，降低分数')

                # 如果存在独立测试器，进行额外测试
                for tester in self.testers:
                    key = tester.key
                    # 检查代理是否在指定key的集合中
                    if self.redis.exists(proxy, key):
                        test_url = tester.test_url
                        headers = tester.headers()
                        cookies = tester.cookies()
                        # 通过代理访问测试器的测试URL
                        async with session.get(test_url, proxy=f'http://{proxy.string()}',
                                               timeout=TEST_TIMEOUT,
                                               headers=headers,
                                               cookies=cookies,
                                               allow_redirects=False) as response:
                            resp_text = await response.text()
                            # 调用测试器的parse方法验证响应
                            is_valid = await tester.parse(resp_text)
                            if is_valid:
                                if tester.test_dont_set_max_score:
                                    logger.info(f'key[{key}] 代理 {proxy.string()} 有效，保留当前分数')
                                else:
                                    # 设置代理在指定key中的分数为最大值
                                    self.redis.max(proxy, key, tester.proxy_score_max)
                                    logger.info(f'key[{key}] 代理 {proxy.string()} 有效，设置为最大分数')
                            else:
                                # 降低代理在指定key中的分数
                                self.redis.decrease(proxy, tester.key, tester.proxy_score_min)
                                logger.info(f'key[{key}] 代理 {proxy.string()} 无效，降低分数')

            # 捕获所有定义的异常
            except EXCEPTIONS:
                # 降低代理的基础分数
                self.redis.decrease(proxy)
                # 降低代理在所有独立测试器中的分数
                [self.redis.decrease(proxy, tester.key, tester.proxy_score_min) for tester in self.testers]
                logger.debug(f'代理 {proxy.string()} 无效，降低分数')
                # raise

    @logger.catch
    def run(self):
        """
        测试的主要方法，批量测试代理
        返回: None
        """
        # 开始测试
        logger.info('开始测试代理...')
        # 获取待测试的代理总数
        count = self.redis.count()
        logger.debug(f'共有 {count} 个代理需要测试')
        cursor = 0
        while True:
            # 批量获取代理进行测试
            logger.debug(f'使用游标 {cursor} 进行测试，批次大小 {TEST_BATCH}')
            cursor, proxies = self.redis.batch(cursor, count=TEST_BATCH)
            if proxies:
                logger.debug(f'获取到 {len(proxies)} 个代理进行测试')
                # 为每个代理创建测试任务
                tasks = [self.loop.create_task(self.proxy_test(proxy)) for proxy in proxies]
                # 运行所有任务直到完成
                self.loop.run_until_complete(asyncio.wait(tasks))
            # 如果没有更多代理，则结束循环
            if not cursor:
                logger.debug('没有更多代理，结束测试')
                break


async def run_tester():
    host = '13.59.113.45'
    port = '123'
    tester = Proxy_Tester()  # 创建实例
    await tester.proxy_test(Proxy(host=host, port=port))

if __name__ == '__main__':
    tester = Proxy_Tester()
    tester.run()
    # tester.loop.run_until_complete(run_tester())
