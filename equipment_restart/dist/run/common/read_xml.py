# -*- encoding: utf-8 -*-
"""
@File    : read_xml.py
@Date    : 2021/1/25 13:39
@Author  : 洪建
"""
import os

from equipment_restart.common.frozen_path import Frozen_Path

'''
读取xml报文
'''


class Read_Xml:

    def __init__(self):

        self.xml_dir = self.path = Frozen_Path().app_path() + "/data/xml"

    def read_xml(self, xml_name):

        with open(file=self.xml_dir + xml_name + ".xml") as f:

            return str(f.read())    #返回xml报文的字符串







if __name__ == '__main__':

    # print(Read_Xml().read_xml("E_RemoteControl"))

    print(Read_Xml().path + "/data/xml")
