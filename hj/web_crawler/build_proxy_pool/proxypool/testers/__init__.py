#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : 洪建
# @File : __init__.py.py
# @Time : 2026/1/9 13:48

import pkgutil
from .base import BaseTester
import inspect


# 加载继承自BaseTester的所有测试器类
classes = []
# 遍历当前包路径下的所有子模块
for loader, name, is_pkg in pkgutil.walk_packages(__path__):
    # 使用loader加载模块
    module = loader.find_module(name).load_module(name)
    # 遍历模块中的所有成员
    for name, value in inspect.getmembers(module):
        # 将模块成员添加到全局命名空间中
        globals()[name] = value
        # 判断是否为满足条件的测试器类：
        # 1. 是一个类对象 (inspect.isclass(value))
        # 2. 继承自BaseTester基类 (issubclass(value, BaseTester))
        # 3. 不是BaseTester基类本身 (value is not BaseTester)
        # 4. 没有被标记为忽略 (not getattr(value, 'ignore', False))
        if inspect.isclass(value) and issubclass(value, BaseTester) and value is not BaseTester \
                and not getattr(value, 'ignore', False):
            classes.append(value)
# 定义模块导出的公共接口，使外部可以访问所有符合条件的测试器类
__all__ = __ALL__ = classes
