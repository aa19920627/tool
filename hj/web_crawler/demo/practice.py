#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : 洪建
# @File : practice.py
# @Time : 2025/10/29 17:08
import re
import urllib
from urllib.request import HTTPPasswordMgrWithDefaultRealm, HTTPBasicAuthHandler, build_opener, ProxyHandler, urlopen
from urllib.error import URLError
from http import cookiejar
from urllib import request, error
from urllib.parse import urlparse, urlunparse, urlsplit, urlunsplit, urljoin, urlencode, parse_qs, quote
from urllib.robotparser import RobotFileParser

import httpx
import requests
import urllib3
from requests_oauthlib import OAuth1

# response = urllib.request.urlopen('https://www.python.org')
# print(response.read().decode('utf-8'))
# print(type(response))
# print(response.status)
# print(response.getheaders())
# print(response.getheader('content-type'))


# data = bytes(urllib.parse.urlencode({'name': 'germey'}), encoding='utf-8')
# response = urllib.request.urlopen('https://httpbin.org/post', data=data)
# print(response.read().decode('utf-8'))


# try:
#     response = urllib.request.urlopen('https://httpbin.org/', timeout=0.1)
# except urllib.error.URLError as e:
#     if isinstance(e.reason, socket.timeout):
#         print('TIME OUT')

# request模块
# request = urllib.request.Request('https://python.org')
# response = urllib.request.urlopen(request)
# print(response.read().decode('utf-8'))

# request构造
# url = 'https://www.httpbin.org/post'
# headers = {
#     'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)',
#     'Host': 'www.httpbin.org'
# }
# dict = {'name': 'germey'}
# data = bytes(urllib.parse.urlencode(dict), encoding='utf-8')
# # req = urllib.request.Request(url=url, data=data, headers=headers, method='POST')
# # 通过add_header方法添加headers
# req = urllib.request.Request(url, data, method='POST')
# req.add_header('User-Agent', 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)')
# response = urllib.request.urlopen(req)
# print(response.read().decode('utf-8'))

# 处理身份认证
# username = 'admin'
# password = 'admin'
# url = 'https://ssr3.scrape.center/'
# p = HTTPPasswordMgrWithDefaultRealm()
# p.add_password(None, url, username, password)
# auth_handler = HTTPBasicAuthHandler(p)
# opener = build_opener(auth_handler)
#
# try:
#     result = opener.open(url)
#     html = result.read().decode('utf-8')
#     print(html)
# except URLError as e:
#     print(e.reason)

# # 添加代理
# proxy_handler = ProxyHandler({
#     'http': 'http://127.0.0.1:8080',
#     'https': 'https://127.0.0.1:8080'
# })
# opener = build_opener(proxy_handler)
# try:
#     response = opener.open('https://www.baidu.com')
#     print(response.read().decode('utf-8'))
# except URLError as e:
#     print(e.reason)


# Cookie
# 获取Cookie
# cookie =  cookiejar.CookieJar()
# handler = request.HTTPCookieProcessor(cookie)
# opener = request.build_opener(handler)
# response = opener.open('https://www.baidu.com')
# for item in cookie:
#     print(item.name + '=' + item.value)

# # 输出文件格式的Cookie
# filename = 'cookie.txt'
# # 将Cookie保存成Mozilla型浏览器的Cookie格式
# # cookie = cookiejar.MozillaCookieJar(filename)
# # 将Cookie保存成LWP（libwww-perl）格式
# cookie = cookiejar.LWPCookieJar(filename)
# handler = request.HTTPCookieProcessor(cookie)
# opener = request.build_opener(handler)
# response = opener.open('https://www.baidu.com')
# cookie.save(ignore_discard=True, ignore_expires=True )
#
# #读取Cookie文件
# cookie = cookiejar.LWPCookieJar()
# cookie.load('cookie.txt', ignore_expires=True, ignore_discard=True)
# handler = request.HTTPCookieProcessor(cookie)
# opener = request.build_opener(handler)
# response = opener.open('https://www.baidu.com')
# print(response.read().decode('utf-8'))

# URLError
# try:
#     response = request.urlopen('https://cuiqingcai.com/404')
# except error.URLError as e:
#     print(e.reason)

# HTTPError
# try:
#     response = request.urlopen('https://cuiqingcai.com/404')
# except error.HTTPError as e:
#     print(e.reason, e.code, e.headers, sep='\n')

# try:
#     response = request.urlopen('https://cuiqingcai.com/404')
# except error.HTTPError as e:
#     print(e.reason, e.code, e.headers, sep='\n')
# except error.URLError as e:
#     print(e.reason)
# else:
#     print('Request Successfully')

