'''
@Author：洪建
@Date：2022/3/30 10:07
'''
import sys

from PyQt5.QtWidgets import QWidget, QHBoxLayout, QTableWidget, QTableWidgetItem, QApplication

'''
QTableWidget基本使用示例
'''


class QTableWidget_Demo1(QWidget):
    def __init__(self, parent=None):
        super(QTableWidget_Demo1, self).__init__(parent)
        self.resize(400, 300)
        layout = QHBoxLayout(self)
        table_widget = QTableWidget()
        table_widget.setRowCount(4)
        table_widget.setColumnCount(3)
        layout.addWidget(table_widget)
        table_widget.setHorizontalHeaderLabels(["姓名", "性别", "体重"])

        new_item = QTableWidgetItem("张三")
        table_widget.setItem(0, 0, new_item)

        new_item = QTableWidgetItem("男")
        table_widget.setItem(0, 1, new_item)

        new_item = QTableWidgetItem("160")
        table_widget.setItem(0, 2, new_item)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = QTableWidget_Demo1()
    win.show()
    sys.exit(app.exec_())
