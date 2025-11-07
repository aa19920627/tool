#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : 洪建
# @File : parsing_extraction.py
# @Time : 2025/11/7 10:42
from io import StringIO

from lxml import etree

"""
网页数据解析提取
"""

html = etree.parse('./parsing_extraction.html', etree.HTMLParser())
result = etree.tostring(html, method="html")
print(result.decode('utf-8'))
result = html.xpath('//*')
# 获取li节点
result = html.xpath('//li')
# 获取li节点下的子节点a
result = html.xpath('//li/a')
# 获取ul节点下的所有子孙节点a
result = html.xpath('//ul//a')
# 获取父节点
result = html.xpath('//a[@href="link4.html"]/../@class')
# 通过parent获取父节点
result = html.xpath('//a[@href="link4.html"]/parent::*/@class')
# 属性匹配，@符号实现属性过滤
result = html.xpath('//li[@class="item-0"]')
# 文本获取,XPATH中的text方法获取文本
result = html.xpath('//li[@class="item-0"]/a/text()')
# 节点属性获取
result = html.xpath('//li/a/@href')
# 属性多值匹配,用contains
result = html.xpath('//li[contains(@class,"li")]/a/text()')
# 多属性匹配,用and连接
result = html.xpath('//li[contains(@class,"li") and @name="item"]/a/text()')
# 按序选择
# 选择第1个节点
result = html.xpath('//li[1]/a/text()')
# 选择最后1个节点
result = html.xpath('//li[last()]/a/text()')
# 选择位置小于3的节点
result = html.xpath('//li[position()<3]/a/text()')
# 选择倒数第3个节点
result = html.xpath('//li[last()-2]/a/text()')
# 节点轴选择
# ancestor轴，获取所有祖先节点
result = html.xpath('//li[1]/ancestor::*')
# 指定获取祖先节点中的div
result = html.xpath('//li[1]/ancestor::div')
# attribute获取所有属性值
result = html.xpath('//li[1]/attribute::*')
# child获取直接子节点
result = html.xpath('//li[1]/child::a[@href="link1.html"]')
# descendant轴，获取所有子孙节点
result = html.xpath('//li[1]/descendant::span')
# following获取当前节点后的所有节点
result = html.xpath('//li[1]/following::*[2]')
# following-sibling轴，获取当前节点之后的所有同级节点
result = html.xpath('//li[1]/following-sibling::*')

print(result)
# print(result[0])
