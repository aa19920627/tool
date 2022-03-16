'''
@Author：洪建
@Date：2022/3/15 15:57
'''
import sys

from PyQt5.QtWidgets import QMainWindow, QApplication

from Pyqt5_demo.layout_demo.packaging_resources.MainWin02 import Ui_Form


class MyMainWindow(QMainWindow,Ui_Form):

    def __init__(self,parent=None):

        super(MyMainWindow, self).__init__(parent)
        self.setupUi(self)

if __name__ == '__main__':

    app = QApplication(sys.argv)
    win = MyMainWindow()
    win.show()
    sys.exit(app.exec_())