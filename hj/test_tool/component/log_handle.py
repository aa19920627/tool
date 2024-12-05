# -*- coding: utf-8 -*-
"""
@Time ： 2024/11/20 13:52
@Auth ： 洪建
"""
import logging
import os
import sys
from logging.handlers import TimedRotatingFileHandler

from component.runtime_environment import Frozen_Path


class Logger:
    def __init__(self, log_dir="b_server_test", log_file="run.log", log_level=logging.DEBUG):
        """
        初始化日志类

        :param log_dir: 日志存储目录
        :param log_file: 日志文件名
        :param log_level: 日志级别（默认为 DEBUG）
        """
        self.log_dir = log_dir
        self.log_file = log_file
        self.log_level = log_level

        # # 确保日志目录存在
        # if not os.path.exists(self.log_dir):
        #     os.makedirs(self.log_dir)

        # 日志文件完整路径
        self.log_path = Frozen_Path().app_path() + '\log'+'/'+self.log_dir+'/'+self.log_file

        # 配置日志记录
        self._setup_logger()

        # 设置异常捕获
        sys.excepthook = self._handle_exception

    def _setup_logger(self):
        """
        设置日志记录器
        """
        # 创建日志记录器
        self.logger = logging.getLogger()
        self.logger.setLevel(self.log_level)

        # 创建处理器（写入文件）
        handler = TimedRotatingFileHandler(self.log_path, when="midnight", interval=1, backupCount=7)
        handler.setLevel(self.log_level)

        # 设置日志格式
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)

        # 添加处理器到日志记录器
        self.logger.addHandler(handler)

    def log(self, message, level=logging.INFO):
        """
        记录日志

        :param message: 日志消息
        :param level: 日志级别
        """
        if level == logging.DEBUG:
            self.logger.debug(message)
        elif level == logging.INFO:
            self.logger.info(message)
        elif level == logging.WARNING:
            self.logger.warning(message)
        elif level == logging.ERROR:
            self.logger.error(message)
        elif level == logging.CRITICAL:
            self.logger.critical(message)

    def _handle_exception(self, exc_type, exc_value, exc_tb):
        """
        处理未捕获的异常并记录日志

        :param exc_type: 异常类型
        :param exc_value: 异常值
        :param exc_tb: 异常的追踪信息
        """
        # 格式化异常信息
        exception_msg = f"未处理的异常:\n{exc_type.__name__}: {exc_value}\n"
        exception_msg += ''.join(logging.formatException((exc_type, exc_value, exc_tb)))

        # 记录到日志
        self.logger.critical(exception_msg)

        # 如果需要将异常信息输出到控制台
        print(exception_msg)

    def get_logger(self):
        """
        返回日志记录器实例
        """
        return self.logger
