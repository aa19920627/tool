'''
@Author：洪建
@Date：2022/3/25 15:10
'''
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QColor, QFont
from PyQt5.QtWidgets import QWidget, QApplication

'''
QPainter绘图控件示例
'''


class QPainter_Demo1(QWidget):
    def __init__(self, parent=None):
        super(QPainter_Demo1, self).__init__(parent)
        self.resize(300, 200)
        self.text = "QPainter示例"

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.begin(self)
        # 自定义绘制方法
        self.draw_text(event, painter)
        painter.end()

    def draw_text(self, event, qp):
        # 设置画笔颜色
        qp.setPen(QColor(168, 34, 3))
        # 设置字体
        qp.setFont(QFont('SimSun', 20))
        # 绘制文字
        qp.drawText(event.rect(), Qt.AlignCenter, self.text)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = QPainter_Demo1()
    win.show()
    sys.exit(app.exec_())
