# -*- encoding: utf-8 -*-
"""
@File    : signal_channel.py
@Date    : 2020/10/30 18:47
@Author  : 洪建
"""

#ui
import threading
import time

from PyQt5 import QtCore, QtGui, QtWidgets

from Atomic_Service_Test.src.component.data_processing import Data_Processing
from Atomic_Service_Test.src.main.build_requests import Build_Requests
from Atomic_Service_Test.src.main.create_tcp_server import Create_Tcp_Server


class Signal_Channel(object):

    def __init__(self):

        self.data_name = str(time.time())

    def setupUi(self, MainWindow):
        '''
        基础属性
        '''
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1100, 850)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.url_line = QtWidgets.QLineEdit(self.centralwidget)
        self.url_line.setGeometry(QtCore.QRect(50, 30, 250, 20))
        self.url_line.setObjectName("url_line")
        self.soapaction_line = QtWidgets.QLineEdit(self.centralwidget)
        self.soapaction_line.setGeometry(QtCore.QRect(380, 30, 120, 20))
        self.soapaction_line.setObjectName("soapaction_line")
        self.equid_line = QtWidgets.QLineEdit(self.centralwidget)
        self.equid_line.setGeometry(QtCore.QRect(50, 70, 100, 20))
        self.equid_line.setObjectName("equid_line")
        self.mfid_line = QtWidgets.QLineEdit(self.centralwidget)
        self.mfid_line.setGeometry(QtCore.QRect(200, 70, 300, 20))
        self.mfid_line.setObjectName("mfid_line")
        self.send_text = QtWidgets.QTextEdit(self.centralwidget)
        self.send_text.setGeometry(QtCore.QRect(50, 140, 450, 550))
        self.send_text.setObjectName("send_text")
        self.reset_button = QtWidgets.QPushButton(self.centralwidget)
        self.reset_button.setGeometry(QtCore.QRect(310, 710, 80, 30))
        self.reset_button.setObjectName("reset_button")
        self.send_button = QtWidgets.QPushButton(self.centralwidget)
        self.send_button.setGeometry(QtCore.QRect(420, 710, 80, 30))
        self.send_button.setObjectName("send_button")
        self.recive_text = QtWidgets.QTextEdit(self.centralwidget)
        self.recive_text.setGeometry(QtCore.QRect(570, 140, 450, 550))
        self.recive_text.setObjectName("recive_text")
        self.url_lable = QtWidgets.QLabel(self.centralwidget)
        self.url_lable.setGeometry(QtCore.QRect(15, 30, 20, 20))
        self.url_lable.setObjectName("url_lable")
        self.soapaction_lable = QtWidgets.QLabel(self.centralwidget)
        self.soapaction_lable.setGeometry(QtCore.QRect(310, 30, 70, 20))
        self.soapaction_lable.setObjectName("soapaction_lable")
        self.euqid_lable = QtWidgets.QLabel(self.centralwidget)
        self.euqid_lable.setGeometry(QtCore.QRect(10, 70, 30, 20))
        self.euqid_lable.setObjectName("euqid_lable")
        self.mfid_lable = QtWidgets.QLabel(self.centralwidget)
        self.mfid_lable.setGeometry(QtCore.QRect(165, 70, 30, 20))
        self.mfid_lable.setObjectName("mfid_lable")

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1100, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        '''
        创建信号槽
        '''

        '''发送button，触发获取url,SoapAction,equid,mfid'''
        # self.send_button.clicked.connect(self.get_parameters)

        '''发送button，触发调用请求,并回显响应'''
        self.send_button.clicked.connect(self.create_thread)



    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.url_line.setToolTip(_translate("MainWindow", "<html><head/><body><p>URL</p></body></html>"))
        self.reset_button.setText(_translate("MainWindow", "重置"))
        self.send_button.setText(_translate("MainWindow", "发送"))
        self.url_lable.setText(_translate("MainWindow", "URL"))
        self.soapaction_lable.setText(_translate("MainWindow", "SoapAction"))
        self.euqid_lable.setText(_translate("MainWindow", "equid"))
        self.mfid_lable.setText(_translate("MainWindow", "mfid"))


    def get_parameters(self):

        '''获取url,SoapAction,equid,mfid'''

        self.url_value = self.url_line.text()
        self.soapaction_value = self.soapaction_line.text()
        self.equid_value = self.equid_line.text()
        self.mfid_value = self.mfid_line.text()

    def create_thread(self):

        self.thread_1 = threading.Thread(target=self.create_tcp_server)
        self.thread_2 = threading.Thread(target=self.call_request)
        self.thread_1.start()
        self.thread_2.start()
        # self.thread_2.setDaemon(True)

    def create_tcp_server(self):

        self.cts = Create_Tcp_Server("192.168.16.181", 7777,self.data_name).recv_message()


    def call_request(self):


        '''发送调用请求'''
        # self.echo_value = self.url_value + self.soapaction_value + self.equid_value + self.mfid_value

        self.data_list = Data_Processing().read_excel_data("test.xlsx")

        for i in self.data_list:

            self.bd = Build_Requests()
            data = self.bd.build_data(i[3], (i[1], i[2], "192.168.16.181", "7777"))
            self.res = self.bd.send_request(i[4], data, i[3])

            time.sleep(5)

            for i in range(10) :

                self.recive_value = Data_Processing().read_recive_data(self.data_name)
                if self.recive_value :
                    self.recive_text.setPlainText(str(self.recive_value))
                else:
                    break;



        '''回显响应'''
        # self.recive_text.setPlainText(self.echo_value)





