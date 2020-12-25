# -*- encoding: utf-8 -*-
"""
@File    : create_tcp_server.py
@Date    : 2020/11/2 13:44
@Author  : 洪建
"""

import socket

import chardet

from Atomic_Service_Test.src.component.data_processing import Data_Processing

'''创建tcp服务器，接收数据'''


class Create_Tcp_Server:

    def __init__(self,ip,port,data_name):

        #创建
        self.tcp_server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        #监听地址和端口
        self.address = (ip,port)
        #绑定
        self.tcp_server.bind(self.address)
        # 使用socket创建的套接字默认的属性是主动的
        # 使用listen将其变为被动
        self.tcp_server.listen(128)
        # 如果有新的客户端来链接服务器，那么就产生一个新的套接字专门为这个客户端服务,client_socket用来为这个客户端服务,
        # tcp_server_socket就可以省下来专门等待其他新客户端的链接
        self.client_socket,self.client_addr = self.tcp_server.accept()

        self.data_name = data_name

    def recv_message(self):

        '''接收客户端数据'''


        while True:
            self.recv_value = self.client_socket.recv(1028)     #接收数据

            Data_Processing().write_recive_data(self.data_name,str(self.recv_value))

            # if self.recv_value:
            #     #获取编码格式
            #     self.encode_value = chardet.detect(self.recv_value)["encoding"]
            #
            # else:
            #     break

        self.client_socket.close()

if __name__ == '__main__':

    Create_Tcp_Server("192.168.16.181",7777).recv_message()





















# class Create_Websocket:
#
#     def __init__(self,ip,port):
#
#         self.start_sever = websockets.serve(self.main_logic,ip,port)
#         asyncio.get_event_loop().run_until_complete(self.start_sever)
#         asyncio.get_event_loop().run_forever()
#
#     async def recv_msg(self,websocket):
#
#         while True:
#
#             self.recv_value = await websocket.recv()
#             print(self.recv_value)
#
#     async def main_logic(self,websocket):
#
#         await self.recv_msg(websocket)