# 解析链接parse模块
# urlparse
# result = urlparse('https://tieba.baidu.com/f?kw=csgo', allow_fragments=False)
# print(result.scheme, result[0], result.netloc, result[1], sep='\n')

# urlunparse
# data = ['https', 'www.baidu.com', 'index.html', 'user','a=6', 'comment']
# print(urlunparse(data))

# urlsplit
# result = urlsplit('https://www.baidu.com/index.php?tn=75144485_1_dg&ch=9')
# print(result, result.scheme, result[0])


# urljoin
# print(urljoin('https://www.baidu.com', 'index.php?tn=75144485_1_dg&ch=9'))
# print(urljoin('https://www.baidu.com/index.php', '?tn=75144485_1_dg&ch=9'))
# print(urljoin('https://www.baidu.com/index.php', 'https://cuiqingcai.com/?tn=75144485_1_dg&ch=9'))

# urlencode
# params = {'name': 'germey', 'age': 22}
# baseurl = 'https://www.baidu.com?'
# url = baseurl + urlencode(params)
# print(url)

# parse_qs
# query = "name=germey&age=22"
# print(parse_qs(query))

# quote
# keyword = '壁纸'
# url = 'https://www.baidu.com/s?wd=' + quote(keyword)
# print(url)

# urllib.robotparser.RobotFileParser(url='')

# # Robot协议解析
# rp = RobotFileParser()
# # rp.set_url('https://www.baidu.com/robots.txt')
# # rp.read()
# rp.parse(urlopen('https://www.baidu.com/robots.txt').read().decode('utf-8').split('\n'))
# print(rp.can_fetch('Baiduspider', 'https://www.baidu.com'))
# print(rp.can_fetch('Baiduspider', 'https://www.baidu.com/homepage/'))
# print(rp.can_fetch('Googlebot', 'https://www.baidu.com/homepage/'))

# requests
# get
# data = {
#     'name': 'germey',
#     'age': 22
# }
# r = requests.get('https://www.httpbin.org/get', params=data)
# print(r.json())

# r = requests.get('https://ssr1.scrape.center')
# pattern = re.compile('<h2.*?>(.*?)</h2>',re.S)
# titles = re.findall(pattern, r.text)
# print(titles)

# 抓取二进制数据
# r = requests.get('https://scrape.center/favicon.ico')
# with open('favicon.ico', 'wb') as f:
#     f.write(r.content)

# 响应
# r = requests.get('https://ssr1.scrape.center/')
# print(type(r.status_code),  r.status_code)
# print(type(r.headers), r.headers)
# print(type(r.cookies), r.cookies)
# print(type(r.url), r.url)
# print(type(r.history), r.history)
#
# exit() if not r.status_code == requests.codes.ok else print('Request Successfully')

# # 文件上传
# files = {'file': open('favicon.ico', 'rb')}
# r = requests.post('http://httpbin.org/post', files=files)
# print(r.text)

# Cookie获取
# r = requests.get('https://docs.qq.com/desktop/')
# print(r.cookies)
# for key, value in r.cookies.items():
#     print(key + '=' + value)

