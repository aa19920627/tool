'''
@Author: 洪建
@Date 2023/7/5 13:56
'''
import socket
import time
from datetime import datetime

import openpyxl
import requests
from ping3 import ping

from main.component import Frozen_Path
from main.manage_xml import ManageXml

'''
自动检测原子服务状态，分为三个步骤：
1.网络检测 
2.原子服务状态检测
3.任务数据检测（暂时不做）
'''


class Test_Network_Connectivity:
    def __int__(self):
        pass

    # 步骤1：检测网络连通性
    def test_network_connectivity(self, host):

        try:
            # 发送ICMP请求，timeout参数设置超时时间
            result = ping(host, timeout=2)

            if result is not None:
                # 主机可达
                # print(f"主机{host}网络正常")
                return True
            else:
                # 主机不可达
                # print(f"主机{host}网络不通")
                return False
        except Exception as e:
            # 发生异常
            print("捕获异常")
            return False

    # 步骤2：检测原子服务端口连通性
    def test_b_server_port_connectivity(self, host, port):

        try:
            # 创建套接字对象
            sock = socket.create_connection((host, port), timeout=5)
            # 连接成功
            # print(f"原子服务端口连接成功 {host}:{port}")
            sock.close()
            return True
        except socket.error as e:
            # 连接失败
            # print(f"原子服务端口连接失败 {host}:{port}")
            return False

    # 步骤3：调用B_QueryFaciDevStat接口，获取原子服务返回的状态
    def check_device_status(self, mfid, equid, url):

        try:
            # 获取B_QueryFaciDevStat的响应报文
            xml_string = RequestInterface().get_B_QueryFaciDevStat(mfid, equid, url)
            # 实例化xml操作类
            mx = ManageXml(xml_string=xml_string)
            # 获取state标签的值
            # 返回实际状态
            state = mx.root[1].find('.//srrc:state', mx.ns).text

            # 正常的返回状态定义
            state_list = ["idle", "busy", "autotask"]

            # 判断返回的state值，return对应的结果
            if state in state_list:
                return "正常"
            elif state == 'failure':
                return "故障"
            else:
                return False

        except Exception as e:
            return False

    # 读取站点数据
    # 按步骤调用，前序步骤不通过立即停止
    def start_checking(self, excel_file_path):

        # 读取测试数据
        # excel_file_path = Frozen_Path().app_path() + "/data/excel/mfname&mfid&equid&url.xlsx"
        workbook = openpyxl.load_workbook(excel_file_path)
        # 选工作表
        sheet = workbook.active
        # 定义测试结果的list，添加表头
        result_list = [
            ["地区", "监测站名称", "MFID", "原子服务集成厂家", "设备ID", "原子服务部署IP", "测试结果", "原子服务地址"]]
        # 读取数据
        # 从第一行读取到最后一行，取每一列的数据
        for row in sheet.iter_rows(min_row=2, max_row=sheet.max_row, min_col=1, max_col=5, values_only=True):
            # 处理数据，生成需要的字段
            mf_name = row[0].strip()
            equid = row[1].strip()  # 去空格，容错
            url = row[2].strip()
            host = row[2].split("/")[2].split(":")[0].strip()
            port = row[2].split("/")[2].split(":")[1].strip()
            mfid = row[2].split("/")[3].strip()
            area = row[3].strip()
            integrated_manufacturer = row[4].strip()

            # 按照步骤依次判断网络-原子服务软件存活-原子服务状态返回
            if self.test_network_connectivity(host):
                if self.test_b_server_port_connectivity(host, port):
                    state = self.check_device_status(mfid, equid, url)
                    if state == "正常":
                        result = "正常"
                    elif state == "故障":
                        result = "故障"
                    else:
                        result = "B_QueryFaciDevStat接口调用异常"
                else:
                    result = "B_QueryFaciDevStat接口调用异常"
            else:
                result = "网络不通"

            # 将测试结果追加到list中，用于写入测试报表
            result_list.append([area, mf_name, mfid, integrated_manufacturer, equid, host, result, url])

            # 手动设置每列的宽度，打印内容对齐
            print(f"{mf_name:<15}{result}")

        # 将测试结果写入excel表
        work_book_result = openpyxl.Workbook()
        # 获取活跃的工作簿
        sheet_result = work_book_result.active

        # 循环写入测试数据，生成测试报表
        for i, row in enumerate(result_list, start=1):
            sheet_result.append(row)

        # 获取时间来作为表名
        # 获取当前时间
        current_time = datetime.now()
        # 格式化时间
        formatted_time = current_time.strftime("%Y-%m-%d")
        # 获取时间戳
        timestamp_integer = int(time.time())
        # 获取测试结果表的路径
        result_path = Frozen_Path().app_path() + f"/data/excel/{formatted_time}_{timestamp_integer}.xlsx"
        # 保存测试报表
        work_book_result.save(result_path)
        # 完成测试，测试结果路径输出
        print("已完成测试，测试报表路径： %s" % result_path)

    # 写入excel数据时，自适应列宽和行高
    # def write_row(self, sheet, data, row_number):
    #     for col_number, value in enumerate(data, start=1):
    #         cell = sheet.cell(row=row_number, column=col_number, value=value)
    #         # 自动换行
    #         # cell.alignment = Alignment(wrap_text=True)
    #         # 自适应列宽
    #         sheet.column_dimensions[cell.column_letter].width = max(sheet.column_dimensions[cell.column_letter].width,
    #                                                                 len(str(value)))


class RequestInterface:
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
        return self.re.post(url=url, data=xml_message, headers=self.headers, timeout=5).text

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
    # Test_Network_Connectivity().test_b_server_port_connectivity("192.168.13.33","8010")
    # print(Test_Network_Connectivity().check_device_status("51010001110001", "17e4dec9-2d50-4167-a49f-8cf5fc95bd72",
    #                                                       "http://192.168.13.33:8010/51010001110001/Demo/B_QueryFaciDevStat"))

    # 读取测试数据
    excel_file_path = Frozen_Path().app_path() + "/data/excel/mfname&mfid&equid&url.xlsx"
    Test_Network_Connectivity().start_checking(excel_file_path)
