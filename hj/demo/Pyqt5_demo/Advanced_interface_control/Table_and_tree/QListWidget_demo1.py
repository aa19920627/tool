'''
@Author：洪建
@Date：2022/3/29 17:22
'''
import sys

from PyQt5.QtWidgets import QListWidget, QWidget, QMessageBox, QApplication

'''
QListWidget示例
'''


class QListWidget_Demo1(QWidget):
    def __init__(self, parent=None):
        super(QListWidget_Demo1, self).__init__(parent)
        list_wdiget = QListWidget(self)
        list_wdiget.resize(300, 120)
        list_wdiget.addItem("Item 1")
        list_wdiget.addItem("Item 2")
        list_wdiget.addItem("Item 3")
        list_wdiget.addItem("Item 4")
        list_wdiget.itemClicked.connect(self.clicked)

    def clicked(self, item):
        QMessageBox.information(self, "ListWidget", "你选择了：" + item.text())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = QListWidget_Demo1()
    win.show()
    sys.exit(app.exec_())
