# -*- encoding: utf-8 -*-
"""
@File    : data_processing.py
@Date    : 2020/11/2 10:15
@Author  : 洪建
"""
import collections
import os
from xml.etree import ElementTree

import xlrd
import xmltodict

'''
数据处理
'''


class Data_Processing:

    def __init__(self):

        pass


    def read_xml(self , soapaction):

        '''
        :读取xml，获取对应能力的报文
        :return : xml报文，str属性
        '''

        self.xml_path = os.path.join(os.path.dirname(__file__),"../../data/xml/%s" % soapaction + ".xml" )

        with open(self.xml_path , encoding = "utf-8") as f :

            xml_value = f.read()

        return xml_value

    def read_excel_data(self,excel_name):

        '''
        :读取excel
        :return: 数据列表
        '''
        self.excel_path = os.path.join(os.path.dirname(__file__),"../../data/excel_data/%s" % excel_name)

        exc = xlrd.open_workbook(self.excel_path)
        exc_list = exc.sheets()[0]
        exc_data_list = []

        for i in range(1,exc_list.nrows):

            exc_data_list.append(exc_list.row_values(i))

        return exc_data_list

    def write_recive_data(self,data_name,recive_data):

        '''
        :把收到的数据写入文件，供界面调取回显
        '''

        self.data_path = os.path.join(os.path.dirname(__file__),'../../log/recive_log/%s' % data_name)

        with open(self.data_path , 'a' , encoding='utf-8') as f:

            f.write(recive_data)

    def read_recive_data(self,data_name):

        '''
        :读取接收到的数据，回显在界面上
        '''

        self.data_path = os.path.join(os.path.dirname(__file__),'../../log/recive_log/%s' % data_name)

        with open(self.data_path, 'rb') as f:

            offset = -50
            while True :
                f.seek(offset , 2)
                lines = f.readlines()
                if len(lines) >=2 :
                    last_line = lines[-1]
                    break
                offset*=2

            return last_line

    def read_xml_by_elementree(self,soapaction):

        '''
        通过elementree读取xml
        return: 读取的对象
        '''

        self.xml_path = os.path.join(os.path.dirname(__file__), "../../data/xml/%s" % soapaction + ".xml")

        element = ElementTree.parse(self.xml_path)

        return element

    def assembly_parameters(self,soapaction,operation_list):

        '''
        组装设备操作服务的参数
        :return: 组装后的报文
        '''

        equipment_operation_xml = Data_Processing().read_xml(soapaction)    #读取设备操作服务的xml报文

        equipment_operation_dict = xmltodict.parse(equipment_operation_xml)      #转换成OrderDict格式

        item_list = operation_list

        equipment_operation_dict['soapenv:Envelope']['soapenv:Body']['srrc:requestbody']['srrc:equpara']['srrc:items'][
            'srrc:item'] = item_list    #操作服务的能力参数列表替换

        xequipment_operation_xml_recv = xmltodict.unparse(equipment_operation_dict)

        return xequipment_operation_xml_recv







if __name__ == '__main__':

    # print(type(Data_Processing().read_xml("B_SglFreqMeas")))
    # print(Data_Processing().read_excel_data("test.xlsx")[0])



    print(Data_Processing().assembly_parameters('B_SglFreqMeas',))
