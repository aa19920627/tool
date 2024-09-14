# -*- coding: utf-8 -*-
"""
@Time ： 2024/9/6 14:52
@Auth ： 洪建
"""
import os
import sys


def get_path(relative_path):
    try:
        base_path=sys._MEIPASS #pyinstaller打包后的路径
    except AttributeError:
        base_path=os.path.abspath('.') #当前工作目录

    return os.path.normpath(os.path.join(base_path,relative_path))  #返回实际路径