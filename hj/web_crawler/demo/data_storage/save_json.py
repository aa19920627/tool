#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : 洪建
# @File : save_json.py
# @Time : 2025/11/10 09:50


"""json文件存储
   json数据必需用双引号
"""

import json

# str = ''' [{
#     "name": "王伟",
#     "gender": "male",
#     "birthday": "1992-10-18"
# },{
#
#     "name": "Selina",
#     "gender": "female",
#     "birthday": "1995-10-18"
#
# }]
# '''

# print(type(str))
# data = json.loads(str)
# print(data)
# print(type(data))
# print(data[0]['name'])
# #通过get来获取字典的值，第二个参数25是获取失败的默认值
# print(data[0].get('age', 25))
#
#
# # 从文件读取json
# data = json.load(open('data.json', encoding='utf-8'))
# print(data)
# print(type(data))
# print(data[0]['name'])


data = [{
    "name": "王伟",
    "gender": "male",
    "birthday": "1992-10-18"
}, {

    "name": "Selina",
    "gender": "female",
    "birthday": "1995-10-18"

}]
# 输出
# dumps方法把json对象转为字符串，indent控制缩进，ensure_ascii禁用Unicode字符编码
with open('data.json', 'w', encoding='utf-8') as f:
    f.write(json.dumps(data, indent=2, ensure_ascii=False))
