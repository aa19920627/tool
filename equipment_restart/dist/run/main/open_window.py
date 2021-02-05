# -*- encoding: utf-8 -*-
"""
@File    : open_window.py
@Date    : 2021/1/25 10:26
@Author  : 洪建
"""
import os
import sys
import threading
import time

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication

from equipment_restart.common.component import Component_method
from equipment_restart.common.read_config import Read_config, Basis_config
from equipment_restart.common.write_log import Write_Log
from equipment_restart.main.monitor_method import Monitor_Method
from equipment_restart.main.restart_equipment import Restart_equipment
from equipment_restart.ui.mode import Ui_MainWindow

'''
构建监控窗口，构建信号槽方法
'''

class Monitor_Window(Ui_MainWindow, QMainWindow):

    def __init__(self):

        super(Monitor_Window, self).__init__()
        self.setupUi(self)

        #获取配置文件的配置
        self.interval = Read_config().interval_time()*60          #监控间隔
        self.dely_restart_time =  Read_config().restart_time()*60   #重启设备等待时间，避免设备还没启动完成，又下发重启命令

        #设置程序运行状态默认为空
        self.label_4.setText("")


        #建立信号槽
        self.pushButton.clicked.connect(self.start_monitor)
        self.pushButton_2.clicked.connect(self.load_config)

        #窗口存活性监测变量
        self.window_alive = True



    def start_monitor(self):

        self.pushButton_value = self.pushButton.text()

        #判断按钮的状态
        if self.pushButton_value == "开始":

            #设置程序状态为正在运行
            self.label_4.setText("正在运行")
            self.label_4.setStyleSheet("color:green")

            # 获取填写的基础信息
            self.remotecontrol_url_value = self.lineEdit_4.text()
            self.mfid_value = self.lineEdit_2.text()
            self.equid_value = self.lineEdit_3.text()
            self.ip_value = self.lineEdit.text()

            #设置按钮为停止按钮
            self.pushButton.setText("停止")
            self.create_threading()


        else:

            #停止后，按钮重置为开始按钮
            self.label_4.setText("")
            self.pushButton.setText("开始")

    def create_threading(self):

        '''
        创建定时器，监控设备的网络连接状态
        监控间隔可配置
        '''
        self.pushButton_value = self.pushButton.text()


        #随按钮的状态来开启和停用定时器
        if self.pushButton_value == "停止" and self.window_alive == True:

            self.t_ping = threading.Timer(self.interval ,self.start_monitor_equipment)   #self.interval监控间隔
            self.t_ping.start()

        else:
            self.t_ping.cancel()    #如果关闭监控，退出定时器


    def start_monitor_equipment(self):

        '''
        监控设备网络连接状态
        '''

        #获取监测结果
        result = Monitor_Method().ping_equipment(self.lineEdit.text())

        if result == 1:

            #记录日志
            Write_Log().write_log("%s发现设备网络不通畅、重启设备" % Component_method().get_log_time())

            #设置设备状态为故障
            self.label_7.setText("故障")
            time.sleep(1)
            self.label_7.setStyleSheet("color:red")

            #调用重启方法
            self.restart_equipment()

        else:

            #设置设备状态为正常
            self.label_7.setText("正常")
            self.label_7.setStyleSheet("color:green")

            #记录日志
            Write_Log().write_log("%s设备网络正常" % Component_method().get_log_time())

        #调用定时器
        self.create_threading()


    def restart_equipment(self):

        '''
        如果监控到了掉线，调用动环服务，重启设备
        '''
        Restart_equipment(self.remotecontrol_url_value, self.mfid_value, self.equid_value).restart_equipment()     #调用公共方法中的重启设备

        time.sleep(self.dely_restart_time)      #睡眠等待设备重启

    def load_config(self):

        #载入动环服务的配置
        self.lineEdit.setText(Basis_config().basis_ip())
        self.lineEdit_4.setText(Basis_config().basis_url())
        self.lineEdit_2.setText(Basis_config().basis_mfid())
        self.lineEdit_3.setText(Basis_config().basis_equid())

    def closeEvent(self, event):    #方法名不可变

        '''
        定义退出确认框
        '''

        reply = QtWidgets.QMessageBox.question(self,u"警告" ,u"确认退出？", QtWidgets.QMessageBox.Yes,
                                               QtWidgets.QMessageBox.No)
        #QtWidgets.QMessageBox.question(self,u"弹窗名", u"弹窗内容", 选项1, 选项2)

        if reply == QtWidgets.QMessageBox.Yes:

            self.window_alive == False
            event.accept()   #关闭窗口，√
            os._exit(5)

        else:
            event.ignore()   #忽视关闭，X



# if __name__ == '__main__':
#
#     app = QApplication(sys.argv)
#     window = Monitor_Window()
#     window.show()
#     sys.exit(app.exec_())