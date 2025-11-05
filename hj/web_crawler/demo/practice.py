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

import requests

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
r = requests.get('https://ssr1.scrape.center/')
print(type(r.status_code),  r.status_code)
print(type(r.headers), r.headers)
print(type(r.cookies), r.cookies)
print(type(r.url), r.url)
print(type(r.history), r.history)

exit() if not r.status_code == requests.codes.ok else print('Request Successfully')