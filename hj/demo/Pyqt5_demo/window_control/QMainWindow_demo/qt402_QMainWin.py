'''
@Author：洪建
@Date：2022/3/15 17:08
'''
import sys

from PyQt5.QtWidgets import QMainWindow, QApplication

'''
案例4-1，创建主窗口，显示状态栏信息
'''
class ManWindow(QMainWindow):

    def __init__(self,parent=None):

        super(ManWindow, self).__init__(parent)
        self.resize(400,200)
        self.status = self.statusBar()

        #5000是状态栏提示信息，5秒后消失
        self.status.showMessage('这是状态栏提示',5000)
        self.setWindowTitle('PyQt MainWindow例子')

if __name__ == '__main__':

    app = QApplication(sys.argv)
    win = ManWindow()
    win.show()
    sys.exit(app.exec_())
