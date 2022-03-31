'''
@Author：洪建
@Date：2022/3/29 16:43
'''
import sys

from PyQt5.QtCore import QStringListModel
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QListView, QMessageBox, QApplication

'''
QListView示例
'''


class QListView_Demo1(QWidget):
    def __init__(self, parent=None):
        super(QListView_Demo1, self).__init__(parent)
        self.resize(300, 270)
        layout = QVBoxLayout(self)

        list_view = QListView()
        sim = QStringListModel()
        self.qlist = ["Item 1", "Item 2", "Item 3", "Item 4"]
        sim.setStringList(self.qlist)
        list_view.setModel(sim)
        list_view.clicked.connect(self.clicked)
        layout.addWidget(list_view)

    def clicked(self, qModelIndex):
        QMessageBox.information(self, "ListWidget", "你选择了：" + self.qlist[qModelIndex.row()])


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = QListView_Demo1()
    win.show()
    sys.exit(app.exec_())
