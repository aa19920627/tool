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


# 匹配设备能力的中文名称
def match_chinese_names(name_dict):
    chinese_names_dict = {"B_SglFreqMeas": "单频测量（B_SglFreqMeas）", "B_WBFFTMon": "宽带FFT频谱观测（B_WBFFTMon）",
                          "B_PScan": "全景扫描频谱观测（B_PScan）", "B_FScan": "频率扫描频谱观测（B_FScan）",
                          "B_MScan": "存储频率列表扫描（B_MScan）", "B_SglFreqDF": "单频测向（B_SglFreqDF）",
                          "B_WBDF": "宽带FFT测向（B_WBDF）", "B_FScanDF": "扫频测向（B_FScanDF）",
                          "B_MScanDF": "频率表扫描测向（B_MScanDF）",
                          "B_DigSglRecDecode": "数字信号识别解调（B_DigSglRecDecode）",
                          "B_AnaTVDem": "模拟电视信号解调（B_AnaTVDem）", "B_DigTVDem": "数字电视信号解调（B_DigTVDem）",
                          "B_DigBroadcastDem": "数字广播信号解调（B_DigBroadcastDem）",
                          "B_SpecCommSysSglDem": "专用通信系统信号解调（B_SpecCommSysSglDem）",
                          "B_OccuMeas": "占用度测量（B_OccuMeas）",
                          "B_GenIFSpecTemp": "生成中频频谱模板（B_GenIFSpecTemp）",
                          "B_GenWBSpecTemp": "生成宽带频谱模板（B_GenWBSpecTemp）",
                          "B_GenFScanSpecTemp": "生成扫频频谱模板（B_GenFScanSpecTemp）",
                          "B_IFSglInte": "中频频谱信号截收（B_IFSglInte）",
                          "B_WBSglInte": "宽带频谱信号截收（B_WBSglInte）",
                          "B_FScanSglInte": "扫频频谱信号截收（B_FScanSglInte）",
                          "B_TDOAqMeas": "TDOA测量服务（B_TDOAqMeas）", "B_DDCMeas": "多路通道监测服务（B_DDCMeas）",
                          "B_StopMeas": "停止测量任务（B_StopMeas）", "B_SelfTest": "监测设备自检（B_SelfTest）",
                          "B_QueryFaciDevStat": "监测站/设备状态查询（B_QueryFaciDevStat）",
                          "B_SetDevicePower": "监测设备电源开关（B_SetDevicePower）",
                          "B_LinkAnteDev": "监测设备天线连接指配（B_LinkAnteDev）",
                          "B_TaskModification": "监测参数修改（B_TaskModification）",
                          "E_QueryDeviceInfo": "动环设备信息查询（E_QueryDeviceInfo）",
                          "E_RemoteControl": "环境监控设备远程控制（E_RemoteControl）",
                          "E_QueryEnviInfo": "环境监控信息查询（E_QueryEnviInfo）",
                          "B_AISCollect": "船舶AIS数据采集（B_AISCollect）",
                          "B_ADSBCollect": "航空ADS-B数据采集（B_ADSBCollect）",
                          "B_TxSingleFreq": "发射单个频率信号（B_TxSingleFreq）",
                          "B_TxMultiFreq": "发射多个频率信号（B_TxMultiFreq）",
                          "B_TXFreqBand": "发射频段扫频信号（B_TXFreqBand）"}

    macthed_values = [chinese_names_dict[key] for key in chinese_names_dict if key in name_dict]

    return macthed_values
