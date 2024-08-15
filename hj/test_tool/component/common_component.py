# -*- coding: utf-8 -*-
"""
@Time ： 2024/6/20 14:04
@Auth ： 洪建
"""
from lxml import etree

from component.read_config import read_equip_config

'''
封装通用工具
'''

namespace = {
    'soapenv': 'http://schemas.xmlsoap.org/soap/envelope/',
    'srrc': 'http://www.srrc.org.cn'
}


# 格式化xml响应报文
def formatting_xml(res_xml):
    # 解析xml
    root_res = etree.fromstring(res_xml)
    # 格式化xml
    formatted_xml = etree.tostring(root_res, encoding="UTF-8", pretty_print=True).decode()

    return formatted_xml


# 获取设备操作服务参数名称和默认值
def get_name_defaultvalue(xml_value):
    # 解析xml
    xml_root = etree.fromstring(xml_value)
    # XPATH获取第一个featurelist节点
    featurelist_root = xml_root.xpath("//srrc:featurelist", namespaces=namespace)[0]
    # print(featurelist_root)
    # 循环获取feature的SoapAction列表
    features = featurelist_root.xpath(".//srrc:code/text()", namespaces=namespace)
    # 读取支持的能力列表
    features_config = read_equip_config()['SOAPAction'].split(',')
    # 筛选deviceinfo中支持的能力
    features_support = [item for item in features if item in features_config]

    # 定义设备能力字典
    feature_dict = {}
    # 构建设备能力的参数字典
    for feature in features_support:
        # 获取feature的能力树
        parameter_list = featurelist_root.xpath(f".//srrc:feature[srrc:code='{feature}']/srrc:input/srrc:parameter",
                                                namespaces=namespace)
        # 定义参数字典
        parameters_dict = {}
        # 获取每个参数的默认值
        for parameter in parameter_list:
            name = parameter.xpath(".//srrc:name/text()", namespaces=namespace)[0]
            displayname = parameter.xpath(".//srrc:displayname/text()", namespaces=namespace)[0]
            defaultvalue = parameter.xpath(".//srrc:defaultvalue/text()", namespaces=namespace)[0]
            parameters_dict[name] = (displayname, defaultvalue)

        feature_dict.update({feature: parameters_dict})

    return feature_dict