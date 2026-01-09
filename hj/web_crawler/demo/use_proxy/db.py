#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : 洪建
# @File : db.py.py
# @Time : 2026/1/4 16:19

from pickle import dumps,loads
from redis import StrictRedis
from web_crawler.demo.use_proxy.config import *
from web_crawler.demo.use_proxy.request import MovieRequest


"""实现请求队列"""


class RedisQueue():
    def __init__(self):
        # 初始化redis连接
        self.db = StrictRedis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD)

    def add(self,request):
        if isinstance(request,MovieRequest):
            # 如果request类型是MovieRequest,则序列化
            return self.db.rpush(REDIS_KEY,dumps(request))
        return False

    def pop(self):
        if self.db.llen(REDIS_KEY):
            return loads(self.db.lpop(REDIS_KEY))
        return False

    def clear(self):
        self.db.delete(REDIS_KEY)

    def empty(self):
        return self.db.llen(REDIS_KEY) == 0