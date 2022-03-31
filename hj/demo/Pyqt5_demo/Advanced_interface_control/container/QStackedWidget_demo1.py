'''
@Author：洪建
@Date：2022/3/30 15:42
'''
import sys

from PyQt5.QtWidgets import QWidget, QListWidget, QStackedWidget, QHBoxLayout, QFormLayout, QLineEdit, QRadioButton, \
    QLabel, QCheckBox, QApplication

'''
QStackedWidget示例
'''


class QStackedWidget_Demo1(QWidget):
    def __init__(self, parent=None):
        super(QStackedWidget_Demo1, self).__init__(parent)
        self.setGeometry(300, 50, 10, 10)

        self.left_list = QListWidget()
        self.left_list.insertItem(0, "联系方式")
        self.left_list.insertItem(1, "个人信息")
        self.left_list.insertItem(2, "教育程度")
        self.stack1 = QWidget()
        self.stack2 = QWidget()
        self.stack3 = QWidget()
        self.stack1UI()
        self.stack2UI()
        self.stack3UI()
        self.stack = QStackedWidget(self)
        self.stack.addWidget(self.stack1)
        self.stack.addWidget(self.stack2)
        self.stack.addWidget(self.stack3)

        hbox = QHBoxLayout(self)
        hbox.addWidget(self.left_list)
        hbox.addWidget(self.stack)
        self.setLayout(hbox)
        self.left_list.currentRowChanged.connect(self.display)

    def stack1UI(self):
        layout = QFormLayout()
        layout.addRow("姓名", QLineEdit())
        layout.addRow("地址", QLineEdit())
        self.stack1.setLayout(layout)


    def stack2UI(self):
        layout = QFormLayout()
        sex = QHBoxLayout()
        sex.addWidget(QRadioButton("男"))
        sex.addWidget(QRadioButton("女"))
        layout.addRow(QLabel("性别"), sex)
        layout.addRow("生日", QLineEdit())
        self.stack2.setLayout(layout)

    def stack3UI(self):
        layout = QHBoxLayout()
        layout.addWidget(QLabel("科目"))
        layout.addWidget(QCheckBox("物理"))
        layout.addWidget(QCheckBox("高数"))
        self.stack3.setLayout(layout)

    def display(self, i):
        self.stack.setCurrentIndex(i)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = QStackedWidget_Demo1()
    win.show()
    sys.exit(app.exec_())
