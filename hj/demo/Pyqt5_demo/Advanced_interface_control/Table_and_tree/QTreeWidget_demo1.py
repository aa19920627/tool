'''
@Author：洪建
@Date：2022/3/30 11:39
'''
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QBrush
from PyQt5.QtWidgets import QWidget, QTreeWidget, QTreeWidgetItem, QApplication, QMainWindow

'''
QTreeWidget示例
'''


class QTreeWidget_Demo1(QWidget):
    def __init__(self, parent=None):
        super(QTreeWidget_Demo1, self).__init__(parent)
        self.tree = QTreeWidget(self)
        self.resize(300, 200)
        # 设置列数
        self.tree.setColumnCount(2)
        # 设置树形控件头部的标题
        self.tree.setHeaderLabels(["Key", "Value"])
        # 设置根节点
        root = QTreeWidgetItem(self.tree)
        root.setText(0, "root")
        root.setIcon(0, QIcon("./wireless.png"))
        # 设置树形控件的列的宽度
        self.tree.setColumnWidth(0, 160)
        # 设置子节点1
        child1 = QTreeWidgetItem(root)
        child1.setText(0, "child1")
        child1.setText(1, "ios")
        child1.setIcon(0, QIcon("./wireless.png"))
        # 设置子节点2
        child2 = QTreeWidgetItem(root)
        child2.setText(0, "child2")
        child2.setText(1, "")
        child2.setIcon(0, QIcon("./wireless.png"))
        # 设置子节点3
        child3 = QTreeWidgetItem(child2)
        child3.setText(0, "child3")
        child3.setText(1, "android")
        child3.setIcon(0, QIcon("./wireless.png"))
        # 设置节点状态
        child3.setCheckState(0, Qt.Checked)

        # 设置节点的背景颜色
        brush_red = QBrush(Qt.red)
        root.setBackground(0, brush_red)
        brush_green = QBrush(Qt.green)
        root.setBackground(1, brush_green)

        # 给节点添加响应时间

        self.tree.addTopLevelItem(root)
        # 节点全部展开
        self.tree.expandAll()

        # 给节点添加响应时间
        self.tree.clicked.connect(self.onTreeClicked)

        # self.tree.setCentralWidget(self.tree)

    def onTreeClicked(self, qmodelindex):
        item = self.tree.currentItem()
        print("key=%s,value=%s" % (item.text(0), item.text(1)))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = QTreeWidget_Demo1()
    win.show()
    sys.exit(app.exec_())
