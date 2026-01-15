#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : 洪建
# @File : proxy.py
# @Time : 2026/1/14 14:15
from web_crawler.build_proxy_pool.proxypool.schemas.proxy import Proxy


def is_valid_proxy(data):
    """
    检查字符串是否符合代理格式
    :param data: 待检查的代理字符串
    :return: 符合格式返回True，否则返回False
    """
    # 检查是否为带认证的代理格式（包含@符号）
    if is_auth_proxy(data):
        host, port = extract_auth_proxy(data)
        return is_ip_valid(host) and is_port_valid(port)
    # 检查是否为普通代理格式（包含冒号）
    elif data.__contains__(':'):
        ip = data.split(':')[0]
        port = data.split(':')[1]
        return is_ip_valid(ip) and is_port_valid(port)
    # 检查是否为纯IP格式
    else:
        return is_ip_valid(data)


def is_ip_valid(ip):
    """
    检查字符串是否符合IP格式
    :param ip: 待检查的IP字符串
    :return: 符合IP格式返回True，否则返回False
    """
    # 如果包含认证信息，提取@后的IP部分
    if is_auth_proxy(ip):
        ip = ip.split('@')[1]
    a = ip.split('.')  # 按点分割IP地址
    if len(a) != 4:  # IP地址的段数必须为4
        return False
    for x in a:
        if not x.isdigit():  # 每段必须是数字
            return False
        i = int(x)
        if i < 0 or i > 255:  # 数字范围必须在0-255之间
            return False
    return True


def is_port_valid(port):
    """
    检查端口是否为纯数字
    :param port: 端口字符串
    :return: 如果是纯数字返回True，否则返回False
    """
    return port.isdigit()


def convert_proxy_or_proxies(data):
    """
    将字符串列表转换为有效的代理对象或代理对象列表
    :param data: 输入的数据，可以是字符串列表或单个字符串
    :return: Proxy对象或Proxy对象列表，如果输入无效则返回None
    """
    # 如果输入数据为空，直接返回None
    if not data:
        return None
    # 如果输入是列表类型
    if isinstance(data, list):
        result = []
        for item in data:
            item = item.strip()
            # 跳过无效的代理字符串
            if not is_valid_proxy(item):
                continue
            # 如果是带认证的代理格式
            if is_auth_proxy(item):
                host, port = extract_auth_proxy(item)
            else:
                host, port, *_ = item.split(':')  # 使用*_忽略多余部分
            # 创建Proxy对象并添加到结果列表
            result.append(Proxy(host, port=int(port)))
        return result
    # 如果输入是字符串且格式有效
    if isinstance(data, str) and is_valid_proxy(data):
        if is_auth_proxy(data):
            host, port = extract_auth_proxy(data)
        else:
            host, port, *_ = data.split(':')
        return Proxy(host, port=int(port))


def is_auth_proxy(data):
    """
    检查代理字符串是否包含认证信息（以@符号为标志）
    :param data: 代理字符串
    :return: 包含认证信息返回True，否则返回False
    """
    return '@' in data


def extract_auth_proxy(data):
    """
    从带认证信息的代理字符串中提取主机和端口
    :param data: 带认证信息的代理字符串，格式如 "username:password@ip:port"
    :return: 返回元组 (host, port)，其中host包含认证信息
    """
    # 提取认证信息部分（@符号前的部分）
    auth = data.split('@')[0]
    # 提取IP和端口部分（@符号后的部分）
    ip_port = data.split('@')[1]
    # 从IP端口部分提取IP和端口
    ip = ip_port.split(':')[0]
    port = ip_port.split(':')[1]
    # 将认证信息和IP地址组合成完整的主机字符串
    host = auth + '@' + ip
    return host, port

if __name__ == '__main__':
    proxy = '117.68.216.212:32425'
    print(extract_auth_proxy(proxy))