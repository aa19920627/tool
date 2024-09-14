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
        self.env = Environment(loader=FileSystemLoader(self.xml_path),
                               trim_blocks=True,
                               lstrip_blocks=True)
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

    # 构建设备操作服务模板
    def build_equipment_operation_service(self, data_list):
        # 加载模板
        template_QueryDeviceinfo = self.env.get_template("equipment_operation_service.xml")
        # 渲染模板
        output = template_QueryDeviceinfo.render()
        # 获取data的值
        feature, host, port, para_dict = data_list
        # 获取参数的键列表
        para_list = para_dict.keys()
        # 构建items列表
        items_list = []
        for para in para_list:
            paravalue = para_dict[para][1]
            items_list.append({'paraname': para, 'paravalue': paravalue})

        data = {
            'feature': feature,
            'host': host,
            'port': port,
            'items': items_list
        }

        # 渲染模板
        output = template_QueryDeviceinfo.render(data)

        # print(output)
        return output