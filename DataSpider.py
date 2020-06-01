#!/usr/bin/env python
# -*- coding:utf-8 -*-
from builtins import object, str, int, isinstance, Exception
import os, sys
import requests as req
import re
import pandas as pd
import pymysql
import tushare as ts
import json
import logging
import datetime as dt
from . import const


class dataSpiderService(object):
    '''
    该类用于从网络上爬取数据相关服务
    '''

    __url = "http://api.waditu.com"
    __token = 'cf8c206c8a3f3919835effcfc672c48a7f3b40315a1867bd15375af5'

    def __init__(self, url=None, token=None):
        '''
        如果没有URL和token的输入的话，默认使用waditu的url和对应的token
        :param url: 需要获取数据的网址地址
        :param token: 该网址需要的token，如果有的话
        '''
        if url is not None:
            self.url = url
        else:
            self.url = __url
        if token is not None:
            self.token = token
        else:
            self.token = __token
        ### 1. 获取到logger句柄用以记录输入，2. 获取到handler句柄，用以记录输出，3.初始化log级别，以及绑定输入输出
        self.logger = logging.getLogger(self.__name__)
        hdr = logging.FileHandler(self.__name__.join('.log'), encoding='UTF-8')
        self.initLogger(logLevel=logging.DEBUG, hdr=hdr, hdrLevel=logging.DEBUG)

    def login(self, username=None, password=None):
        '''
        功能：登陆到目标网站，用以获取到数据
        :param username: 登陆用户名
        :param password: 登陆密码
        :return:
        '''
        pass

    def initLogger(self, logLevel=None, hdr=None, hdrLevel=None):
        '''
        功能：在此处初始化logger的日志级别，handle
        :param logLevel: 为需要记录的日志级别，对应的参数内容为：
                logging.DEBUG， logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL
        :param hdr: 为log最终要输出的目的地，默认为标准stream输出。
        :param hdrLevel: 为要输出到终端的日志级别，具体参数如下：
                logging.DEBUG， logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL
        :return:
        '''
        if logLevel is None:
            self.logger.setLevel(logging.DEBUG)
        else:
            self.logger.setLevel(logLevel)

        if hdr is None:
            hdrInit = logging.StreamHandler()
        else:
            hdrInit = hdr

        if hdrLevel is None:
            hdrInit.setLevel(logging.INFO)
        else:
            hdrInit.setLevel(hdrLevel)

        tmpfmt = logging.Formatter(fmt='%(funcName)s:%(lineno)d :%(asctime)s:%(msecs)d :%(message)s')
        hdrInit.setFormatter(tmpfmt)

        self.logger.addHandler(hdrInit)

    def fetchHisData(self, stockCode, startDate='', endDate=''):
        '''
        获取昨天到初始日期期间的历史数据
        比如：
        假设今天为：20200420，上市日期为：19920323
        那么该函数获取的是从19920323~20200419的数据
        '''
        # 1. 准备好需要获取到API对应数据的参数
        # 2. 需要考虑到超时，以备重试多次还没有获取到数据而导致的异常，不允许程序退出
        # 3. 需要把每次获取到的数据都保存到csv文件中，以对应的股票代码命名

        # 获取到正确的股票代码
        if stockCode is None:
            self.logger.critical("必须输入正确股票代码！当前代码为空")
            return False
        if const.stockCode.get(str(stockCode)) is None:
            self.logger.error("输入错误的股票代码：%s,请重新输入！" % stockCode)
            return False

        #如果没有输入开始日期和截止日期的话，获取到当前前一个交易日的数据
        #如果截止日期早于开始日期的话，说明输入错误，需要重新输入
        if isinstance(startDate,str) and startDate is not '':
            tmpStartDate = re.sub('-', '', str(startDate))
        else:
            tmpStartDate = dt.date.today().strftime('%Y%m%d')

        if isinstance(endDate,str) and endDate is not '':
            tmpEndDate = re.sub('-', '', str(endDate))
        else:
            tmpEndDate = dt.date.today().strftime('%Y%m%d')

        if int(tmpEndDate) < int(tmpStartDate):
            self.logger.error("获取股票的截止日期要在开始日期之后！请重新输入对应日期！ startDate:%s, endDate:%s" % startDate, endDate)
            return False

        reqPara = {
                'api_name': 'daily',
                'token': 'cf8c206c8a3f3919835effcfc672c48a7f3b40315a1867bd15375af5',
                'params': {'ts_code': stockCode, 'start_date': tmpStartDate, 'end_date': tmpEndDate},
                'fields': ''
                 }
        #该处算法为，对每一个股票，最多重试5次，如果5次还没有获取到该股票数据的话，把对应信息写到log日志中
        iloop:int = 0
        while iloop < 5:
            try:
                res = req.post(self.url,json=reqPara,timeout=5, headers={'Connection':'close'})
            except Exception as e:
                self.logger.error("获取股票 %s 历史数据失败。 网络连接失败：Exception: %s, 循环次数：%d" % stockCode, e,iloop)
                iloop += 1
            else:
                '''
                此处已经获取到服务器的响应，但是响应内容是否正确，需要进一步检查，
                若数据正确，则把该数据传递给storeData()函数，用以存储数据
                '''
                if res.status_code == 200:
                    result = json.loads(res.text)
                    if result['code'] == 0: #成功获取数据
                        data = result['data']
                        self.storeData(data,stockCode)
                        return True
                    else:
                        self.logger.error("获取股票%s历史数据失败,错误码为：%s, 输入参数错误:%s" % stockCode, result['msg'],reqPara)
                        return False
                else:
                    self.logger.error("获取股票：%s 历史数据失败，HTTP连接层错误，输入参数错误:%s" % stockCode, reqPara)
                    return False
                break


    def fetchAllHisData(self):
        pass

    def fetchTodayData(self, stockCode=None):
        '''
        每天定时启动该任务获取数据，获取当天的所有股票数据
        '''
        pass

    def fetchTradeData(self, stockCode=None, tradeDate=None):
        '''
        功能：获取指定交易日的交易数据
        :return:
        '''
        pass

    def dataProxy(self):
        '''
        设置代理服务器
        '''
        pass

    def storeData(self, data, stockCode):
        '''
        功能：存储股票数据，把对应的股票数据存储到csv文件中，该文件命名原则为：股票代码+获取日期
                该文件存放位置为：./Data 目录

        :return:
        '''
        curDir = os.path.abspath(__file__)
        newDir = curDir + r'\Data'
        if not os.path.exists(newDir):
            os.mkdir(newDir)
        os.chdir(newDir)

        if data:
            fileName = newDir + r'\\'+ str(stockCode)+'.'+ dt.datetime.today().strftime('%Y%m%d')
            tmpColumn = data['fields']
            tmpData = data['items']
            df = pd.DataFrame(data=tmpData, columns=tmpColumn)

            with open(fileName,'r+') as fp:
                df.to_csv(fp,index=False)
        else:
            self.logger.warning("传入参数为None!")
        os.chdir(curDir)
        return

    def storeHisData(self):
        '''
        存储获取到的历史数据
        '''
        pass

    def storeTodayData(self):
        '''
        存储获取到的今天的数据
        '''
        pass


class databaseService(object):
    '''
    该类用于数据库管理相关内容操作
    启动数据库，
    创建数据表，
    写数据，
    读数据
    '''

    def __init__(self):
        self.conn = pymysql.connect(host='localhost', user='mingjliu', password='qwe`1234', port=3306)
        self.cursor = self.conn.cursor()

    def __close__(self):
        '''
        close the DB resource
        '''
        self.cursor.close()
        self.conn.close()

    def createDB(self):

        pass

    def createTable(self):
        pass

    def readTable(self):
        pass

    def writeTable(self):
        pass
    def selectTable(self):
        pass

class analyzeDataService(object):
    '''
    该类用于对获取到的数据进行分析，
    可以根据不同的算法得到不同的结果
    输入：数据库中的每一支股票的历史数据
    输入：根据不同的算法，得到不同的分析图标数据
    '''

    def __init__(self):
        pass


class schedService(object):
    '''
    该类主要用于协调各个模块之间的协同工作
    获取数据模块
    数据库模块
    数据分析模块
    日志输出模块
    '''

    def __init__(self):
        pass

    def runningService(self):
        pass


if __name__ == '__main__':
    pass
