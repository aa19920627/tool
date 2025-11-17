#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : 洪建
# @File : beautiful_soup.py
# @Time : 2025/11/7 14:24
import re

from bs4 import BeautifulSoup

"""
beautiful soup的使用
"""

# html = """
# <html>
# <head>
#     <title>The Dormouse's story</title>
# </head>
# <body>
#     <p class="title" name="dromouse"><b>The Dormouse's story</b></p>
#     <p class="story">Once upon a time there were three little sisters; and their names were
#     <a href="http://example.com/elsie" class="sister" id="link1"><!-- Elsie --></a>,
#     <a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
#     <a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
#     and they lived at the bottom of a well.</p>
#     <p class="story">...</p>
# </body>
# </html>
# """

# soup = BeautifulSoup(html, 'lxml')
# print(soup.prettify())
# print(soup.title.string)
#
# # 节点选择器
# print(soup.title)
# print(type(soup.title))
# print(soup.title.string)
# print(soup.head)
# print(soup.p)
#
# # 提取信息
# # 获取节点名称
# print(soup.title.name)
# # 获取属性
# print(soup.p.attrs)
# print(soup.p.attrs['name'])
# # 获取属性更简洁的方法
# print(soup.p['name'])
# print(soup.p['class'])
# # 获取内容
# print(soup.p.string)
# # 嵌套选择
# print(soup.head.title)
# print(type(soup.head.title))
# print(soup.head.title.string)
# # 关联选择
# # contents获取直接子节点组成的列表
# print(soup.p.contents)
# # children也可也获取子节点，返回生成器类型
# print(soup.p.children)
# for i,children in enumerate(soup.p.children):
#     print(i,children)
# # descendants获取所有子孙节点，返回生成器类型
# print(soup.p.descendants)
# for i, child in enumerate(soup.descendants):
#     print(i, child)
# # 父节点和祖先节点
# # 调用parent属性获取父节点
# print(soup.a.parent)
# # 调用parents属性获取所有祖先节点
# print(soup.a.parents)
# print(list(enumerate(soup.a.parents)))
# # 兄弟节点
# # next_sibling和previous_sibling分别用于获取节点的下一个和上一个兄弟节点
# # next_siblings和previous_siblings分别返回后面和前面的所有兄弟节点
# print(soup.a.next_sibling)
# print(soup.a.previous_sibling)
# print(soup.a.next_siblings)
# print(soup.a.previous_siblings)

# 方法选择器
# findall


html = """
<div class="panel">
    <div class="panel-heading">
        <h4>Hello</h4>
    </div>
    <div class="panel-body">
        <ul class="list" id="list-1" , name = "elements">
            <li class="element">Foo</li>
            <li class="element">Bar</li>
            <li class="element">Jay</li>
        </ul>
        <ul class="list list-small" id="list-2">
            <li class="element">Foo</li>
            <li class="element">Bar</li>
        </ul>
    </div>
</div>
"""

soup = BeautifulSoup(html, 'lxml')

# 通过name参数查询节点
print(soup.find_all(name='ul'))
# 嵌套查询
for ul in soup.find_all(name='ul'):
    print(ul.find_all(name='li'))

# attrs通过属性查询
print(soup.find_all(attrs = {'id':'list-1'}))
print(soup.find_all(attrs = {'name':'elements'}))

# text参数可以用来匹配节点的文本
print(soup.find_all(text=re.compile('Fo')))

# find，返回第一个匹配的元素
print(soup.find(class_ = 'list'))
