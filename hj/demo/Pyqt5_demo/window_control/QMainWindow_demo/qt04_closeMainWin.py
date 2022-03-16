'''
@Author：洪建
@Date：2022/3/15 17:23
'''
import sys

from PyQt5.QtWidgets import QMainWindow, QPushButton, QApplication, QHBoxLayout, QWidget

'''
本例演示关闭主窗口
'''


class WinForm(QMainWindow):

    def __init__(self, parent=None):
        super(WinForm, self).__init__(parent)
        self.setWindowTitle('关闭主窗口的例子')
        self.button1 = QPushButton('关闭主窗口')
        self.button1.clicked.connect(self.onButtonClick)

        layout = QHBoxLayout()
        layout.addWidget(self.button1)

        main_frame = QWidget()
        main_frame.setLayout(layout)
        self.setCentralWidget(main_frame)

    def onButtonClick(self):
        # sender是发送信号的对象
        sender = self.sender()
        print(sender.text() + ' 被按下了 ')
        q_app = QApplication.instance()
        q_app.quit()

if __name__ == '__main__':

    app = QApplication(sys.argv)
    win = WinForm()
    win.show()
    sys.exit(app.exec_())
