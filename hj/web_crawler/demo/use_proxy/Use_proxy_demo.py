#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : 洪建
# @File : Use_proxy_demo.py
# @Time : 2025/12/31 14:38


import requests

"""代理的使用"""

proxy = '121.232.71.107:23355'
proxies = {
    'https': 'http://' + proxy,
    'http': 'http://' + proxy,
}
secret_id = 'ud1x1e7pk8ecbevmyqze'
secret_key = 'e48rrng1f2jpd4sdfnlmqj0ft1vxzih8'

try:
    response = requests.get('https://www.httpbin.org/get/' + '? ', proxies=proxies)
    print(response.text)
except requests.exceptions.ConnectionError as e:
    print('Error', e.args)

