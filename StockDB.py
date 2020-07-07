#!/usr/bin/env python 
# -*- coding:utf-8 -*-

import pymysql as psql

class stockDB(object):
    '''
    class stockDB: use this class to implement the specific DB access using pymysql lib
    '''
    def __init__(self, user, password):
        self.conn = psql.connect(host='localhost', autocommit=True, user=user, password=password, port=3306)
        self.cursor = self.conn.cursor()
        # get the filePath to be stored into Database
        dirPath, filename = os.path.split(sys.argv[0])
        self.filePath = dirPath + r'/'

    def login(self):
        pass

    def createDB(self, dbName):
        sql = 'CREATE DATABASE IF NOT EXISTS ' + dbName +';'
        self.cursor.execute(sql)

    def createTbl(self, tblName, dbName):
        sql = 'use ' + dbName
        self.cursor.execute(sql)
        sql = 'CREATE TABLE IF NOT EXISTS ' + tblName + ' (stCode VARCHAR(15), tradeDate DATE, open FLOAT, high FLOAT, low FLOAT, close FLOAT, pre_close FLOAT, chang FLOAT, pct_chg FLOAT, vol FLOAT, amount FLOAT)' + ';'
        self.cursor.execute(sql)

    def useDB(self, dbName):
        sql = 'use ' + dbName
        self.cursor.execute(sql)

    def selectData(self, tblName, dbName, stockCode):
        self.useDB(dbName)
        sql = 'SELECT open, trade_date, close FROM ' + tblName + ' WHERE trade_date > 19950101 AND trade_date < 20200101' + ';'
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def storeData(self, tblName, stockCode):
        filePath = self.filePath + ''.join(stockCode) + '.csv'
        sql = 'LOAD DATA INFILE "{}" INTO TABLE '.format(filePath) + tblName + ' FIELDS TERMINATED BY ","' + r' LINES TERMINATED BY "\r\n"' + ';'
        self.cursor.execute(sql)

    def exitDB(self):
        self.cursor.close()
        self.conn.close()

if __name__ == __main__:
    pass
