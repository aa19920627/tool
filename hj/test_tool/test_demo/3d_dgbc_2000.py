# -*- coding: utf-8 -*-
"""
@Time ： 2024/8/22 13:39
@Auth ： 洪建
"""
import requests
import matplotlib.pyplot as plt
import rasterio
import numpy as np
import seaborn as sns

# 通过高德API获取公司两公里范围内的建筑物经纬度
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


def read_dem_data():
# 高程数据文件路径（.img 格式）
    file_path = './ASTGTM_N30E103Y.img'

    # 使用 rasterio 打开高程数据文件
    with rasterio.open(file_path) as src:
        print(f"File Name: {src.name}")
        print(f"Driver: {src.driver}")
        print(f"Width: {src.width}")
        print(f"Height: {src.height}")
        print(f"Count of Bands: {src.count}")
        print(f"CRS: {src.crs}")
        print(f"Transform: {src.transform}")

        # 读取第一个波段的数据
        elevation_data = src.read(1)


def lonlat_to_pixel(lon, lat, transform):
    """ 将经纬度转换为图像像素坐标 """
    px, py = ~transform * (lon, lat)
    return int(px), int(py)


if __name__ == '__main__':

    # step1:获取周边建筑经纬度信息

    api_key = 'a69474d340e43a07fa7cb7534e854b66'
    center_location = '103.871062,30.765959'  # 替换为你的位置
    radius = 2000

    # POI 类型列表
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

    all_pois = get_pois(api_key, center_location, radius, poi_types)

    buildings=[]
    for poi in all_pois:
        # print(f"名称: {poi['name']}, 经度: {poi['location'].split(',')[0]}, 纬度: {poi['location'].split(',')[1]}")
        buildings.append({
            'name':poi['name'],
            'lat':poi['location'].split(',')[1],
            'lon':poi['location'].split(',')[0]
        })

    # step2:读取高程数据
    read_dem_data()

    # step3:计算高程数据的基本统计信息，并将建筑物的经纬度转换为图像中的像素坐标
    with rasterio.open('./ASTGTM_N30E103Y.img') as src:
        elevation_data = src.read(1)
        transform = src.transform

        # 计算并打印数据的统计信息
        print(f"Data Type: {elevation_data.dtype}")
        print(f"Min Elevation: {np.min(elevation_data)}")
        print(f"Max Elevation: {np.max(elevation_data)}")
        print(f"Mean Elevation: {np.mean(elevation_data)}")

        # 将建筑物经纬度转换为像素坐标
        building_coords = []
        for building in buildings:
            px, py = lonlat_to_pixel(float(building['lon']), float(building['lat']), transform)
            building_coords.append((px, py, building['name']))

    # step4: 可视化数据
    file_path = './ASTGTM_N30E103Y.img'

    with rasterio.open(file_path) as src:
        elevation_data = src.read(1)

        # 打印数据的统计信息
        print(f"Data Type: {elevation_data.dtype}")
        print(f"Min Elevation: {np.min(elevation_data)}")
        print(f"Max Elevation: {np.max(elevation_data)}")
        print(f"Mean Elevation: {np.mean(elevation_data)}")

        # 可视化数据
        # 设置中文字体
        sns.set(font='SimHei')  # 使用 SimHei 字体（黑体）

        # 打开高程数据文件
        file_path = './ASTGTM_N30E103Y.img'
        with rasterio.open(file_path) as src:
            elevation_data = src.read(1)

            # 打印数据的统计信息
            print(f"数据类型: {elevation_data.dtype}")
            print(f"最小高程: {np.min(elevation_data)}")
            print(f"最大高程: {np.max(elevation_data)}")
            print(f"平均高程: {np.mean(elevation_data)}")

            # 可视化数据
            plt.figure(figsize=(12, 12))
            plt.title("高程数据")
            plt.imshow(elevation_data, cmap='terrain', origin='upper', extent=[0, src.width, 0, src.height],
                       interpolation='bilinear')
            plt.colorbar(label='高程 (米)')
            plt.xlabel('列')
            plt.ylabel('行')
            plt.show()
