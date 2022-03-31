'''
@Author：洪建
@Date：2022/3/28 16:19
'''
import sys

from PyQt5.QtCore import QDateTime, QDate
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QDateTimeEdit, QPushButton, QApplication

'''
QDateTimeEdit(编辑日期时间控件)示例
'''


class QDate_Time_Edit_Demo1(QWidget):
    def __init__(self, parent=None):
        super(QDate_Time_Edit_Demo1, self).__init__(parent)
        self.resize(300,90)

        vlayout = QVBoxLayout(self)
        self.date_edit = QDateTimeEdit(QDateTime.currentDateTime(),self)
        self.date_edit.setDisplayFormat("yyyy-MM-dd HH:mm:ss")
        #设置最小日期
        self.date_edit.setMinimumDate(QDate.currentDate().addDays(-365))
        #设置最大日期
        self.date_edit.setMaximumDate(QDate.currentDate().addDays(365))
        self.date_edit.setCalendarPopup(True)

        self.date_edit.dateChanged.connect(self.onDateChanged)
        self.date_edit.dateTimeChanged.connect(self.onDateTimeChanged)
        self.date_edit.timeChanged.connect(self.onTimeChanged)

        self.btn = QPushButton("获取日期和时间")
        self.btn.clicked.connect(self.onButtonClick)

        vlayout.addWidget(self.date_edit)
        vlayout.addWidget(self.btn)

    #日期发生改变时执行
    def onDateChanged(self,date):
        print(date)
    #无论是日期还是时间发生改变时都会执行
    def onDateTimeChanged(self,dateTime):
        print(dateTime)
    #时间发生改变时执行
    def onTimeChanged(self,time):
        print(time)
    def onButtonClick(self):
        dateTime = self.date_edit.dateTime()
        print(dateTime)
        #最大日期
        maxDate = self.date_edit.maximumDate()
        print(maxDate)
        #最大时间日期
        maxDateTime = self.date_edit.maximumDateTime()
        print(maxDateTime)
        #最大时间
        maxTime = self.date_edit.maximumTime()
        print(maxTime)
        #最小日期
        minDate = self.date_edit.minimumDate()
        print(minDate)
        #最小日期时间
        minDateTime = self.date_edit.minimumDateTime()
        print(minDateTime)
        #最小时间
        minTime = self.date_edit.minimumTime()
        print(str(minTime))

if __name__ == '__main__':

    app = QApplication(sys.argv)
    win = QDate_Time_Edit_Demo1()
    win.show()
    sys.exit(app.exec_())