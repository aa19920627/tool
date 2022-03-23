'''
@Author：洪建
@Date：2022/3/16 11:24
'''
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QPixmap
from PyQt5.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QApplication, QWidget, QDialog

'''
标签的使用方法示例
'''


class Lable_Demo(QDialog):

    def __init__(self, parent=None):
        super(Lable_Demo, self).__init__(parent)

        self.resize(400, 300)
        lable1 = QLabel(self)
        lable2 = QLabel(self)
        lable3 = QLabel(self)
        lable4 = QLabel(self)

        # 初始化标签控件
        lable1.setText('文本标签')
        lable1.setAutoFillBackground(True)
        palette = QPalette()
        palette.setColor(QPalette.Window, Qt.blue)
        lable1.setPalette(palette)
        lable1.setAlignment(Qt.AlignHCenter)

        lable2.setText("<a href='http://192.168.11.149'>访问广西一体化平台</a>")
        lable2.setAlignment(Qt.AlignRight)
        lable2.setToolTip('超链接标签')

        lable3.setAlignment(Qt.AlignCenter)
        lable3.setToolTip('图片标签')
        lable3.setPixmap(QPixmap("./wireless.png"))

        lable4.setText("<a href='http://192.168.11.149'>访问广西一体化平台</a>")
        lable4.setAlignment(Qt.AlignRight)
        lable4.setToolTip('超链接标签')

        # 在窗口布局中添加控件
        vbox = QVBoxLayout(self)
        vbox.addWidget(lable1)
        vbox.addWidget(lable2)
        vbox.addWidget(lable3)
        vbox.addWidget(lable4)

        # 允许lable1控件访问超链接
        lable2.setOpenExternalLinks(False)
        lable4.setOpenExternalLinks(True)

        # 点击文本框绑定槽事件
        lable4.linkActivated.connect(self.link_clicked)
        lable2.linkActivated.connect(self.link_clicked)

        # 滑过文本框绑定槽事件
        # lable2.linkHovered.connect(self.link_hovered)

        # lable2.setTextInteractionFlags(Qt.TextSelectableByMouse)

        # self.setLayout(vbox)
        self.setWindowTitle('QLable例子')

    def link_clicked(self):
        print('当用鼠标点击lable4标签时，触发事件')

    def link_hovered(self):
        print("当用鼠标滑过label2标签时，触发事件")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Lable_Demo()
    win.show()
    sys.exit(app.exec_())
