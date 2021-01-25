# -*- encoding: utf-8 -*-
"""
@File    : component.py
@Date    : 2021/1/25 14:08
@Author  : 洪建
"""
import time

'''
公共方法
'''


class Component_method:

    def __init__(self):

        pass

    def get_log_time(self):

        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())