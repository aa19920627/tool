#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : 洪建
# @File : request.py
# @Time : 2026/1/4 16:13

from requests import Request

"""继承request库中的Request对象实现一个请求对象"""

TIMEOUT = 10


class MovieRequest(Request):
    def init_request(self, url, callback, method='GET', headers=None, need_proxy=False, fail_time=0, timeout=TIMEOUT):
        Request.__init__(self, method, url, headers)
        self.callback = callback
        self.fail_time = fail_time
        self.timeout = timeout

