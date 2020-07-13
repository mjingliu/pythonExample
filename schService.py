#!/usr/bin/env python
# -*- coding:utf-8 -*-
from . import StockDB as db
from . import DataSpider as spider
import threading

'''
design:
1. prepare for the resource out of the class schedService
2. in class schedService which is inherited from Thread, implement the thread functionality
3. prepare for another class to combine thread/resource, implement the final functionality
4. there exist three service at least, 
    a. fetching data, b. DB, c. data process, need to draw one chart to descript the whole process
'''

class schedService():
    '''
    该类主要用于协调各个模块之间的协同工作
    获取数据模块
    数据库模块
    数据分析模块
    日志输出模块
    '''
    def __init__(self):
        self.myDB = db.stockDB("mingjliu", "qwe`1234")
        self.spider = spider.dataSpiderService()

    def run(self):
        pass

if __name__ == '__main__':
    pass
    '''
    start = schedService()
    start.run()
    '''

