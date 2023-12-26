'''
@Author: 洪建
@Date 2023/7/5 13:56
'''
import socket

import requests
from ping3 import ping

from auto_test_b_server.main.manage_xml import ManageXml

'''
自动检测原子服务状态，分为三个步骤：
1.网络检测 
2.原子服务状态检测
3.任务数据检测（暂时不做）
'''


class Test_Network_Connectivity:
    def __int__(self):
        pass

    def test_network_connectivity(self, host):
        '''
        步骤1：检测网络连通性
        '''
        try:
            # 发送ICMP请求，timeout参数设置超时时间
            result = ping(host, timeout=2)

            if result is not None:
                # 主机可达
                print(f"主机{host}网络正常")
                return True
            else:
                # 主机不可达
                print(f"主机{host}网络不通")
                return False
        except Exception as e:
            # 发生异常
            print("捕获异常")
            return False

    def test_b_server_port_connectivity(self, host, port):
        '''
        步骤2：检测原子服务端口连通性
        '''
        try:
            # 创建套接字对象
            sock = socket.create_connection((host, port), timeout=5)
            # 连接成功
            print(f"原子服务端口连接成功 {host}:{port}")
            sock.close()
            return True
        except socket.error as e:
            # 连接失败
            print(f"原子服务端口连接失败 {host}:{port}")
            return False
    def check_device_status(self, equid):
        '''
        步骤3：调用B_QueryFaciDevStat接口，获取原子服务返回的状态
        '''
        # 获取B_QueryFaciDevStat的响应报文
        xml_string = RequestInterface().get_B_QueryFaciDevStat(equid)
        # 实例化xml操作类
        mx = ManageXml(xml_string=xml_string)
        # 获取state标签的值
        # 返回实际状态
        return mx.root[1].find('.//srrc:state', mx.ns).text

class Check_B_Server:

    def __int__(self):
        pass

    def check_device_status(self, equid):
        '''
        检测原子服务中的state值来判断设备状态
        state值异常或无此节点，判断原子服务异常
        '''
        # 获取B_QueryFaciDevStat的响应报文
        xml_string = RequestInterface().get_B_QueryFaciDevStat(equid)
        # 实例化xml操作类
        mx = ManageXml(xml_string=xml_string)
        # 获取state标签的值
        # 返回实际状态
        return mx.root[1].find('.//srrc:state', mx.ns).text


class RequestInterface(object):
    '''
    接口调用通用方法类
    '''

    def __init__(self):
        self.re = requests.session()
        self.headers = {'SOAPAction': '', 'Content-Type': 'text/xml;charset=UTF-8'}

    # B_QueryDeviceInfo通用方法
    def get_B_QueryDeviceInfo(self, mfid=None, equid=None, url=None):
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
    def get_B_QueryFaciDevStat(self, mfid=None, equid=None, url=None):
        # 实例化xml操作类
        xm = ManageXml(xml_file_name='B_QueryFaciDevStat.xml')
        # 替换请求报文中的mfid,equid
        xm.root[1].find('.//srrc:mfid', xm.ns).text = mfid
        xm.root[1].find('.//srrc:equid', xm.ns).text = equid
        # 保存修改
        xm.write_xml()
        # 获取xml报文的字符串
        xml_message = xm.get_xml_string(xm.temp_path).encode(encoding='utf-8')
        # 设置header头
        self.headers['SOAPAction'] = 'B_QueryFaciDevStat'
        # 返回B_QueryFaciDevStat的响应报文
        return self.re.post(url=url, data=xml_message, headers=self.headers).text

    # # 下面两个函数是设备操作服务调用的通用方法
    # # 获取url,request_message,ip,port
    # def cequipment_operation_servic_data(self, equid, soapaction):
    #     # 获取请求报文和设备的基本信息
    #     # 根据soapaction和equid查询请求报文和url、mfid
    #     ms = ManageSqlite(DATABASE_NAME)
    #     mfid, url, request_message = ms.get_fetchone(
    #         "SELECT mfid,url,request_message FROM function WHERE fuc_en_name='%s' AND equid='%s'" % (soapaction, equid))
    #     # 根据equid查询mfid
    #
    #     # 实例化xml操作类
    #     xm = ManageXml(xml_string=request_message)
    #     # 替换executetime(通过配置文件)，mfid，equid的值
    #     xm.root.find('.//srrc:executetime', xm.ns).text = str(EXECUTETIME)
    #     xm.root.find('.//srrc:mfid', xm.ns).text = mfid
    #     xm.root.find('.//srrc:equid', xm.ns).text = equid
    #
    #     # 替换outputchannel中的host（配置文件）和port
    #     xm.root.find('.//srrc:host', xm.ns).text = str(HOST_ADDR)
    #     port = str(random.randint(60000, 65000))
    #     xm.root.find('.//srrc:port', xm.ns).text = port
    #
    #     # 获取修改后的xml报文
    #     request_message = xm.tosrting_xml(xm.root)
    #
    #     return url, request_message, str(HOST_ADDR), port
    #
    # # 调用设备操作服务，获取响应结果
    # def call_equipment_operation_service(self, url, request_message, soapaction):
    #     # headers替换值
    #     self.headers['SOAPAction'] = soapaction
    #     # 发送请求，获取响应报文
    #     return self.re.post(url=url, data=request_message, headers=self.headers)


if __name__ == '__main__':
    # Test_Network_Connectivity().test_network_connectivity("192.168.11.1")
    Test_Network_Connectivity().test_b_server_port_connectivity("192.168.13.33","8010")
