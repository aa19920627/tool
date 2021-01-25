# -*- encoding: utf-8 -*-
"""
@File    : read_xml.py
@Date    : 2021/1/25 13:39
@Author  : 洪建
"""
import os

'''
读取xml报文
'''


class Read_Xml:

    def __init__(self):

        self.xml_dir = os.path.join(os.path.dirname(__file__), "../data/xml/")

    def read_xml(self, xml_name):

        with open(file=self.xml_dir + xml_name + ".xml") as f:

            return str(f.read())    #返回xml报文的字符串







if __name__ == '__main__':

    print(Read_Xml().read_xml("E_RemoteControl"))


