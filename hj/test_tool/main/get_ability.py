# -*- coding: utf-8 -*-
"""
@Time ： 2024/6/20 11:37
@Auth ： 洪建
"""
from component.build_xml import Build_Xml
from component.common_component import formatting_xml
from component.send_request import send_request

'''
通过deviceinfo接口获取设备支持的所有能力，并根据能力值生成参数列表
'''


class Get_Deviceinfo:

    def __init__(self, url, mfid, equid):
        self.url = url
        self.mfid = mfid
        self.equid = equid

    # 调用接口，返回deviceinfo报文
    def get_rse(self):
        # 构建报文
        bx = Build_Xml(self.mfid, self.equid)
        xml_data = bx.build_B_QueryDeviceInfo()

        # 发送请求
        res = send_request(url=self.url, data=xml_data, soapaction="B_QueryDeviceInfo")

        # 格式化响应报文
        self.res_xml = formatting_xml(res.text)

        print(self.res_xml)

    #
if __name__ == '__main__':
    gd = Get_Deviceinfo(url="http://192.168.139.196:8010/51010001110001/Demo/B_QueryDeviceInfo",
                        mfid="51010001110001",
                        equid="30252f2d-23fd-47a8-9dbd-f883aeb8c065")
    gd.get_rse()
