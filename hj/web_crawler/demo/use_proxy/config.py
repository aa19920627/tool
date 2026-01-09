#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : 洪建
# @File : config.py.py
# @Time : 2026/1/8 11:44

from environs import Env

env = Env()
env.read_env()

REDIS_HOST = env.str('REDIS_HOST', 'localhost')

REDIS_PORT = env.int('REDIS_PORT', 6379)

REDIS_PASSWORD = env.str('REDIS_PASSWORD', 'dgbc@Passw0rd')

REDIS_KEY = env.str('REDIS_KEY', 'antispider5')

PROXY_POOL_URL = env.str('PROXY_POOL_URL', 'http://127.0.0.1:5555/random')

TIMEOUT = env.int('TIMEOUT', 10)

MAX_FAILED_TIME = env.int('MAX_FAILED_TIME', 20)

VALID_STATUSES = env.list('VALID_STATUSES', [200])