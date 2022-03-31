'''
@Author：洪建
@Date：2022/3/24 15:18
'''
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QSlider, QApplication

'''
QSlider滑动条示例
'''


class QSlider_Demo1(QWidget):
    def __init__(self, parent=None):
        super(QSlider_Demo1, self).__init__(parent)
        self.setWindowTitle("QSlider 例子")
        self.resize(300, 100)

        layout = QVBoxLayout(self)
        self.label1 = QLabel("Hello")
        self.label1.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label1)

        # 水平方向
        self.s1 = QSlider(Qt.Horizontal)
        # 设置最小值
        self.s1.setMinimum(10)
        # 设置最大值
        self.s1.setMaximum(50)
        # 步长
        self.s1.setSingleStep(3)
        # 设置当前值
        self.s1.setValue(20)
        # 刻度位置，在下方
        self.s1.setTickPosition(QSlider.TicksBelow)
        # 设置刻度间隔
        self.s1.setTickInterval(5)
        layout.addWidget(self.s1)

        # 连接信号槽
        self.s1.valueChanged.connect(self.valuechange)

    def valuechange(self):
        print("current slider value=%s" % self.s1.value())
        size = self.s1.value()
        self.label1.setFont(QFont("Arial", size))

if __name__ == '__main__':

    app = QApplication(sys.argv)
    win = QSlider_Demo1()
    win.show()
    sys.exit(app.exec_())
