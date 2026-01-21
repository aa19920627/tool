#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : 洪建
# @File : base.py
# @Time : 2026/1/9 13:48
from web_crawler.build_proxy_pool.proxypool.setting import *


class BaseTester(object):
    # 测试URL，用于验证代理是否可用
    test_url = ""
    # 测试器标识键，用于区分不同的测试器
    key = ""
    # 是否不设置最大分数的标志
    test_dont_set_max_score = TEST_DONT_SET_MAX_SCORE
    # 代理初始分数
    proxy_score_init = PROXY_SCORE_INIT
    # 代理最大分数
    proxy_score_max = PROXY_SCORE_MAX
    # 代理最小分数
    proxy_score_min = PROXY_SCORE_MIN

    def headers(self):
        """
        获取请求头
        :return: None - 子类可重写此方法返回自定义请求头
        """
        return None

    def cookies(self):
        """
        获取cookies
        :return: None - 子类可重写此方法返回自定义cookies
        """
        return None

    async def parse(self,html,url,proxy,expr='{"code":0}'):
        """
        解析响应内容，判断代理是否有效
        :param html: 响应内容
        :param url: 测试URL
        :param proxy: 代理对象
        :param expr: 判断表达式，默认为'{"code":0'
        :return: bool - 代理是否有效，如果expr在html中则返回True，否则返回False
        """
        return True if expr in html else False