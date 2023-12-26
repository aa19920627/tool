'''
@Author：洪建
@Date：2022/1/26 14:12
主程序
'''
import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget

from component.small_tool import deal_select_data
from component.sqlite_method import ManageSqlite
from main.function_module.register_center.register import RegisterStationDevice
from ui.auto_test import Ui_Form


class MainWindow(QWidget, Ui_Form):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.register_window()

    # 下面时注册窗口的组件设置
    def register_window(self):
        # 初始化数据库操作类
        _ms = ManageSqlite('auto_b_server')
        # 点击注册按钮，触发get_register_text,并调用注册方法
        self.pushButton.clicked.connect(self.get_register_text)

        # 设置省份下拉框的选项和城市下拉框关联关系，通过序号
        self.comboBox_2.activated[str].connect(self.comboBox_3)
        # 省份下拉框添加数据
        self.comboBox_2.addItems(deal_select_data(_ms.get_fetchall("SELECT province FROM area ")))

        # 关闭数据库连接
        _ms.close_cur_conn()

    def get_register_text(self):
        # 获取注册输入框输入的信息，保存到列表中
        mfid = self.lineEdit.text()
        mfname = self.lineEdit_2.text()
        equid = self.lineEdit_3.text()
        equname = self.lineEdit_5.text()
        ip = self.lineEdit_6.text()
        port = self.lineEdit_7.text()

        # 注册监测站
        # RegisterStationDevice().insert_station_info((mfid,mfname,)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
