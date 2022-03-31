'''
@Author：洪建
@Date：2022/3/28 14:30
'''
import sys

from PyQt5 import QtCore
from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QWidget, QCalendarWidget, QLabel, QApplication

'''
QCalendar（日历）示例
'''


class QCalendar_Demo1(QWidget):
    def __init__(self, parent=None):
        super(QCalendar_Demo1, self).__init__(parent)
        self.cal = QCalendarWidget(self)
        self.cal.setMinimumDate(QDate(1980, 1, 1))
        self.cal.setMaximumDate(QDate(3000, 1, 1))
        self.cal.setGridVisible(True)
        self.cal.move(20, 20)
        self.cal.clicked[QtCore.QDate].connect(self.showData)

        self.label1 = QLabel(self)
        date = self.cal.selectedDate()
        self.label1.setText(date.toString("yyyy-MM-dd dddd"))
        self.label1.move(20, 300)


        self.setGeometry(100, 100, 400, 350)

    def showData(self, date):
        self.label1.setText(date.toString("yyyy-MM-dd dddd"))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = QCalendar_Demo1()
    win.show()
    sys.exit(app.exec_())
