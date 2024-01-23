# -*- coding: utf-8 -*-
"""
@Time ： 2024/1/19 13:42
@Auth ： 洪建
"""
import ctypes
import os
import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import pyqtSignal
from main.app_ui import Ui_MainWindow
from main.auto_task import Test_Network_Connectivity
from main.component import Frozen_Path


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    # 自定义信号，用于接收日志信息
    log_signal = pyqtSignal(str)

    def __init__(self):
        super(MainWindow, self).__init__()
        # 初始化UI
        self.setupUi(self)
        # 设置窗口标题
        self.setWindowTitle("原子服务自动巡检工具")

        # 设置背景图片路径（根据实际情况替换成你的背景图片路径）
        background_image_path = Frozen_Path().app_path() + "/data/image/back.jpg"

        # 使用 QPalette 设置背景图片并使其适应窗口大小
        palette = QtGui.QPalette()
        background_image = QtGui.QPixmap(background_image_path)
        palette.setBrush(QtGui.QPalette.Window, QtGui.QBrush(
            background_image.scaled(self.size(), QtCore.Qt.IgnoreAspectRatio, QtCore.Qt.SmoothTransformation)))
        self.setPalette(palette)

        # 将按钮的点击事件与相应的方法连接
        self.pushButton.clicked.connect(self.open_excel_dialog)
        self.pushButton_2.clicked.connect(self.process_data)

        # 初始状态下，设置按钮 B 为不可点击
        self.pushButton_2.setEnabled(False)

        # 设置源文件的默认路径
        self.excel_file_path = ""

        # 设置禁止调整窗口大小
        self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.MSWindowsFixedSizeDialogHint)

        # 添加用于显示日志的 QPlainTextEdit
        self.log_text_edit = QtWidgets.QPlainTextEdit(self)
        self.log_text_edit.setGeometry(10, 200, 780, 390)
        self.log_text_edit.setReadOnly(True)  # 设置为只读，用于显示日志
        self.log_text_edit.setStyleSheet("background-color: rgba(255, 255, 255, 150);")  # 设置背景颜色和透明度

        # 重定向 sys.stdout 到日志窗口
        sys.stdout = CustomLogger(self.log_signal)
        # 重定向 sys.stderr 到日志窗口
        sys.stderr = CustomLogger(self.log_signal)

        # 连接自定义信号与槽函数，用于追加日志到日志窗口
        self.log_signal.connect(self.append_log)

    def open_excel_dialog(self):
        # 获取当前工作目录
        current_directory = os.getcwd() + "../data/excel"

        # 打开 Excel 文件选择对话框，并设置默认打开路径为当前目录
        file_dialog = QtWidgets.QFileDialog(self)
        file_dialog.setFileMode(QtWidgets.QFileDialog.ExistingFile)
        file_dialog.setNameFilter("Excel文件 (*.xlsx *.xls)")

        file_dialog.setDirectory(current_directory)  # 设置默认打开路径

        if file_dialog.exec_():
            self.excel_file_path = file_dialog.selectedFiles()[0]
            print("Selected Excel File:", self.excel_file_path)

            # 检测已经读取到文件，设置为可执行状态
            self.pushButton_2.setEnabled(True)

    def process_data(self):

        if not self.pushButton.isEnabled():  # 防止连续点击
            return

        # 创建并启动后台线程
        self.worker_thread = WorkerThread(self.excel_file_path)
        # 连接任务完成信号与槽
        self.worker_thread.task_completed.connect(self.task_completed)
        # 启动后台线程
        self.worker_thread.start()

        # 将所有按钮设置为不可点击状态
        self.disable_all_buttons(False)

    def task_completed(self):
        # 后台任务完成后恢复按钮状态
        self.disable_all_buttons(True)
        # 确保线程安全退出
        self.worker_thread.wait()
        self.worker_thread = None  # 清理线程对象

    # 在 MainWindow 类中添加一个方法，让所有按钮处于不可点击状态
    def disable_all_buttons(self, status=None):
        for button in self.findChildren(QtWidgets.QPushButton):
            button.setEnabled(status)

    def append_log(self, log_text):
        # 在日志窗口中追加文本
        self.log_text_edit.appendPlainText(log_text)


class WorkerThread(QtCore.QThread):
    # 任务完成信号
    task_completed = QtCore.pyqtSignal()

    def __init__(self, excel_file_path):
        super(WorkerThread, self).__init__()
        self.excel_file_path = excel_file_path

    def run(self):
        # 在这里执行读取excel，开始巡检的主代码
        Test_Network_Connectivity().start_checking(self.excel_file_path)
        # 发送完成信号
        self.task_completed.emit()
        # 任务执行完毕后退出线程
        self.quit()


class CustomLogger:
    def __init__(self, log_signal):
        self.log_signal = log_signal

    def write(self, message):
        # 发送日志信号，将 message 追加到日志窗口
        self.log_signal.emit(message)


if __name__ == '__main__':
    ctypes.windll.shcore.SetProcessDpiAwareness(1)  # 设置高 DPI 缩放策略
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
