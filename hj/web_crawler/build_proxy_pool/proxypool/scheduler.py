#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : 洪建
# @File : scheduler.py
# @Time : 2026/1/9 13:30

import time
from loguru import logger
import multiprocessing
from aiohttp.helpers import IS_WINDOWS

from web_crawler.build_proxy_pool.proxypool.setting import *

# Windows系统下多进程的特殊处理
if IS_WINDOWS:
    multiprocessing.freeze_support()  # 修复Windows下多进程打包时可能出现的问题

# 定义全局变量，用于存储三个进程的引用
tester_process, getter_process, server_process = None, None, None


class Scheduler():
    """
    调度器类，负责管理代理池的各个组件（测试器、获取器、服务器）的运行
    """

    def run_tester(self, cycle=CYCLE_TESTER):
        """
        运行测试器，定期测试代理的可用性
        参数:
            cycle: 测试周期（秒），从配置文件中读取默认值
        """
        if not ENABLE_TESTER:  # 检查测试器是否启用
            logger.info('测试器未启用，退出')
            return
        tester = Tester()  # 创建测试器实例
        loop = 0
        while True:  # 无限循环，定期执行测试
            logger.debug(f'测试器第{loop}轮开始...')
            tester.run()  # 执行测试
            loop += 1
            time.sleep(cycle)

    def run_getter(self, cycle=CYCLE_GETTER):
        """
        运行获取器，定期从源网站获取新的代理
        参数:
            cycle: 获取周期（秒），从配置文件中读取默认值
        """
        if not ENABLE_GETTER:  # 检查获取器是否启用
            logger.info('获取器未启用，退出')
            return
        getter = Getter()  # 创建获取器实例
        loop = 0
        while True:  # 无限循环，定期执行获取
            logger.debug(f'获取器第 {loop} 轮开始...')
            getter.run()  # 执行获取
            loop += 1
            time.sleep(cycle)  # 等待指定的周期

    def run_server(self):
        """
        运行API服务器，提供代理获取的HTTP接口
        """
        if not ENABLE_SERVER:  # 检查服务器是否启用
            logger.info('服务器未启用，退出')
            return

        # 生产环境:使用高性能服务器
        if IS_PROD:
            # 使用gevent作为生产服务器
            if APP_PROD_METHOD == APP_PROD_METHOD_GEVENT:
                try:
                    from gevent.pywsgi import WSGIServer
                except ImportError as e:
                    logger.exception(e)  # 记录导入错误
                else:
                    http_server = WSGIServer((API_HOST, API_PORT), app)  # 创建gevent服务器
                    http_server.serve_forever()  # 启动服务器

            # 使用tornado作为生产服务器
            elif APP_PROD_METHOD == APP_PROD_METHOD_TORNADO:
                try:
                    from tornado.wsgi import WSGIContainer
                    from tornado.httpserver import HTTPServer
                    from tornado.ioloop import IOLoop
                except ImportError as e:
                    logger.exception(e)  # 记录导入错误
                else:
                    http_server = HTTPServer(WSGIContainer(app))  # 创建tornado服务器
                    http_server.listen(API_PORT)
                    IOLoop.current().start()  # 启动事件循环

            # 使用meinheld作为生产服务器
            elif APP_PROD_METHOD == APP_PROD_METHOD_MEINHELD:
                try:
                    import meinheld
                except ImportError as e:
                    logger.exception(e)  # 记录导入错误
                else:
                    meinheld.listen((API_HOST, API_PORT))  # 配置监听地址和端口
                    meinheld.run(app)
            # 不支持的服务器类型
            else:
                logger.error('不支持的APP_PROD_METHOD')
                return
        # 开发环境：使用FLASK自带的服务器
        else:
            app.run(host=API_HOST, port=API_PORT, threaded=API_THREADED, use_reloader=False)  # 启动Flask开发服务器

    def run(self):
        """
        主调度方法，启动所有启用的组件（测试器、获取器、服务器）作为独立的进程
        """
        global tester_process, getter_process, server_process
        try:
            logger.info('正在启动代理池...')

            # 启动测试器进程
            if ENABLE_TESTER:
                tester_process = multiprocessing.Process(target=self.run_tester)  # 创建测试器进程
                logger.info(f'启动测试器，进程ID {tester_process.pid}...')
                tester_process.start()  # 启动进程

            # 启动获取器进程
            if ENABLE_GETTER:
                getter_process = multiprocessing.Process(
                    target=self.run_getter)  # 创建获取器进程
                logger.info(f'启动获取器，进程ID {getter_process.pid}...')
                getter_process.start()  # 启动进程

            # 启动服务器进程
            if ENABLE_SERVER:
                server_process = multiprocessing.Process(
                    target=self.run_server)  # 创建服务器进程
                logger.info(f'启动服务器，进程ID {server_process.pid}...')
                server_process.start()  # 启动进程

            # 等待所有进程结束（正常情况下不会结束）
            tester_process and tester_process.join()  # 等待测试器进程结束
            getter_process and getter_process.join()  # 等待获取器进程结束
            server_process and server_process.join()  # 等待服务器进程结束

        # 捕获键盘中断（Ctrl+C），优雅地关闭程序
        except KeyboardInterrupt:
            logger.info('收到键盘中断信号')
            # 终止所有进程
            tester_process and tester_process.terminate()
            getter_process and getter_process.terminate()
            server_process and server_process.terminate()

        # 最终处理，确保进程被正确清理
        finally:
            # 必须先调用join方法再调用is_alive检查
            tester_process and tester_process.join()
            getter_process and getter_process.join()
            server_process and server_process.join()

            # 打印进程状态
            logger.info(
                f'测试器状态: {"存活" if tester_process and tester_process.is_alive() else "已终止"}')
            logger.info(
                f'获取器状态: {"存活" if getter_process and getter_process.is_alive() else "已终止"}')
            logger.info(
                f'服务器状态: {"存活" if server_process and server_process.is_alive() else "已终止"}')

            logger.info('代理池已终止')


if __name__ == '__main__':
    scheduler = Scheduler()  # 创建调度器实例
    scheduler.run()  # 启动调度器
