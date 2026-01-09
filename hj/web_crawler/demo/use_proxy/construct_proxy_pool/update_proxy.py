#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : 洪建
# @File : update_proxy.py
# @Time : 2026/1/8 15:47

"""
更新代理池列表
"""
import json
import requests
from datetime import datetime


# 定义代理数据源API端点
# JSON_ENDPOINTS1: 第一个代理网站的数据接口，支持分页
JSON_ENDPOINTS1 = [
    {"url": "https://proxy-daily.com/api/serverside/proxies?draw=1&start=0&length=100"},
    {"url": "https://proxy-daily.com/api/serverside/proxies?draw=2&start=100&length=100"},
    {"url": "https://proxy-daily.com/api/serverside/proxies?draw=3&start=200&length=100"},
    {"url": "https://proxy-daily.com/api/serverside/proxies?draw=4&start=300&length=100"},
    {"url": "https://proxy-daily.com/api/serverside/proxies?draw=5&start=400&length=100"},
]

# JSON_ENDPOINTS2: 第二个代理网站的数据接口（全球和美国地区）
JSON_ENDPOINTS2 = [
    {"url": "https://cdn.jsdelivr.net/gh/proxifly/free-proxy-list@main/proxies/all/data.json"},
    {"url": "https://cdn.jsdelivr.net/gh/proxifly/free-proxy-list@main/proxies/countries/us/data.json"},
]

# 定义请求头，模拟浏览器访问
DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
}


'''从JSON_ENDPOINTS1获取代理数据'''
def fetchjsonendpoint1(ep):
    # 获取API URL
    url = ep["url"]
    print(f"[JSON1] 正在从 {url} 获取数据...")

    try:
        # 发送GET请求，设置超时时间为25秒
        resp = requests.get(url, timeout=25, headers=DEFAULT_HEADERS)
        resp.raise_for_status()  # 检查HTTP响应状态，非200会抛出异常
        data = resp.json()  # 解析JSON数据
    except Exception as e:
        print(f"[JSON1] 获取JSON端点数据时出错: {e}")
        return []  # 出错时返回空列表

    # 从返回的JSON中提取代理数据
    rows = data.get("data", []) or []  # 获取data字段，如果不存在则返回空列表
    proxies = []  # 存储解析后的代理信息

    for row in rows:
        ip = row.get("ip")
        port = row.get("port")
        # 确保ip和port都不为空
        if not ip or not port:
            continue

        # 整理代理信息
        proxies.append({
            "ip": ip,
            "port": port,
            "protocol": row.get("protocol"),  # 协议（HTTP/HTTPS/SOCKS）
            "country": row.get("country"),  # 国家
            "anonymity": row.get("anonymity"),  # 匿名级别
            "speed": row.get("speed"),  # 速度
        })

    print(f"[JSON1] 已获取 {len(proxies)} 个代理")
    return proxies


'''从JSON_ENDPOINTS2获取代理数据'''
def fetchjsonendpoint2(ep):
    url = ep["url"]
    print(f"[JSON2] 正在从 {url} 获取数据...")

    try:
        resp = requests.get(url, timeout=25, headers=DEFAULT_HEADERS)
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        print(f"[JSON2] 获取JSON端点数据时出错: {e}")
        return []

    # 第二个接口直接返回代理数组
    rows = data or []
    proxies = []

    for row in rows:
        ip = row.get("ip")
        port = row.get("port")
        if not ip or not port:
            continue

        # 提取地理位置信息
        geolocation = row.get("geolocation", {})
        proxies.append({
            "ip": ip,
            "port": port,
            "protocol": row.get("protocol"),
            "country": geolocation.get("country"),  # 从geolocation对象中获取国家
            "anonymity": row.get("anonymity"),
            "speed": row.get("speed", 100),  # 默认速度设为100
        })

    print(f"[JSON2] 已获取 {len(proxies)} 个代理")
    return proxies


'''主函数'''
def main():
    all_proxies = []  # 存储所有代理

    # 从第一个数据源获取代理
    for ep in JSON_ENDPOINTS1:
        try:
            all_proxies.extend(fetchjsonendpoint1(ep))
        except Exception as err:
            print(f"[警告] 获取JSON1端点 {ep} 失败: {err}")

    # 从第二个数据源获取代理
    for ep in JSON_ENDPOINTS2:
        try:
            all_proxies.extend(fetchjsonendpoint2(ep))
        except Exception as err:
            print(f"[警告] 获取JSON2端点 {ep} 失败: {err}")

    # 去重：基于IP、端口和协议的组合去重
    uniq = {}
    for p in all_proxies:
        key = (p["ip"], p["port"], p["protocol"])
        uniq[key] = p

    all_proxies = list(uniq.values())  # 获取去重后的代理列表

    # 构建最终输出的数据结构
    data = {
        "updated_at": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"),  # 更新时间（UTC）
        "count": len(all_proxies),  # 代理总数
        "data": all_proxies  # 代理数据
    }

    # 将数据写入JSON文件
    with open("proxies.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)  # ensure_ascii=False支持中文，indent=2美化格式

    print(f"[完成] 已将 {len(all_proxies)} 个代理保存到 proxies.json")


'''程序入口'''
if __name__ == "__main__":
    main()