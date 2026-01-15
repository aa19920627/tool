#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : 洪建
# @File : getter.py
# @Time : 2026/1/13 15:46


class Getter:

    """
    代理池的获取器类，用于从各种网站爬取代理IP
    """

    def init(self):
        """
        初始化Redis连接和爬虫列表
        """
        self.redis = RedisClient()