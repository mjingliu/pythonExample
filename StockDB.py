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

    def login(self):
        pass
    def useDB(self):
        pass
    def selectData(self):
        pass
    def storeData(self):
        pass
    def exitDB(self):
        self.cursor.close()
        self.conn.close()
