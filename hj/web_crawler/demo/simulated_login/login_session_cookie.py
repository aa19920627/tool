#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : 洪建
# @File : login_session_cookie.py
# @Time : 2026/1/29 16:22


"""基于Session和Cookie的模拟登陆实例"""

import requests
from urllib.parse import urljoin

BASE_URL = 'https://login2.scrape.center/'
LOGIN_URL = urljoin(BASE_URL, '/login')
INDEX_URL = urljoin(BASE_URL, '/page/1')
USERNAME = 'admin'
PASSWORD = 'admin'

session = requests.Session()
response_login = session.post(LOGIN_URL, data={
    'username': USERNAME,
    'password': PASSWORD
}, allow_redirects=False)
cookies = response_login.cookies
print('Cookies', cookies)

response_index = session.get(INDEX_URL)
print('Response Status', response_index.status_code)
print('Response URL', response_index.url)
