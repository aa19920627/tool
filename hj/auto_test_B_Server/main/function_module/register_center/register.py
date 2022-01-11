'''
@Author：洪建
@Date：2021/12/31 16:16
注册服务：
1.监测站
2.设备
3.设备能力
'''
from component.loading_config import database_config
from component.sqlite_method import ManageSqlite

# 数据库名
DATABASE_NAME = database_config()


class RegisterStationDevice(object):

    def __init__(self):
        # 初始化sqlite操作类
        self.ms = ManageSqlite(DATABASE_NAME)

    # 往数据库写入监测站注册信息
    def insert_station_info(self, values):
        try:
            self.ms.operation_sqlite('INSERT INTO station (mfid,mfname,area) values %s' % values)
            self.ms.close_cur_conn()
        except:
            return '注册失败'
        return '注册成功'

    # 往数据库写入设备注册信息
    def insert_device_info(self, values):
        try:
            self.ms.operation_sqlite('INSERT INTO device (mfid,mfname,equid,equname,type,ip,port) values %s' % values)
            self.ms.close_cur_conn()
        except:
            return '注册失败'
        return '注册成功'

    # 往function表写入设备操作服务的基本信息
    # {'mfid': mfid, 'equid': equid, 'url': url, 're_message': request_xml_string,
    #                      'SoapAction': feature_soapaction}
    def insert_function_info(self, function):

        for func in function:
            # 获取mfname,equname,func_name的值
            mfname, equname = self.ms.get_fetchone(
                "SELECT mfname,equname FROM device WHERE equid = '%s'" % func['equid'])
            func_name = self.ms.get_fetchone(
                "SELECT fuc_name FROM function_base_info WHERE fuc_en_name = '%s'" % func['SoapAction'])[0]

            # 往function表插入数据
            valuse = (func['mfid'], mfname, func['equid'], equname, func_name, func['SoapAction'], func['url'],
                      func['re_message'])
            self.ms.operation_sqlite(
                'INSERT INTO function (mfid,mfname,equid,equname,fuc_name,fuc_en_name,url,request_message) values %s ' % str(
                    valuse))
        self.ms.close_cur_conn()


if __name__ == '__main__':
    red = RegisterStationDevice()
    # print(red.insert_station_info("('51010001120999','山西信号分析','510100')"))
    # red.insert_device_info("('51010001120999','山西信号分析','a6590676-f5a7-4220-b105-a6ea4edbd77b','DGR2212','1',"
    #                        "'192.168.11.119','8010')")
