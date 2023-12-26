'''
@Author: 洪建
@Date 2023/7/5 13:56
'''
import os
import sys

'''
公共类
'''


class Frozen_Path:

    def __init__(self):
        pass

    def app_path(self):
        '''
        判断程序的运行环境，返回对应程序目录
        '''
        if hasattr(sys, "frozen"):  # 判断运行环境为pyinstaller打包后的环境

            return os.path.dirname(sys.executable)  # 使用pyinstaller打包后exe的运行环境

        return os.path.dirname(os.path.dirname(__file__))  # 使用打包前的目录，用于本地运行


if __name__ == '__main__':
    print(Frozen_Path().app_path())
