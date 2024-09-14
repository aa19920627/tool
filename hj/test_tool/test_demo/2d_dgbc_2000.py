import json
import osmnx as ox
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point, box

# Step 1: 加载高德API获取的建筑物数据
with open('building_data.json', 'r', encoding='utf-8') as f:
    pois = json.load(f)

# 提取建筑物中心点的经纬度
buildings_coords = [(float(poi['location'].split(',')[0]), float(poi['location'].split(',')[1])) for poi in pois]

# Step 2: 使用OSMnx获取建筑物多边形形状
# 中心点坐标 (纬度, 经度)
center_point = (30.765959, 103.871062)  # 根据实际情况调整这个点
distance = 2000  # 2公里的缓冲区

# 使用bbox_from_point创建边界框元组
north, south, east, west = ox.utils_geo.bbox_from_point(center_point, dist=distance)

# 使用geometries_from_bbox直接获取建筑物数据
buildings_gdf = ox.geometries_from_bbox(north, south, east, west, tags={'building': True})

# Step 3: 关联建筑物的形状和高度信息
def get_building_height(building):
    """尝试从OSM中提取建筑物高度"""
    return building.get('height', None)

# 为每个建筑物添加高度属性，如果有高程数据，直接使用
buildings_gdf['height'] = buildings_gdf.apply(lambda row: get_building_height(row), axis=1)

# 将高德API的数据转换为GeoDataFrame
gaode_buildings_gdf = gpd.GeoDataFrame({
    'geometry': [Point(lon, lat) for lon, lat in buildings_coords]
}, crs='EPSG:4326')

# 将高德的GeoDataFrame转换为与建筑物相同的坐标系
gaode_buildings_gdf = gaode_buildings_gdf.to_crs(buildings_gdf.crs)

# 创建缓冲区并过滤出在高德数据范围内的建筑物
buffer = gaode_buildings_gdf.buffer(0.001)
filtered_buildings = buildings_gdf[buildings_gdf.intersects(buffer.unary_union)]

# Step 4: 在二维地图上绘制建筑物的形状和高度
fig, ax = plt.subplots()

# 绘制建筑物形状
filtered_buildings.plot(ax=ax, color='lightblue', edgecolor='k')

# 标注建筑物高度
for idx, row in filtered_buildings.iterrows():
    if row['height']:
        centroid = row['geometry'].centroid
        ax.text(centroid.x, centroid.y, str(row['height']) + 'm', fontsize=8, ha='center')

plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title('Building Heights and Shapes in 2D')
plt.show()
