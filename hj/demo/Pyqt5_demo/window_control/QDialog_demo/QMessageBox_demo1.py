'''
@Author：洪建
@Date：2022/3/24 16:11
'''
import sys

from PyQt5.QtWidgets import QWidget, QPushButton, QMessageBox, QApplication

'''
QMessageBox(通用的弹出式对话框)示例
'''


class QMessageBox_Demo1(QWidget):
    def __init__(self, parent=None):
        super(QMessageBox_Demo1, self).__init__(parent)
        self.resize(300, 100)
        self.btn = QPushButton(self)
        self.btn.setText("点击")
        self.btn.clicked.connect(self.msg)

    def msg(self):
        # 使用infomation信息框
        reply = QMessageBox.information(self, "标题", "消息正文", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        print(reply)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = QMessageBox_Demo1()
    win.show()
    sys.exit(app.exec_())
