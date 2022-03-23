'''
@Author：洪建
@Date：2022/3/22 14:46
'''
import sys

from PyQt5.QtWidgets import QWidget, QHBoxLayout, QRadioButton, QApplication

'''
QRadioButton示例
'''


class QRadioButton_Demo1(QWidget):

    def __init__(self, parent=None):

        super(QRadioButton_Demo1, self).__init__(parent)

        layout = QHBoxLayout(self)
        self.btn1 = QRadioButton('button1')
        self.btn1.setChecked(True)
        self.btn1.toggled.connect(lambda: self.btnstate(self.btn1))
        layout.addWidget(self.btn1)

        self.btn2 = QRadioButton("button2")
        self.btn2.toggled.connect(lambda: self.btnstate(self.btn2))
        layout.addWidget(self.btn2)

        self.setWindowTitle('RadioButton demo')

    def btnstate(self, btn):

        if btn.text() == "button1":
            if btn.isChecked() == True:
                print(btn.text() + "is selected")
            else:
                print(btn.text() + "is deselected")

        if btn.text() == "button2":
            if btn.isChecked() == True:
                print(btn.text() + "is selected")
            else:
                print(btn.text() + "is deselected")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = QRadioButton_Demo1()
    win.show()
    sys.exit(app.exec_())
