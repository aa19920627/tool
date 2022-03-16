'''
@Author：洪建
@Date：2022/3/2 16:09
'''
import sys

from PyQt5.QtWidgets import QMainWindow, QApplication

from Pyqt5_demo.signal_slots.easy_demo.MainWinSignalSlog01 import Ui_Form


class MyMainWindow(QMainWindow,Ui_Form):

    def __init__(self,parent=None):

        super(MyMainWindow, self).__init__(parent)
        self.setupUi(self)


if __name__ == '__main__':

    app = QApplication(sys.argv)
    myWin = MyMainWindow()
    myWin.show()
    sys.exit(app.exec_())