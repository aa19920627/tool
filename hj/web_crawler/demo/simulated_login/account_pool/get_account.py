#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : 洪建
# @File : get_account.py
# @Time : 2026/1/30 15:16

"""
账号池-获取模块
"""

from accountpool.exceptions.init import InitException
from accountpool.storages.redis import RedisClient
from loguru import logger


class BaseGenerator(object):

    def __init__(self, website=None):
        self.website = website
        if not self.website:
            raise InitException
        self.account_operator = RedisClient(type='account', website=self.website)
        self.credential_operator = RedisClient(type='credential', website=self.website)

    def generate(self, username, password):
        raise NotImplementedError

    def init(self):
        pass

    def run(self):
        self.init()
        logger.debug('start to run generator')
        for username, password in self.account_operator.all().items():
            if self.credential_operator.get(username):
                continue
            logger.debug(f'start to generate credential of {username}')
            self.generate(username, password)