'''
@Author：洪建
@Date：2022/3/29 14:42
'''
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QPixmap, QIcon, QPainter
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog
from PyQt5.QtWidgets import QLabel, QSizePolicy, QAction, QMainWindow, QApplication

'''
QPrinter（图像打印控件）示例
'''


class QPrinter_Demo1(QMainWindow):
    def __init__(self, parent=None):
        super(QPrinter_Demo1, self).__init__(parent)
        self.image_label1 = QLabel()
        self.image_label1.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.setCentralWidget(self.image_label1)
        self.image = QImage()
        self.createActions()
        self.createMenus()
        self.createToolBars()

        if self.image.load("./wireless.png"):
            self.image_label1.setPixmap(QPixmap.fromImage(self.image))
            self.resize(self.image.width(), self.image.height())

    def createActions(self):
        self.PrintAction = QAction(QIcon('./wireless.png'), self.tr("打印"), self)
        self.PrintAction.setShortcut("Ctrl+p")
        self.PrintAction.setStatusTip(self.tr("打印"))
        self.PrintAction.triggered.connect(self.slot_print)

    def createMenus(self):
        print_menu = self.menuBar().addMenu(self.tr("打印"))
        print_menu.addAction(self.PrintAction)

    def createToolBars(self):
        file_tool_bar = self.addToolBar("print")
        file_tool_bar.addAction(self.PrintAction)

    def slot_print(self):
        printer = QPrinter()
        print_dialog = QPrintDialog(printer, self)
        if print_dialog.exec_():
            painter = QPainter(printer)
            rect = painter.viewport()
            size = self.image.setText()
            size.scale(rect.size(), Qt.KeepAspectRatio)
            painter.setViewport(rect.x(), rect.y(), size.width(), size.height())
            painter.setWindow(self.image.rect())
            painter.drawImage(0,0,self.image)

if __name__ == '__main__':

    app = QApplication(sys.argv)
    win = QPrinter_Demo1()
    win.show()
    sys.exit(app.exec_())
