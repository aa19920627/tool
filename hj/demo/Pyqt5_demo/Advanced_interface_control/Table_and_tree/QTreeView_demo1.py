'''
@Author：洪建
@Date：2022/3/30 14:51
'''
import sys

from PyQt5.QtWidgets import QWidget, QDirModel, QTreeView, QApplication

'''
QTreeView示例
'''


class QTreeView_Demo1(QWidget):
    def __init__(self, parent=None):
        super(QTreeView_Demo1, self).__init__(parent)
        # windows系统提供的模式
        model = QDirModel()
        tree = QTreeView(self)
        # 为控件添加模式
        tree.setModel(model)
        tree.resize(640, 480)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = QTreeView_Demo1()
    win.show()
    sys.exit(app.exec_())
