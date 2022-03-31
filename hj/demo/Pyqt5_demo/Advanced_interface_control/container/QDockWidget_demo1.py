'''
@Author：洪建
@Date：2022/3/30 16:57
'''
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QHBoxLayout, QDockWidget, QListWidget, QTextEdit, QApplication

'''
QDockWidget示例
'''


class QDockWidget_Demo1(QMainWindow):
    def __init__(self, parent=None):
        super(QDockWidget_Demo1, self).__init__(parent)
        layout = QHBoxLayout()
        bar = self.menuBar()
        file = bar.addMenu("File")
        file.addAction("New")
        file.addAction("save")
        file.addAction("quit")
        self.items = QDockWidget("Dockable", self)
        self.list_widget = QListWidget()
        self.list_widget.addItem("item1")
        self.list_widget.addItem("item2")
        self.list_widget.addItem("item3")
        self.items.setWidget(self.list_widget)
        self.items.setFloating(False)
        self.setCentralWidget(QTextEdit())
        self.addDockWidget(Qt.RightDockWidgetArea, self.items)
        self.setLayout(layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = QDockWidget_Demo1()
    win.show()
    sys.exit(app.exec_())
