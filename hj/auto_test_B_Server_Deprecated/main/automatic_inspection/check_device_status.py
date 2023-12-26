'''
@Author：洪建
@Date：2022/1/11 10:54
该包用于检查设备状态，基于B_QueryFaciDevStat能力来获取设备状态
'''
from component.manage_xml import ManageXml
from main.base_component.request_interface import RequestInterface


class CheckDeviceStatus(object):

    def __init__(self):
        pass

    # 获取设备的状态，报文中的state参数的值
    def check_device_status(self, equid):
        # 获取B_QueryFaciDevStat的响应报文
        xml_string = RequestInterface().get_B_QueryFaciDevStat(equid)
        # 实例化xml操作类
        mx = ManageXml(xml_string=xml_string)
        # 获取state标签的值
        # 返回实际状态
        return mx.root[1].find('.//srrc:state', mx.ns).text



if __name__ == '__main__':
    cds = CheckDeviceStatus()
    print(cds.check_device_status('a6590676-f5a7-4220-b105-a6ea4edbd77b'))
