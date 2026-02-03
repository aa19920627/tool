#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : 洪建
# @File : login_jwt.py
# @Time : 2026/1/29 17:01

"""基于JWT的网站的模拟登陆实例"""
import requests
from urllib.parse import urljoin

BASE_URL = 'https://login3.scrape.center/'
LOGIN_URL = urljoin(BASE_URL, '/api/login')
INDEX_URL = urljoin(BASE_URL, '/api/book')
USERNAME = 'admin'
PASSWORD = 'admin'

# 登录获取JWT令牌
response_login = requests.post(LOGIN_URL, json={'username': USERNAME, 'password': PASSWORD})
jwt = response_login.json().get('token')

# 携带令牌请求数据（limit=18条，offset=0起始）
response_index = requests.get(
    INDEX_URL,
    params={'limit': 18, 'offset': 0},
    headers={'Authorization': f'jwt {jwt}'}
)

print('状态码:', response_index.status_code)
print('数据:', response_index.json())