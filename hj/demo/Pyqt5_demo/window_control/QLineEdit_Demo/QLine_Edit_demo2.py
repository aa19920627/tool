'''
@Author：洪建
@Date：2022/3/17 17:20
'''
import sys

from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QIntValidator, QDoubleValidator, QRegExpValidator
from PyQt5.QtWidgets import QWidget, QFormLayout, QLineEdit, QApplication

'''
QLineEdit，验证器示例
'''


class LineEditDemo2(QWidget):

    def __init__(self, parent=None):
        super(LineEditDemo2, self).__init__(parent)
        self.setWindowTitle('验证器例子')

        flo = QFormLayout(self)
        line_edit_1 = QLineEdit()
        line_edit_2 = QLineEdit()
        line_edit_3 = QLineEdit()

        flo.addRow("整形", line_edit_1)
        flo.addRow("浮点型", line_edit_2)
        flo.addRow("字母和数字", line_edit_3)

        line_edit_1.setPlaceholderText("整型")
        line_edit_2.setPlaceholderText("浮点型")
        line_edit_3.setPlaceholderText("字母和数字")

        # 整形，范围[1，99]
        validator_1 = QIntValidator(self)
        validator_1.setRange(1, 99)

        # 浮点型，范围[-360，360]，精度：小数点后两位
        validator_2 = QDoubleValidator(self)
        validator_2.setRange(-360, 360)
        validator_2.setNotation(QDoubleValidator.StandardNotation)
        validator_2.setDecimals(2)

        # 字母和数字
        reg = QRegExp("[a-zA-Z0-9]+$")
        validator_3 = QRegExpValidator(self)
        validator_3.setRegExp(reg)

        #设置验证器
        line_edit_1.setValidator(validator_1)
        line_edit_2.setValidator(validator_2)
        line_edit_3.setValidator(validator_3)

if __name__ == '__main__':

    app = QApplication(sys.argv)
    win = LineEditDemo2()
    win.show()
    sys.exit(app.exec_())
