#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : 洪建
# @File : save_rabbitmq_producer.py
# @Time : 2025/11/13 16:11
import pickle

import pika
import requests

"""
存储数据到消息队列RabbitMQ中,生产者
"""

MAX_PRIORITY = 100
TOTAL = 100
QUEUE_NAME = "scrapy_queue"

# 连接rabbitmq
credentials = pika.PlainCredentials('rabbitmq', 'rabbitmq')
connection = pika.BlockingConnection(pika.ConnectionParameters(
    host='192.168.36.76',
    port=5672,
    credentials=credentials))

# 频道对象
channel = connection.channel()
# # 声明一个队列，名称叫QUEUE_NAME,durable为持久化开关
# channel.queue_declare(queue=QUEUE_NAME, arguments={'x-max-priority': MAX_PRIORITY}, durable=True)
channel.queue_declare(queue=QUEUE_NAME, durable=True)

# 构造100个请求发送给rabbitmq
for i in range(1, TOTAL + 1):
    url = f'https://ssr1.scrape.center/detail/{i}'
    request = requests.Request('GET', url)
    channel.basic_publish(exchange='',
                          routing_key=QUEUE_NAME,
                          properties=pika.BasicProperties(
                              delivery_mode=2,
                          ),
                          body=pickle.dumps(request))
    print(f'Put request of {url}')

# # 添加信息
# channel.basic_publish(exchange='',
#                       routing_key=QUEUE_NAME,
#                       body='hello')


# while True:
#     data, priority = input().split()
#     channel.basic_publish(exchange='',
#                           routing_key=QUEUE_NAME,
#                           properties=pika.BasicProperties(
#                               priority=int(priority),
#                               delivery_mode=2, ),
#                           body=data)
#
#     print(f"Put {data}")
