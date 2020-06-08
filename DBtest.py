#!/usr/bin/env python
# -*- coding:utf-8 -*-

import pymysql
import os,sys
import numpy as np

import pywt

import matplotlib.pyplot as plt

'''
1. 假设每一个行业都是以一年为周期，也就是说一年为通用周期
2. 某些行业可能是以季节为周期
3. 某些行业是以假期为周期
4. 从周期的维度看，在时域上，以某个固定的windows，获取距离最小的部分，
5. 需要在所有的stock数据中，进行分析，看一下是否有周期类型的数据，如果有的话，可以做后续指导
6. 高频部分代表的是波动和细节，低频部分代表的是整体趋势，如何规划高频和低频，是需要判断的一个问题，需要有判断准则。
7，如果去除低频数据，
8. 需要按照行业来划分类别，有可能是每一个行业有属于行业自己的周期
9. 按照地域划分，看一下地域的影响
'''

#conn = pymysql.connect(host='localhost', user="spider", password='R~!@34qwe-spider', port=3306)
conn = pymysql.connect(host='localhost', autocommit=True, user='root', password='R~!@34qwe', port=3306)
#conn = pymysql.connect(host='localhost', user="mingjliu", password='R~!@34qwe', port=3306)
cursor = conn.cursor()
dbName = "db_stock12"
tblName = "stock_tbl"
dirPath, filename = os.path.split(sys.argv[0])
filePath = dirPath + r'/' + 'data.csv'
try:
    sql = 'CREATE DATABASE IF NOT EXISTS ' + dbName +';'
    result = cursor.execute(sql)
    print(result)
    print(cursor.fetchall())
    sql = 'use ' + dbName
    result = cursor.execute(sql)
    print("change db: %s" % result)
    #sql = 'CREATE TABLE stock_tbl (stCode VARCHAR(15), tradeDate DATE, open FLOAT, high FLOAT, low FLOAT, close FLOAT, pre_close FLOAT, chang FLOAT, pct_chg FLOAT, vol FLOAT, amount FLOAT);'
    sql = 'CREATE TABLE IF NOT EXISTS ' + tblName + ' (stCode VARCHAR(15), tradeDate DATE, open FLOAT, high FLOAT, low FLOAT, close FLOAT, pre_close FLOAT, chang FLOAT, pct_chg FLOAT, vol FLOAT, amount FLOAT)' + ';'
    result = cursor.execute(sql)
    print("create table: %s" % result)

    #sql = 'LOAD DATA INFILE C:/5CG7093DK2-Data/Mingjingliu/ForMyself/github/pythonExample/data.csv INTO TABLE stock_tbl FIELDS TERMINATED BY "," LINES TERMINATED BY "\\r\\n";'
    sql = 'LOAD DATA INFILE "{}" INTO TABLE '.format(filePath) + tblName + ' FIELDS TERMINATED BY ","' + r' LINES TERMINATED BY "\r\n"' + ';'
    print("sql:%s" % sql)
    result = cursor.execute(sql)

    print("load data: %s" % result)
    sql = 'SELECT open, trade_date, close FROM ' + tblName + ';'
    result = cursor.execute(sql)

    #np.ndarray(cursor.fetchmany(10),dtype=float)

    tmpList = list(cursor.fetchall())
    print("all the Select data is :%d " % len(tmpList))
    aList = []
    aListDif = []
    aListClose = []
    aListDate = []
    '''
    for each in tmpList:
        aList = each[0]
        print(aList)
    '''
    for i in range(len(tmpList)):
        aList.append(tmpList[i][0])
        aListDate.append(tmpList[i][1])
        aListClose.append(tmpList[i][2])
        if i != 0:
            aListDif.append(tmpList[i][0])
    aList.pop()
    aListDate.pop()
    aListClose.pop()

    print(aList)
    print("len of aList:%d" % len(aList))
    print("len of aListDif:%d" % len(aListDif))
    #tmpArr = np.ndarray([2.73, 2.75, 2.78, 2.82, 2.85, 2.9, 2.95, 2.95, 2.97, 2.98], dtype='f')
    tmpArr = np.array(aList, dtype=np.float)
    tmpArrDif = np.array(aListDif, dtype=np.float)
    tmpArrClose = np.array(aListClose, dtype=np.float)

    tmpResOpen = tmpArrDif-tmpArr
    tmpResOpenClose = tmpArrDif-tmpArrClose
    tmpRes = tmpResOpen-tmpResOpenClose
    tmpArrDate = np.array(aListDate, dtype=np.datetime64)

    plt.plot(tmpArrDate,tmpResOpen)
    #plt.ylim(4,-4)
    #plt.xlim(tmpArrDate[-1], tmpArrDate[0])
    plt.show()
    print(tmpArr)
    print(tmpArrDate)
    print(type(tmpArr))
    print(len(tmpArrDate))
    '''
    sql = 'DELETE FROM ' + tblName + ';'
    result = cursor.execute(sql)
    print(result)
    '''
except Exception as e:
    print("Exception: %s" % e)
finally:
    cursor.close()
    conn.close()
