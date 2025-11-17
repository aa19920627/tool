#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : 洪建
# @File : save_elasticsearch.py
# @Time : 2025/11/11 13:27

from elasticsearch import Elasticsearch
from pandas.core.interchange.from_dataframe import primitive_column_to_ndarray

"""
存储elasticsearch搜索引擎存储
"""

# 创建索引
# es = Elasticsearch('http://192.168.36.76:9200')
# result = es.indices.create(index='news', ignore=400)
# print(result)
#
# # 删除索引
# result = es.indices.delete(index='news',ignore=400)
# print(result)

#
# # 插入数据
# data = {
#     'title': '乘风破浪',
#     'url': 'https://www.elastic.co/docs/deploy-manage/deploy/self-managed/install-elasticsearch-from-archive-on-linux-macos'
# }
# # 调用create方法，必须传id
# result = es.create(index='news', id='1' ,body=data)
# # 调用index方法，会自动生成id
# es.index(index='news',body=data)
# print(result)

# # 更新数据,还是可以用index方法，如果数据存在就覆盖，不存在就新增
# data = {
#     'title': '乘风破浪',
#     'url': 'https://www.elastic.co/docs/deploy-manage/deploy/self-managed/install-elasticsearch-from-archive-on-linux-macos',
#     'date':'2025-11-12'
# }
# result = es.index(index='news', id='1', body=data)
# print(result)
#
# # 更新部分数据，用update方法。更新的数据要放在doc中
# data = {
#     'doc':{
#         'date':'2025-11-14',
#     }
# }
# result = es.update(index='news', id='1', body=data)
# print(result)

# # 删除数据
# result = es.delete(index='news',id = '1',ignore=404)
# print(result)


# # 查询
# # 更新mapping信息，指定分词器和搜索分词器
es = Elasticsearch('http://192.168.36.76:9200')
# mapping = {
#     'properties': {
#         'title': {
#             'type': 'text',
#             'analyzer': 'ik_max_word',
#             'search_analyzer': 'ik_max_word',
#         }
#     }
# }
#
# es.indices.delete(index='news', ignore=[400, 404])
# es.indices.create(index='news', ignore=[400, 404])
# result = es.indices.put_mapping(index='news', body=mapping)
# print(result)

# 插入几条数据
# datas = [
#     {
#         'title':'金鸡奖开幕星光黯淡，周冬雨开场陈飞宇主持，网友感慨电影圈萧条',
#         'url':'https://www.msn.cn/zh-cn/news/other/%E9%87%91%E9%B8%A1%E5%A5%96%E5%BC%80%E5%B9%95%E6%98%9F%E5%85%89%E9%BB%AF%E6%B7%A1-%E5%91%A8%E5%86%AC%E9%9B%A8%E5%BC%80%E5%9C%BA%E9%99%88%E9%A3%9E%E5%AE%87%E4%B8%BB%E6%8C%81-%E7%BD%91%E5%8F%8B%E6%84%9F%E6%85%A8%E7%94%B5%E5%BD%B1%E5%9C%88%E8%90%A7%E6%9D%A1/ar-AA1QhtSA?ocid=msedgntp&pc=U531&cvid=6915763d9a7947b0874adb402717a311&ei=8',
#     },
#     {
#         'title':'上海高清放映回归，2秒售罄却藏10部国际大戏？',
#         'url':'https://www.msn.cn/zh-cn/news/other/%E4%B8%8A%E6%B5%B7%E9%AB%98%E6%B8%85%E6%94%BE%E6%98%A0%E5%9B%9E%E5%BD%92-2%E7%A7%92%E5%94%AE%E7%BD%84%E5%8D%B4%E8%97%8F10%E9%83%A8%E5%9B%BD%E9%99%85%E5%A4%A7%E6%88%8F/ar-AA1Ql2ad?ocid=msedgntp&pc=U531&cvid=6915763d9a7947b0874adb402717a311&ei=32'
#     }
# ]
# for data in datas:
#     es.index(index='news', body=data)

# 根据关键词查询内容
result = es.search(index="news")
print(result)
# 全文检索
dsl = {
    "query": {
        "match": {
            'title': '国际 开场 网友'
        }
    }
}
result = es.search(index="news", body=dsl)
print(result)
