#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : 洪建
# @File : empty.py
# @Time : 2026/1/14 15:45


class PoolEmptyException(Exception):
    def __str__(self):
        """
        proxypool is used out
        :return:
        """
        return repr('代理池中没有代理')
