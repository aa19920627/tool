# -*- encoding: utf-8 -*-
"""
@File    : get_token.py
@Date    : 2021/3/12 10:51
@Author  : 洪建
"""
from hj.small_tool.common.basic_data import Basic_data


class Get_Token:

    # 获取万能token

    def __init__(self):

        pass

    def get_token(self):

        token = {'test-key': '123',
                 'token': Basic_data().token(),
                 'X-Requested-With': 'XMLHttpRequest',
                 'Content-Type':'application/json;charset=UTF-8'}

        return token