# # Cookie设置，直接放到headers中
# headers = {
#     'Cookie': '_octo=GH1.1.295542215.1731389551; cpu_bucket=xlg; preferred_color_mode=light; tz=Asia%2FShanghai; _device_id=17de21cf84d8665be28ebaf1166e841f; saved_user_sessions=52519794%3Aoo8DZ6st8OpcTbQT6lE_Yuigc9fr7XorCeUc-BTwVXvgmb6x; user_session=oo8DZ6st8OpcTbQT6lE_Yuigc9fr7XorCeUc-BTwVXvgmb6x; __Host-user_session_same_site=oo8DZ6st8OpcTbQT6lE_Yuigc9fr7XorCeUc-BTwVXvgmb6x; tz=Asia%2FShanghai; color_mode=%7B%22color_mode%22%3A%22auto%22%2C%22light_theme%22%3A%7B%22name%22%3A%22light%22%2C%22color_mode%22%3A%22light%22%7D%2C%22dark_theme%22%3A%7B%22name%22%3A%22dark%22%2C%22color_mode%22%3A%22dark%22%7D%7D; logged_in=yes; dotcom_user=aa19920627; _gh_sess=pkmG58sTWR%2FI8DCqt0lhCQPKtIcvSpmw90UW4qdZhUgiIypkrKo8BKDvjjpLNeNSbiQ9BlEm93Lw1%2F%2BTEVFNgndBwBZiLfvPGJQkqfXvSyZN7qjbnkcEzPt%2BUmlpmPaBh5qMBXuvxKlDRZSAmFuucKMSSFMr4XHNuSfV8rSecpBXERH%2B55Jx54emXWekApaCzbNdz1ZeIrwFgGzkRLPJzDQIbyAufG8eTrH4n1KcaTwux6MuuF1t19YcIiPnN270sCM7KMGI8Buxrl7lgsvcwWEFQle%2FTYO55ZGF6DtUVdXfiLb20IMMYBZLSoQD03%2F3eMdoi%2BdayOWWHbTf1mhfO2%2BHheiuWcdCWSgA7VKdHUkGYK2Z7DU1G2zL6%2FYM9Mk4QkAisR%2B%2FTeJ%2FR3PHeMtuGCG9LpnK%2FN6NwNYSAGXdDZkZQ7zIFwZ%2ByuMJaUyw9UOGJW%2BqVtrzLkY7NnJopSK6gQcmGxLo2woNPGW4uU%2FlFf8Bx7bP6V7kMvQQp8ZWJSqaJ7bOIV88DSNZxTEUzRAA0b%2FyQIJdWZUe2Yj8PRuZPUCrLuPSKPs8PhXBHL1w%2BbFRjsocpuRQXMmEJOw0zM%2FAkx0Taj3ajtmRA7rBJkHVh6sFMT59iBGLrFrSTJJP1G6lCA%2FnYj6q3WBuvv7C%2BjVDNAaqNsf1kVvPK06KrjxCz7gWSFEw9QsrW6TizNPSt44Halj3oWD3nKYtTQiShRccJZsLxHfCdPj1MTqQfWeDYLOnz0hpqQymR1oaawPm31KPPdI9xYr%2FK%2BtBu5zpqupcv11HRWGXBG2wL01GTZCRaQ72%2FVaRsCJRPAX0boW%2BUGqAW6J90ENnh5UJ4Zc%2FozXfj1KzvYmfIDEe8MUVR1%2FbQWkAlG02l3%2Bds8Txd8zYO%2BbP9BWyA0j9KbsxBzvQ0556XtCQbnXWwGhIpLFBRGr28LpWbcowbgGlRf7uOoIirXqSr2vWjuu9KogdfWDymK6W%2FeE3oCzq4%2B9HU%2B2Cf20%2Fp9nj%2FqSdtbXy5ovdupqVAE0oaS5Rilh2ZLmF%2BprH%2BElLxKJOXMXxw0KenGWRog%3D%3D--WDXgu0r8e6hOzsre--UG87HShC6bWY2GHJCgMU%2Fw%3D%3D',
#     'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36 Edg/142.0.0.0'
# }
#
# r = requests.get('https://github.com/', headers=headers)
# print(r.text)
#
# # Cookie设置，通过Cookies参数设置
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36 Edg/142.0.0.0'
# }
# cookies = '_octo=GH1.1.295542215.1731389551; cpu_bucket=xlg; preferred_color_mode=light; tz=Asia%2FShanghai; _device_id=17de21cf84d8665be28ebaf1166e841f; saved_user_sessions=52519794%3Aoo8DZ6st8OpcTbQT6lE_Yuigc9fr7XorCeUc-BTwVXvgmb6x; user_session=oo8DZ6st8OpcTbQT6lE_Yuigc9fr7XorCeUc-BTwVXvgmb6x; __Host-user_session_same_site=oo8DZ6st8OpcTbQT6lE_Yuigc9fr7XorCeUc-BTwVXvgmb6x; tz=Asia%2FShanghai; color_mode=%7B%22color_mode%22%3A%22auto%22%2C%22light_theme%22%3A%7B%22name%22%3A%22light%22%2C%22color_mode%22%3A%22light%22%7D%2C%22dark_theme%22%3A%7B%22name%22%3A%22dark%22%2C%22color_mode%22%3A%22dark%22%7D%7D; logged_in=yes; dotcom_user=aa19920627; _gh_sess=pkmG58sTWR%2FI8DCqt0lhCQPKtIcvSpmw90UW4qdZhUgiIypkrKo8BKDvjjpLNeNSbiQ9BlEm93Lw1%2F%2BTEVFNgndBwBZiLfvPGJQkqfXvSyZN7qjbnkcEzPt%2BUmlpmPaBh5qMBXuvxKlDRZSAmFuucKMSSFMr4XHNuSfV8rSecpBXERH%2B55Jx54emXWekApaCzbNdz1ZeIrwFgGzkRLPJzDQIbyAufG8eTrH4n1KcaTwux6MuuF1t19YcIiPnN270sCM7KMGI8Buxrl7lgsvcwWEFQle%2FTYO55ZGF6DtUVdXfiLb20IMMYBZLSoQD03%2F3eMdoi%2BdayOWWHbTf1mhfO2%2BHheiuWcdCWSgA7VKdHUkGYK2Z7DU1G2zL6%2FYM9Mk4QkAisR%2B%2FTeJ%2FR3PHeMtuGCG9LpnK%2FN6NwNYSAGXdDZkZQ7zIFwZ%2ByuMJaUyw9UOGJW%2BqVtrzLkY7NnJopSK6gQcmGxLo2woNPGW4uU%2FlFf8Bx7bP6V7kMvQQp8ZWJSqaJ7bOIV88DSNZxTEUzRAA0b%2FyQIJdWZUe2Yj8PRuZPUCrLuPSKPs8PhXBHL1w%2BbFRjsocpuRQXMmEJOw0zM%2FAkx0Taj3ajtmRA7rBJkHVh6sFMT59iBGLrFrSTJJP1G6lCA%2FnYj6q3WBuvv7C%2BjVDNAaqNsf1kVvPK06KrjxCz7gWSFEw9QsrW6TizNPSt44Halj3oWD3nKYtTQiShRccJZsLxHfCdPj1MTqQfWeDYLOnz0hpqQymR1oaawPm31KPPdI9xYr%2FK%2BtBu5zpqupcv11HRWGXBG2wL01GTZCRaQ72%2FVaRsCJRPAX0boW%2BUGqAW6J90ENnh5UJ4Zc%2FozXfj1KzvYmfIDEe8MUVR1%2FbQWkAlG02l3%2Bds8Txd8zYO%2BbP9BWyA0j9KbsxBzvQ0556XtCQbnXWwGhIpLFBRGr28LpWbcowbgGlRf7uOoIirXqSr2vWjuu9KogdfWDymK6W%2FeE3oCzq4%2B9HU%2B2Cf20%2Fp9nj%2FqSdtbXy5ovdupqVAE0oaS5Rilh2ZLmF%2BprH%2BElLxKJOXMXxw0KenGWRog%3D%3D--WDXgu0r8e6hOzsre--UG87HShC6bWY2GHJCgMU%2Fw%3D%3D'
# jar = requests.cookies.RequestsCookieJar()
# for cookie in cookies.split(';'):
#     key, value = cookie.split('=', 1)
#     jar.set(key, value)

