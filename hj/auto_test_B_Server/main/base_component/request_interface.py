'''
@Author：洪建
@Date：2022/1/4 15:13
通用接口调用方法
'''
import requests as requests
from component.manage_xml import ManageXml


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


if __name__ == '__main__':
    ri = RequestInterface()
    print(ri.get_B_QueryDeviceInfo('a6590676-f5a7-4220-b105-a6ea4edbd77b'))
