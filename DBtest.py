#!/usr/bin/env python
# -*- coding:utf-8 -*-

import pymysql
import os, sys

<<<<<<< HEAD
#conn = pymysql.connect(host='localhost', user="spider", password='R~!@34qwe-spider', port=3306)
conn = pymysql.connect(host='localhost', user='root', password='Rewq`1234', port=3306)
=======
conn = pymysql.connect(host='localhost', user="mingjliu", password='R~!@34qwe', port=3306)
>>>>>>> 5fb3b4498d4f6e6409d618980332665a6403a02a
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

<<<<<<< HEAD
'''
sql = 'CREATE DATABASE db_stock12;'
result = cursor.execute(sql)
print(result)
print(cursor.fetchall())
'''
sql = 'SHOW DATABASES;'
result = cursor.execute(sql)
print("show db:%s" % result)
print(cursor.fetchmany(size=3))
sql = ''
cursor.close()
conn.close()
=======
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
    sql = 'SELECT * FROM ' + tblName + ';'
    result = cursor.execute(sql)
    print(cursor.fetchall())

except Exception as e:
    print("Exception: %s" % e)
finally:
    cursor.close()
    conn.close()
>>>>>>> 5fb3b4498d4f6e6409d618980332665a6403a02a
