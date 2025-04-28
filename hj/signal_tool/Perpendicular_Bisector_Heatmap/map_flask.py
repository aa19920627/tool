#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : 洪建
# @File : map_flask.py
# @Time : 2025/4/27 13:57
from flask import Flask, send_file, Response
import sqlite3
from io import BytesIO
from PIL import Image



# 初始化Flask应用
app = Flask(__name__)

# MBTiles文件路径
MBTILES_PATH = "D:\map\sichuan.mbtiles"


@app.after_request
def add_cors_headers(response):
    """添加CORS头，允许跨域请求（本地文件需要）"""
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


@app.route('/tiles/<int:z>/<int:x>/<int:y>.png')
def get_tile(z, x, y):
    """处理瓦片请求，返回PNG图片"""
    try:
        # TMS坐标转换：将XYZ格式的y转换为MBTiles的tile_row格式
        tms_y = (2 ** z - 1) - y

        # 连接SQLite数据库
        conn = sqlite3.connect(MBTILES_PATH)
        cur = conn.cursor()

        # 查询瓦片数据（注意列名需与MBTiles表结构匹配）
        cur.execute("""
            SELECT tile_data FROM tiles 
            WHERE zoom_level = ? AND tile_column = ? AND tile_row = ?
        """, (z, x, tms_y))

        tile_data = cur.fetchone()
        conn.close()

        if tile_data:
            # 返回真实瓦片（设置缓存头优化性能）
            return Response(
                tile_data[0],  # 二进制图片数据
                mimetype='image/png',
                headers={'Cache-Control': 'max-age=86400'}  # 缓存1天
            )

        # 如果瓦片不存在，返回透明PNG（避免Plotly报错）
        img = Image.new('RGBA', (256, 256), (0, 0, 0, 0))  # 创建透明图片
        img_byte_arr = BytesIO()
        img.save(img_byte_arr, format='PNG')
        return Response(
            img_byte_arr.getvalue(),
            mimetype='image/png'
        )

    except Exception as e:
        # 返回错误信息（调试用）
        return Response(
            str(e),
            status=500,
            mimetype='text/plain'
        )


if __name__ == '__main__':
    # 启动服务（默认端口5000）
    app.run(port=5000, debug=True)