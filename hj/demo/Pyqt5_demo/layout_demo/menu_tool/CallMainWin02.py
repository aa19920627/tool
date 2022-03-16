'''
@Author：洪建
@Date：2022/3/3 9:51
'''
import sys

from PyQt5.QtWidgets import QMainWindow, QWidget, QFileDialog, QApplication

from Pyqt5_demo.layout_demo.menu_tool.ChildrenForm2 import Ui_ChildrenForm2
from Pyqt5_demo.layout_demo.menu_tool.Menu_Tool01 import Ui_MainWindow


class MainForm(QMainWindow, Ui_MainWindow):
    '''
    加载其他子窗口
    '''

    def __init__(self, parent=None):
        super(MainForm, self).__init__(parent)
        self.setupUi(self)

        # 生成子窗口实例
        self.child = ChildrenForm()
        # 菜单的点击事件，点击关闭菜单，关闭
        self.fileCloseAction.triggered.connect(self.close)
        # 菜单的点击事件，当点击打开菜单，调用槽函数openMsg()
        self.fileOpenAction.triggered.connect(self.openMsg)
        # 单击添加窗口，子窗口就会显示在主窗口的MaingridLayout中
        self.addWinAction.triggered.connect(self.childshow)

    def childshow(self):
        # 添加子窗口
        self.MaingridLayout.addWidget(self.child)
        self.child.show()

    def openMsg(self):
        file, ok = QFileDialog.getOpenFileName(self, "打开", "C:/", "ALL Files(*);;Text Files(*.txt))")
        # 在状态栏显示文件地址
        self.statusbar.showMessage(file)


class ChildrenForm(QWidget, Ui_ChildrenForm2):
    '''
    子窗口
    '''

    def __init__(self, parent=None):
        super(ChildrenForm, self).__init__(parent)
        self.setupUi(self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainForm()
    win.show()
    sys.exit(app.exec_())
