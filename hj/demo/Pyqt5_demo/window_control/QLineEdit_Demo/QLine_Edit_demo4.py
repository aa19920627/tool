'''
@Author：洪建
@Date：2022/3/21 13:32
'''
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIntValidator, QFont, QDoubleValidator
from PyQt5.QtWidgets import QWidget, QLineEdit, QFormLayout, QApplication

'''
QLine_Edit的综合运用示例
'''


class QLine_Edit_Demo(QWidget):

    def __init__(self, parent=None):
        super(QLine_Edit_Demo, self).__init__(parent)
        e1 = QLineEdit()
        e1.setValidator(QIntValidator())
        e1.setMaxLength(4)
        e1.setAlignment(Qt.AlignRight)
        e1.setFont(QFont("Arial", 20))

        e2 = QLineEdit()
        e2.setValidator(QDoubleValidator(0.99, 99.99, 2))

        flo = QFormLayout(self)
        flo.addRow('整数', e1)
        flo.addRow('小数', e2)

        e3 = QLineEdit()
        e3.setInputMask('+99_9999_999999')

        flo.addRow("Input Mask",e3)

        e4 = QLineEdit()
        e4.textChanged.connect(self.textchanged)

        flo.addRow("Text Changed",e4)

        e5 = QLineEdit()
        e5.setEchoMode(QLineEdit.Password)
        flo.addRow("Password",e5)

        e6 = QLineEdit("Hello")
        e6.setReadOnly(True)
        flo.addRow("Read Only",e6)

        e5.editingFinished.connect(self.enterPress)
        self.setWindowTitle("QLineEdit综合使用")

    def textchanged(self,text):

        print("输入内容：" + text)

    def enterPress(self):
        print("已输入值")


if __name__ == '__main__':

    app = QApplication(sys.argv)
    win = QLine_Edit_Demo()
    win.show()
    sys.exit(app.exec_())