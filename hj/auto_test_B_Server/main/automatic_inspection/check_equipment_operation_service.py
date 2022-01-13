'''
@Author：洪建
@Date：2022/1/11 13:38
该包用于检查设备操作服务的调用情况，检查步骤
1.调用结果
2.数据返回结果
其他要求：
1.重试n（可配置）次，间隔n（可配置）秒
'''
import threading
from concurrent.futures import ThreadPoolExecutor

from component.manage_xml import ManageXml
from main.base_component.create_data_receiving_server import CreateReceivingServer
from main.base_component.request_interface import RequestInterface


class CheckRequest(object):
    '''
    检查调用的返回结果
    '''

    def __init__(self):
        # 实例化通用接口类
        self.ri = RequestInterface()

    # 获取调用设备操作服务后的响应报文
    def check_request_respose(self, url, request_message, soapaction):
        # 检查调用设备操作服务后的响应结果和sink模式接收数据的端口port,ip地址
        res = self.ri.call_equipment_operation_service(url, request_message, soapaction)
        # 初始化xml操作类
        mx = ManageXml(xml_string=res.text)
        if len(mx.root.find('.//srrc:taskid', mx.ns).text) != 0:
            return True
        else:
            return False

    # 检查数据返回结果
    def check_data_respose(self, equid, soapaction):

        # 获取调用设备操作服务需要的参数
        url, request_message, ip, port = self.ri.cequipment_operation_servic_data(equid, soapaction)

        # 实例化tcp服务器类
        crs = CreateReceivingServer(ip, int(port))
        # 创建2个线程池
        with ThreadPoolExecutor(max_workers=2) as executor:
            # 向线程池提交receive_message()函数开启tcp服务器接收数据，调用check_request_respose来获取调用结果
            future1 = executor.submit(self.check_request_respose, url, request_message, soapaction)
            future2 = executor.submit(crs.receive_message)

        # 获取调用结果和数据端口
        if future1.result() is True:
            print('调用成功')
        if future2.result() is True:
            print('成功接收数据')



if __name__ == '__main__':
    cr = CheckRequest()
    cr.check_data_respose('c4a5f62f-07cd-4876-a368-cf78bd688144', 'B_FScan')
