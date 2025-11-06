#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : 洪建
# @File : regular_expression.py
# @Time : 2025/11/5 16:21

import re

# 正则表达式练习

# match
# content = 'Hello 1234567 World_This is a Regex Demo'
# print(len(content))
# result = re.match('^Hello.*?(\d+).*Demo$', content)
# print(result)
# print(result.group())
# print(result.group(1))
# print(result.span())

# 修饰符
# content = 'Hello 1234567 World_This '
#            'is a Regex Demo'
# print(len(content))
# result = re.match('^Hello.*?(\d+).*Demo$', content ,re.S)
# print(result)
# print(result.group())
# print(result.group(1))
# print(result.span())

# 转义匹配
# content = '(百度) www.baidu.com'
# result = re.match('\(百度\) www\.baidu\.com', content)
# print(result)

# # search
# html = '''
# <div id="songs-list">
#     <h2 class="title">经典老歌</h2>
#     <p class="introduction">经典老歌列表</p>
#     <ul id="list" class="list-group">
#         <li data-view="2">一路上有你</li>
#         <li data-view="7">
#             <a href="/2.mp3" singer="任贤齐">沧海一声笑</a>
#         </li>
#         <li data-view="4" class="active">
#             <a href="/3.mp3" singer="齐秦">往事随风</a>
#         </li>
#         <li data-view="6"><a href="/4.mp3" singer="beyond">光辉岁月</a></li>
#         <li data-view="5"><a href="/5.mp3" singer="陈慧琳">记事本</a></li>
#         <li data-view="5">
#             <a href="/6.mp3" singer="邓丽君">但愿人长久</a>
#         </li>
#     </ul>
# </div>
# '''
#
# result = re.search('<li.*?active.*?singer="(.*?)">(.*?)</a>', html, re.S)
# if result:
#     print(result.group(1), result.group(2))

# # findall
#
# html = '''
# <div id="songs-list">
#     <h2 class="title">经典老歌</h2>
#     <p class="introduction">经典老歌列表</p>
#     <ul id="list" class="list-group">
#         <li data-view="2">一路上有你</li>
#         <li data-view="7">
#             <a href="/2.mp3" singer="任贤齐">沧海一声笑</a>
#         </li>
#         <li data-view="4" class="active">
#             <a href="/3.mp3" singer="齐秦">往事随风</a>
#         </li>
#         <li data-view="6"><a href="/4.mp3" singer="beyond">光辉岁月</a></li>
#         <li data-view="5"><a href="/5.mp3" singer="陈慧琳">记事本</a></li>
#         <li data-view="5">
#             <a href="/6.mp3" singer="邓丽君">但愿人长久</a>
#         </li>
#     </ul>
# </div>
# '''
#
# results = re.findall('<li.*?href="(.*?)".*?singer="(.*?)">(.*?)</a>', html, re.S)
# print(results)
# for result in results:
#     print(result)
#     print(result[0],result[1],result[2])

# # sub
# html = '''
# <div id="songs-list">
#     <h2 class="title">经典老歌</h2>
#     <p class="introduction">经典老歌列表</p>
#     <ul id="list" class="list-group">
#         <li data-view="2">一路上有你</li>
#         <li data-view="7">
#             <a href="/2.mp3" singer="任贤齐">沧海一声笑</a>
#         </li>
#         <li data-view="4" class="active">
#             <a href="/3.mp3" singer="齐秦">往事随风</a>
#         </li>
#         <li data-view="6"><a href="/4.mp3" singer="beyond">光辉岁月</a></li>
#         <li data-view="5"><a href="/5.mp3" singer="陈慧琳">记事本</a></li>
#         <li data-view="5">
#             <a href="/6.mp3" singer="邓丽君">但愿人长久</a>
#         </li>
#     </ul>
# </div>
# '''
#
# html = re.sub('<a.*?>|</a>','',html)
# print(html)
# results = re.findall('<li.*?>(.*?)</li>',html,re.S)
# for result in results:
#     print(result.strip())

# compile
content1 = '2019-12-15 12:00'
content2 = '2019-12-17 12:55'
content3 = '2019-12-22 13:21'

pattern = re.compile('\d{2}:\d{2}')
result1 = re.sub(pattern, '', content1)
result2 = re.sub(pattern, '', content2)
result3 = re.sub(pattern, '', content3)
print(result1, result2, result3)