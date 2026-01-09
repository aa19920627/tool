#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : 洪建
# @File : run.py.py
# @Time : 2026/1/9 11:50
import argparse

from web_crawler.build_proxy_pool.proxypool.scheduler import Scheduler

# 创建命令行参数解析器
parser = argparse.ArgumentParser(description='ProxyPool')
# 添加命令行参数
parser.add_argument('--processor', type=str, help='processor to run')  # # 添加一个名为'--processor'的可选参数，类型为字符串，用于指定要运行的处理器
# 解析命令行参数
args = parser.parse_args()  # 解析命令行参数并将结果存储在args对象中

# 主程序入口
if __name__ == '__main__':
    # 如果指定了processor参数，则只运行对应的处理器
    if args.processor:
        # 使用getattr函数动态获取Scheduler实例的方法并执行
        # 例如：如果args.processor='tester'，则调用Scheduler().run_tester()
        getattr(Scheduler(), f'run_{args.processor}')()
    # 如果未指定processor参数，则运行所有处理器
    else:
        Scheduler().run()  # 调用Scheduler的run()方法，运行默认的所有任务
