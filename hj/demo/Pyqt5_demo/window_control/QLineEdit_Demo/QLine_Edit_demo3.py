'''
@Author：洪建
@Date：2022/3/21 13:20
'''
import sys

from PyQt5.QtWidgets import QWidget, QFormLayout, QLineEdit, QApplication

'''
输入掩码示例
'''

class QLine_Edit_Demo3(QWidget):

    def __init__(self,parent=None):

        super(QLine_Edit_Demo3, self).__init__(parent)
        self.setWindowTitle("输入掩码示例")

        self.resize(300,150)
        flo = QFormLayout(self)
        line_edit1 = QLineEdit()
        line_edit2 = QLineEdit()
        line_edit3 = QLineEdit()
        line_edit4 = QLineEdit()

        line_edit1.setInputMask("000.000.000.000;_")
        line_edit2.setInputMask("HH:HH:HH:HH:HH:HH;_")
        line_edit3.setInputMask("0000-00-00")
        line_edit4.setInputMask(">AAAAA-AAAAA-AAAAA-AAAAA-AAAAA;#")

        flo.addRow("数字掩码",line_edit1)
        flo.addRow("Mac掩码",line_edit2)
        flo.addRow("日期掩码",line_edit3)
        flo.addRow("许可证掩码",line_edit4)


if __name__ == '__main__':

    app = QApplication(sys.argv)
    win = QLine_Edit_Demo3()
    win.show()
    sys.exit(app.exec_())