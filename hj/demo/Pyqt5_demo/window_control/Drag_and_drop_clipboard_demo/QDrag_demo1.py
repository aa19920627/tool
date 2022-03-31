'''
@Author：洪建
@Date：2022/3/25 16:54
'''
import sys

from PyQt5.QtWidgets import QWidget, QComboBox, QFormLayout, QLabel, QLineEdit, QApplication

'''
QDrag(拖拽),示例
'''

class QDrag_Demo1(QComboBox):
    def __init__(self,parent=None):
        super(QDrag_Demo1, self).__init__(parent)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        print(event)
        if event.mimeData().hasText():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self,event):
        self.addItem(event.mimeData().text())

class Example(QWidget):
    def __init__(self,parent=None):
        super(Example, self).__init__(parent)
        lo = QFormLayout(self)
        lo.addRow(QLabel("请把左边文本拖拽到右边下拉菜单中"))
        edit = QLineEdit()
        edit.setDragEnabled(True)
        com = QDrag_Demo1(self)
        lo.addRow(edit,com)

if __name__ == '__main__':

    app = QApplication(sys.argv)
    win = Example()
    win.show()
    sys.exit(app.exec_())