# r = requests.get('https://github.com/', cookies=jar, headers=headers)
# print(r.text)

# Session维持
# s = requests.Session()
# s.get('https://www.httpbin.org/cookies/set/number/123456789')
# r = s.get('https://www.httpbin.org/cookies')
# print(r.text)

# # SSL证书验证
# # 忽视证书警告
# urllib3.disable_warnings()
# # verify设置关闭证书验证
# response = requests.get("https://ssr2.scrape.center", verify=False)
# print(response.status_code)


# # 超时设置
# # 连接和读取超时时间总和
# r = requests.get('http://httpbin.org/get', timeout=5)
# # 分别设置连接和读取超时
# r_one = requests.get('http://httpbin.org/get', timeout=(2,3))
# # 永久等待，设置None或传该参数
# r_two = requests.get('http://httpbin.org/get', timeout=None)

# # 身份认证
# # basic认证
# r = requests.get('http://ssr3.scrape.center', auth=('admin', 'admin'))
# # OAuth认证
#
# url = 'https://api.twitter.com/1.1/account/verify_credentials.json'
# auth = OAuth1('YOUR_APP_KEY', 'YOUR_APP_SECRET', 'USER_OAUTH_TOKEN', 'USER_OAUTH_TOKEN_SECRET')
# requests.get(url, auth=auth)

# # 代理设置
# proxies = {
#     'http': 'http://127.0.0.1:8080',
#     'https': 'https://127.0.0.1:8080',
# }
# requests.get('https://www.baidu.com/', proxies=proxies)
# # 代理有身份认证
# proxies = {'https': 'http://user:password@127.0.0.1:8080',}
# # socks代理
# proxies_socks = {
#     'http': 'socks5://user:password@host:port',
#     'https': 'socks5://user:password@host:port',
# }
# requests.get('https://www.baidu.com/', proxies=proxies)


# # httpx
# # 声明http2.0
# client = httpx.Client(http2=True)
# response = client.get('https://spa16.scrape.center')
# print(response.text)

# Client对象

# url = 'https://httpbin.org/headers'
# headers = {'User-Agent': 'ma-app/0.0.1'}
# with httpx.Client(headers=headers) as client:
#     r = client.get(url)
#     print(r.json()['headers']['User-Agent'])

resp = requests.get("https://github.com/CharlesPikachu/freeproxy/blob/master/proxies.json")
print(resp.text)