'''
@Author：洪建
@Date：2022/3/28 17:16
'''
import sys

from PyQt5.QtWidgets import QMainWindow, QAction, QTextEdit, QStatusBar, QApplication

'''
QStatusBar（状态栏）示例
'''


class QStatusBar_Demo1(QMainWindow):
    def __init__(self, parent=None):
        super(QStatusBar_Demo1, self).__init__(parent)
        bar = self.menuBar()
        file = bar.addMenu("File")
        file.addAction("show")
        file.triggered[QAction].connect(self.processTrigger)
        self.setCentralWidget(QTextEdit())
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)

    def processTrigger(self, action):
        if (action.text() == "show"):
            self.statusBar.showMessage(action.text() + "菜单选项被点击于", 5000)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = QStatusBar_Demo1()
    win.show()
    sys.exit(app.exec_())
