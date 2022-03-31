'''
@Author：洪建
@Date：2022/3/25 15:46
'''
import math
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QWidget, QApplication

'''
QPainter绘制点
'''


class QPainter_Demo2(QWidget):
    def __init__(self, parent=None):
        super(QPainter_Demo2, self).__init__(parent)
        self.resize(300, 200)

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        self.draw_points(qp)
        qp.end()

    def draw_points(self, qp):
        qp.setPen(Qt.red)
        size = self.size()

        for i in range(1000):
            # 绘制正弦函数，周期[-100，100]
            x = 100 * (-1 + 2 * i / 1000) + size.width() / 2
            y = -50 * math.sin((x - size.width() / 2) * math.pi / 50) + size.height() / 2
            qp.drawPoint(x, y)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = QPainter_Demo2()
    win.show()
    sys.exit(app.exec_())
