'''
@Author：洪建
@Date：2022/3/21 13:55
'''
import sys

from PyQt5.QtWidgets import QWidget, QTextEdit, QPushButton, QVBoxLayout, QApplication

'''
 
'''


class QTextEdit_Demo1(QWidget):

    def __init__(self,parent=None):

        super(QTextEdit_Demo1, self).__init__(parent)
        self.setWindowTitle('QTextEdit 例子')
        self.resize(300,270)
        self.textEdit = QTextEdit()
        self.btn1 = QPushButton('显示文本')
        self.btn2 = QPushButton('显示HTML')

        layout = QVBoxLayout(self)
        layout.addWidget(self.textEdit)
        layout.addWidget(self.btn1)
        layout.addWidget(self.btn2)

        self.btn1.clicked.connect(self.btn1_clicked)
        self.btn2.clicked.connect(self.btn2_clicked)

    def btn1_clicked(self):
        self.textEdit.setPlainText("Hello PyQt5!\n单击按钮")

    def btn2_clicked(self):
        self.textEdit.setHtml("<font color='red' size='6'><red>Hello PyQt5!\n单击按钮。</font>")

if __name__ == '__main__':

    app = QApplication(sys.argv)
    win = QTextEdit_Demo1()
    win.show()
    sys.exit(app.exec_())
