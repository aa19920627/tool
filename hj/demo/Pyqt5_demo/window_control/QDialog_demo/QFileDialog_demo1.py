'''
@Author：洪建
@Date：2022/3/25 14:50
'''
import sys

from PyQt5.QtCore import QDir
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QTextEdit, QFileDialog, QApplication

'''
QFileDialog（打开和保存文件的标准对话框）示例
'''


class QFileDialog_Demo1(QWidget):
    def __init__(self, parent=None):
        super(QFileDialog_Demo1, self).__init__(parent)
        layout = QVBoxLayout(self)
        self.btn = QPushButton("加载图片")
        self.btn.clicked.connect(self.getfile)
        layout.addWidget(self.btn)
        self.le = QLabel("")
        layout.addWidget(self.le)
        self.btn1 = QPushButton("加载文本文件")
        self.btn1.clicked.connect(self.getfiles)
        layout.addWidget(self.btn1)
        self.contents = QTextEdit()
        layout.addWidget(self.contents)

    def getfile(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open file", "d:\\", "Image files(*.jpg *.gif)")
        self.le.setPixmap(QPixmap(filename))

    def getfiles(self):
        dig = QFileDialog()
        dig.setFileMode(QFileDialog.AnyFile)
        dig.setFilter(QDir.Files)
        if dig.exec_():
            filenames = dig.selectedFiles()
            f = open(filenames[0], "r")
            with f:
                data = f.read()
                self.contents.setText(data)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = QFileDialog_Demo1()
    win.show()
    sys.exit(app.exec_())
