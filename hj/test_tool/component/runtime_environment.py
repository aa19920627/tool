# -*- coding: utf-8 -*-
"""
@Time ： 2024/6/20 14:11
@Auth ： 洪建
"""
import os
import sys

'''
定义运行环境路径
'''
class Frozen_Path:

    def __init__(self):
        pass

    def app_path(self):
        '''
        判断程序的运行环境，返回对应程序目录
        '''
        if hasattr(sys, "frozen"):  # 判断运行环境为pyinstaller打包后的环境

            return os.path.dirname(sys.executable)  # 使用pyinstaller打包后exe的运行环境

        return os.path.dirname(os.path.dirname(__file__))  # 使用打包前的目录，用于本地运行