'''
@Author：洪建
@Date：2022/1/4 15:13
通用接口调用方法
'''
import requests as requests

from component.loading_config import database_config
from component.manage_xml import ManageXml
from component.sqlite_method import ManageSqlite

DATABASE_NAME = database_config()

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

        #返回B_QueryFaciDevStat的响应报文
        return self.re.post(url=url, data=xml_message, headers=self.headers).text

if __name__ == '__main__':
    ri = RequestInterface()
    print(ri.get_B_QueryFaciDevStat('a6590676-f5a7-4220-b105-a6ea4edbd77b'))
