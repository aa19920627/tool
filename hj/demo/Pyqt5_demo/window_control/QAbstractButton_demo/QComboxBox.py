'''
@Author：洪建
@Date：2022/3/23 17:15
'''
import sys

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QApplication

'''
QComboBox下拉列表框，示例
'''


class QComboBox_Demo1(QWidget):

    def __init__(self, parent=None):
        super(QComboBox_Demo1, self).__init__(parent)
        self.setWindowTitle("ComBox 例子")
        self.resize(300, 90)
        layout = QVBoxLayout(self)
        self.lb1 = QLabel("")

        self.cb = QComboBox()
        self.cb.addItem("C")
        self.cb.addItem("C++")
        self.cb.addItems(["Java", "C#", "Python"])
        self.cb.currentIndexChanged.connect(self.selectionchange)
        layout.addWidget(self.cb)
        layout.addWidget(self.lb1)

    def selectionchange(self, i):
        self.lb1.setText(self.cb.currentText())
        print("Items in the list are:")
        print("Current index", i, "selection changed", self.cb.currentText())
        for count in range(self.cb.count()):
            print("item" + str(count) + "=" + self.cb.itemText(count))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = QComboBox_Demo1()
    win.show()
    sys.exit(app.exec_())
