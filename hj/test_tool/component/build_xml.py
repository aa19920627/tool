# -*- coding: utf-8 -*-
"""
@Time ： 2024/6/20 13:54
@Auth ： 洪建
"""
from jinja2 import Environment, FileSystemLoader

from component.runtime_environment import Frozen_Path

'''
构建请求的xml报文
'''


class Build_Xml:

    def __init__(self, mfid, equid):
        # 初始化环境路径
        self.frozen_path = Frozen_Path().app_path()
        # 指定模板文件目录
        self.xml_path = self.frozen_path + '/data/wsdl_templates'
        # 设置环境变量
        self.env = Environment(loader=FileSystemLoader(self.xml_path))
        # 定义全局变量
        self.env.globals['mfid'] = mfid
        self.env.globals['equid'] = equid

    # 构建B_QueryDeviceInfo的报文
    def build_B_QueryDeviceInfo(self):
        # 加载模板
        template_QueryDeviceinfo = self.env.get_template("B_QueryDeviceInfo.xml")
        # 渲染模板
        output = template_QueryDeviceinfo.render()

        return output

    #构建设备操作服务模板
    def build_equipment_operation_service(self,data):
        # 加载模板
        template_QueryDeviceinfo = self.env.get_template("equipment_operation_service.xml")
        # 渲染模板
        output = template_QueryDeviceinfo.render()


