#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : 洪建
# @File : redis_client.py
# @Time : 2026/1/9 14:50
from random import choice
import redis
from loguru import logger
from web_crawler.build_proxy_pool.proxypool.exceptions.empty import PoolEmptyException
from web_crawler.build_proxy_pool.proxypool.setting import *
from web_crawler.build_proxy_pool.proxypool.utils.proxy import is_valid_proxy, convert_proxy_or_proxies

# 获取redis客户端版本
REDIS_CLIENT_VERSION = redis.__version__
# 判断是否为redis 2.x版本
IS_REDIS_VERSION_2 = REDIS_CLIENT_VERSION.startswith('2')


class RedisClient(object):
    """
    代理池的Redis连接客户端，用于与Redis进行交互
    """

    def __init__(self, host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, db=REDIS_DB,
                 connection_string=REDIS_CONNECTION_STRING, **kwargs):
        """
        初始化redis客户端
        参数:
            host: redis主机地址
            port: redis端口
            password: redis密码
            connection_string: redis连接字符串（如果提供，则优先使用）
        """
        # === 设置超时 + 启动验证）===
        kwargs.setdefault('socket_timeout', 5)  # 操作5秒超时
        kwargs.setdefault('socket_connect_timeout', 5)  # 连接5秒超时
        kwargs.setdefault('retry_on_timeout', False)  # 超时直接失败，不重试
        # ==============================================

        # 如果设置了连接字符串，则使用连接字符串
        if connection_string:
            self.db = redis.StrictRedis.from_url(connection_string, decode_responses=True, **kwargs)
        else:
            # 否则使用单独的参数连接
            self.db = redis.StrictRedis(
                host=host, port=port, password=password, db=db, decode_responses=True, **kwargs
            )

        # === （启动时验证连接）===
        try:

            self.db.ping()
            # logger.info(f"Redis连接成功")
        except Exception as e:
            logger.error(f"Redis初始化失败，程序终止: {e}")
            import sys
            sys.exit(1)
        # ======================================

    def add(self, proxy, score=PROXY_SCORE_INIT, redis_key=REDIS_KEY):
        """
        添加代理并设置初始分数
        :param proxy: 代理对象，格式为ip:port，例如 8.8.8.8:88
        :param score: 初始分数，默认为PROXY_SCORE_INIT
        :param redis_key: Redis中的键名，默认为REDIS_KEY
        :return: 添加结果（成功返回1，失败返回None）
        """

        # 验证代理是否有效（IP和端口格式是否正确）
        if not is_valid_proxy(f'{proxy.host}:{proxy.port}'):
            # 如果代理无效，则记录日志并返回
            logger.info(f'代理无效：{proxy}')
            return
        # 检查代理是否已存在于Redis中
        if not self.exists(proxy, redis_key):
            # 根据Redis版本选择不同的zadd语法
            if IS_REDIS_VERSION_2:
                # Redis 2.x 版本的语法：zadd key score member
                return self.db.zadd(redis_key, score, proxy.string())
            # Redis 3.x+ 版本的语法：zadd key {member: score}
            return self.db.zadd(redis_key, {proxy.string(): score})

    def random(self, redis_key=REDIS_KEY, proxy_score_min=PROXY_SCORE_MIN, proxy_score_max=PROXY_SCORE_MAX):
        """
        获取一个随机代理
        首先尝试获取最高分数的代理
        如果不存在，尝试按排名获取代理
        如果仍不存在，抛出异常
        :param redis_key: Redis键名，默认为REDIS_KEY
        :param proxy_score_min: 代理最小分数，默认为PROXY_SCORE_MIN
        :param proxy_score_max: 代理最大分数，默认为PROXY_SCORE_MAX
        :return: Proxy对象，如 8.8.8.8:8
        """
        # 尝试获取最高分数的代理（分数等于proxy_score_max的所有代理）
        proxies = self.db.zrangebyscore(
            redis_key, proxy_score_max, proxy_score_max
        )
        if len(proxies):
            # 如果找到了最高分数的代理，从中随机选择一个返回
            return convert_proxy_or_proxies(choice(proxies))
        # 否则按分数从高到低获取代理（获取指定分数范围内的所有代理）
        proxies = self.db.zrevrange(
            redis_key, proxy_score_min, proxy_score_max
        )
        if len(proxies):
            # 如果找到了代理，从中随机选择一个返回
            return convert_proxy_or_proxies(choice(proxies))
        # 如果以上都没有找到代理，抛出代理池为空的异常
        raise PoolEmptyException

    def decrease(self, proxy, redis_key=REDIS_KEY, proxy_scoce_min=PROXY_SCORE_MIN):
        """
        降低代理的分数，如果低于PROXY_SCORE_MIN，则删除它
        :param proxy: 代理对象
        :param redis_key: Redis键名，默认为REDIS_KEY
        :param proxy_score_min: 代理最小分数阈值，默认为PROXY_SCORE_MIN
        """
        # 根据Redis版本差异处理zincrby命令的不同调用方式
        if IS_REDIS_VERSION_2:
            self.db.zincrby(redis_key, proxy.string(), -1)
        else:
            self.db.zincrby(redis_key, -1, proxy.string())
        # 获取代理当前的分数
        score = self.db.zscore(redis_key, proxy.string())
        # 记录分数减少的日志
        logger.info(f'代理 {proxy} 减1，当前分数 {score}')
        # 检查代理分数是否小于等于最低分数阈值
        if score <= proxy_scoce_min:
            # 如果分数过低，记录删除日志并从Redis有序集合中移除该代理
            logger.info(f'代理 {proxy} 移除')
            self.db.zrem(redis_key, proxy.string())

    def exists(self, proxy, redis_key=REDIS_KEY):
        """
        检查代理是否存在
        :param proxy: 代理对象
        :param redis_key: Redis键名，默认为REDIS_KEY
        :return: 存在返回True，否则返回False
        """
        # 通过获取代理分数来判断是否存在，若不存在则zscore返回None
        return not self.db.zscore(redis_key, proxy.string()) is None

    def max(self, proxy, redis_key=REDIS_KEY, proxy_score_max=PROXY_SCORE_MAX):
        """
        将代理分数设置为最大值
        :param proxy: 代理对象
        :param redis_key: Redis键名，默认为REDIS_KEY
        :param proxy_score_max: 最大分数值，默认为PROXY_SCORE_MAX
        """
        # 记录代理被设置为最大分数的日
        logger.info(f'代理 {proxy} 被设置为 {proxy_score_max}')
        # 根据Redis版本差异处理zadd命令的不同语法
        if IS_REDIS_VERSION_2:
            # Redis 2.x版本语法：key, score, member
            return self.db.zadd(redis_key, proxy_score_max, proxy.string())
        # Redis 3.x+版本语法：key, {member: score}
        return self.db.zadd(redis_key, {proxy.string(): proxy_score_max})

    def count(self, redis_key=REDIS_KEY):
        """
        获取代理总数
        :param redis_key: Redis键名，默认为REDIS_KEY
        :return: 代理数量，整数
        """
        # 使用zcard命令获取有序集合中成员的数量
        return self.db.zcard(redis_key)

    def all(self, redis_key=REDIS_KEY, proxy_score_min=PROXY_SCORE_MIN, proxy_score_max=PROXY_SCORE_MAX):
        """
        获取所有代理
        :param redis_key: Redis键名，默认为REDIS_KEY
        :param proxy_score_min: 最小分数阈值，默认为PROXY_SCORE_MIN
        :param proxy_score_max: 最大分数阈值，默认为PROXY_SCORE_MAX
        :return: 代理对象列表
        """
        # 获取指定分数范围内所有代理，并转换为Proxy对象列表
        return convert_proxy_or_proxies(self.db.zrangebyscore(redis_key, 0, proxy_score_max))

    def batch(self, cursor, count, redis_key=REDIS_KEY):
        """
        批量获取代理
        :param cursor: 扫描游标
        :param count: 扫描数量
        :param redis_key: Redis键名，默认为REDIS_KEY
        :return: 游标和代理对象列表
        """
        # 使用zscan命令批量扫描有序集合中的代理
        cursor, proxies = self.db.zscan(redis_key, cursor, count=count)
        # print(proxies)
        # 转换返回的代理字符串为Proxy对象列表
        return cursor, convert_proxy_or_proxies([i[0] for i in proxies])

if __name__ == '__main__':
    conn = RedisClient()
    result = conn.random()
    print(conn.count())
    print(result)
    # print(conn.batch(0,20))

    # # 清除代理池
    # proxies = conn.all()
    # for proxy in proxies:
    #     conn.decrease(proxy)