import re
import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QLineEdit, QPushButton,
    QScrollArea, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QComboBox, QTextEdit, QSpacerItem, QSizePolicy,
    QBoxLayout
)

from component.common_component import match_chinese_names
from component.log_handle import Logger
from main.out_tool.b_server_test.b_server_test import Get_Deviceinfo


class Ui_MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi()
        # 实例化log类
        # self.logger = Logger(log_dir="b_server_test", log_file="run.log", log_level=logging.DEBUG)

    def setupUi(self):
        self.setWindowTitle("测试工具")
        self.resize(800, 600)

        # 设置中心区域
        self.central_widget = QWidget(self)  # 主窗口的中央部件
        self.setCentralWidget(self.central_widget)

        # 使用网格布局管理顶部区域（输入框）
        self.top_layout_widget = QWidget(self.central_widget)
        self.top_layout_widget.setGeometry(0, 0, 800, 200)  # 高度为窗口的 1/3
        self.top_layout_widget.setMinimumHeight(50)
        self.top_layout = QGridLayout(self.top_layout_widget)

        # Mfid输入框
        self.label_mfid = QLabel("mfid", self)
        self.lineEdit_mfid = QLineEdit(self)

        # Equid输入框
        self.label_equid = QLabel("equid", self)
        self.lineEdit_equid = QLineEdit(self)

        # URL输入框
        self.label_url = QLabel("url", self)
        self.label_url.setToolTip("填入B_QueryDeviceInfo的接口地址")
        self.lineEdit_url = QLineEdit(self)

        # 获取参数按钮
        self.pushButton = QPushButton("获取参数", self)

        # 响应结果窗口
        # 创建滚动区域
        self.scroll_area_res = QScrollArea(self)
        self.scroll_area_res.setWidgetResizable(True)
        # 设置宽高最大值
        # self.scroll_area_res.setMaximumHeight(450)
        # self.scroll_area_res.setMaximumWidth(500)
        self.text_res = QTextEdit(self)
        self.text_res.setReadOnly(True)  # 只读
        self.text_res.setStyleSheet("font-family: Consolas; font-size: 12px;")  # 设置字体样式
        # 将text_res添加到滚动区域
        self.scroll_area_res.setWidget(self.text_res)

        # 滚动区域放置下拉列表(设备能力参数列表)
        self.scroll_area = QScrollArea(self)
        self.scroll_area_widget = QWidget(self.central_widget)
        self.scroll_area_layout = QVBoxLayout(self.scroll_area_widget)

        # 监测能力列表
        self.label_soapaction = QLabel("设备能力", self)
        self.combo_box_soapaction = QComboBox(self)
        self.combo_box_soapaction.currentTextChanged.connect(self.select_soapaction_connect)
        # self.combo_box_soapaction.addItem("监测站/设备状态查询（B_QueryFaciDevStat）")

        # 测试按钮
        self.pushButton_request = QPushButton("启动", self)

        # 将控件添加到顶部区域的布局
        self.top_layout.addWidget(self.label_mfid, 0, 2)
        self.top_layout.addWidget(self.lineEdit_mfid, 0, 3)
        self.top_layout.addWidget(self.label_equid, 0, 4)
        self.top_layout.addWidget(self.lineEdit_equid, 0, 5)
        self.top_layout.addWidget(self.label_url, 0, 0)
        self.top_layout.addWidget(self.lineEdit_url, 0, 1)
        self.top_layout.addWidget(self.pushButton, 0, 6)
        self.top_layout.addWidget(self.label_soapaction, 1, 0)
        self.top_layout.addWidget(self.combo_box_soapaction, 1, 1)
        self.top_layout.addWidget(self.pushButton_request, 1, 3)

        # 使用QGridLayout来安排顶部区域和滚动区域
        main_layout = QGridLayout(self.central_widget)
        main_layout.addWidget(self.top_layout_widget, 0, 0, 1, 2)  # 顶部区域
        main_layout.addWidget(self.scroll_area, 2, 0)  # 滚动区域
        main_layout.addWidget(self.scroll_area_res, 2, 1)

        # 设置参数列表和响应内容框的比例
        main_layout.setColumnStretch(0, 1)  # 左侧（滚动区域）占据1份空间
        main_layout.setColumnStretch(1, 2)  # 右侧（响应区域）占据2份空间

        # 以下为信号和槽函数
        # 点击获取参数按钮，触发get_input
        self.pushButton.clicked.connect(self.get_input)

    # 获取输入框内容，调用deviceinfo接口获取设备能力列表，并填入设备能力列表中
    def get_input(self):
        #获取输入框内的数据
        # self.mfid = self.lineEdit_mfid.text()
        # self.equid = self.lineEdit_equid.text()
        # self.url = self.lineEdit_url.text()
        '''调试代码'''
        self.mfid = "51010001110001"
        self.equid = "68587579-b751-4611-be72-1ec14117366a"
        self.url = "http://192.168.13.201:8010/51010001110001/Demo/B_QueryDeviceInfo"

        #实例化deviceinfo类
        self.gd = Get_Deviceinfo(self.url, self.mfid, self.equid)
        # 获取设备能力
        self.feature_dict = self.gd.build_parameter_dictionary(self.gd.get_rse())
        # 用match_chinese_names方法匹配设备能力的中英文方法
        self.soapaction_keys = match_chinese_names(self.feature_dict)
        # 添加设备能力到下拉列表中
        self.combo_box_soapaction.addItems(self.soapaction_keys)

    # 选择设备能力后，刷新对应的参数列表
    def  select_soapaction_connect(self):
        # 清空滚动区域布局（移除现有内容）
        self.clear_layout(self.scroll_area_layout)
        self.scroll_area.setGeometry(0, 250, 400, 300)  # 滚动区域的位置和大小
        # 获取当前选中的能力
        self.select_text = self.combo_box_soapaction.currentText()
        # 正则匹配提取soapaction
        self.select_soapaction = re.search(r"(?<=（).+?(?=）)", self.select_text).group()
        # 获取设备能力的参数字典
        self.select_soapaction_dict = self.feature_dict[self.select_soapaction]
        # 获取参数的取值列表
        self.select_soapaction_values = self.select_soapaction_dict.values()


        # 添加取值列表到参数下拉列表
        for value in self.select_soapaction_values:
            self.label_parameter = QLabel(value[0])
            self.combo_box_parameter = QComboBox(self)
            self.combo_box_parameter.addItem(value[1])

            # 创建水平布局容纳标签和下拉框
            self.horizontal_layout = QHBoxLayout()
            # 标签和下拉列表添加到水平布局中
            self.horizontal_layout.addWidget(self.label_parameter)
            self.horizontal_layout.addWidget(self.combo_box_parameter)

            # 将水平布局的窗口添加到容器 滚动窗口中中
            self.scroll_area_layout.addLayout(self.horizontal_layout)

        # 设置滚动区的内容
        self.scroll_area_widget.setLayout(self.scroll_area_layout)
        self.scroll_area.setWidget(self.scroll_area_widget)
        self.scroll_area.setWidgetResizable(False)

    # 清空布局，方便放新数据
    def clear_layout(self,layout):
        # 获取布局中的所有项
        item_list = list(range(layout.count()))
        item_list.reverse()  # 倒序删除，避免影响布局顺序

        # 删除所有项
        for i in item_list:
            item = layout.itemAt(i)
            if item:
                layout.removeItem(item)  # 从布局中移除项
                if item.widget():  # 如果该项是控件
                    item.widget().deleteLater()  # 删除控件并释放资源
                elif item.layout():  # 如果该项是子布局，递归清理
                    self.clear_layout(item.layout())

        # # 删除布局本身
        # sip.delete(layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Ui_MainWindow()
    window.show()  # 显示窗口
    sys.exit(app.exec())
