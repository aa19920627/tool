# -*- coding: utf-8 -*-
"""
@Time ： 2024/6/20 14:04
@Auth ： 洪建
"""
from lxml import etree

'''
封装通用工具
'''


# 格式化xml响应报文
def formatting_xml(res_xml):
    # 解析xml
    root_res = etree.fromstring(res_xml)
    # 格式化xml
    formatted_xml = etree.tostring(root_res, encoding="UTF-8", pretty_print=True).decode()

    return formatted_xml
