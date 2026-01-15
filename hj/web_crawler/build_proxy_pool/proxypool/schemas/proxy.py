#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : 洪建
# @File : proxy.py
# @Time : 2026/1/14 15:02

from attr import attr, attrs


@attrs
class Proxy(object):
    """
    代理对象模型类
    """
    # 定义代理主机地址属性，类型为字符串，默认值为None
    host = attr(type=str, default=None)
    # 定义代理端口属性，类型为整数，默认值为None
    port = attr(type=int, default=None)

    def __str__(self):
        """
        字符串表示方法，用于打印输出
        :return: 格式为 'host:port' 的字符串
        """
        # 返回主机和端口的组合字符串，格式为 'host:port'
        return f'{self.host}:{self.port}'

    def string(self):
        """
        获取代理的字符串格式
        :return: <host>:<port> 格式的字符串
        """
        # 调用 __str__ 方法返回字符串表示

