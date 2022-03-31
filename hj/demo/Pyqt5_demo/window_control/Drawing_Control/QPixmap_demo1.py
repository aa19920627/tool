'''
@Author：洪建
@Date：2022/3/25 16:45
'''
import sys

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QApplication

'''
QPixmap(绘制图像)示例
'''


class QPixmap_Demo1(QWidget):
    def __init__(self, parent=None):
        super(QPixmap_Demo1, self).__init__(parent)
        self.le = QLabel(self)
        self.le.setPixmap(QPixmap("./wireless.png"))
        vbox = QVBoxLayout(self)
        vbox.addWidget(self.le)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = QPixmap_Demo1()
    win.show()
    sys.exit(app.exec_())