'''
@Author：洪建
@Date：2022/3/1 10:22
'''

import sys
from PyQt5.QtWidgets import QMainWindow, QApplication
from Pyqt5_demo.layout_demo.layout.FirstMainWindow import Ui_MainWindow

class MyMainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)
        self.setupUi(self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = MyMainWindow()
    myWin.show()
    sys.exit(app.exec_())
