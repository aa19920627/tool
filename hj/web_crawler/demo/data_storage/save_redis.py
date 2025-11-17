#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : 洪建
# @File : save_redis.py
# @Time : 2025/11/11 11:00

from redis import StrictRedis

"""
redis缓存存储示例
"""

# 连接redis
redis = StrictRedis(host='localhost', port=6379, db=0, password='')
redis.set('name','jordan')
print(redis.get('name'))
