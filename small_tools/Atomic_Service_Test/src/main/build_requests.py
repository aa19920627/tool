# -*- encoding: utf-8 -*-
"""
@File    : build_requests.py
@Date    : 2020/11/2 11:20
@Author  : 洪建
"""
import requests

from Atomic_Service_Test.src.component.data_processing import Data_Processing
from Atomic_Service_Test.src.main.create_tcp_server import Create_Tcp_Server

'''构建请求'''


class Build_Requests:

    def __init__(self):

        self.re = requests.session()

    def send_request(self,url,data,soapaction):

        '''
        :发送请求
        :return 响应报文
        '''
        headers = {"Content-Type" : "text/xml;charset=UTF-8" ,
                   "SOAPAction" : soapaction}

        try :
            res = self.re.post(url = url , data = data , headers = headers , timeout = 10)
        except  requests.exceptions.Timeout as e :
            return "响应超时"

        return res.text


    def build_data(self , *args):

        '''
        :构建请求的body
        :return 请求body,data
        '''

        xml_value = Data_Processing().read_xml(args[0])
        data = (xml_value % args[1]).encode("utf-8").decode("latin-1")

        return data


if __name__ == '__main__':

    data_list = Data_Processing().read_excel_data("test.xlsx")

    for i in data_list:
        try :
            data = Build_Requests().build_data(i[3] , (i[1],i[2],"192.168.16.181" , "7777"))
            res = Build_Requests().send_request(i[4] , data , i[3])
        except:
            print("失败")



