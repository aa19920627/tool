#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : 洪建
# @File : setting.py.py
# @Time : 2026/1/9 13:30
from environs import Env

env = Env()
env.read_env()

# 测试器状态
ENABLE_TESTER = env.bool('ENABLE_TESTER', True)
ENABLE_GETTER = env.bool('ENABLE_GETTER', True)
ENABLE_SERVER = env.bool('ENABLE_SERVER', True)

# 用于运行应用的 WSGI 容器配置
# - gevent: pip install gevent
# - tornado: pip install tornado
# - meinheld: pip install meinheld
# 上面是三种常用的 WSGI 容器，分别需要安装对应的包
# 定义三种 WSGI 容器类型的常量
APP_PROD_METHOD_GEVENT = 'gevent'  # 使用 gevent（基于协程的高性能容器）
APP_PROD_METHOD_TORNADO = 'tornado'  # 使用 tornado（异步网络库，也可作为WSGI容器）
APP_PROD_METHOD_MEINHELD = 'meinheld'  # 使用 meinheld（基于picoev的高性能WSGI服务器）
# 从环境变量 APP_PROD_METHOD 中获取用户选择的 WSGI 容器
# 如果没有设置，则默认使用 gevent，并将值转换为小写
APP_PROD_METHOD = env.str('APP_PROD_METHOD', APP_PROD_METHOD_GEVENT).lower()

# Redis相关设置
# Redis主机地址
REDIS_HOST = env.str('PROXYPOOL_REDIS_HOST',
                     env.str('REDIS_HOST', '192.150.179.128'))
# Redis端口号
REDIS_PORT = env.int('PROXYPOOL_REDIS_PORT', env.int('REDIS_PORT', 6379))
# Redis密码，如果没有密码，设置为None
REDIS_PASSWORD = env.str('PROXYPOOL_REDIS_PASSWORD',
                         env.str('REDIS_PASSWORD', 'dgbc@Passw0rd'))
# Redis数据库，如果没有特别选择，设置为0
REDIS_DB = env.int('PROXYPOOL_REDIS_DB', env.int('REDIS_DB', 0))
# Redis连接字符串，格式如 redis://[password]@host:port 或 rediss://[password]@host:port/0，
# 详情请参考 https://redis-py.readthedocs.io/en/stable/connections.html#redis.client.Redis.from_url
REDIS_CONNECTION_STRING = env.str(
    'PROXYPOOL_REDIS_CONNECTION_STRING', env.str('REDIS_CONNECTION_STRING', None))

# Redis哈希表键名
REDIS_KEY = env.str('PROXYPOOL_REDIS_KEY', env.str(
    'REDIS_KEY', 'proxies:universal'))

# 定义代理的评分标准
PROXY_SCORE_MAX = env.int('PROXY_SCORE_MAX', 100)
PROXY_SCORE_MIN = env.int('PROXY_SCORE_MIN', 0)
PROXY_SCORE_INIT = env.int('PROXY_SCORE_INIT', 10)

# 定义环境常量
DEV_MODE, TEST_MODE, PROD_MODE = 'dev', 'test', 'prod'  # 三种环境模式：开发、测试、生产
# 从环境变量中获取APP_ENV，如果没有设置则默认为DEV_MODE，并转换为小写
APP_ENV = env.str('APP_ENV', DEV_MODE).lower()
# 设置调试模式：从环境变量获取APP_DEBUG，如果未设置则根据环境自动判断
# 如果是开发环境(DEV_MODE)则默认开启调试，否则关闭
APP_DEBUG = env.bool('APP_DEBUG', True if APP_ENV == DEV_MODE else False)
# 环境判断布尔变量
APP_DEV = IS_DEV = APP_ENV == DEV_MODE  # 是否开发环境
APP_PROD = IS_PROD = APP_ENV == PROD_MODE  # 是否生产环境
APP_TEST = IS_TEST = APP_ENV == TEST_MODE  # 是否测试环境

# 定义测试周期，每CYCLE_TESTER秒进行一次测试
CYCLE_TESTER = env.int('CYCLE_TESTER', 20)
# 定期从代理发布网站获取代理源，每CYCLE_GETTER秒获取一次
CYCLE_GETTER = env.int('CYCLE_GETTER', 20)

# tester调度器的相关配置
TEST_URL = env.str('TEST_URL', 'http://www.baidu.com')
TEST_TIMEOUT = env.int('TEST_TIMEOUT', 10)
TEST_BATCH = env.int('TEST_BATCH', 20)
# 是否进行匿名性测试
TEST_ANONYMOUS = env.bool('TEST_ANONYMOUS', True)

# 定义代理池的数量
PROXY_NUMBER_MAX = 50000
PROXY_NUMBER_MIN = 0

# 访问成功的有效状态码
TEST_VALID_STATUS = env.list('TEST_VALID_STATUS', [200, 206, 302])
# 是否将测试通过的代理设置为最大分数
TEST_DONT_SET_MAX_SCORE = env.bool('TEST_DONT_SET_MAX_SCORE', False)

# API 服务定义和配置
# API 服务监听的主机地址
# 从环境变量 API_HOST 读取，如果未设置则默认为 '0.0.0.0'（表示监听所有网络接口）
API_HOST = env.str('API_HOST', '0.0.0.0')
# API 服务监听的端口号
# 从环境变量 API_PORT 读取，如果未设置则默认为 5555
API_PORT = env.int('API_PORT', 5555)
# API 服务是否启用多线程模式
# 从环境变量 API_THREADED 读取，如果未设置则默认为 True（启用多线程）
API_THREADED = env.bool('API_THREADED', True)
# 添加 API 密钥以获取代理
# 需要在 GET 请求中添加 `API-KEY` 请求头来通过身份验证
# 如果 API_KEY=''，则不需要 `API-KEY` 请求头
# 从环境变量 API_KEY 读取，如果未设置则默认为空字符串
API_KEY = env.str('API_KEY', '')
