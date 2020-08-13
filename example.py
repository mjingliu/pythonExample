#!/usr/bin/env python 
# -*- coding:utf-8 -*-
from builtins import print
from typing import Any

import requests as req
import pymysql
import json
import pandas as pd
import tushare as ts
import const
import sys, os
import time
import datetime

'''
1. 每一次抓取的数据存放在../tmpData/目录下，故当前要工作在../data/目录下
'''
tmpDir, tmpFile = os.path.split(sys.argv[0])
tmpDataDir = tmpDir + r'\tmpData'
if not os.path.exists(tmpDataDir):
    os.mkdir(tmpDataDir)
os.chdir(tmpDataDir)
print(os.getcwd())
print("\n sys.argv")

url = "http://api.waditu.com"
timeout = 15
headers = {'Connection': 'close'}
# 当适用公司网络的时候，需要适用如下proxies，在家里的网络不需要适用proxies
proxies = {"http": "http://10.144.1.10:8080"}

td = datetime.date.today().strftime("%Y%m%d")
cNum = 0

for eachCode in const.stockCode:
    '''
    eachCode: 每一支股票的在深市/沪市的编号
    const.stockCode[eachCode]: 获取到每一支股票在Tushare中的映射
    '''
    # cNum += 1
    time.sleep(1) # 1 second取一次数据，用以规避频繁取数据，被服务器禁止服务
    stckCode = const.stockCode[eachCode]
    filename = td + '_' + stckCode + '.csv'
    #if cNum <= 10:
    req_para = {
        'api_name' : 'daily',
        'token' : 'cf8c206c8a3f3919835effcfc672c48a7f3b40315a1867bd15375af5',
        'params' : {'ts_code' : ''.join(stckCode), 'start_date' : '19950101', 'end_date' : ''.join(td)},
        'fields' : ''
    }
    # 海康：002415.SZ
    # 工行：601398.SH
    # 东方通信：600776.SH
    # 茅台：600519.SH
    '''
    req_para = {
        'api_name': 'daily',
        'token': 'cf8c206c8a3f3919835effcfc672c48a7f3b40315a1867bd15375af5',
        'params': {'exchange': '', 'list_status': 'L'},
        'fields': ''
    }
    '''
    # result = req.post(url=url, json=req_para, timeout=timeout, headers=headers, proxies=proxies)
    try :
        result = req.post(url=url, json=req_para, timeout=timeout, headers=headers, proxies=proxies)
    except Exception as e :
        print("exception take place: code:%s" % stckCode)
        print("exception is :%s" % e)
    else :
        if result :
            res = json.loads(result.text)
            if res['code'] != 0 :
                print("Fail to fetch data: %s" % res['msg'])
            else :
                data = res['data']
                col = data['fields']
                record = data['items']
                df = pd.DataFrame(data=record, columns=col)
                # print(df)
                df.to_csv("".join(filename), columns=col, header=False, index=False)

        else :
            print('\n')
            print("failed to fetch data this time!\n")

'''
股票精选步骤：
1. 使用TuShare提供的数据API获取到对应的数据，该数据类型为DataFrame类型，
2. 当获取到DF类型的数据后，对该数据进行存储到MySQL数据库中
3. 对存储到MySQL中的数据进行加工，根据自己的想法，可以采用FFT变换，看一下在另一个空间中的数据是什么样子的？
4. 结合当下的历史数据分析，筛选出对应的行业，看看不同类型的行业中，是否有属于行业自己的特性
5. 如果要自动化交易的话，需要根据历史数据进行有限的分析，具体该如何分析，暂时还不清楚
    a. 从当前的实验情况来看，FFT/iFFT不适用该分析，
    b. 
6. 可以做一个可视化的界面，更有利于交易分析
'''
