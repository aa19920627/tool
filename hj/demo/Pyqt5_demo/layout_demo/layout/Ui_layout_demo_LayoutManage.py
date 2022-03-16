'''
@Author：洪建
@Date：2022/3/1 13:39
'''
import sys

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QApplication

from Pyqt5_demo.layout_demo.layout.layout_demo_LayoutManage import Ui_LayoutDemo


class LayoutDemo(QMainWindow, Ui_LayoutDemo):
    """
    布局的进阶使用Demo
    """

    def __init__(self, parent=None):
        super(LayoutDemo, self).__init__(parent)
        self.setupUi(self)

    @pyqtSlot()
    def on_pushButton_clicked(self):
        print('分割线')
        print("收益_min", self.doubleSpinBox.text())
        print("收益_max", self.doubleSpinBox_2.text())
        print("最大回撤_min", self.doubleSpinBox_3.text())
        print("最大回撤_max", self.doubleSpinBox_4.text())
        print("sharp值_min", self.doubleSpinBox_5.text())
        print("sharp值_max", self.doubleSpinBox_6.text())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = LayoutDemo()
    ui.show()
    sys.exit(app.exec_())
