#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : 洪建
# @File : ads-b_log.py
# @Time : 2025/2/27 10:42
import pandas as pd

'''读取server日志中的ads-b数据，输出excel'''

# 读取ads-b日志并写入excel
file_path = './data/ads-b.log'
excel_path = './data/ads-b.xlsx'
log_data = []
with open(file_path, 'r', encoding='GB2312') as f:
    for line_num, line in enumerate(f, 1):
        try:
            # print(line_num, line)
            line_list = line.split(',')
            # print(line_list)
            if '航班号' in line_list[3]:
                process_data = {
                    '航班号': line_list[3].split(':')[1],
                    '时间': line_list[0],
                    '经度': line_list[6].split(':')[1],
                    '纬度': line_list[7].split(':')[1]
                }
                log_data.append(process_data)
                # print(line_list[3].split(':')[1], line_list[6].split(':')[1], line_list[7].split(':')[1])

        except Exception as e:
            print(e)

    # 转换为DataFrame
    df = pd.DataFrame(log_data)
    # 写入Excel（自动创建新文件，覆盖已有文件）
    df.to_excel(excel_path, index=False,sheet_name='log',engine='openpyxl')