# -*- coding: utf-8 -*-
'''
@Author：洪建
@Date：2022/1/4 15:13
通用接口调用方法
'''
import random

import requests as requests

from component.loading_config import database_config, executetime_config, host_config
from component.manage_xml import ManageXml
from component.sqlite_method import ManageSqlite

# 数据库名
DATABASE_NAME = database_config()
# 任务执行时间
EXECUTETIME = executetime_config()
# 接收数据的ip地址
HOST_ADDR = host_config()


class RequestInterface(object):
    '''
    接口调用通用方法类
    '''

    def __init__(self):
        self.re = requests.session()
        self.headers = {'SOAPAction': '', 'Content-Type': 'text/xml;charset=UTF-8'}

    # B_QueryDeviceInfo通用方法
    def get_B_QueryDeviceInfo(self, mfid, equid, url):
        # 实例化xml操作类
        xm = ManageXml(xml_file_name='B_QueryDeviceInfo.xml')
        # 替换xml报文中的mfid,equid
        xm.root[1].find('.//srrc:mfid', xm.ns).text = mfid
        xm.root[1].find('.//srrc:equid', xm.ns).text = equid
        # 保存修改
        xm.write_xml()
        # 获取xml报文的字符串
        xml_message = xm.get_xml_string(xm.temp_path).encode(encoding='utf-8')

        self.headers['SOAPAction'] = 'B_QueryDeviceInfo'
        # 返回B_QueryDeviceInfo响应报文
        return self.re.post(url=url, data=xml_message, headers=self.headers).text

    # B_QueryFaciDevStat的通用方法
    def get_B_QueryFaciDevStat(self, equid):
        # 实例化xml操作类
        xm = ManageXml(xml_file_name='B_QueryFaciDevStat.xml')
        # 根据equid查询设备的基本信息
        ms = ManageSqlite(DATABASE_NAME)
        ip, port, mfid, equname = ms.get_fetchone(
            "SELECT ip,port,mfid,equname FROM device WHERE equid = '%s'" % equid)
        ms.close_cur_conn()
        # 替换请求报文中的mfid,equid
        xm.root[1].find('.//srrc:mfid', xm.ns).text = mfid
        xm.root[1].find('.//srrc:equid', xm.ns).text = equid
        # 保存修改
        xm.write_xml()
        # 获取xml报文的字符串
        xml_message = xm.get_xml_string(xm.temp_path).encode(encoding='utf-8')
        # 组装url
        url = 'http://%s:%s/%s/%s/%s' % (ip, port, mfid, equname, 'B_QueryFaciDevStat')
        self.headers['SOAPAction'] = 'B_QueryFaciDevStat'

        # 返回B_QueryFaciDevStat的响应报文
        return self.re.post(url=url, data=xml_message, headers=self.headers).text

    # 下面两个函数是设备操作服务调用的通用方法
    # 获取url,request_message,ip,port
    def cequipment_operation_servic_data(self, equid, soapaction):
        # 获取请求报文和设备的基本信息
        # 根据soapaction和equid查询请求报文和url、mfid
        ms = ManageSqlite(DATABASE_NAME)
        mfid, url, request_message = ms.get_fetchone(
            "SELECT mfid,url,request_message FROM function WHERE fuc_en_name='%s' AND equid='%s'" % (soapaction, equid))
        # 根据equid查询mfid

        # 实例化xml操作类
        xm = ManageXml(xml_string=request_message)
        # 替换executetime(通过配置文件)，mfid，equid的值
        xm.root.find('.//srrc:executetime', xm.ns).text = str(EXECUTETIME)
        xm.root.find('.//srrc:mfid', xm.ns).text = mfid
        xm.root.find('.//srrc:equid', xm.ns).text = equid

        # 替换outputchannel中的host（配置文件）和port
        xm.root.find('.//srrc:host', xm.ns).text = str(HOST_ADDR)
        port = str(random.randint(60000, 65000))
        xm.root.find('.//srrc:port', xm.ns).text = port

        # 获取修改后的xml报文
        request_message = xm.tosrting_xml(xm.root)

        return url, request_message, str(HOST_ADDR), port

    # 调用设备操作服务，获取响应结果
    def call_equipment_operation_service(self, url, request_message, soapaction):
        # headers替换值
        self.headers['SOAPAction'] = soapaction
        # 发送请求，获取响应报文
        return self.re.post(url=url, data=request_message, headers=self.headers)


if __name__ == '__main__':
    ri = RequestInterface()
    ri.get_B_QueryDeviceInfo('a6590676-f5a7-4220-b105-a6ea4edbd77b')
