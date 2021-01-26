# -*- encoding: utf-8 -*-
"""
@File    : monitor_method.py
@Date    : 2021/1/25 10:36
@Author  : 洪建
"""
import subprocess

'''
设备监控的方法
'''


class Monitor_Method:

    def __init__(self):

        pass

    def ping_equipment(self, equipment_ip):

        #获取ping网络的命令输入和返回代码
        result = subprocess.Popen(['ping', equipment_ip], stdout=subprocess.PIPE, universal_newlines=True)

        try:
            #命令行输出
            shuchu, _ = result.communicate(timeout=10)

        except:

           return 1

        return result.returncode    #return放回代码，0代表连通，1代表不通


if __name__ == '__main__':

    print(Monitor_Method().ping_equipment("192.168.11.128"))