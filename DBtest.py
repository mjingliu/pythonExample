#!/usr/bin/env python
# -*- coding:utf-8 -*-

import pymysql
import os, sys
import numpy as np
import matplotlib as mpl
import pywt
pywt.Wavelet()

#conn = pymysql.connect(host='localhost', user="spider", password='R~!@34qwe-spider', port=3306)
conn = pymysql.connect(host='localhost', user='root', password='Rewq`1234', port=3306)
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
    '''
    #sql = 'LOAD DATA INFILE C:/5CG7093DK2-Data/Mingjingliu/ForMyself/github/pythonExample/data.csv INTO TABLE stock_tbl FIELDS TERMINATED BY "," LINES TERMINATED BY "\\r\\n";'
    sql = 'LOAD DATA INFILE "{}" INTO TABLE '.format(filePath) + tblName + ' FIELDS TERMINATED BY ","' + r' LINES TERMINATED BY "\r\n"' + ';'
    print("sql:%s" % sql)
    result = cursor.execute(sql)
    '''
    print("load data: %s" % result)
    sql = 'SELECT open FROM ' + tblName + ';'
    result = cursor.execute(sql)

    #np.ndarray(cursor.fetchmany(10),dtype=float)

    tmpList = list(cursor.fetchmany(10))
    aList = []
    '''
    for each in tmpList:
        aList = each[0]
        print(aList)
    '''
    for i in range(len(tmpList)):
        aList.append(tmpList[i][0])
    print(aList)
    #tmpArr = np.ndarray([2.73, 2.75, 2.78, 2.82, 2.85, 2.9, 2.95, 2.95, 2.97, 2.98], dtype='f')
    tmpArr = np.array(aList)
    print(tmpArr)
    print(type(tmpArr))
    print(tmpList)
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
