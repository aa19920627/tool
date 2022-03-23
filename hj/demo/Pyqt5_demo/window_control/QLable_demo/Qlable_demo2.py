'''
@Author：洪建
@Date：2022/3/17 14:59
'''
import sys

from PyQt5.QtWidgets import QMainWindow, QLabel, QLineEdit, QPushButton, QGridLayout, QApplication, QDialog

from Pyqt5_demo.window_control.QLable_demo.untitled import Ui_Form

'''
QLable快捷键示例
'''


class QLable_Demo2(QDialog,Ui_Form):

    def __init__(self, parent=None):
        super(QLable_Demo2, self).__init__(parent)
        self.setupUi(self)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = QLable_Demo2()
    win.show()
    sys.exit(app.exec_())
