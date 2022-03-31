'''
@Author：洪建
@Date：2022/3/28 17:06
'''
import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QVBoxLayout, QMainWindow, QAction, QApplication

'''
QToolBar示例
'''


class QToolBar_Demo1(QMainWindow):
    def __init__(self, parent=None):
        super(QToolBar_Demo1, self).__init__(parent)
        self.resize(300, 200)

        layout = QVBoxLayout(self)
        tb = self.addToolBar("File")
        new = QAction(QIcon("./wireless.png"), "new", self)
        tb.addAction(new)
        open = QAction(QIcon("./wireless.png"), "open", self)
        tb.addAction(open)
        save = QAction(QIcon("./wireless.png"), "save", self)
        tb.addAction(save)
        tb.actionTriggered[QAction].connect(self.toolbtnpressed)

    def toolbtnpressed(self, action):
        print("pressed tool btton is ", action.text)

if __name__ == '__main__':

    app = QApplication(sys.argv)
    win = QToolBar_Demo1()
    win.show()
    sys.exit(app.exec_())