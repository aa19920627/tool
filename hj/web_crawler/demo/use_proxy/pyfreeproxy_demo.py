#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : 洪建
# @File : pyfreeproxy_demo.py
# @Time : 2026/1/8 15:47
import json
import random

from freeproxy.freeproxy import ProxiedSessionClient
from tqdm import tqdm
from freeproxy.modules import ProxyInfo, BuildProxiedSession, printtable, colorize, ProxiedSessionBuilder

"""pyfreeproxy免费代理池的使用练习"""


# """抓取、处理、存储"""
# '''配置'''
# SOURCES = ["ProxiflyProxiedSession", "QiyunipProxiedSession", "ProxylistProxiedSession"]
# TITLES = ["Source", "Retrieved Example", "HTTP", "HTTPS", "SOCKS4", "SOCKS5", "Chinese IP", "Elite", "Total"]
#
# '''抓取'''
# def scrape(src: str) -> list[ProxyInfo]:
#     try:
#         sess = BuildProxiedSession({"max_pages": 1, "type": src, "disable_print": False})
#         return sess.refreshproxies()
#     except Exception as e:
#         return []
#
#
# '''状态'''
# def stats(proxies: list[ProxyInfo]) -> dict:
#     return {
#         "http": sum(p.protocol.lower() == "http" for p in proxies),
#         "https": sum(p.protocol.lower() == "https" for p in proxies),
#         "socks4": sum(p.protocol.lower() == "socks4" for p in proxies),
#         "socks5": sum(p.protocol.lower() == "socks5" for p in proxies),
#         "cn": sum(bool(p.in_chinese_mainland) for p in proxies),
#         "elite": sum(p.anonymity.lower() == "elite" for p in proxies),
#         "total": len(proxies),
#         "ex": (random.choice(proxies).proxy if proxies else "NULL")
#     }
#
#
# '''row'''
# def row(src: str, s: dict) -> list:
#     ex = colorize(s["ex"], "green") if s["total"] else "NULL"
#     return [
#         src.removesuffix("ProxiedSession"),
#         ex,
#         colorize(s["http"], "number"),
#         colorize(s["https"], "number"),
#         colorize(s["socks4"], "number"),
#         colorize(s["socks5"], "number"),
#         colorize(s["cn"], "number"),
#         colorize(s["elite"], "number"),
#         colorize(s["total"], "number"),
#     ]
#
#
# '''main'''
# def main():
#     free_proxies, items = {}, []
#     for src in tqdm(SOURCES):
#         proxies = scrape(src)
#         items.append(row(src, stats(proxies)))
#         free_proxies[src] = [p.todict() for p in proxies]
#     print("The proxy distribution for each source you specified is as follows:")
#     printtable(titles=TITLES, items=items, terminal_right_space_len=1)
#     json.dump(free_proxies, open("free_proxies.json", "w"), indent=2)

# # 获取支持的代理来源列表
# print(ProxiedSessionBuilder.REGISTERED_MODULES.keys())

"""自动维护的代理池"""

proxy_sources = ["QiyunipProxiedSession"]
init_proxied_session_cfg = {"filter_rule":{"country_code":["CN"]}}
client = ProxiedSessionClient(
    proxy_sources=proxy_sources,init_proxied_session_cfg=init_proxied_session_cfg,
)
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"
}
resp = client.get("https://www.baidu.com",headers=headers)
print(resp.text)

# if __name__ == '__main__':
#     main()
