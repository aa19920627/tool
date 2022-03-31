'''
@Author：洪建
@Date：2022/3/24 15:04
'''
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QSpinBox, QApplication

'''
QSpinBox(计数器)，示例
'''


class QSpinBox_Demo1(QWidget):
    def __init__(self, parent=None):
        super(QSpinBox_Demo1, self).__init__(parent)
        self.setWindowTitle("SpinBox 例子")
        self.resize(300, 100)

        layout = QVBoxLayout(self)
        self.label1 = QLabel("current value:")
        self.label1.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label1)
        self.sp = QSpinBox()
        layout.addWidget(self.sp)
        self.sp.valueChanged.connect(self.valuechange)

    def valuechange(self):
        self.label1.setText("current value:" + str(self.sp.value()))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = QSpinBox_Demo1()
    win.show()
    sys.exit(app.exec_())
