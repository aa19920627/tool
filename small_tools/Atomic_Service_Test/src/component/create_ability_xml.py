# -*- encoding: utf-8 -*-
"""
@File    : create_ability_xml.py
@Date    : 2020/12/18 15:08
@Author  : 洪建
"""
import collections
from xml.etree import ElementTree
from xml.etree.ElementTree import Element

import requests
import xmltodict as xmltodict

from Atomic_Service_Test.src.component.data_processing import Data_Processing

'''获取设备能力详情，组装设备操作服务的报文'''



class Create_Ability_Xml:

    def __init__(self):

        self.re = requests.session()

    def get_deviceinfo(self,url,data):

        '''
        构建B_QueryDeviceInfo的接口请求，return响应报文
        '''
        headers = {"Content-Type" : "text/xml;charset=UTF-8" ,
                   "SOAPAction" : 'B_QueryDeviceInfo'}

        try :
            res = self.re.post(url = url , data = data , headers = headers , timeout = 10)
        except  requests.exceptions.Timeout as e :
            return "响应超时"

        return res.text



if __name__ == '__main__':

    excel_data = Data_Processing().read_excel_data('test.xlsx')

    xml_data = Data_Processing().read_xml('B_QueryDeviceInfo') % (excel_data[0][1],excel_data[0][2])

    rec_value = Create_Ability_Xml().get_deviceinfo(excel_data[0][5],xml_data)

    # print(type(rec_value))

    # element = Data_Processing().read_xml_by_elementree('B_QueryDeviceInfo')

    # for deviceinfo_dict in element.iter('B_PScan') :
    # namespace = '{http://www.srrc.org.cn}'
    #
    # element = ElementTree.fromstring(rec_value)
    #
    # for i in element.iter(namespace +'feature'):
    #
    #     print(i[0].text)


    # print(deviceinfo_et.iter("srrc:code"))


    #deviceinfo返回报文转换字典
    dict_xml = xmltodict.parse(rec_value)

    feature_dict = dict_xml['soapenv:Envelope']['soapenv:Body']['srrc:responsebody']['srrc:result']['srrc:featurelist']['srrc:feature']

    for i in feature_dict :

        if i['srrc:code'] == 'B_SglFreqMeas' :

            for j in i['srrc:input']['srrc:parameter'] :



                print(j['srrc:name'] + ':' + j['srrc:defaultvalue'])



    # bility_1 = collections.OrderedDict()
    # bility_1['srrc:paraname'] = 'test'
    # bility_1['srrc:paravalue'] = 'test'



    # item_list.append({('srrc:paraname','')})

