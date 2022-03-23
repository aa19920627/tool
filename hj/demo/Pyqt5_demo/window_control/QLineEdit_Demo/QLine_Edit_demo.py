'''
@Author：洪建
@Date：2022/3/17 17:07
'''
import sys

from PyQt5.QtWidgets import QWidget, QFormLayout, QLineEdit, QApplication

'''
文本框，LineEdit示例,EchoMode的显示效果
'''

class Qline_Demo(QWidget):

    def __init__(self,parent=None):
        super(Qline_Demo, self).__init__(parent)
        self. setWindowTitle('QLineEdit例子')

        flo = QFormLayout()
        pNormalLineEdit = QLineEdit()
        pNoEchoLineEdit = QLineEdit()
        pPasswordLineEdit = QLineEdit()
        pPasswordEchoOnEditLineEdit = QLineEdit()

        flo.addRow("Normal",pNormalLineEdit)
        flo.addRow("NoEcho",pNoEchoLineEdit)
        flo.addRow("Password",pPasswordLineEdit)
        flo.addRow("PasswordEchoOnEdit",pPasswordEchoOnEditLineEdit)

        pNormalLineEdit.setPlaceholderText("Normal")
        pNoEchoLineEdit.setPlaceholderText('NoEcho')
        pPasswordLineEdit.setPlaceholderText('Password')
        pPasswordEchoOnEditLineEdit.setPlaceholderText('passwordEchoOnEdit')

        #设置显示效果
        pNormalLineEdit.setEchoMode(QLineEdit.Normal)
        pNoEchoLineEdit.setEchoMode(QLineEdit.NoEcho)
        pPasswordLineEdit.setEchoMode(QLineEdit.Password)
        pPasswordEchoOnEditLineEdit.setEchoMode(QLineEdit.PasswordEchoOnEdit)

        self.setLayout(flo)

if __name__ == '__main__':

    app = QApplication(sys.argv)
    win = Qline_Demo()
    win.show()
    sys.exit(app.exec_())
