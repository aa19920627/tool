#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : 洪建
# @File : __init__.py.py
# @Time : 2026/1/15 16:13
import inspect
import pkgutil

# 动态加载继承自BaseCrawler的所有爬虫类
classes = []
# 遍历当前包路径下的所有子模块
for loader, name, is_pkg in pkgutil.walk_packages(__path__):
    # 加载模块
    module = loader.find_module(name).load_module(name)
    # 遍历模块中的所有对象
    for name, value in inspect.getmembers(module):
        # 将模块成员添加到全局命名空间
        globals()[name] = value
        # 筛选出满足条件的爬虫类：
        # 1. 是类对象
        # 2. 继承自BaseCrawler基类
        # 3. 不是BaseCrawler本身
        # 4. 没有设置ignore属性为True
        if inspect.isclass(value) and issubclass(value, BaseCrawler) and value is not BaseCrawler and not getattr(value,'ignore',False):
            classes.append(value)

# 导出所有符合条件的爬虫类
__all__ = __ALL__ = classes