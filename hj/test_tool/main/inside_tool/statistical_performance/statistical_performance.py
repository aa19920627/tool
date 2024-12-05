# -*- coding: utf-8 -*-
"""
@Time ： 2024/9/23 10:37
@Auth ： 洪建
"""
from collections import defaultdict
from datetime import datetime

'''统计季度绩效'''

from openpyxl import load_workbook

# 指定 Excel 文件路径
file_path = '测试组9月季度绩效&原始统计数据.xlsx'

# 加载 Excel 文件
wb = load_workbook(file_path,data_only=True)

# 选择要操作的工作表，假设是第一个工作表
ws = wb.active
ws2 = wb.worksheets[1]

# ----------------- 设置日期范围 -----------------
start_date = datetime(2024, 7, 1, 0, 0, 0)  # 起始日期
end_date = datetime(2024, 9, 30, 23, 59, 59)  # 结束日期

# ----------------- 读取并筛选符合条件的行 -----------------
filtered_rows = []
# 创建一个字典用于存储统计结果
# 结构为： {人员名: {项目名: 工时总和}}
hours_data = defaultdict(lambda: defaultdict(float))

for row in ws.iter_rows(min_row=2, max_row=ws.max_row, values_only=True):  # 从第2行开始

    column_value = row[9]  # 实际列的值
    # print(column_value)

    # 检查时间是否符合
    if isinstance(column_value, datetime) and start_date <= column_value <= end_date :
        project_id = row[0]
        project_name = row[1]
        time_hour = float(row[6])
        name = row[10]
        if project_id != 'FXMGZ':
            hours_data[name][project_id+project_name]+=time_hour
# print(hours_data)

# ----------------- 将统计结果写入到 Excel 从第20行开始 -----------------
start_row = 28  # 指定开始写入的行
ws2.cell(row=start_row, column=1, value="姓名")  # 写入标题
ws2.cell(row=start_row, column=2, value="项目名称")  # 写入标题
ws2.cell(row=start_row, column=5, value="总工时")  # 写入标题

current_row = start_row + 1
# 获取每个人在项目中投入的工时
for name,projects in hours_data.items():
    for project,total_hours in projects.items():
        # print(f"{name}在{project}投入公式为{total_hours}")
        # 写入姓名
        ws2.cell(row=current_row, column=1, value=name)
        # 写入项目名称
        ws2.cell(row=current_row, column=2, value=project)
        ws2.merge_cells(start_row=current_row, start_column=2, end_row=current_row, end_column=4)
        # 写入总工时
        ws2.cell(row=current_row, column=5, value=total_hours)
        current_row += 1  # 移动到下一行
# 保存 Excel 文件
wb.save(file_path)
print("统计完成")



