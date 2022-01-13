'''
@Author：洪建
@Date：2022/1/12 10:45
该包用于创建tcp服务器，用于接收数据
'''
import socket


class CreateReceivingServer(object):
    '''
    建立tcp服务器，用于接收数据
    '''

    def __init__(self, ip, port):
        # 指定协议
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 让端口可用重复使用
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # 设置超时时间10秒
        self.server.settimeout(10)
        # 绑定ip和端口
        self.server.bind((ip, port))
        # print('%s:%s' % (ip, port))
        # 监听
        self.server.listen(128)

    # 接收消息
    def receive_message(self):

        # 等待消息
        client_socket, self.address = self.server.accept()
        # 接收消息
        for i in range(10):
            client_socket.recv(1024)

        self.server.close()

        if i == 9 : return True

    # 关闭socket
    def close_socket(self, client_socket):

        client_socket.close()
        self.server.close()


if __name__ == '__main__':
    cr = CreateReceivingServer('192.168.11.74', 60026)
    cr.receive_message()
    # cr.close_socket()
