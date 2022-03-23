'''
@Author：洪建
@Date：2022/3/21 14:52
'''
import sys

from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QApplication

'''
QPushButton的使用示例
'''


class QPushButton_Demo1(QWidget):

    def __init__(self, parent=None):
        super(QPushButton_Demo1, self).__init__(parent)

        layout = QVBoxLayout(self)

        self.btn1 = QPushButton('Button1')
        self.btn1.setCheckable(True)
        self.btn1.toggle()
        self.btn1.clicked.connect(lambda:self.whichbtn(self.btn1))
        self.btn1.clicked.connect(self.btnstate)
        layout.addWidget(self.btn1)

        self.btn2 = QPushButton('image')
        self.btn2.setIcon(QIcon(QPixmap("./wireless.png")))
        self.btn2.clicked.connect(lambda:self.whichbtn(self.btn2))
        layout.addWidget(self.btn2)

        self.btn3 = QPushButton("Disabled")
        self.btn3.setEnabled(False)
        layout.addWidget(self.btn3)

        self.btn4 = QPushButton("&Download")
        self.btn4.setDefault(True)
        self.btn4.clicked.connect(lambda:self.whichbtn(self.btn4))
        layout.addWidget(self.btn4)
        self.setWindowTitle("Button demo")

    def btnstate(self):
        if self.btn1.isChecked():
            print("button pressed")
        else:
            print("button released")

    def whichbtn(self, btn):
        print("clicked button is " + btn.text())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = QPushButton_Demo1()
    win.show()
    sys.exit(app.exec_())
