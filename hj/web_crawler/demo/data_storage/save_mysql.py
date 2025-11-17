#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : 洪建
# @File : save_mysql.py
# @Time : 2025/11/10 10:53

"""
在mysql中存储数据
"""
import pymysql

# 连接数据库，创建spiders库
# db = pymysql.connect(host='localhost', user='root', passwd='root', port=3306)
# cursor = db.cursor()
# cursor.execute('SELECT VERSION()')
# data = cursor.fetchone()
# print(data)
# cursor.execute('CREATE DATABASE spiders DEFAULT CHARACTER SET utf8mb4')
# db.close()

# 创建表
# db = pymysql.connect(host='localhost', user='root', passwd='root', port=3306, db='spiders')
# cursor = db.cursor()
# sql = 'CREATE TABLE IF NOT EXISTS students (id VARCHAR(255) NOT NULL,name VARCHAR(255) NOT NULL,age INT NOT NULL,PRIMARY KEY(id))'
# cursor.execute(sql)
# db.close()

# # 插入数据
# data = {
#     'id': '20120001',
#     'name': 'Bob',
#     'age': 20,
# }
# table = 'students'
# keys = ','.join(data.keys())
# values = ','.join(['%s'] * len(data))
#
# db = pymysql.connect(host='localhost', user='root', passwd='root', port=3306, db='spiders')
# cursor = db.cursor()
#
# sql = 'INSERT INTO {table}({keys}) VALUES({values})'.format(table=table, keys=keys, values=values)
#
# print(sql)
#
# try:
#     if cursor.execute(sql, tuple(data.values())):
#         print('Success')
#         db.commit()
# except:
#     print('Failed')
#     db.rollback()
# db.close()

# # 更新数据
# data = {
#     'id': '20120002',
#     'name': 'seob',
#     'age': 21,
# }
# table = 'students'
# keys = ','.join(data.keys())
# values = ','.join(['%s'] * len(data))
#
# db = pymysql.connect(host='localhost', user='root', passwd='root', port=3306, db='spiders')
# cursor = db.cursor()
#
# # ON DUPLICATE KEY 判断主键是否存在，存在则更新，不存在则插入
# sql = 'INSERT INTO {table}({keys}) VALUES({values}) ON DUPLICATE KEY UPDATE '.format(table=table, keys=keys,
#                                                                                      values=values)
# # 构造update的sql
# update = ','.join(["{key} = %s".format(key=key) for key in data])
# sql += update
#
# try:
#     # insert和update均需要构造占位符，需要乘2
#     if cursor.execute(sql, tuple(data.values()) * 2):
#         print('Successful')
#         db.commit()
# except:
#     print('Failed')
#     db.rollback()
# db.close()

# # 删除数据
# table = 'students'
# condition = 'age > 20'
# sql = 'DELETE FROM {table} WHERE {condition}'.format(table=table, condition=condition)
#
# db = pymysql.connect(host='localhost', user='root', passwd='root', port=3306, db='spiders')
# cursor = db.cursor()
#
# try:
#     cursor.execute(sql)
#     db.commit()
# except:
#     db.rollback()
# db.close()

#查询数据
db = pymysql.connect(host='localhost', user='root', passwd='root', port=3306, db='spiders')
cursor = db.cursor()
sql = 'SELECT * FROM students WHERE age >= 20'

try:
    cursor.execute(sql)
    print('Count:', cursor.rowcount)
    # 查询一条数据，fetchone查询后指针移到下一行
    one = cursor.fetchone()
    print('One:', one)
    results = cursor.fetchall()
    print('Results:', results)
    print('Results Type:', type(results))

except :
    print('Error')