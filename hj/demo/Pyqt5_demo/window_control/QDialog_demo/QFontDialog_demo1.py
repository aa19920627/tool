'''
@Author：洪建
@Date：2022/3/24 16:30
'''
import sys

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QFontDialog, QApplication

'''
QFontDialog(字体选择框)示例
'''


class QFontDialog_Demo1(QWidget):
    def __init__(self, parent=None):
        super(QFontDialog_Demo1, self).__init__(parent)
        layout = QVBoxLayout(self)
        self.fontbutton = QPushButton("choose font")
        self.fontbutton.clicked.connect(self.getfont)
        layout.addWidget(self.fontbutton)
        self.fonline = QLabel("测试字体")
        layout.addWidget(self.fonline)

    def getfont(self):
        font, ok = QFontDialog.getFont()
        if ok:
            self.fonline.setFont(font)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = QFontDialog_Demo1()
    win.show()
    sys.exit(app.exec_())
