'''
@Author：洪建
@Date：2022/3/24 16:17
'''
import sys

from PyQt5.QtWidgets import QWidget, QFormLayout, QPushButton, QLineEdit, QInputDialog, QApplication

'''
Inputdialog示例
'''


class Inputdialog_Demo1(QWidget):
    def __init__(self, parent=None):
        super(Inputdialog_Demo1, self).__init__(parent)
        layout = QFormLayout(self)
        self.btn = QPushButton("获得列表选项")
        self.btn.clicked.connect(self.getItem)
        self.line = QLineEdit()
        layout.addRow(self.btn, self.line)

        self.btn2 = QPushButton("获得字符串")
        self.btn2.clicked.connect(self.gettext)
        self.line2 = QLineEdit()
        layout.addRow(self.btn2, self.line2)

        self.btn3 = QPushButton("获得整数")
        self.btn3.clicked.connect(self.getInt)
        self.line3 = QLineEdit()
        layout.addRow(self.btn3, self.line3)

    def getItem(self):
        items = ("C", "C++", "Java", "Python")
        item, ok = QInputDialog.getItem(self, "select input dialog", "语言列表", items, 0, False)
        if ok and item:
            self.line.setText(item)

    def gettext(self):
        text, ok = QInputDialog.getText(self, 'Text Input Dialog', "输入姓名:")
        if ok:
            self.line2.setText(str(text))

    def getInt(self):
        num, ok = QInputDialog.getInt(self, "integer input dialog", "请输入数字")
        if ok:
            self.line3.setText(str(num))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Inputdialog_Demo1()
    win.show()
    sys.exit(app.exec_())
