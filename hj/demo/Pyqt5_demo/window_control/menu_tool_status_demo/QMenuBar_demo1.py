'''
@Author：洪建
@Date：2022/3/28 16:46
'''
import sys

from PyQt5.QtWidgets import QHBoxLayout, QMainWindow, QAction, QApplication

'''
QMenuBar(菜单栏)示例
'''


class QMenuBar_Demo1(QMainWindow):
    def __init__(self, parent=None):
        super(QMenuBar_Demo1, self).__init__(parent)
        layout = QHBoxLayout(self)
        bar = self.menuBar()
        file = bar.addMenu("File")
        file.addAction("New")
        save = QAction("Save", self)
        save.setShortcut("Ctrl+S")
        file.addAction(save)
        edit = file.addMenu("Edit")
        edit.addAction("Copy")
        edit.addAction("paste")
        quit = QAction("Quit", self)
        file.addAction(quit)
        file.triggered[QAction].connect(self.processtrigger)

    def processtrigger(self, action):
        print(action.text() + " is triggered")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = QMenuBar_Demo1()
    win.show()
    sys.exit(app.exec_())
