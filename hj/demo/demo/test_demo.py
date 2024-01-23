from tabulate import tabulate

# 假设 areas、mf_names、integrated_manufacturers 和 results 是相应的列表
areas = ["Area1", "Area2", "Area3"]
mf_names = ["Manufacturer1", "Manufacturer22", "Manufacturer333"]
integrated_manufacturers = ["Integrated1", "Integrated22", "Integrated333"]
results = ["Result1", "Result22", "Result333"]

# 创建数据字典
data = {"Area": areas, "Manufacturer": mf_names, "Integrated Manufacturer": integrated_manufacturers, "Result": results}

# 使用 tabulate 打印表格
table = tabulate(data, headers="keys", tablefmt="grid")

# 输出表格
print(table)