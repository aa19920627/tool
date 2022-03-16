'''
@Author：洪建
@Date：2022/3/2 17:16
'''
import sys

from PyQt5.QtWidgets import QMainWindow, QFileDialog, QApplication

from Pyqt5_demo.layout_demo.menu_tool.Menu_Tool01 import Ui_MainWindow


class MainWindow(QMainWindow,Ui_MainWindow):

    def __init__(self,parent=None):

        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        #菜单的点击事件，点击关闭菜单，关闭
        self.fileCloseAction.triggered.connect(self.close)
        #菜单的点击事件，当点击打开菜单，调用槽函数openMsg()
        self.fileOpenAction.triggered.connect(self.openMsg)

    def openMsg(self):

        file,ok = QFileDialog.getOpenFileName(self,"打开","C:/","ALL Files(*);;Text Files(*.txt))")
        #在状态栏显示文件地址
        self.statusbar.showMessage(file)

if __name__ == '__main__':

    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
