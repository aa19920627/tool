# 导入必要的库
from itertools import combinations

import plotly.express as px
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from scipy.stats import gaussian_kde

# 中垂线热力图类
class HeatmapGenerator:
    def __init__(self,aiport):
        self.path = "./data/华东机场干扰数据.xlsx"
        self.leng_km = 10  # 中垂线长度/公里
        # 读取干扰数据源
        self.interference_data_lit = self.read_data(aiport)

    # 生成热力图方法
    def heatmap_generator(self):

        # 用于计算中垂线交点的列表
        bisectors = []
        # 计算中垂线交点，用于绘制热力图
        for interference_data in self.interference_data_lit:
            # 获取中垂线计算结果
            lat_list, lon_list = self.calculate_point(interference_data[3], interference_data[4], interference_data[5],
                                                      interference_data[6], self.leng_km)

            # 将用于计算中垂线交点的数据追加到列表中
            bisectors.append(((lat_list[0], lon_list[0]), (lat_list[1], lon_list[1])))

        # 计算中垂线交点
        pt_list = self.calculate_intersection_all_point(bisectors)

        # 转换为经度列表和纬度列表
        lat_iter, lon_iter = zip(*pt_list)  # 解包获得元组
        lat_list, lon_list = list(lat_iter), list(lon_iter)  # 转换为列表

        data = {'lat': lat_list, 'lon': lon_list, 'z': [100] * len(lat_list)}
        df = pd.DataFrame(data)

        # 动态半径计算
        grid_size = 0.001  # 约100米网格
        df['grid_lat'] = (df['lat'] // grid_size) * grid_size
        df['grid_lon'] = (df['lon'] // grid_size) * grid_size
        grid_counts = df.groupby(['grid_lat', 'grid_lon']).size().reset_index(name='counts')
        df = pd.merge(df, grid_counts, on=['grid_lat', 'grid_lon'])

        # 安全的动态半径计算
        df['dynamic_radius'] = np.clip(10 + np.log(df['counts'] + 1) * 5, 10, 30).astype(int)

        # 热力值增强计算
        df['z'] = np.power(df['counts'], 1.5)  # 指数增强

        # 创建热力图
        self.fig = px.density_mapbox(
            df,
            lat='lat',  # 纬度列名
            lon='lon',  # 经度列名
            z='z',  # 热力值列名
            radius=15,  # 热力点半径
            opacity=0.8,    #增加透明度
            zoom=11,  # 初始缩放级别
            title='热力图',  # 图表标题
            mapbox_style="white-bg",  # 使用本地地图是需要此设置
            color_continuous_scale="Jet"  # 热力图色阶
        )

        # 动态更新半径（正确方式）
        self.fig.update_traces(
            radius=np.array(df['dynamic_radius']),  # 传入数值数组
            selector={'type': 'densitymapbox'}
        )
        # 绘制异常轨迹线和中垂线
        self.draw_line()

        # 使用本地地图
        self.fig.update_layout(
            mapbox_layers=[{
                "below": "traces",  # 图层位置
                "sourcetype": "raster",  # 数据源类型
                "source": ["http://127.0.0.1:5000/tiles/{z}/{x}/{y}.png"],  # 本地瓦片地图
                "maxzoom": 15,
                "minzoom": 8
            }],
            mapbox=dict(
                center=dict(lat=df['lat'].mean(), lon=df['lon'].mean()),
            ),
            margin=dict(l=0, r=0, t=0, b=0),  # 四个边距全部设为0
            width=1920,  # 固定宽度
            height=1080,  # 固定高度
            showlegend=False,
        )

        # 输出html文件并自动打开
        self.fig.write_html("heatmap.html", auto_open=True, config=dict(scrollZoom=True))

    # 读取干扰数据
    def read_data(self,airport):
        # 读取excel文件
        df = pd.read_excel(self.path, sheet_name='Sheet1')

        self.interference_data_lit = []

        # 按行顺序读取，从第二行开始
        for row in df.itertuples():
            air_addr = row[2]
            interference_time = row[3]
            air_high = row[4]
            star_lat = row[5]
            end_lat = row[6]
            start_lon = row[7]
            end_lon = row[8]
            # print(air_addr,interference_time,air_high,star_lat,end_lat,start_lon,end_lon)
            if air_addr == airport:
                self.interference_data_lit.append(
                    [air_addr, interference_time, air_high, star_lat, end_lat, start_lon, end_lon])
        # print(self.interference_data_lit)
        return self.interference_data_lit

    # 绘制干扰轨迹线和中垂线，并获取中垂线交点坐标
    def draw_line(self):

        for interference_data in self.interference_data_lit:
            # 绘制原始归纳绕轨迹线
            self.fig.add_trace(go.Scattermapbox(
                mode="lines+markers",
                lon=[interference_data[5], interference_data[6]],
                lat=[interference_data[3], interference_data[4]],
                marker={'color': 'red', 'size': 5},
                line={'color': 'red', 'width': 1},
            ))
            # 绘制中垂线
            # 获取中垂线计算结果
            lat_list, lon_list = self.calculate_point(interference_data[3], interference_data[4], interference_data[5],
                                                      interference_data[6], self.leng_km)
            self.fig.add_trace(go.Scattermapbox(
                mode="lines",
                lon=lon_list,
                lat=lat_list,
                line={'color': 'blue', 'width': 1},
            ))

    # 计算中垂直点
    def calculate_point(self, lat1, lat2, lon1, lon2, length_km):

        """
        平面地图中计算两点连线的中垂线

        参数:
            lat1, lon1: 起点坐标（纬度, 经度）
            lat2, lon2: 终点坐标（纬度, 经度）
            length_km: 中垂线长度（公里）

        返回:
            (bisector_lats, bisector_lons): 中垂线端点坐标
        """

        # 计算中点（严格保持纬度在前）
        mid_lat = (lat1 + lat2) / 2
        mid_lon = (lon1 + lon2) / 2

        # 计算方向向量（dx对应经度-x轴，dy对应纬度-y轴）
        dx = lon2 - lon1  # x轴分量（经度差）
        dy = lat2 - lat1  # y轴分量（纬度差）

        # 计算垂直向量（逆时针旋转90度）
        perp_dx = -dy  # 垂直向量的x分量
        perp_dy = dx  # 垂直向量的y分量

        # 归一化
        norm = np.sqrt(perp_dx ** 2 + perp_dy ** 2)
        if norm > 0:
            perp_dx /= norm
            perp_dy /= norm

        # 将公里数转换为经纬度差值（考虑纬度缩放）
        km_per_deg_lat = 111.0  # 纬度方向1度≈111km
        km_per_deg_lon = 111.0 * np.cos(np.radians(mid_lat))  # 经度方向1度≈111*cos(lat)km

        # 计算延伸长度（纬度/经度方向分别缩放）
        extend_lat = (length_km / km_per_deg_lat) * perp_dy
        extend_lon = (length_km / km_per_deg_lon) * perp_dx

        # 生成中垂线端点（严格保持纬度在前）
        bisector_lats = [
            round(mid_lat + extend_lat, 6),
            round(mid_lat - extend_lat, 6)
        ]
        bisector_lons = [
            round(mid_lon + extend_lon, 6),
            round(mid_lon - extend_lon, 6)
        ]
        return bisector_lats, bisector_lons

    # 计算两条中垂线的交点
    def calculate_intersection_point(self, line1, line2):

        """
        计算两条中垂线的精确交点
        Args:
            line1: 第一条中垂线的起点和终点 ((lat1, lon1), (lat2, lon2))
            line2: 第二条中垂线的起点和终点 ((lat3, lon3), (lat4, lon4))
        Returns:
            (lat, lon): 交点坐标，若无交点返回None
        """

        # 转换成计算数据
        (x1, y1), (x2, y2) = (line1[0][1], line1[0][0]), (line1[1][1], line1[1][0])
        (x3, y3), (x4, y4) = (line2[0][1], line2[0][0]), (line2[1][1], line2[1][0])

        # 计算两条线的方向向量
        dx1, dy1 = x2 - x1, y2 - y1  # 第一条线的方向向量
        dx2, dy2 = x4 - x3, y4 - y3  # 第二条线的方向向量

        # 计算行列式判断是否平行
        det = dx1 * dy2 - dx2 * dy1
        if abs(det) < 1e-2:
            return None

        # 计算交点参数
        t1 = ((x3 - x1) * dy2 - (y3 - y1) * dx2) / det
        t2 = ((x3 - x1) * dy1 - (y3 - y1) * dx1) / det

        # 严格判断交点是否在两条线段上
        if 0 <= t1 <= 1 and 0 <= t2 <= 1:
            return (y1 + t1 * dy1, x1 + t1 * dx1)  # 转回(lat,lon)
        return None


    # 计算两两中垂线的交点
    def calculate_intersection_all_point(self, bisectors):
        """
        计算所有中垂线两两之间的交点
        Args:
            bisectors: 中垂线列表，每条中垂线格式为((起点lat,起点lon), (终点lat,终点lon))
        Returns:
            list: 所有交点的(lat,lon)坐标列表，已去重
        """

        intersections = []
        seen = set()  # 用于去重的集合

        # 遍历所有中垂线两两组合
        for line1, line2 in combinations(bisectors, 2):
            # 计算两条中垂线的交点
            pt = self.calculate_intersection_point(line1, line2)

            if pt is not None and not any(np.isnan(pt)):  # 有效交点且非NONE
                # 对坐标保留6位小数并去重
                rounded_pt = (round(pt[0], 6), round(pt[1], 6))
                if rounded_pt not in seen:
                    seen.add(rounded_pt)
                    intersections.append(pt)
        return intersections


if __name__ == '__main__':
    hg = HeatmapGenerator('济南遥墙机场')
    # hg.read_data()
    hg.heatmap_generator()
    # hg.calculate_point(36.31411,36.27806,120.359,120.37,5)
    # hg.draw_line()
