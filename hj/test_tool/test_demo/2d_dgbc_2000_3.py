import requests
import pandas as pd

# 定义经纬度和半径
latitude = 30.766085
longitude = 103.871099
radius = 2000  # 2公里

# 使用另一公共数据源（例如 Overpass API）
url = f'https://overpass-api.de/api/interpreter?data=[out:json];(node["building"]({latitude - radius/111},{longitude - radius/111},{latitude + radius/111},{longitude + radius/111});way["building"]({latitude - radius/111},{longitude - radius/111},{latitude + radius/111},{longitude + radius/111}););out;'

response = requests.get(url)

# 打印响应内容以进行调试
print("响应内容:", response.text)

# 尝试解析 JSON
try:
    data = response.json()
except requests.exceptions.JSONDecodeError as e:
    print(f"JSON 解析错误: {e}")
    data = {'elements': []}

# 处理数据
building_data = []
for element in data.get('elements', []):
    building_data.append({
        '建筑物名称': element.get('tags', {}).get('name', '未知'),
        '纬度': element.get('lat', '未知'),
        '经度': element.get('lon', '未知'),
        '建筑物海拔高度（相对地面）': '未知',  # 需要其他数据源提供高度
        '地面海拔': '未知',
        '总海拔高度': '未知'
    })

# 保存到Excel
buildings_df = pd.DataFrame(building_data)
buildings_df.to_excel('建筑物数据.xlsx', index=False, engine='openpyxl')

print("建筑物数据已成功保存到 '建筑物数据.xlsx'")
