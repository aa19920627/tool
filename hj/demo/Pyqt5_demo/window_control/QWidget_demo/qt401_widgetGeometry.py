'''
@Author：洪建
@Date：2022/3/16 10:11
'''
import sys

from PyQt5.QtWidgets import QMainWindow, QPushButton, QApplication

'''
QWdiget使用示例
'''


class QWdiget_Demo(QMainWindow):

    def __init__(self, parent=None):
        super(QWdiget_Demo, self).__init__(parent)
        self.setWindowTitle('QWdiget使用示例')
        self.bt1 = QPushButton(self)
        self.bt1.setText('Button')
        self.bt1.move(20, 30)
        self.resize(400, 300)
        self.move(400, 400)

        print("QWdiget:")
        print("w.x()=%d" % self.x())
        print("w.y()=%d" % self.y())
        print("w.width()=%d" % self.width())
        print("w.height()=%d" % self.height())
        print("QWidget.geometry")
        print("widget.geometry().x()=%d" % self.geometry().x())
        print("widget.geometry().y()=%d" % self.geometry().y())
        print("widget.geometry().width()=%d" % self.geometry().width())
        print("widget.geometry().height()=%d" % self.geometry().height())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = QWdiget_Demo()
    win.show()
    sys.exit(app.exec_())
