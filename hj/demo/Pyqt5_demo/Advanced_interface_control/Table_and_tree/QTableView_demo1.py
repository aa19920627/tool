'''
@Author：洪建
@Date：2022/3/29 16:18
'''
import sys

from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QWidget, QTableView, QVBoxLayout, QApplication, QHeaderView

'''
QTableView表格示例
'''


class QTableView_Demo1(QWidget):
    def __init__(self, parent=None):
        super(QTableView_Demo1, self).__init__(parent)
        self.resize(500, 300)
        self.mode1 = QStandardItemModel(4, 4)
        self.mode1.setHorizontalHeaderLabels(["标题1", "标题2", "标题3", "标题4"])

        for row in range(4):
            for column in range(4):
                item = QStandardItem("row %s,column %s" % (row, column))
                self.mode1.setItem(row, column, item)
        self.table_view = QTableView()
        self.table_view.setModel(self.mode1)
        # 表格填满窗口
        self.table_view.horizontalHeader().setStretchLastSection(True)
        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # 添加数据
        self.mode1.appendRow(QStandardItem("row add"))

        #删除当前选中的数据
        #方法1
        #取当前选中的所有行
        indexs = self.table_view.selectionModel().selection().indexes()
        if len(indexs) > 0 :
            #取第一行索引
            index = indexs[0]
            self.mode1.removeRows(index.row(),1)
        #方法2
        index = self.table_view.currentIndex()
        self.mode1.removeRow(index.row())

        layout = QVBoxLayout(self)
        layout.addWidget(self.table_view)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = QTableView_Demo1()
    win.show()
    sys.exit(app.exec_())
