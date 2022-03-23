'''
@Author：洪建
@Date：2022/3/16 11:06
'''

'''
气泡提示示例
'''

'''
@Author：洪建
@Date：2022/3/16 10:58
'''
import sys

from PyQt5.QtGui import  QFont
from PyQt5.QtWidgets import QWidget, QApplication, QToolTip

'''
设置气泡提示示例
'''


class Tips(QWidget):

    def __init__(self, parent=None):
        super(Tips, self).__init__(parent)
        self.initUI()

    # 初始化窗口
    def initUI(self):
        # self.bt1 = QPushButton(self)
        # self.bt1.setText('气泡提示')
        QToolTip.setFont(QFont('SansSerif', 10))
        self.setToolTip('这是一个<b>气泡提示</b>')
        self.setGeometry(200, 300, 400, 400)
        self.setWindowTitle('气泡提示demo')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Tips()
    win.show()
    sys.exit(app.exec_())
