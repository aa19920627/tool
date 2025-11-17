#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : 洪建
# @File : save_rabbitmq_consume.py
# @Time : 2025/11/13 16:27
import pickle

import pika
import requests

"""rabbitmq实例的消费者"""

MAX_CONNECTIONS = 100
QUEUE_NAME = "scrapy_queue"

# 连接rabbitmq
credentials = pika.PlainCredentials('rabbitmq', 'rabbitmq')
connection = pika.BlockingConnection(pika.ConnectionParameters(
    host='192.168.36.76',
    port=5672,
    credentials=credentials))

# 频道对象
channel = connection.channel()
session = requests.Session()


def scrape(request):
    try:
        response = session.send(request.prepare())
        print(f'sucess scraped: {response.url}')
    except requests.RequestException:
        print(f'error occurred when scraping: {request.url}')


# basic方法获取消息，pickle工具把消息反序列化成一个请求对象，再调用爬取数据请求
while True:
    method_frame, header, body = channel.basic_get(
        queue=QUEUE_NAME, auto_ack=True
    )
    if body:
        request = pickle.loads(body)
        print(f'GET {request}')
        scrape(request)
# 声明一个队列，名称叫QUEUE_NAME
# channel.queue_declare(queue=QUEUE_NAME)


# # 从队列中获取数据
# def callback(ch, method, properties, body):
#     print(f"Get {body}")
#
#
# channel.basic_consume(queue=QUEUE_NAME,
#                       auto_ack=True,
#                       on_message_callback=callback)
# channel.start_consuming()

while True:
    input()
    method_frame, header_frame, body = channel.basic_get(queue=QUEUE_NAME, auto_ack=True)

    if body:
        print(f'Get {body}')
