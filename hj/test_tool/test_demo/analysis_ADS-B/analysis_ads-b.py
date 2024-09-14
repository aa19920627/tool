# -*- coding: utf-8 -*-
"""
@Time ： 2024/9/3 13:11
@Auth ： 洪建
"""


'''分析容仓图的ADS-B数据'''

import json
import pandas as pd

# 假设文本内容保存在一个文件中
file_path = './data/ads_b_i_b_original_0.dat'

# 读取文件内容
with open(file_path, 'r', encoding='utf-8') as file:
    content = file.read()

# 将多个JSON对象拆分出来
json_objects = content.split('}\n{')
json_objects = [obj + '}' if i != len(json_objects) - 1 else obj for i, obj in enumerate(json_objects)]
json_objects = ['{' + obj if i != 0 else obj for i, obj in enumerate(json_objects)]

# 解析JSON数据
data = [json.loads(obj) for obj in json_objects]

# 创建DataFrame
df = pd.DataFrame(data)

# 写入Excel文件
output_path = './data/output.xlsx'
df.to_excel(output_path, index=False)

print(f"数据已成功写入 {output_path}")

