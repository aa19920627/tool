# -*- encoding: utf-8 -*-
"""
@File    : write_log.py
@Date    : 2021/1/25 13:53
@Author  : 洪建
"""
import datetime
import os
import time

'''
调用日志记录，记录设备重启
'''

class Write_Log:

    def __init__(self):

        self.log_name = time.strftime("%Y%m%d", time.localtime())
        self.log_path = os.path.join(os.path.dirname(__file__), "../log/%s.log" %self.log_name)

    def write_log(self, mode):

        with open(self.log_path, "a+" ,encoding="utf-8") as f:

            f.write(mode + "\n")


