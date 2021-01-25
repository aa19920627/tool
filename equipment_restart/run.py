# -*- encoding: utf-8 -*-
"""
@File    : run.py.py
@Date    : 2021/1/25 17:05
@Author  : 洪建
"""
import sys

from PyQt5.QtWidgets import QApplication

from equipment_restart.main.open_window import Monitor_Window

app = QApplication(sys.argv)
window = Monitor_Window()
window.show()
sys.exit(app.exec_())