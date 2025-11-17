#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : 洪建
# @File : save_csv.py

import csv

import pandas as pd

'''
存储CSV数据文件
'''
#
# # 列表数据写入,参数newline避免出现中间空行问题
# with open('data.csv', 'w', encoding='utf-8', newline='') as f:
#     writer = csv.writer(f)
#     writer.writerow(['id', 'name', 'age'])
#     writer.writerow(['10001', '张强', '25'])
#     writer.writerow(['10002', '李强', '27'])
#     writer.writerow(['10003', '陈强', '31'])
#     # 一次性写入多行数据
#     writer.writerows([['10004', '王强', '25'], ['10005', '周强', '19']])
#
# # 写入字典数据
# with open('data.csv', 'w', newline='', encoding='utf-8') as f:
#     # 定义表头
#     fieldnames = ['id', 'name', 'age']
#     # 初始化字典写入对象
#     writer = csv.DictWriter(f, fieldnames=fieldnames)
#     # 先写入表头
#     writer.writeheader()
#     writer.writerow({'id': 10001, 'name': '陈强', 'age': 25})

# # 用pandas库写入
# data = [
#     {'id': 10001, 'name': '陈强', 'age': 25},
#     {'id': 10001, 'name': '王强', 'age': 25}
# ]
# df = pd.DataFrame(data)
# df.to_csv('data.csv', index=False)

# csv库来读取
with open('data.csv','r',encoding='utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)
# pandas库来读取
df = pd.read_csv('data.csv')
print(df)
# 将df对象转换成列表
data = df.values.tolist()
print(data)
