#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : 洪建
# @File : save_mongodb.py
# @Time : 2025/11/10 15:25

import pymongo
from pymongo import MongoClient

"""
MongoDB文档存储
"""

# 建立连接
client = MongoClient('localhost', 27017)
# 指定数据库
db = client.test
# 指定集合
collection = db.students
# # 插入数据
# student1 = {
#     'id':'20170101',
#     'name':'jordan',
#     'age':22,
#     'gender':'male',
# }
# student2 = {
#     'id':'20160101',
#     'name':'zhaolin',
#     'age':23,
#     'gender':'male',
# }
# # 插入1条数据
# # result = collection.insert_one(student1)
# # 插入多条数据
# result = collection.insert_many([student1, student2])
# print(result)
# print(result.inserted_ids)


# # 查询
# # find_one查询返回单条结果,字典格式,条件可以是id
# # find查询返回1个生成器对象,可遍历获取结果
# result = collection.find_one({'name': 'jordan'})
# # print(result)
# results = collection.find({'name': 'jordan'})
# print(results)
# for result in results:
#     print(result)
#
# # 查询年龄大于22的数据
# results = collection.find({'age': {'$gt': 22}})
# for result in results:
#     print(result)
#
# # 通过正则条件来匹配
# results = collection.find({'name': {'$regex': '^j.*'}})
# for result in results:

# # 计数
# # 统计包含多少条数据,用count_documents方法,统计所有传入空字典
# count = collection.count_documents({})
# print(count)
# count = collection.count_documents({'age':22})
# print(count)

# 排序,调用sort方法,排序条件:pymongo.ASCENDING
# results = collection.find().sort('name', pymongo.ASCENDING)
# print([result['name'] for result in results])

# # 偏移,利用skip偏移位置,忽略指定数量的元素
# results = collection.find().sort('name',pymongo.ASCENDING).skip(2)
# print([result['name'] for result in results])
# # 使用limit方法指定要获取的结果个数
# results = collection.find().sort('name',pymongo.ASCENDING).skip(2).limit(1)
# print([result['name'] for result in results])

# # 更新
# condition = {'name':'jordan'}
# student = collection.find_one(condition)
# student['age'] = 31
# result = collection.update_one(condition, {'$set': student})
# print(result)
# print(result.matched_count,result.modified_count)
#
# # 更新多条,条件更新
# condition = {'age':{'$gt':10}}
# result = collection.update_many(condition,{'$inc':{'age':1}})
# print(result)

# 删除
result = collection.delete_one({'name':'jordan'})
print(result)
print(result.deleted_count)
result = collection.delete_many({'age':{'$lt':25}})
print(result.deleted_count)
