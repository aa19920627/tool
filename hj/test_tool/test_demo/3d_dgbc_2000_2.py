import requests
import json
import os
import rasterio
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from pyproj import Transformer

# 高德 API 密钥
api_key = '9b9470ece01b35024cdc99a33adda00f'
center_location = '103.871062,30.765959'  # 替换为你的位置
radius = 2000
local_file = 'building_data.json'

# 高德API获取POI数据函数
def get_pois(api_key, location, radius, poi_types):
    url = "https://restapi.amap.com/v3/place/around"
    pois = []
    for poi_type in poi_types:
        params = {
            'key': api_key,
            'location': location,
            'radius': radius,
            'types': poi_type,
            'offset': 50
        }
        response = requests.get(url, params=params)
        data = response.json()
        if data.get('status') == '1':
            pois.extend(data.get('pois', []))
    return pois

# 获取建筑物数据
def fetch_building_data():
    poi_types = [
        '120000',  # 商务住宅
        '150000',  # 交通设施
        '200000',  # 生活服务
        '170000',  # 餐饮服务
        '190000',  # 娱乐设施
        '160000',  # 金融服务
        '180000',  # 政府机构
        '210000',  # 教育机构
        '220000',  # 医疗机构
        '230000',  # 旅游景点
        '240000'   # 购物服务
    ]
    return get_pois(api_key, center_location, radius, poi_types)

# 读取或获取建筑物数据
if os.path.exists(local_file):
    with open(local_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
else:
    data = fetch_building_data()
    with open(local_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# 解析建筑物数据
buildings = []
for item in data:
    if 'polygon' in item:
        polygon = item['polygon']
        coordinates = [(float(coord.split(',')[0]), float(coord.split(',')[1])) for coord in polygon.split(';')]
        buildings.append({
            'name': item['name'],
            'coordinates': coordinates,
            'height': None  # 初始高度为 None
        })

# 读取高程数据
file_path = './ASTGTM_N30E103Y.img'  # DEM 数据文件路径

with rasterio.open(file_path) as src:
    elevation_data = src.read(1)
    transform = src.transform
    crs = src.crs  # 这里获取到影像的 CRS（坐标参考系）

# WGS84 到投影坐标系的转换器
transformer = Transformer.from_crs("EPSG:4326", crs, always_xy=True)

# 经纬度到图像像素坐标的转换
def latlon_to_pixel(lat, lon, transform):
    try:
        proj_x, proj_y = transformer.transform(lon, lat)  # 先经度后纬度
        x, y = rasterio.transform.rowcol(transform, proj_x, proj_y)
        return x, y
    except Exception as e:
        print(f"Error converting lat/lon to pixel: {e}")
        return None, None

# 获取建筑物实际高度
def get_building_actual_height(coords):
    heights = []
    for lat, lon in coords:
        x, y = latlon_to_pixel(lat, lon, transform)
        if x is not None and y is not None and 0 <= x < elevation_data.shape[1] and 0 <= y < elevation_data.shape[0]:
            heights.append(elevation_data[y, x])
    if heights:
        return np.mean(heights)
    else:
        return None

# 计算所有建筑物的高度
for building in buildings:
    building['height'] = get_building_actual_height(building['coordinates'])
    print(f"Building: {building['name']}, Height: {building['height']}")

# 绘制建筑物平面形状并标注高度
fig, ax = plt.subplots()
for building in buildings:
    if building['height'] is not None:
        polygon = Polygon(building['coordinates'], closed=True, edgecolor='black', facecolor='lightblue')
        ax.add_patch(polygon)
        centroid = np.mean(building['coordinates'], axis=0)
        ax.text(centroid[0], centroid[1], f"{building['height']:.1f}m", ha='center', va='center', fontsize=8)

ax.set_title('Building Heights on Map')
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')
plt.show()
