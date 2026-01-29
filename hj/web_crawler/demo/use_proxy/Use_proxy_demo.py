import asyncio
from asyncio import timeout
from concurrent.futures.thread import ThreadPoolExecutor

import aiohttp
import httpx
import requests

# 解决方案A（首选）：显式设置事件循环策略并使用现代运行方式
import sys

import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

_executor = ThreadPoolExecutor(max_workers=10)

# async def get_proxyip():
#     async with aiohttp.ClientSession() as session:
#         async with session.get(url='https://www.baidu.com/', proxy='http://36.25.243.9:20472') as response:
#             print(await response.text())
# #
proxies = {'http': 'http://13.232.2.142:8082',
           'https': 'http://89.43.31.134:3128'}
resp = requests.get('https://www.baidu.com/', proxies=proxies, timeout=20, verify=False)
# resp = requests.get('https://www.baidu.com/', proxies=proxies)
print(resp.text)
#
# async def get_proxyip():
#     # 注意：httpx 中参数名为 proxy，而不是 proxies
#     loop = asyncio.get_event_loop()
#
#     def sync_fetch():
#         proxies = {'http': 'http://192.150.179.128:3128/',
#                    'https':'http://180.97.254.82:30049/'}
#         return requests.get('https://httpbin.org/ip', proxies=proxies, timeout=10)
#
#     try:
#         # 异步等待同步操作完成
#         response = await loop.run_in_executor(_executor, sync_fetch)
#         print(response.status_code)
#         # 后续逻辑
#         if response.status_code == 200:
#             print(response.text)
#     except Exception as e:
#         print(e)


# if __name__ == '__main__':
# asyncio.run(get_proxyip())


# curl -x http://47.76.254.247:443 https://httpbin.org/ip