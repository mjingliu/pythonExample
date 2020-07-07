#!/usr/bin/env python 
# -*- coding:utf-8 -*-

import pymysql as psql
import const
import os, sys

def getCurPath():
    dirPath, filename = os.path.split(sys.argv[0])
    return dirPath + r'/' + 'tmpData/'

def getAllFilename():
    return os.listdir(getCurPath())

class stockDB(object):
    '''
    class stockDB: use this class to implement the specific DB access using pymysql lib
    '''
    def __init__(self, user, password):
        self.conn = psql.connect(host='localhost', autocommit=True, user=user, password=password, port=3306)
        self.cursor = self.conn.cursor()
        # get the filePath to be stored into Database
        self.filePath = getCurPath()

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
        filePath = self.filePath + ''.join(stockCode)
        sql = 'LOAD DATA INFILE "{}" INTO TABLE '.format(filePath) + tblName + ' FIELDS TERMINATED BY ","' + r' LINES TERMINATED BY "\r\n"' + ';'
        self.cursor.execute(sql)
    def deleteData(self, tblName,dbName):
        self.useDB(dbName)
        sql = 'DELETE FROM "{}" '.format(tblName)
        self.cursor.execute(sql)

    def exitDB(self):
        self.cursor.close()
        self.conn.close()

if __name__ == '__main__':
    myDB = stockDB(user="mingjliu", password="qwe`1234")
    myDB.createDB("db_stock12")
    myDB.createTbl(const.tblName,const.dbName)

    allFileName = getAllFilename()
    findFlag = False

    for each in const.stockCode:
        print(each)
        filename = '20200623' + '_' + ''.join(const.stockCode[each]) + '.csv'
        findFlag = False
        for i in range(len(allFileName)):
            if filename == allFileName[i]:
                myDB.storeData(const.tblName, filename)
                findFlag = True
                break
        if findFlag == False:
            print("do not find the matched file in current dir, filename is %s" % filename)

    myDB.exitDB() #release the resource



