#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : 洪建
# @File : gps_heatmap.py
# @Time : 2025/4/27 13:29


import plotly.express as px
import pandas as pd
import numpy as np

# 生成成都范围内200个随机点（纬度范围：30.4~30.8，经度范围：103.9~104.3）
np.random.seed(42)  # 固定随机种子保证可复现
data = {
    'location': ['成都'] * 200,
    'lat': np.random.uniform(30.4, 30.8, 200),  # 成都纬度范围
    'lon': np.random.uniform(103.9, 104.3, 200),  # 成都经度范围
    'value': np.random.randint(10, 100, 200)  # 随机热力值(10~100)
}
df = pd.DataFrame(data)

# 使用plotly express创建热力图
fig = px.density_mapbox(
    df,  # 数据框
    lat='lat',  # 纬度列名
    lon='lon',  # 经度列名
    z='value',  # 热力值列名
    radius=20,  # 热力点半径
    center=dict(lat=30.4, lon=103.6),  # 地图初始中心点
    zoom=10,  # 初始缩放级别
    title='热力图',  # 图表标题
    mapbox_style="white-bg",  # 使用本地地图是需要此设置
    color_continuous_scale="rainbow"    #热力图色阶
)

# 使用本地地图
fig.update_layout(
    mapbox_layers=[{
            "below": "traces",  # 图层位置
            "sourcetype": "raster",  # 数据源类型
            "source": ["http://127.0.0.1:5000/tiles/{z}/{x}/{y}.png"],  # 本地瓦片地图
            "maxzoom": 15,
            "minzoom": 8
        }],
    mapbox=dict(
        center=dict(lat=data['lat'].mean(), lon=data['lon'].mean()),
    ),
    margin=dict(l=0, r=0, t=0, b=0),  # 四个边距全部设为0
    width=1920,  # 固定宽度
    height=1080,  # 固定高度
)


# 输出html文件并自动打开
fig.write_html("heatmap.html", auto_open=True,config=dict(scrollZoom=True) )
