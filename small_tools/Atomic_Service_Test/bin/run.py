# -*- encoding: utf-8 -*-
"""
@File    : conftest.py
@Date    : 2020/10/29 13:09
@Author  : 洪建
@Software: PyCharm

"""
import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication

from Atomic_Service_Test.src.main.create_tcp_server import Create_Tcp_Server
from Atomic_Service_Test.src.ui.signal_channel import Signal_Channel


class Inspection_Window(QMainWindow,Signal_Channel):

    def __init__(self,parent=None):

        super(Inspection_Window, self).__init__(parent)

        self.setupUi(self)



if __name__ == '__main__':

    app = QApplication(sys.argv)
    inspection_window = Inspection_Window()
    inspection_window.show()
    sys.exit(app.exec_())