# -*- coding:utf-8 -*-

import logging
from config import *

logging.basicConfig(filename=LogFile, format=LogFormat, level=LogLevel)


class Base:
    def __init__(self):
        logging.debug('Load configuration file.')
        self.config = config
        logging.debug('Database operation initialization.')
        self.mysql_util = None
        self.mongo_util = None
    
    def initialize(self, event_name=''):
        logging.debug('Loading events.')
        self.event = None
        logging.debug('Parsing event rules.')
        self.event_rule = None

    def process(self):
        logging.info('Data Processing.')

    def conversion(self, data=[]):
        logging.info('Data Conversion.')
    
    def save(self, row_list=[]):
        logging.info('Data Storage.')

    def run(self, event_name=''):
        self.initialize(event_name)
        self.process()
        self.save()

# https://www.cnblogs.com/jiangxiaobo/p/12786205.html