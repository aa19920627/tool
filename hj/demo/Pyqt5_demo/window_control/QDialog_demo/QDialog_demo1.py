'''
@Author：洪建
@Date：2022/3/24 16:01
'''
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QPushButton, QDialog, QApplication

'''
QDialog（对话框）示例
'''


class Dialog_Demo1(QWidget):
    def __init__(self, parent=None):
        super(Dialog_Demo1, self).__init__(parent)
        self.setWindowTitle("QDialog")
        self.resize(350, 300)

        self.btn = QPushButton(self)
        self.btn.setText("弹出对话框")
        self.btn.move(50, 50)
        self.btn.clicked.connect(self.showdialog)

    def showdialog(self):
        dialog = QDialog()
        btn = QPushButton("ok", dialog)
        btn.move(50, 50)
        dialog.setWindowTitle("Dialog")
        dialog.setWindowModality(Qt.ApplicationModal)
        dialog.exec_()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Dialog_Demo1()
    win.show()
    sys.exit(app.exec_())
