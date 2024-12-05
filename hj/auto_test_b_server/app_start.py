# -*- coding: utf-8 -*-
"""
@Time ： 2024/1/22 16:35
@Auth ： 洪建
"""
import ctypes
import os
import sys

from PyQt5 import QtWidgets

from main.application_program_interface import MainWindow

# 获取当前脚本所在目录
script_dir = os.path.dirname(os.path.realpath(__file__))

# 添加项目根目录到 sys.path
sys.path.append(script_dir)

ctypes.windll.shcore.SetProcessDpiAwareness(1)  # 设置高 DPI 缩放策略
app = QtWidgets.QApplication([])
window = MainWindow()
window.show()
app.exec_()