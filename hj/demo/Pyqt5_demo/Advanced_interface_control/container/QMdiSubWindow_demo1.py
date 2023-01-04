'''
@Author：洪建
@Date：2022/3/31 14:56
'''
import sys

from PyQt5.QtWidgets import QMainWindow, QMdiArea, QAction, QMdiSubWindow, QTextEdit, QApplication

'''
多文档界面示例
'''


class MainWindow(QMainWindow):
    count = 0
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.mdi = QMdiArea()
        self.setCentralWidget(self.mdi)
        bar = self.menuBar()
        file = bar.addMenu("File")
        file.addAction("New")
        file.addAction("cascade")
        file.addAction("Tiled")
        file.triggered[QAction].connect(self.windowaction)

    def windowaction(self, q):
        print("triggered")

        if q.text() == "New":
            MainWindow.count = MainWindow.count + 1
            sub = QMdiSubWindow()
            sub.setWidget(QTextEdit())
            sub.setWindowTitle("subwindow" + str(MainWindow.count))
            self.mdi.addSubWindow(sub)
            sub.show()
        if q.text() == "cascade":
            self.mdi.cascadeSubWindows()
        if q.text() == "Tiled":
            self.mdi.tileSubWindows()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
