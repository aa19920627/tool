'''
@Author：洪建
@Date：2022/3/16 10:58
'''
import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow

'''
设置图标示例
'''


class Icon(QMainWindow):

    def __init__(self, parent=None):
        super(Icon, self).__init__(parent)
        self.initUI()

    # 初始化窗口
    def initUI(self):
        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('程序图标')
        self.setWindowIcon(QIcon('./wireless.png'))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Icon()
    win.show()
    sys.exit(app.exec_())
