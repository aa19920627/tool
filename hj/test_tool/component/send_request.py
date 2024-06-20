# -*- coding: utf-8 -*-
"""
@Time ： 2024/6/20 11:40
@Auth ： 洪建
"""
import requests

'''
接口请求组件
'''

def send_request(url,soapaction,data):

    headers={
        "Content-Type":"text/xml;charset=utf-8",
        "SOAPAction":soapaction
    }

    res = requests.post(url=url, data=data, headers=headers)

    return res

