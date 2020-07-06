#!/usr/bin/env python
# -*- coding:utf-8 -*-
from . import StockDB as db
from . import DataSpider as spider

class schedService(object):
    '''
    该类主要用于协调各个模块之间的协同工作
    获取数据模块
    数据库模块
    数据分析模块
    日志输出模块
    '''
    def __init__(self):
        self.myDB = db.stockDB()
        self.spider = spider.dataSpiderService()

    def running(self):
        pass

if __name__ == '__main__':
    start = schedService()
    start.running()

